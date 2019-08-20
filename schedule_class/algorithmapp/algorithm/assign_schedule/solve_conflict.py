"""
深度交换策略：
    1.当天课程冲突时，交换本班可以交换的位置，或者交换另一冲突点的位置
    2.关联课程冲突时，交换本班可以交换的位置，或者交换另一个班冲突点的位置
    3.固定条件冲突，交换本班可以交换的位置，
    当以上不能解决时，固定条件冲突，需要转换成为其他冲突，然后再去解决
"""
import copy
from . import data_source as data_source


class Cell:

    def __init__(self, course, week, section):
        self.course = course
        self.week = week
        self.section = section

    def get_time(self):
        return {'week': self.week, 'section': self.section}

    @staticmethod
    def set(course, time):
        return Cell(course, time['week'], time['section'])


class SolveConflict:

    def __init__(self, data: data_source.DataSource):
        self.schedules = {}
        self.schedules_state = {}

        self.link_sign = None

        self.conflict_list = [
            {'class': '2班', 'course': '英'},
            {'class': '7班', 'course': '数'}
        ]

        self.static_week = data.WEEK
        self.static_section = data.SECTION
        self.bind_classes = copy.deepcopy(data.BIND_CLASSES)
        self.classes = copy.deepcopy(data.CLASSES)
        self.courses = list(data.COURSE_TOTAL.keys())
        # 关联的课程，教师相同的班级
        self.link_classes = {}
        # 固定约束条件
        self.fixed_not_assign = {}
        # 固定排课
        self.fixed_assign = {}

        self.class_course_teacher = copy.deepcopy(data.CLASSES_COURSE_TEACHER)
        self.static_not_assign_teacher = copy.deepcopy(data.NOT_ASSIGN_TEACHER)

        self.static_not_assign_time = copy.deepcopy(data.NOT_ASSIGN_TIME)
        self.static_not_assign_time.extend(copy.deepcopy(data.FLOW_CLASS_TIME))

        self.static_not_assign_course = copy.deepcopy(data.NOT_ASSIGN_COURSE)
        self.static_part_schedule = copy.deepcopy(data.PART_SCHEDULE)

        self.init_data()

    def init_data(self):
        # 初始化关联班级
        class_course_teacher = self.class_course_teacher
        for a_class in self.classes:
            self.link_classes[a_class] = {}
            for course in class_course_teacher[a_class]:
                for other_class in self.classes:
                    if a_class == other_class or course not in class_course_teacher[other_class]:
                        continue
                    if class_course_teacher[a_class][course] == class_course_teacher[other_class][course]:
                        if course in self.link_classes[a_class]:
                            self.link_classes[a_class][course].append(other_class)
                        else:
                            self.link_classes[a_class][course] = [other_class]

        # 教师不排
        for teacher in self.static_not_assign_teacher:
            for time in self.static_not_assign_teacher[teacher]:
                key = str(time['week'] - 1) + str(time['section'] - 1)
                if key in self.fixed_not_assign and self.fixed_not_assign[key] is not None:
                    if 'teacher' in self.fixed_not_assign[key]:
                        self.fixed_not_assign[key]['teacher'].append(teacher)
                    else:
                        self.fixed_not_assign[key]['teacher'] = [teacher]
                else:
                    self.fixed_not_assign[key] = {'teacher': [teacher]}
        # 科目不排
        for course in self.static_not_assign_course:
            for time in self.static_not_assign_course[course]:
                key = str(time['week'] - 1) + str(time['section'] - 1)
                if key in self.fixed_not_assign and self.fixed_not_assign[key] is not None:
                    if 'course' in self.fixed_not_assign[key]:
                        self.fixed_not_assign[key]['course'].append(course)
                    else:
                        self.fixed_not_assign[key]['course'] = [course]
                else:
                    self.fixed_not_assign[key] = {'course': [course]}
        # 初始化固定不排
        for time in self.static_not_assign_time:
            key = str(time['week'] - 1) + str(time['section'] - 1)
            self.fixed_not_assign[key] = None
        for info in self.static_part_schedule:
            key = info['class'] + str(info['week'] - 1) + str(info['section'] - 1)
            self.fixed_assign[key] = info['course']
        pass

    # 当天课程冲突
    def check_current_course_conflict(self, a_class, course, time):
        if course is None:
            return False
        # if course in self.schedules[a_class][time['week']]:
        #     return True
        for i in range(len(self.schedules[a_class][time['week']])):
            if course == self.schedules[a_class][time['week']][i] and i != time['section']:
                return True
        return False

    # 关联班级课程冲突
    def check_link_teacher_conflict(self, a_class, course, time):
        if a_class not in self.link_classes or course not in self.link_classes[a_class]:
            return False
        link_classes = self.link_classes[a_class][course]
        for a_class in link_classes:
            if self.schedules[a_class][time['week']][time['section']] == course:
                return True
        return False

    # 固定条件冲突, 冲突返回true
    def check_fixed_condition_conflict(self, a_class, course, time):
        key = str(time['week']) + str(time['section'])
        if key in self.fixed_not_assign:
            condition = self.fixed_not_assign[key]
            if condition is None:
                return True
            if 'course' in condition:
                if course in condition['course']:
                    return True
            if 'teacher' in condition and course is not None:
                if self.class_course_teacher[a_class][course] in condition['teacher']:
                    return True
        key = a_class + key
        if key in self.fixed_assign:
            return True
        return False

    # 课程约束，固定条件约束，关联课程约束
    def _fit(self, a_class, course, time):

        if self.check_fixed_condition_conflict(a_class, course, time):
            return False
        if course is None:
            return True
        if self.check_link_teacher_conflict(a_class, course, time):
            return False
        if self.check_current_course_conflict(a_class, course, time):
            return False
        return True

    # 连堂课约束条件检测
    def _fit_link(self, link_course_position):
        # 一天最大连堂
        for x in range(self.static_week):
            count = 0
            for y in range(self.static_section):
                if link_course_position[x][y] is not None:
                    count += 1
            if count > 2:
                return False

        link_course_location = {}
        for x in range(self.static_week):
            for y in range(self.static_section):
                course = link_course_position[x][y]
                if course is not None:
                    if course in link_course_location:
                        if x - link_course_location[course] < 2:
                            return False
                    link_course_location[course] = x
        return True

    # 交换两个点的课程
    def _cell_swap(self, a_class, one_cell, other_cell):
        self.schedules[a_class][one_cell.week][one_cell.section] = other_cell.course
        self.schedules[a_class][other_cell.week][other_cell.section] = one_cell.course

    # 将cells在课表中的位置设置为空
    def _set_cell_empty(self, a_class, cells):
        def set_empty(a_cell):
            self.schedules[a_class][a_cell.week][a_cell.section] = None

        if isinstance(cells, list):
            for cell in cells:
                set_empty(cell)
        else:
            set_empty(cells)

    # 将cells设置到课表中
    def _set_cell(self, a_class, cells):
        def set_value(a_cell):
            self.schedules[a_class][a_cell.week][a_cell.section] = a_cell.course

        if isinstance(cells, list):
            for cell in cells:
                set_value(cell)
        else:
            set_value(cells)

    # 移动普通点, 判断是否可以交换，如果可以交换直接交换，不可以返回false
    def swap_common(self, a_class, one_cell: Cell, other_cell: Cell):
        self._set_cell_empty(a_class, [one_cell, other_cell])
        if self._fit(a_class, one_cell.course, other_cell.get_time()) \
                and self._fit(a_class, other_cell.course, one_cell.get_time()):
            self._cell_swap(a_class, one_cell, other_cell)
            return True
        self._set_cell(a_class, [one_cell, other_cell])
        return False

    # 移动连堂课，连堂课-整体移动 不改变连堂课的数量
    def swap_link_course(self, a_class, one_cell_list, other_cell_list):
        def set_empty():
            self._set_cell_empty(a_class, one_cell_list)
            self._set_cell_empty(a_class, other_cell_list)

        def set_value():
            self._set_cell(a_class, one_cell_list)
            self._set_cell(a_class, other_cell_list)

        if len(one_cell_list) != len(other_cell_list):
            return False

        set_empty()
        for i in range(len(one_cell_list)):
            if not self._fit(a_class, one_cell_list[i].course, other_cell_list[i].get_time()) \
                    or not self._fit(a_class, other_cell_list[i].course, one_cell_list[i].get_time()):
                set_value()
                return False
        # 修改连堂课位置
        one_link_location = one_cell_list[0]
        other_link_location = other_cell_list[0]
        one_course = None
        if one_cell_list[0].course == one_cell_list[1].course:
            one_course = one_cell_list[0].course
        self.link_sign[a_class][one_link_location.week][one_link_location.section] = other_link_location.course
        self.link_sign[a_class][other_link_location.week][other_link_location.section] = one_course

        # 判定是否满足连堂课设置
        if not self._fit_link(self.link_sign[a_class]):
            self.link_sign[a_class][one_link_location.week][one_link_location.section] = one_course
            self.link_sign[a_class][other_link_location.week][other_link_location.section] = other_link_location.course
            set_value()
            return False

        # 交换两个位置
        for i in range(len(one_cell_list)):
            self._cell_swap(a_class, one_cell_list[i], other_cell_list[i])
        return True

    # TODO: 移动联结课程
    def swap_bind_class(self, a_class, one_cell, other_cell):
        other_course = other_cell.course
        key = a_class + '-' + other_course
        bind_classes = self.bind_classes[key]
        self._set_cell_empty(a_class, [one_cell, other_cell])
        if not self._fit(a_class, one_cell.course, other_cell.get_time()) \
                or not self._fit(a_class, other_cell.course, one_cell.course):
            return False

        for class_info in bind_classes:
            other_class = class_info['class']
            if not self._fit(other_class, other_course):
                pass
        return False

    # 连堂课转换，只与连堂课进行转换
    # TODO: 增加连堂课与非连堂课之间的转换
    def sort_swap_link(self, a_class, one_link_cell, other_cell):
        schedule = self.schedules[a_class]
        if one_link_cell[0].course == other_cell.course:
            return False
        if other_cell.course is not None:
            key = a_class + '-' + other_cell.course
            if key in self.bind_classes:
                return False
        if other_cell.section + 1 < self.static_section and \
                other_cell.course == schedule[other_cell.week][other_cell.section + 1]:
            other_cell_list = [other_cell, Cell(other_cell.course, other_cell.week, other_cell.section + 1)]
            self._set_cell_empty(a_class, other_cell_list)
            self._set_cell_empty(a_class, one_link_cell)
            if self.swap_link_course(a_class, one_link_cell, other_cell_list):
                return True
            else:
                self._set_cell(a_class, one_link_cell)
                self._set_cell(a_class, other_cell_list)
        return False

    def swap_common_conflict(self, a_class, one_cell, other_cell):
        if self._fit(a_class, other_cell.course, one_cell.get_time()) \
                and not self.check_fixed_condition_conflict(a_class, one_cell.course, other_cell.get_time()):
            self._cell_swap(a_class, one_cell, other_cell)
            return True, {'class': a_class, 'course': one_cell.course, 'week': other_cell.week,
                          'section': other_cell.section}
        if self._fit(a_class, one_cell.course, other_cell.get_time()) \
                and not self.check_fixed_condition_conflict(a_class, other_cell.course, one_cell.get_time()):
            self._cell_swap(a_class, one_cell, other_cell)
            return True, {'class': a_class, 'course': other_cell.course, 'week': one_cell.week,
                          'section': one_cell.section}
        return False, None

    # 两点之间交换
    # 交换冲突点
    def sort_swap_conflict(self, a_class, one_cell, other_cell):
        schedule = self.schedules[a_class]
        if one_cell.course == other_cell.course:
            return False, None
        if other_cell.course is not None:
            key = a_class + '-' + other_cell.course
            if key in self.bind_classes:
                return False, None
        if other_cell.section + 1 < self.static_section and \
                other_cell.course == schedule[other_cell.week][other_cell.section + 1]:
            return False, None
        if other_cell.section > 0 and other_cell.course == schedule[other_cell.week][other_cell.section - 1]:
            return False, None
        # 普通点交换
        self._set_cell_empty(a_class, [one_cell, other_cell])
        flag, next_cell = self.swap_common_conflict(a_class, one_cell, other_cell)
        if flag:
            self._set_cell_empty(a_class, Cell(next_cell['course'], next_cell['week'], next_cell['section']))
            return True, next_cell
        else:
            self._set_cell(a_class, [one_cell, other_cell])
        return False, None

    # 两个点 之间交换
    # 判断other_cell点的类型(联结课程，连堂课，普通课),然后进行交换判定
    def sort_swap(self, a_class, one_cell, other_cell):
        schedule = self.schedules[a_class]
        if one_cell.course == other_cell.course:
            return False
        # 联结课程
        if other_cell.course is not None:
            key = a_class + '-' + other_cell.course
            if key in self.bind_classes:
                return False
        # 连堂课判定
        if other_cell.section + 1 < self.static_section and \
                other_cell.course == schedule[other_cell.week][other_cell.section + 1]:
            other_cell_list = [other_cell, Cell(other_cell.course, other_cell.week, other_cell.section + 1)]
            if one_cell.section not in [0, 2, 4]:
                course = schedule[one_cell.week][one_cell.section - 1]
                one_cell_list = [Cell(course, one_cell.week, one_cell.section - 1), one_cell]
                if self.swap_link_course(a_class, one_cell_list, other_cell_list):
                    return True
            if one_cell.section not in [1, 3, self.static_section - 1]:
                course = schedule[one_cell.week][one_cell.section + 1]
                one_cell_list = [one_cell, Cell(course, one_cell.week, one_cell.section + 1)]
                if self.swap_link_course(a_class, one_cell_list, other_cell_list):
                    return True
            return False

        if other_cell.section > 0 and other_cell.course == schedule[other_cell.week][other_cell.section - 1]:
            return False

        # 普通点交换
        if self.swap_common(a_class, one_cell, other_cell):
            return True

    def lookup(self, a_class, one_cell):
        for x in range(self.static_week):
            for y in range(self.static_section):
                course = self.schedules[a_class][x][y]
                if isinstance(one_cell, list):
                    if course == one_cell[0].course:
                        continue
                    if self.sort_swap_link(a_class, one_cell, Cell(course, x, y)):
                        return True
                else:
                    if course == one_cell.course:
                        continue
                    if self.sort_swap(a_class, one_cell, Cell(course, x, y)):
                        return True
        return False

    # 检测冲突类型
    def check_conflict_type(self, a_class, course, time):
        if self.check_fixed_condition_conflict(a_class, course, time):
            return False
        if self.check_current_course_conflict(a_class, course, time) and self.check_link_teacher_conflict(a_class,
                                                                                                          course, time):
            return False
        if self.check_current_course_conflict(a_class, course, time):
            self._set_cell(a_class, Cell(course, time['week'], time['section']))
            return self.solve_current_course_conflict(a_class, course, time)
        if self.check_link_teacher_conflict(a_class, course, time):
            return self.solve_link_teacher_conflict(a_class, course, time)
        return None

    # 当天课程冲突, 移动另一个冲突点
    def solve_current_course_conflict(self, a_class, course, time):
        schedule = self.schedules[a_class]
        for y in range(self.static_section):
            if schedule[time['week']][y] == course and y != time['section']:
                # 判断另一冲突点是否为连堂课
                if y + 1 < self.static_section and schedule[time['week']][y + 1] == course:
                    return self.lookup(a_class, [Cell(course, time['week'], y), Cell(course, time['week'], y + 1)])
                return self.lookup(a_class, Cell(course, time['week'], y))

    # 关联班级课程冲突
    def solve_link_teacher_conflict(self, a_class, course, time):
        classes = self.link_classes[a_class][course]
        for other_class in classes:
            if self.schedules[other_class][time['week']][time['section']] == course:
                if not self.lookup(other_class, Cell(course, time['week'], time['section'])):
                    return False
        self._set_cell(a_class, Cell(course, time['week'], time['section']))
        return True

    # 固定条件冲突, 转换冲突点
    def solve_fixed_condition_conflict(self, a_class, course, old_course, time):
        for x in range(self.static_week):
            for y in range(self.static_section):
                other_course = self.schedules[a_class][x][y]
                if course == other_course or other_course == old_course:
                    continue
                flag, next_cell = self.sort_swap_conflict(a_class, Cell(course, time['week'], time['section']),
                                                  Cell(other_course, x, y))
                if flag:
                    return next_cell
        return False

    # 获取空余位置
    def get_schedule_empty_position(self, a_class):
        # 获取空余位置
        schedule = self.schedules[a_class]
        for x in range(self.static_week):
            for y in range(self.static_section):
                course = schedule[x][y]
                key = str(x) + str(y)
                if course is None:
                    if key in self.fixed_not_assign and self.fixed_not_assign[key] is None:
                        continue
                    return {'week': x, 'section': y}

    # 标记连堂课位置
    def _sign_link_course(self):
        if not self.link_sign:
            self.link_sign = {}
            for a_class in self.classes:
                self.link_sign[a_class] = []
                for x in range(self.static_week):
                    self.link_sign[a_class].append([None for i in range(self.static_section)])
                    for y in range(self.static_section):
                        if y >= self.static_section - 1:
                            continue
                        if self.schedules[a_class][x][y] is not None \
                                and self.schedules[a_class][x][y] == self.schedules[a_class][x][y + 1]:
                            self.link_sign[a_class][x][y] = self.schedules[a_class][x][y]

    def run(self):
        for conflict in self.conflict_list:
            flag = False
            time = self.get_schedule_empty_position(conflict['class'])
            a_class = conflict['class']
            conflict['week'] = time['week']
            conflict['section'] = time['section']

            old_course = '旧'
            count = 0
            while not flag and count < 10:
                cell = Cell(conflict['course'], conflict['week'], conflict['section'])
                flag = self.lookup(a_class, cell)
                if not flag:
                    self._set_cell_empty(a_class, cell)
                    value = self.check_conflict_type(a_class, cell.course, cell.get_time())
                    if value is None:
                        self._set_cell(a_class, cell)
                        break
                    if not value:
                        new_conflict = self.solve_fixed_condition_conflict(a_class, cell.course,
                                                                           old_course,
                                                                           cell.get_time())
                        if isinstance(new_conflict, dict):
                            old_course = conflict['course']
                            conflict = new_conflict
                        else:
                            return False
                    if value:
                        break
                count += 1
            if count >= 10:
                return False
        return True

    def run_of_outer(self, schedules, conflict_list):
        for i in range(len(schedules)):
            class_name = self.classes[i]
            self.schedules[class_name] = schedules[i]
        self.conflict_list = conflict_list
        self._sign_link_course()
        return self.run()
