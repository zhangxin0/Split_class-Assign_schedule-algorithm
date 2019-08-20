"""
分班数据
"""
import random

"""
Parameters:
    Data.STUDENTS: 学生人数
    Data.MIN_STU_NUM: 最小成班人数
    Data.MAX_STU_NUM: 最大成班人数
    stus: 学生信息，eg[1,2,3,50] 1,2,3表示科目编码，50表示学生id
"""


class DataSource:

    def __init__(self):
        self.STUDENTS = None
        self.MIN_STU_NUM = None
        self.MAX_STU_NUM = None
        self.stus = None

    def _generateStus(self, num):
        stus = []
        # a_stu last element is stu id
        a_stu = []
        subjects = [1, 2, 3, 4, 5, 6]
        weight = [3, 3, 3, 2, 2, 3]
        for i in range(num):
            a_stu = self.random_weight(subjects, weight, 3)
            a_stu.append(i)
            stus.append(a_stu)
        # print(stus)
        return stus

    # 轮盘赌法生成学生所选科目
    def random_weight(self, subjects, weight, n):
        sum = 0
        pos = []
        res = set()
        sample = []
        for i in weight:
            sum += i
            pos.append(sum)
        while len(res) < n:
            t = random.randint(0, sum)
            for v in range(len(pos)):
                if t < pos[v] and v not in res:
                    res.add(v)
                    break
        for i in res:
            sample.append(subjects[i])
        return sample

    def set_from_generator(self):
        self.STUDENTS = 300
        self.MIN_STU_NUM = 25
        self.MAX_STU_NUM = 38
        self.stus = self._generateStus(self.STUDENTS)
        # 按照权重矩阵weight 随机生成测试num个学生

    def set_from_json(self, json_map):
        self.__dict__ = json_map
