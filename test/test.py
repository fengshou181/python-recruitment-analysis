# import pymysql
# from scipy import stats
# import numpy as np
# import pandas
#
#
# class Spe(object):
#     # 建立数据库链接
#     def __init__(self):
#         self.connect = pymysql.connect(host="127.0.0.1",
#                                        user="KOISHI",
#                                        password="yangyang0815",
#                                        database="spiderdatabase",
#                                        charset="utf8")
#         self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
#
#     # 关闭链接
#     def __del__(self):
#         self.connect.close()
#         self.cursor.close()
#
#     def test(self):
#         sql = '''
#                 select avg_salary from java_data
#                 where city = '厦门' and area = '思明区'
#                 and education = '本科'
#                 and skill like '%Spring%'
#             '''
#         self.cursor.execute(sql)
#         self.connect.commit()
#         return self.cursor.fetchall()
#
# s = Spe()
# data = s.test()
# dataList = []
# for var in data:
#     dataList.append(var['avg_salary'])
# print(dataList)


# a = 0.95
# alpha_list = [] # 可信度列表
# ci_width_list = [] # 置信区间宽度列表
# ci_upper_limit = [] # 置信区间上极限
# ci_lower_limit = [] # 置信区间下极限
# """  置信区间  """
# df = len(dataList) - 1
# ci = stats.t.interval(a, df, loc=np.mean(dataList), scale=stats.sem(dataList))
# # 算出置信区间的宽度
# print(type(ci))
# print(ci)
# ci_element = ci
#
# ci_lower_limit.append(ci_element[0])
# ci_upper_limit.append(ci_element[1])
# # ci_element.append(ci)
# ci_width = ci_element[1] - ci_element[0]  # 定义置信区间宽度
# ci_width_list.append(ci_width)
# print(ci_element[0],ci_element[1])  # 输出置信区间宽度

#
# while True:
#     try:
#         score = int(input("请输入你的成绩："))
#         assert score >= 0 and score <= 100, "输入有误请重新输入！"
#         if score >= 90:
#             print('成绩为：A')
#         elif score >= 80 and score <= 89:
#             print('成绩为：B')
#         elif score >= 60 and score <= 79:
#             print('成绩为：C')
#         else:
#             print('成绩为：D,不及格！！！')
#     except AssertionError as reason:
#         print(reason)
cmd = 'sss'

print(str(type(cmd)) + '22')