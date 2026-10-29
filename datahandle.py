import re
import mysql
import pandas
import pymysql
import math
class DataHandle:

    def __init__(self):
        # 实例化数据库对象
        print(">>>链接数据库")
        self.__sql = mysql.MySql()
        self.connect = pymysql.connect(host="127.0.0.1",
                                       port=3306,
                                       user="root",
                                       password="123456",
                                       database="spiderdatabase",
                                       charset="utf8")

    def run(self):
        self.__dataHandle()
        self.__dataToCsv()

    # 将原始数据转换为csv文件 Data.csv 同时清除重复项
    def __dataToCsv(self):
        # 从数据库获取原始数据
        row_data = self.__sql.readHandledData()
        # 将数据转换为dataframe格式
        data = pandas.DataFrame(row_data)
        # 设置数据索引
        data_1 = data.set_index('num', drop=True)
        # 写入csv
        pandas.DataFrame.to_csv(data_1, 'Data.csv', encoding='utf-8')
        print(">>>数据转换csv格式成功")

        # 删除重复值
        df = pandas.read_csv('Data.csv', index_col=0)
        # 在当前数据集操作
        df.drop_duplicates(inplace=True)
        print(">>>删除重复值成功")

    # 原始数据处理,写到处理数据表
    def __dataHandle(self):
        #self.__sql.delInternship()
        # 从原始数据表获取数据
        table = self.__sql.readRowData()
        # 记录处理的数据数量
        count = 0
        # 遍历表单
        for data in table:
            # 获取工作名称
            name = data['name']
            # 获取工作地点
            place = self.__placeHandle(data['place'])
            city = place[0]
            area = place[1]
            detail = place[2]
            # 获取公司名字
            company = data['company']
            # 获取公司规模
            scale = self.__scaleHandle(data['scale'])
            # 获取薪资
            salary_list = self.__salaryHandle(data['salary'])
            min_salary = salary_list[0]
            max_salary = salary_list[1]
            avg_salary = salary_list[2]
            # 获取学历要求
            education = data['education']
            # 获取经验要求
            experience = self.__experienceHandle(data['experience'])
            # 获取公司标签
            label = data['label']
            # 获取技能需求
            skill = data['skill']
            # 获取公司福利
            welfare = data['welfare']

            type = data['type']
            #已有不处理
            self.__sql.saveHandledData(name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
                                experience,label, skill, welfare)
            self.__SubTable(type,name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
                                experience,label, skill, welfare)
            count = count + 1

        print('>>>数据处理完成 共处理 {} 条数据'.format(count))

    # 薪资处理---> 最大值、最低值、平均值
    def __salaryHandle(self,str_salary):
        # salary[0]:最小值
        # salary[1]:最大值
        # salary[2]:平均值
        salary = []
        if "薪" in str_salary:  # 工资月大于12 的情况
            # 薪资系数
            k = int(str_salary[-3:-1]) / 12
            # 去除 ‘-’ 便于分割
            str_1 = str_salary[:-5].replace('-', ' ')
            list_1 = str_1.split(" ")
            minSalary = int(int(list_1[0]) * k * 1000)
            maxSalary = int(int(list_1[1]) * k * 1000)
            avgSalary = (maxSalary + minSalary) / 2.0
            salary.append(minSalary)
            salary.append(maxSalary)
            salary.append(avgSalary)
        elif "以上" in str_salary:  # 只给出最低工资的情况
            minSalary = int(str_salary[:2]) * 1000
            maxSalary = int(str_salary[:2]) * 1000
            avgSalary = (maxSalary + minSalary) / 2.0
            salary.append(minSalary)
            salary.append(maxSalary)
            salary.append(avgSalary)
        else:
            str_1 = str_salary[:-1].replace('-', ' ')
            list_1 = str_1.split(" ")
            #minSalary = int(int(list_1[0]) * 1000)
            minSalary = int(int(re.sub("[^0-9]", "", list_1[0])) * 1000)
            maxSalary = int(int(re.sub("[^0-9]", "", list_1[1])) * 1000)
            avgSalary = (maxSalary + minSalary) / 2.0
            salary.append(minSalary)
            salary.append(maxSalary)
            salary.append(avgSalary)

        return salary

    # 地点处理
    def __placeHandle(self,str_place):
        # place[0] 城市
        # place[1] 具体区
        # place[2] 具体地点
        # 如果为空则用其他代替
        place = []
        if '·' in str_place:
            place = str_place.split("·")
            if len(place) == 2:
                place.append('其他')
            else:
                return place
        else:
            place.append(str_place)
            place.append('其他')
            place.append('其他')
        return place

    # 经验处理---->  保留经验去除学历
    def __experienceHandle(self,str_exp):
        if "学历不限" in str_exp:
            var = str_exp[:-4]
        else:
            var = str_exp[:-2]
        return var

    # 公司规模处理
    def __scaleHandle(self,str_scale):
        ret = re.findall(r"\d+", str_scale)
        if len(ret) != 1:
            scale = ret[0] + '-' + ret[1] + '人'
        else:
            scale = ret[0] + '人以上'
        return scale

    def __SubTable(self,type,name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
                                experience,label, skill, welfare):
        if type == 'java':
            table = 'java_data'
        elif type == 'python':
            table = 'python_data'
        elif type == 'c++' or 'c':
            table = 'c_data'
        elif type == 'c#' or '.net':
            table = 'c23_data'
        elif type == 'web前端':
            table = 'web_data'
        elif type == 'u3d' or 'ue':
            table = 'u3due_data'
        elif type == '算法':
            table = 'algorithm_data'
        elif type == '运维':
            table = 'oam_data'
        elif type == '测试':
            table = 'test_data'
        elif type == 'ios':
            table = 'ios_data'
        elif type == 'php':
            table = 'php_data'
        elif type == '安卓' or 'Android':
            table = 'android_data'

        str1 = 'insert into '
        str2 = '''(name, city, area, detail, company, scale, min_salary, max_salary,
                                          avg_salary, education, experience, label, skill, welfare)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        sql = str1 + table + str2
        try:

            #self.__sql.cursor.execute(sql, (name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
            #                    experience,label, skill, welfare))
            self.connect\
                .cursor(cursor=pymysql.cursors.DictCursor)\
                .execute(sql,
                         (name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
                          experience, label, skill, welfare)
                        )
            self.connect.commit()
            print(">>>【Sub子表模块】插入数据成功 ")
            print(sql)
            print((name, city, area, detail, company, scale, min_salary, max_salary, avg_salary, education,
                                experience,label, skill, welfare))
            #self.__sql.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(">>>【Sub子表模块】插入数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

