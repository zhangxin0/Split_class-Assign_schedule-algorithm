"""
 高二排课
"""


class DataSource:

    def __init__(self):
        # 课程标准数
        # {'语': 5,}
        self.COURSE_TOTAL = None
        # 连堂课总数
        # {'语': 1}
        self.COURSE_LINKED_HOURS = None
        # 所有课程数
        # ['语', '数']
        self.COURSE = None
        # 所有班级
        # ['1班', '2班']
        self.CLASSES = None
        # 班级教师安排
        self.CLASSES_COURSE_TEACHER = {}
        # 走班教师
        self.GO_TEACHERS = None

        self.WEEK = 5
        self.SECTION = 8

        # 一天最多的连堂课数
        self.LINK_COURSE_COUNT_PEER_DAY = None

        # 额外需要安排的课程
        # '1班': [{'course': '政', 'num': 2, 'teacher': '许鑫'}],
        self.EXTRA_ASSIGN_COURSE = None

        # 联结班级
        # {'1班-化': {'class': '2班', 'subject': '生'}, '9班-政': {'class': '7班', 'subject': '地'}}
        self.BIND_CLASSES = None

        # FIXED COURSES POSITION:
        # 固定不排课-走班课 / 只考虑走班情况 / + 固定不排类
        # [{'week': 2, 'section': 5}]
        self.FLOW_CLASS_TIME = None

        # 不安排任何科目的位置
        # [{'week': 1, 'section': 8}]
        self.NOT_ASSIGN_TIME = None

        # 固定教师不排科
        # '杨静': [{'week': 1, 'section': 7}, {'week': 2, 'section': 7}]
        self.NOT_ASSIGN_TEACHER = None

        # 固定不排科目
        # '语': [{'week': 4, 'section': 5}, {'week': 4, 'section': 6}, {'week': 4, 'section': 7},
        #                   {'week': 4, 'section': 8},
        #                   {'week': 3, 'section': 2}],
        self.NOT_ASSIGN_COURSE = None

        # 排好的固定课程
        # {'week': 4, 'section': 6, 'class': '2班', 'course': '生'},
        self.PART_SCHEDULE = None

        # 连堂课时间
        # {'week': 1, 'section': 1},
        self.LINK_COURSE_TIMES = None

    def set_from_file(self, data):
        for key in self.__dict__:
            if key in data.__dict__:
                self.__dict__[key] = data.__dict__[key]

    def set_from_json(self, json_map):
        self.__dict__ = json_map

