# 分班、排课算法的Django http服务代码库

Python精确分班、排课算法在schedule_class/algorithrmapp/algorithm目录下

Java 聚类、邻域搜索算法在AssignClass目录下

# Pyhton算法引擎-安装步骤

1、安装django
 > pip3 install django -i  https://pypi.tuna.tsinghua.edu.cn/simple/

2、安装pymysql
> pip3 install pymysql -i  https://pypi.tuna.tsinghua.edu.cn/simple/

3、激活虚拟环境
> source bin/activate


4、遇到问题：`You have 17 unapplied migration(s)....`

解决方法

> python3 manage.py migrate
