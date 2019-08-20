"""""
精确分班算法： 5005 iterations
author: xin
"""
import time
import random
# import openpyxl
# import copy
import math
import functools

"""
精确分班算法流程： 
主函数random_run(self, clusterKinds, stus, time)：
    聚类结果表明，把班级分为6类能够满足将所有选课种类的学生安排到班级中
    因此，本算法作为分班搜索的第二个阶段，从C6，2 = 15 种定二走一分班类型
    然后C15,6 从15种里面选出6类最为学校（年级）的最后分班方案 cluster_kinds
    
    _generateStus(self, num)： 按照权重矩阵weight 采用轮盘赌法随机生成num个测试学生群体
    
    对于所有的分班方案 for all a_cluster_kind in cluster_kinds:
        算法首先将学生按其所选科目随机分配到可选的6类中：assign_classes(self, clusterKinds, stus)
        调整类中的学生使其满足分班条件：adjust(self, classes, a_cluster_kind):
            根据成班条件限制，按照多了移动到其他班级 move_to_other，少了从其他班级获取学生的原则 get_from_other
    将所有可行的分班情况存储到 res, cluster_kind. res 记录每个班级的学生， cluster_kind 记录成班方案（所有班级的类型）
    
    对于所有的可分班结果 res：
        统计分班后各个班级走班科目的学生人数，并计算各走班科目是否符合成班条件，计算冲突学生数量： count_flow_conflict
        
Parameters:
    Data.STUDENTS: 学生人数
    Data.MIN_STU_NUM: 最小成班人数
    Data.MAX_STU_NUM: 最大成班人数
    stus: 学生信息，eg[1,2,3,50] 1,2,3表示科目编码，50表示学生id
    
Data Structure:
    classKinds[[1, 3], [2, 4], [.].[],...] contains C6,2 classKinds
    clusterKinds [[[1,3],[2,4],[.].[]],[[1,3],[2,4],[.].[]..],....] contain C15,6 clusters
    stu[subj1, subj2, subj3, ID]： 根据学生ID输出最后的分班信息 

输出结果：
    Conflict Num: 运行time 次的冲突数量列表-分班都符合条件，走班的成班人数冲突个数
    Cluster Kind：输出分班种类（6类）
    flow subject stu：[] 输出走班科目人数列表
    Failed time： 分班失败次数
    result : {'Conflict Num': 走班的成班人数冲突个数,'best_cluster_kind':分班种类 ,'count_flow_subj':走班科目人数列表, 
            'classes': class—students info}

注意：
    算法结果评价分为两个阶段：
        第一阶段：算法运行结果Failed = 0 表明分班失败次数
        第二阶段：冲突个数表明：分班结果满足，但是走班的学生不满足成班条件的冲突数量
    
"""


