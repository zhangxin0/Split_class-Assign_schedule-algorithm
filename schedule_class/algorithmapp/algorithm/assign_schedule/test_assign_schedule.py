from . import assign_class_SA_v3_SaveConflict_LockedCla as assign_schedule
from . import solve_conflict as solve_conflict
import copy


def main(data_source):
    data1 = copy.deepcopy(data_source)
    solve_conflict_object = solve_conflict.SolveConflict(data1)

    data2 = copy.deepcopy(data_source)
    translate_data = assign_schedule.AssignSchedule.translate_from(data2)

    assign_schedule_object = assign_schedule.AssignSchedule(translate_data)
    result = assign_schedule_object.run(translate_data, solve_conflict_object.run_of_outer)

    return result
