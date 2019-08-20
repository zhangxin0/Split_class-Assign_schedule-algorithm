from django.shortcuts import render
import json
import algorithmapp.algorithm.assign_schedule.test_assign_schedule as assign_schedule
import algorithmapp.algorithm.assign_class.test_split_class as assign_class
import algorithmapp.algorithm.assign_schedule.data_source as data_source
import algorithmapp.algorithm.assign_schedule.data_g2_demo as data
import algorithmapp.algorithm.assign_class.split_class_data as split_class_source


# 模拟访问schedule_course，并传入数据
def moc_assign_course(request):
    data_source_object = data_source.DataSource()
    data_source_object.set_from_file(data)
    # 序列化对象
    json_object = json.dumps(data_source_object, default=lambda obj: obj.__dict__, indent=4)
    result = schedule_course(request, json_object)
    return render(request, 'algorithmapp/index.html', {'result': result})


# 模拟访问split_class，并传入数据
def moc_split_class(request):
    split_class_data = split_class_source.DataSource()
    split_class_data.set_from_generator()
    # 序列化对象
    json_object = json.dumps(split_class_data, default=lambda obj: obj.__dict__, indent=4)
    result = split_class(request, json_object)
    return render(request, 'algorithmapp/split_class.html', {'result': result})


def schedule_course(request, json_object):
    # 解析数据
    data_transfer = json.loads(json_object)
    data_source_object = data_source.DataSource()
    data_source_object.set_from_json(data_transfer)

    result = assign_schedule.main(data_source_object)
    return result


def split_class(request, json_object):
    # 解析数据
    data_transfer = json.loads(json_object)
    data_source_object = split_class_source.DataSource()
    data_source_object.set_from_json(data_transfer)

    result = assign_class.main(data_source_object)
    return result