class PreciseSplit:

    def __init__(self, data):
        self.data = data
        self.STUDENTS = data.STUDENTS
        self.min_stu_num = data.MIN_STU_NUM
        self.max_stu_num = data.MAX_STU_NUM
        self.x2_min_stu_num = 2 * data.MIN_STU_NUM
        self.mid_min_max = (self.x2_min_stu_num + data.MAX_STU_NUM) / 2

    # List all possibilities C6,2 = 15 然后 C15,6 = 5005 种分班情况
    def _all_class_kind(self):
        # generate C6,2 class kinds
        classKinds = []
        for i in range(1, 6):
            for j in range(i + 1, 7):
                a_class_kind = [i, j]
                classKinds.append(a_class_kind)
        #  get CLUSTER kinds from C15,6
        clusterKinds = []
        for i1 in range(15 - 5):
            for i2 in range(i1 + 1, 15 - 4):
                for i3 in range(i2 + 1, 15 - 3):
                    for i4 in range(i3 + 1, 15 - 2):
                        for i5 in range(i4 + 1, 15 - 1):
                            for i6 in range(i5 + 1, 15):
                                a_cluster_kind = [classKinds[i1], classKinds[i2], classKinds[i3] \
                                    , classKinds[i4], classKinds[i5], classKinds[i6]]
                                # if self.count_subjects(a_cluster_kind):
                                clusterKinds.append(a_cluster_kind)
                                # print(a_cluster_kind)
        return clusterKinds

    # 判断一种分班结果a_cluster_kind 是否包含了所有的科目， 剪枝算法，如果不包含所有科目则放弃当前分枝搜索
    def count_subjects(self, a_cluster_kind):
        flag = False
        s = set([])
        for classKinds in a_cluster_kind:
            if classKinds[0] not in s:
                s.add(classKinds[0])
            if classKinds[1] not in s:
                s.add(classKinds[1])
        if len(s) == 6:
            flag = True
        return flag

    # 学生分班函数
    # res 记录所有可以分班的方案， cluster_kind 记录所有的分班类型
    def assign_classes(self, clusterKinds, stus):
        res = []
        # 一种分班方案： 6类班级种类
        cluster_kind = []
        for a_cluster_kind in clusterKinds:
            # Assign students to clusters:
            # classes 储存的是分好类的学生
            classes = self.assign_stus_cluster(stus, a_cluster_kind)
            if classes is None:
                continue
            num_assigned = 0
            for i in range(len(classes)):
                num_assigned += len(classes[i])
            # Add class conditions here:
            cluster_size = []
            # 判断所有学生是否完全分配到班级类别中
            if num_assigned == self.STUDENTS:
                # Now start adjust:
                for i in range(len(classes)):
                    cluster_size.append(len(classes[i]))
                # Adjust students to clusters:
                if not self.adjust(classes, a_cluster_kind):
                    continue
                cluster_size2 = []
                for i in range(len(classes)):
                    cluster_size2.append(len(classes[i]))
                if self.could_split(classes):
                    res.append(classes)
                    cluster_kind.append(a_cluster_kind)
        return res, cluster_kind

    # 调整6类下学生的数量，使其满足成班人数限制
    def adjust(self, classes, a_cluster_kind):
        def belong_to(stu, a_cluster_kind, i):
            count = 0
            for subj in stu[0:3]:
                if subj in a_cluster_kind[i]:
                    count += 1
            if count >= 2:
                return True
            return False

        # 策略1： 从其他类别种获取： 
        def get_from_other(i, classes):
            for x in range(len(classes)):
                if x != i:
                    len1 = len(classes[x])
                    if (len1 > self.min_stu_num and len1 < self.mid_min_max) or (len1 > self.x2_min_stu_num):
                        # move from cluster x to i:
                        for j in range(len(classes[x]) - 1, -1, -1):
                            stu_mv = classes[x][j]
                            if belong_to(stu_mv, a_cluster_kind, i):
                                classes[i].append(stu_mv)
                                classes[x].pop(j)
                                if (len(classes[i]) >= self.min_stu_num and len(classes[i]) <= self.max_stu_num) or len(
                                        classes[i]) >= self.x2_min_stu_num:
                                    return True
                                if (len(classes[x]) > self.min_stu_num and len(classes[x]) < self.mid_min_max) or (
                                        len(classes[x]) > self.x2_min_stu_num):
                                    continue
                                else:
                                    break
            return False

        # 移动到其他班级中：
        def move_to_other(i, classes):
            for x in range(len(classes)):
                if x != i:
                    len1 = len(classes[x])
                    if (len1 < self.max_stu_num) or (len1 >= self.mid_min_max):
                        # move from class i to x:
                        # list delete use reverse order
                        for j in range(len(classes[i]) - 1, -1, -1):
                            stu_mv = classes[i][j]
                            if belong_to(stu_mv, a_cluster_kind, x):
                                classes[x].append(stu_mv)
                                classes[i].pop(j)
                                if len(classes[x]) == self.max_stu_num:
                                    break
                                if len(classes[i]) <= self.max_stu_num:
                                    return True

            return False

        for i in range(len(classes)):
            cla = classes[i]
            n = len(cla)
            # < self.min_stu_num
            if n < self.min_stu_num:
                if not get_from_other(i, classes):
                    return False
            elif (n > self.max_stu_num) and (n < self.x2_min_stu_num):
                if not move_to_other(i, classes):
                    if not get_from_other(i, classes):
                        return False
        return True

    # 判断该类是否可拆班
    def could_split(self, classes):
        for i in range(len(classes)):
            n = len(classes[i])
            left = math.ceil(n / float(self.max_stu_num))
            right = math.floor(n / float(self.min_stu_num))
            if left > right:
                return False
        return True

    # Assign students to corresponded cluster
    # Random choose from all fit cluster to avoid last cluster no chance to get from other or move to other cluster
    def assign_stus_cluster(self, stus, a_cluster_kind):
        classes = []
        for i in range(len(a_cluster_kind)):
            classes.append([])
        for stu in stus:
            # Repeated count to another class_kind
            record_available_cluster = []
            for j in range(len(a_cluster_kind)):
                count = 0
                a_class_kind = a_cluster_kind[j]
                for subj in stu[0:3]:
                    if subj in a_class_kind:
                        count += 1
                if count >= 2:
                    # classes[j].append(stu)
                    record_available_cluster.append(j)
            if len(record_available_cluster) == 0:
                return None
            else:
                classes[record_available_cluster[random.randint(0, len(record_available_cluster) - 1)]].append(stu)
        return classes

    @staticmethod
    def count_subj(stus):
        list0 = [0, 0, 0, 0, 0, 0]
        for stu in stus:
            for subj in stu[0:3]:
                list0[subj - 1] += 1
        for i in range(len(list0)):
            print("Subject {} student number is: {}".format(i + 1, list0[i]))
        print("===========================")

    # 统计走班科目的学生人数
    def count_flow_stu(self, res, clusterKind):
        count_flow_conflict = []
        for i in range(len(res)):
            clusters = res[i]
            flow_count = [0, 0, 0, 0, 0, 0]
            for j in range(len(clusters)):
                cluster = clusters[j]
                for stu in cluster:
                    for subj in stu[0:3]:
                        if subj not in clusterKind[i][j]:
                            flow_count[subj - 1] += 1
            temp = 0
            for value in flow_count:
                if value < self.min_stu_num:
                    temp += self.min_stu_num - value
                elif value > self.max_stu_num and value < self.mid_min_max:
                    temp += value - self.max_stu_num
                elif value >= self.mid_min_max and value < self.x2_min_stu_num:
                    temp += self.x2_min_stu_num - value
            count_flow_conflict.append(temp)
        return count_flow_conflict

    # 分班后，计算走班科目的学生人数：
    def count_flow_subj(self, res, cluster):
        count_subj = [0, 0, 0, 0, 0, 0]
        for i in range(len(res)):
            for stu in res[i]:
                for subj in stu[0:3]:
                    if subj not in cluster[i]:
                        count_subj[subj - 1] += 1
        return count_subj

    # 主函数：
    # 运行 time 次，选取分班后走班科目成班的冲突数最小解
    def random_run(self, clusterKinds, stus, time):
        res_total_set = []
        best_cluster_kind = []
        count_flow_subj = []
        count_min = self.STUDENTS
        flag = False
        result = {}
        classes = []
        for i in range(time):
            # res:{res1 conf, res2 conf,...} 分班结果集， clusterKind：分班类别集合
            res, clusterKind = self.assign_classes(clusterKinds, stus)
            # time 次运行总解集： 记录每次运行后的解集
            res_total_set.append(res)
            if len(res) == 0:
                print("No result is found")
                continue
            flag = True
            count_flow_conflict = self.count_flow_stu(res, clusterKind)
            # 记录本次运行解集中，所有解中最小冲突数和结果
            for j in range(len(count_flow_conflict)):
                if count_min > count_flow_conflict[j]:
                    count_min = count_flow_conflict[j]
                    best_cluster_kind = clusterKind[j]
                    count_flow_subj = self.count_flow_subj(res[j], best_cluster_kind)
                    classes = res[j]
        if not flag:
            return None
        print("Conflict Num: {}".format(count_min))
        print("Cluster Kind:{}".format(best_cluster_kind))
        print("Count flow subject:{}".format(count_flow_subj))
        result['conflict_num'] = count_min
        result['best_cluster_kind'] = best_cluster_kind
        result['count_flow_subj'] = count_flow_subj
        result['classes'] = classes
        return result

    def log_execution_time(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print('{} average execute time is {}'.format(func.__name__, (end - start)))
            return result

        return wrapper

    #@log_execution_time
    def run(self):
        clusterKinds = self._all_class_kind()
        # time 运行次数： 多次运行选最优
        time = 1
        fail = 0
        sum = 0.0
        stus = self.data.stus
        self.count_subj(stus)
        # Test 100 and calculate conflict average:
        result = self.random_run(clusterKinds, stus, time)
        conf = result['conflict_num']
        if conf is None:
            fail += 1
        else:
            sum += conf
        print("Experiment {} time, average conflict time:{}".format(time, sum / (time - fail)))
        print("Failed time: {}".format(fail))
        # 返回分班结果
        return result
