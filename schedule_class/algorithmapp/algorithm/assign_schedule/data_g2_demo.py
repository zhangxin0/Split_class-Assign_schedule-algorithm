"""
 高二排课数据Demo 不可变动
"""
COURSE_TOTAL = {'语': 5, '数': 6, '英': 5, '物': 4, '化': 4, '生': 4, '历': 4, '政': 4, '地': 4, '体': 3, '音-美': 1, '班': 1}
COURSE_LINKED_HOURS = {'语': 1, '数': 1, '英': 1, '物': 1, '化': 1, '生': 1, '历': 1, '政': 1, '地': 1, '体': 0, '音-美': 0, '班': 0}
COURSE = ['语', '数', '英', '物', '化', '生', '历', '政', '地', '体', '班', '音-美']
CLASSES = ['1班', '2班', '3班', '4班', '5班', '6班', '7班', '8班', '9班']
# Notice: 班级所排科目从此数据结构中遍历，因此固定不排科目中Map的key值必须包含所有的科目
CLASSES_COURSE_TEACHER = {
    '1班': {'语': '毕姗', '数': '曹宇', '英': '路平', '物': '王碧雪', '化': '刘臣', '音-美': '王祎', '班': '刘臣', '体': '体-1', '政': '许鑫'},
    '2班': {'语': '杨青', '数': '高金华', '英': '骆晓梦', '物': '齐伟华', '生': '王丹', '音-美': '王祎', '班': '王丹', '体': '体-1', '政': '许鑫'},
    '3班': {'语': '何映', '数': '高金华', '英': '骆晓梦', '物': '徐金宝', '化': '谭湘湘', '音-美': '王祎', '班': '徐金宝', '体': '体-1', '政': '许鑫'},
    '4班': {'语': '毕姗', '数': '季琳琳', '英': '孙敏嘉', '化': '谭湘湘', '生': '王丹', '音-美': '王祎', '班': '谭湘湘', '体': '体-1', '政': '韩志红',
           '物': '齐伟华'},
    '5班': {'语': '于安琪', '数': '白彩芳', '英': '孙敏嘉', '物': '齐伟华', '化': '刘臣', '音-美': '王祎', '班': '孙敏嘉', '体': '体-1', '政': '韩志红'},
    '6班': {'语': '吉茹颖', '数': '齐雪然', '英': '张文阁', '物': '徐金宝', '化': '王晓捷', '音-美': '王祎', '班': '齐雪然', '体': '体-2', '政': '韩志红'},
    '7班': {'语': '何映', '数': '季琳琳', '英': '德永红', '地': '雷志清', '政': '刘婕', '音-美': '王祎', '班': '何映', '体': '体-2', '物': '齐伟华'},
    '8班': {'语': '于安琪', '数': '白彩芳', '英': '德永红', '历': '黄艳', '地': '刘壮壮', '音-美': '王祎', '班': '白彩芳', '体': '体-2', '政': '刘婕',
           '物': '徐金宝'},
    '9班': {'语': '杨青', '数': '曹宇', '英': '路平', '历': '黄艳', '政': '刘婕', '音-美': '王祎', '班': '路平', '体': '体-2', '物': '王碧雪'}
}
# 添加一天最大的连堂课数目
# 走班教师
GO_TEACHERS = ['王碧雪', '王晓捷', '王丹', '于秀艳', '黄艳', '雷志清', '刘壮壮', '许鑫']

WEEK = 5
SECTION = 8

# 连堂课一天最大数
LINK_COURSE_COUNT_PEER_DAY = 1

# 额外需要安排的课程
EXTRA_ASSIGN_COURSE = {
    # '1班': [{'course': '语', 'num': 5, 'link': 1}, {'course': '数', 'num': 5, 'link': 1},
    #        {'course': '英', 'num': 5, 'link': 1}, {'course': '化', 'num': 4, 'link': 1},
    #        {'course': '生', 'num': 4, 'link': 1}, {'course': '体', 'num': 0, 'link': 0}],
    '1班': [{'course': '政', 'num': 2, 'teacher': '许鑫'}],
    '2班': [{'course': '政', 'num': 2, 'teacher': '许鑫'}],
    '3班': [{'course': '政', 'num': 2, 'teacher': '许鑫'}],
    '4班': [{'course': '政', 'num': 2, 'teacher': '韩志红'}, {'course': '物', 'num': 2, 'teacher': '齐伟华'}],
    '5班': [{'course': '政', 'num': 2, 'teacher': '韩志红'}],
    '6班': [{'course': '政', 'num': 2, 'teacher': '韩志红'}],
    '7班': [{'course': '物', 'num': 2, 'teacher': '齐伟华'}],
    '8班': [{'course': '政', 'num': 2, 'teacher': '刘婕'}, {'course': '物', 'num': 2, 'teacher': '徐金宝'}],
    '9班': [{'course': '物', 'num': 2, 'teacher': '王碧雪'}]
}

# 联结班级
BIND_CLASSES = {'1班-化': {'class': '2班', 'subject': '生'}, '9班-政': {'class': '7班', 'subject': '地'}}

