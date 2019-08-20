import data_g2_demo as data
import assign_schedule.data_source as data_source

data_source1 = data_source.DataSource()
data_source1.set_from_file(data)
print(data_source1.__dict__)
