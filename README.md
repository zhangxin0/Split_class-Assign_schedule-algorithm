# 安装步骤

1、安装django
 > pip3 install django -i  https://pypi.tuna.tsinghua.edu.cn/simple/

2、安装pymysql
> pip3 install pymysql -i  https://pypi.tuna.tsinghua.edu.cn/simple/

3、激活虚拟环境
> source bin/activate


4、遇到问题：`You have 17 unapplied migration(s)....`

解决方法

> python3 manage.py migrate