# FIXED COURSES POSITION:
# 固定不排课-走班课 / 只考虑走班情况 / + 固定不排类
FLOW_CLASS_TIME = [
    {'week': 2, 'section': 5},
    {'week': 4, 'section': 5},
    {'week': 5, 'section': 5},
    {'week': 3, 'section': 3},
]
# 不安排任何科目的位置
NOT_ASSIGN_TIME = [
    {'week': 1, 'section': 8},
    {'week': 2, 'section': 8},
]
# 固定教师不排科
NOT_ASSIGN_TEACHER = {
    # demo
    # '杨静': [{'week': 1, 'section': 7}, {'week': 2, 'section': 7}, {'week': 3, 'section': 7}, {'week': 5, 'section': 7}]
}
# 固定不排科目
NOT_ASSIGN_COURSE = {
    '语': [{'week': 4, 'section': 5}, {'week': 4, 'section': 6}, {'week': 4, 'section': 7}, {'week': 4, 'section': 8},
          {'week': 3, 'section': 2}],
    '数': [{'week': 4, 'section': 1}, {'week': 4, 'section': 2}, {'week': 4, 'section': 3}, {'week': 4, 'section': 4},
          {'week': 2, 'section': 5},
          {'week': 1, 'section': 5}, {'week': 1, 'section': 6}, {'week': 1, 'section': 7}, {'week': 1, 'section': 8},
          {'week': 2, 'section': 6}, {'week': 2, 'section': 7}, {'week': 2, 'section': 8},
          # {'week': 4, 'section': 5}, {'week': 4, 'section': 6}, {'week': 4, 'section': 7}, {'week': 4, 'section': 8},
          {'week': 5, 'section': 5}, {'week': 5, 'section': 6}, {'week': 5, 'section': 7}, {'week': 5, 'section': 8}],
    '英': [{'week': 3, 'section': 1}, {'week': 3, 'section': 2}, {'week': 3, 'section': 3}, {'week': 3, 'section': 4},
          {'week': 2, 'section': 6}, {'week': 2, 'section': 7}],
    '物': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 5, 'section': 4}],
    '化': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 5, 'section': 2}],
    '生': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 1, 'section': 1}],
    '历': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 1, 'section': 1}],
    '政': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 5, 'section': 1}],
    '地': [{'week': 3, 'section': 5}, {'week': 3, 'section': 6}, {'week': 3, 'section': 7}, {'week': 3, 'section': 8},
          {'week': 1, 'section': 1}],
    '体': [{'week': 4, 'section': 5}, {'week': 4, 'section': 6}, {'week': 4, 'section': 7}, {'week': 4, 'section': 8}],
    '音-美': [{'week': 2, 'section': 3}],
    '班': [],
}

# 排好的固定课程
PART_SCHEDULE = [
    # 手排关联课-demo
    # {'week': 4, 'section': 6, 'class': '2班', 'course': '生'},
    {'week': 2, 'section': 6, 'class': '1班', 'course': '体'},
    {'week': 2, 'section': 6, 'class': '2班', 'course': '体'},
    {'week': 2, 'section': 6, 'class': '3班', 'course': '体'},
    {'week': 2, 'section': 6, 'class': '4班', 'course': '体'},
    {'week': 2, 'section': 6, 'class': '5班', 'course': '体'},

    {'week': 2, 'section': 7, 'class': '6班', 'course': '体'},
    {'week': 2, 'section': 7, 'class': '7班', 'course': '体'},
    {'week': 2, 'section': 7, 'class': '8班', 'course': '体'},
    {'week': 2, 'section': 7, 'class': '9班', 'course': '体'},

    {'week': 4, 'section': 8, 'class': '1班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '2班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '3班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '4班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '5班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '6班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '7班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '8班', 'course': '体'},
    {'week': 4, 'section': 8, 'class': '9班', 'course': '体'},

    {'week': 5, 'section': 3, 'class': '1班', 'course': '体'},
    {'week': 5, 'section': 3, 'class': '2班', 'course': '体'},
    {'week': 5, 'section': 3, 'class': '3班', 'course': '体'},
    {'week': 5, 'section': 3, 'class': '4班', 'course': '体'},
    {'week': 5, 'section': 3, 'class': '5班', 'course': '体'},

    {'week': 5, 'section': 4, 'class': '6班', 'course': '体'},
    {'week': 5, 'section': 4, 'class': '7班', 'course': '体'},
    {'week': 5, 'section': 4, 'class': '8班', 'course': '体'},
    {'week': 5, 'section': 4, 'class': '9班', 'course': '体'},

]

# 连堂课时间
LINK_COURSE_TIMES = [
    {'week': 1, 'section': 1},
    # {'week': 1, 'section': 2},
    {'week': 1, 'section': 3},
    {'week': 1, 'section': 5},
    {'week': 1, 'section': 6},
    {'week': 1, 'section': 7},
    {'week': 1, 'section': 8},
    {'week': 2, 'section': 1},
    # {'week': 2, 'section': 2},
    {'week': 2, 'section': 3},
    {'week': 2, 'section': 5},
    {'week': 2, 'section': 6},
    {'week': 2, 'section': 7},
    {'week': 2, 'section': 8},
    {'week': 3, 'section': 1},
    # {'week': 3, 'section': 2},
    {'week': 3, 'section': 3},
    {'week': 3, 'section': 5},
    {'week': 3, 'section': 6},
    {'week': 3, 'section': 7},
    {'week': 3, 'section': 8},
    {'week': 4, 'section': 1},
    # {'week': 4, 'section': 2},
    {'week': 4, 'section': 3},
    {'week': 4, 'section': 5},
    {'week': 4, 'section': 6},
    {'week': 4, 'section': 7},
    {'week': 4, 'section': 8},
    {'week': 5, 'section': 1},
    # {'week': 5, 'section': 2},
    {'week': 5, 'section': 3},
    {'week': 5, 'section': 5},
    {'week': 5, 'section': 6},
    {'week': 5, 'section': 7},
    {'week': 5, 'section': 8},
]
