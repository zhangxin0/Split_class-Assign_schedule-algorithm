from . import precise_devide_class as assign_class
import copy


def main(data_source):
    data = copy.deepcopy(data_source)
    result = assign_class.PreciseSplit(data).run()
    return result

