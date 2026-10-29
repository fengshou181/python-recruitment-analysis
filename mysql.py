import os
import pymysql
from collections import Counter
import json
import traceback


# 数据库对象
class MySql(object):
    # 建立数据库链接
    def __init__(self):
        self.connect = pymysql.connect(host=os.getenv("DB_HOST", "127.0.0.1"),
                                       port=int(os.getenv("DB_PORT", "3306")),
                                       user=os.getenv("DB_USER", "root"),
                                       password=os.getenv("DB_PASSWORD", "123456"),
                                       database=os.getenv("DB_NAME", "spiderdatabase"),
                                       charset="utf8")
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭链接
    def __del_(self):
        self.connect.close()
        self.cursor.close()

    # 手动关闭数据库链接
    def close(self):
        self.connect.close()
        self.cursor.close()

    '''============================================数据处理======================================================='''

    # 原始数据存储
    def saveData(self, job_name, job_place, job_company, job_scale, job_salary, job_education, job_experience,
                 job_label, job_skill, job_welfare,type):

        sql = '''
                insert into row_data(name,place,company,scale,salary,education,experience,label,skill,welfare,type)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        try:
            self.cursor.execute(sql, (job_name, job_place, job_company, job_scale, job_salary, job_education,
                                      job_experience, job_label, job_skill, job_welfare,type))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(">>>插入数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 原始数据存储
    def saveHandledData(self, name, city, area, detail, company, scale, salary_min, salary_max, salary_avg, education,
                        experience, label, skill, welfare):

        sql = '''
                insert into handled_data (name, city, area, detail, company, scale, min_salary, max_salary,
                                          avg_salary, education, experience, label, skill, welfare)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        try:
            self.cursor.execute(sql, (name, city, area, detail, company, scale, salary_min, salary_max, salary_avg,
                                      education, experience, label, skill, welfare))
            self.connect.commit()
            print("【数据处理模块】===>SUCCESS！插入数据成功 执行MySQL打印 ")
            print((name, city, area, detail, company, scale, salary_min, salary_max, salary_avg,
                                      education, experience, label, skill, welfare))
        except Exception as e:
            self.connect.rollback()
            print(">>>插入数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readRowData(self):
        sql = '''
                select * from row_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取处理后表单
    def readHandledData(self):
        sql = '''
                select * from handled_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readAlgorithmData(self):
        sql = '''
                select * from algorithm_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readAndroidData(self):
        sql = '''
                select * from android_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readCData(self):
        sql = '''
                select * from c_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readC23Data(self):
        sql = '''
                select * from c23_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readIosData(self):
        sql = '''
                select * from ios_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readJavaData(self):
        sql = '''
                select * from java_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readOamData(self):
        sql = '''
                select * from oam_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readPhpData(self):
        sql = '''
                select * from php_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readPythonData(self):
        sql = '''
                select * from python_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readTestData(self):
        sql = '''
                select * from test_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readU3dueData(self):
        sql = '''
                select * from u3due_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 读取原始表单
    def readWebData(self):
        sql = '''
                select * from web_data
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            # 获取所有字段
            fields = self.cursor.fetchall()
            return fields
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 去除薪资为的实习岗位，便于计算

    '''================================================首页======================================================'''

    # 获取表数据量
    def getLastNum(self):
        sql = '''
                select count(*) as total from handled_data
            '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def getMaxSalary(self):
        # 设置合理的最高薪资上限（月薪100万）
        reasonable_max = 1000000  
        sql = '''
                select max_salary from handled_data
                where max_salary = (
                    select MAX(max_salary) from handled_data 
                    where max_salary <= %s
                )
            '''

        try:
            self.cursor.execute(sql, (reasonable_max,))
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))
            return 100000  # 出错时返回默认值

    # 查询最低薪资
    def getMinSalary(self):
        sql = '''
                select min_salary from handled_data
                where min_salary = (select MIN(min_salary) from handled_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 计算全部数据的平均薪资
    def getAllAvgSalary(self):
        sql = '''
                select ROUND(AVG(avg_salary), 2) as avg_salary from handled_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询所有学历的薪资平均情况
    def getSalaryForEducation(self):
        sql_0 = '''
                select  edu from educationforsalary
        '''
        sql_1 = '''
                select AVG(min) from educationforsalary
                where edu = %s
        '''
        sql_2 = '''
                select AVG(max) from educationforsalary
                where edu = %s
        '''
        sql_3 = '''
                select AVG(avg) from educationforsalary
                where edu = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['edu'])
            edu = dict(Counter(education_list))
            for key in list(edu.keys()):
                if edu[key] < 26:
                    del edu[key]
                    continue
            edu_list = list(edu)
            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询总体学历
    def getEducation(self):
        sql = '''
                select education from handled_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            for key in list(edu.keys()):
                if edu[key] < 26:
                    del edu[key]
                    continue
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询总体经验与薪资关系
    def getSalaryForExperience(self):
        sql_0 = '''
                        select experience from experienceforsalary
                '''
        sql_1 = '''
                        select AVG(min_salary) from experienceforsalary
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from experienceforsalary
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from experienceforsalary
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 188:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询总体经验
    def getExperience(self):
        sql = '''
                select experience from handled_data
                       
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 188:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询总体城市情况情况
    def getCity(self):
        sql = '''
                select city from handled_data 
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            city = []
            for var in result:
                city.append(var['city'])
            return list(set(city))
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询所有岗位名称
    def getJobName(self):
        sql = '''
                select name from handled_data 
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            name = []
            for var in result:
                name.append(var['name'])
            return name
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 城市平均待遇
    def getSalaryForCity(self):

        city = self.getCity()
        sql = '''
                select AVG(salary) from salaryforcity
                where city = %s
          '''
        try:
            salary = []
            for var in city:
                self.cursor.execute(sql, var)
                self.connect.commit()
                result = self.cursor.fetchall()
                salary.append(result)

            salary_list = []
            for var in salary:
                for i in var:
                    salary_list.append(round(int(i['AVG(salary)'])))

            return json.dumps({'name': city, 'value': salary_list}, ensure_ascii=False)



        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 福利查询
    def getWelfare(self):
        sql = '''
                select welfare from handled_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            welfare = []
            for var in result:
                welfare.append(var['welfare'])
            return welfare

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    '''================================================Java======================================================'''

    # 取得Java的岗位数量
    def javaGetNum(self):
        sql = '''
                select count(*) as total from java_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得Java岗位的总体平均薪资
    def javaGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from java_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def javaGetMaxSalary(self):
        sql = '''
                select max_salary from java_data
                where max_salary = (select MAX(max_salary) from java_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def javaGetMinSalary(self):
        sql = '''
                select min_salary from java_data
                where min_salary = (select MIN(min_salary) from java_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def javaGetEdu(self):
        sql = '''
                       select education from java_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询java经验要求
    def javaGetExp(self):
        sql = '''
                   select experience from java_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # java薪资与学历的关系
    def javaGetEduForSalary(self):
        sql_0 = '''
                select distinct education from java_data
        '''
        sql_1 = '''
                select AVG(min_salary) from java_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from java_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from java_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # java经验与薪资
    def javaGetExpForSalary(self):
        sql_0 = '''
                        select experience from java_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from java_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from java_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from java_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def javaGetSkill(self):
        sql = '''
                select skill from java_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def javaRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        javaSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        javaMin = float(self.javaGetMinSalary())
        javaMax = float(self.javaGetMaxSalary())
        javaAvg = float(self.javaGetAvgSalary())
        javaNum = float(self.javaGetNum())
        # 添加最低薪资分数
        javaSocre.append(javaMin / Min)
        # 添加最高薪资分数
        javaSocre.append(javaMax / Max)
        # 添加平均薪资分数
        javaSocre.append(javaAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from java_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from java_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            javaSocre.append(1 - (Exp / javaNum))
            # 添加学历分数
            javaSocre.append(Edu / javaNum)
            # 添加数量分
            javaSocre.append((javaNum / Num) * 100)
            return json.dumps({'name': 'Java', 'value': javaSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================python============================================='''

    def pythonGetNum(self):
        sql = '''
                select count(*) as total from python_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得python岗位的总体平均薪资
    def pythonGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from python_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def pythonGetMaxSalary(self):
        sql = '''
                select max_salary from python_data
                where max_salary = (select MAX(max_salary) from python_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def pythonGetMinSalary(self):
        sql = '''
                select min_salary from python_data
                where min_salary = (select MIN(min_salary) from python_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def pythonGetEdu(self):
        sql = '''
                       select education from python_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询java经验要求
    def pythonGetExp(self):
        sql = '''
                   select experience from python_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # java薪资与学历的关系
    def pythonGetEduForSalary(self):
        sql_0 = '''
                select distinct education from python_data
        '''
        sql_1 = '''
                select AVG(min_salary) from python_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from python_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from python_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # java经验与薪资
    def pythonGetExpForSalary(self):
        sql_0 = '''
                        select experience from python_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from python_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from python_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from python_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def pythonGetSkill(self):
        sql = '''
                select skill from python_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def pythonRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        pythonSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        pythonMin = float(self.pythonGetMinSalary())
        pythonMax = float(self.pythonGetMaxSalary())
        pythonAvg = float(self.pythonGetAvgSalary())
        pythonNum = float(self.pythonGetNum())
        # 添加最低薪资分数
        pythonSocre.append(pythonMin / Min)
        # 添加最高薪资分数
        pythonSocre.append(pythonMax / Max)
        # 添加平均薪资分数
        pythonSocre.append(pythonAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from python_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from python_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            pythonSocre.append(1 - (Exp / pythonNum))
            # 添加学历分数
            pythonSocre.append(Edu / pythonNum)
            # 添加数量分
            pythonSocre.append((pythonNum / Num) * 100)
            return json.dumps({'name': 'Python', 'value': pythonSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================data============================================='''

    def dataGetNum(self):
        # 原实现取 MAX(num)（自增主键），清洗删行后与实际条数不符，改为真实行数
        sql = '''
                select count(*) as total from data_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            total = result['total']
            return total
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得数据分析岗位的总体平均薪资
    def dataGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from data_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def dataGetMaxSalary(self):
        sql = '''
                select max_salary from data_data
                where max_salary = (select MAX(max_salary) from data_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def dataGetMinSalary(self):
        sql = '''
                select min_salary from data_data
                where min_salary = (select MIN(min_salary) from data_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得数据分析学历情况
    def dataGetEdu(self):
        sql = '''
                       select education from data_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询数据分析经验要求
    def dataGetExp(self):
        sql = '''
                   select experience from data_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 数据分析薪资与学历的关系
    def dataGetEduForSalary(self):
        sql_0 = '''
                select distinct education from data_data
        '''
        sql_1 = '''
                select AVG(min_salary) from data_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from data_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from data_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 数据分析经验与薪资
    def dataGetExpForSalary(self):
        sql_0 = '''
                        select experience from data_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from data_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from data_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from data_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def dataGetSkill(self):
        sql = '''
                select skill from data_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def dataRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        dataSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        dataMin = float(self.dataGetMinSalary())
        dataMax = float(self.dataGetMaxSalary())
        dataAvg = float(self.dataGetAvgSalary())
        dataNum = float(self.dataGetNum())
        # 添加最低薪资分数
        dataSocre.append(dataMin / Min)
        # 添加最高薪资分数
        dataSocre.append(dataMax / Max)
        # 添加平均薪资分数
        dataSocre.append(dataAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from data_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from data_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            dataSocre.append(1 - (Exp / dataNum))
            # 添加学历分数
            dataSocre.append(Edu / dataNum)
            # 添加数量分
            dataSocre.append((dataNum / Num) * 100)
            return json.dumps({'name': '数据分析', 'value': dataSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================C============================================='''

    def cGetNum(self):
        sql = '''
                select count(*) as total from c_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得c岗位的总体平均薪资
    def cGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from c_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            # SQL 侧 AVG 会忽略薪资为 NULL 的异常记录，避免 Python 求和时 TypeError
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def cGetMaxSalary(self):
        sql = '''
                select max_salary from c_data
                where max_salary = (select MAX(max_salary) from c_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            # 设置合理的最高薪资上限（月薪10万元）
            if Max > 100000:
                Max = 100000
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def cGetMinSalary(self):
        sql = '''
                select min_salary from c_data
                where min_salary = (select MIN(min_salary) from c_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def cGetEdu(self):
        sql = '''
                       select education from c_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询java经验要求
    def cGetExp(self):
        sql = '''
                   select experience from c_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 11:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # java薪资与学历的关系
    def cGetEduForSalary(self):
        sql_0 = '''
                select distinct education from c_data
        '''
        sql_1 = '''
                select AVG(min_salary) from c_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from c_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from c_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # java经验与薪资
    def cGetExpForSalary(self):
        sql_0 = '''
                        select experience from c_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from c_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from c_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from c_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 11:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def cGetSkill(self):
        sql = '''
                select skill from c_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def cRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        cSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        cMin = float(self.cGetMinSalary())
        cMax = float(self.cGetMaxSalary())
        cAvg = float(self.cGetAvgSalary())
        cNum = float(self.cGetNum())
        # 添加最低薪资分数
        cSocre.append(cMin / Min)
        # 添加最高薪资分数
        cSocre.append(cMax / Max)
        # 添加平均薪资分数
        cSocre.append(cAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from c_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from c_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            cSocre.append(1 - (Exp / cNum))
            # 添加学历分数
            cSocre.append(Edu / cNum)
            # 添加数量分
            cSocre.append((cNum / Num) * 100)
            return json.dumps({'name': 'c', 'value': cSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================c23============================================='''

    def c23GetNum(self):
        sql = '''
                select count(*) as total from c23_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得c23岗位的总体平均薪资
    def c23GetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from c23_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def c23GetMaxSalary(self):
        sql = '''
                select max_salary from c23_data
                where max_salary = (select MAX(max_salary) from c23_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def c23GetMinSalary(self):
        sql = '''
                select min_salary from c23_data
                where min_salary = (select MIN(min_salary) from c23_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def c23GetEdu(self):
        sql = '''
                       select education from c23_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询java经验要求
    def c23GetExp(self):
        sql = '''
                   select experience from c23_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # java薪资与学历的关系
    def c23GetEduForSalary(self):
        sql_0 = '''
                select distinct education from c23_data
        '''
        sql_1 = '''
                select AVG(min_salary) from c23_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from c23_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from c23_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # java经验与薪资
    def c23GetExpForSalary(self):
        sql_0 = '''
                        select experience from c23_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from c23_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from c23_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from c23_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def c23GetSkill(self):
        sql = '''
                select skill from c23_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def c23Radar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        c23Socre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        c23Min = float(self.c23GetMinSalary())
        c23Max = float(self.c23GetMaxSalary())
        c23Avg = float(self.c23GetAvgSalary())
        c23Num = float(self.c23GetNum())
        # 添加最低薪资分数
        c23Socre.append(c23Min / Min)
        # 添加最高薪资分数
        c23Socre.append(c23Max / Max)
        # 添加平均薪资分数
        c23Socre.append(c23Avg / Avg)

        sql_1 = '''
                    select COUNT(num) from c23_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from c23_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            c23Socre.append(1 - (Exp / c23Num))
            # 添加学历分数
            c23Socre.append(Edu / c23Num)
            # 添加数量分
            c23Socre.append((c23Num / Num) * 100)
            return json.dumps({'name': 'c23', 'value': c23Socre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================u3dUe============================================='''

    def u3dUeGetNum(self):
        sql = '''
                select count(*) as total from u3dUe_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得u3dUe岗位的总体平均薪资
    def u3dUeGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from u3dUe_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def u3dUeGetMaxSalary(self):
        sql = '''
                select max_salary from u3dUe_data
                where max_salary = (select MAX(max_salary) from u3dUe_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def u3dUeGetMinSalary(self):
        sql = '''
                select min_salary from u3dUe_data
                where min_salary = (select MIN(min_salary) from u3dUe_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def u3dUeGetEdu(self):
        sql = '''
                       select education from u3dUe_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询java经验要求
    def u3dUeGetExp(self):
        sql = '''
                   select experience from u3dUe_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # java薪资与学历的关系
    def u3dUeGetEduForSalary(self):
        sql_0 = '''
                select distinct education from u3dUe_data
        '''
        sql_1 = '''
                select AVG(min_salary) from u3dUe_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from u3dUe_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from u3dUe_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # java经验与薪资
    def u3dUeGetExpForSalary(self):
        sql_0 = '''
                        select experience from u3dUe_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from u3dUe_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from u3dUe_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from u3dUe_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def u3dUeGetSkill(self):
        sql = '''
                select skill from u3dUe_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def u3dUeRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        u3dUeSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        u3dUeMin = float(self.u3dUeGetMinSalary())
        u3dUeMax = float(self.u3dUeGetMaxSalary())
        u3dUeAvg = float(self.u3dUeGetAvgSalary())
        u3dUeNum = float(self.u3dUeGetNum())
        # 添加最低薪资分数
        u3dUeSocre.append(u3dUeMin / Min)
        # 添加最高薪资分数
        u3dUeSocre.append(u3dUeMax / Max)
        # 添加平均薪资分数
        u3dUeSocre.append(u3dUeAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from u3dUe_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from u3dUe_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            u3dUeSocre.append(1 - (Exp / u3dUeNum))
            # 添加学历分数
            u3dUeSocre.append(Edu / u3dUeNum)
            # 添加数量分
            u3dUeSocre.append((u3dUeNum / Num) * 100)
            return json.dumps({'name': 'u3dUe', 'value': u3dUeSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================php============================================='''

    def phpGetNum(self):
        sql = '''
                select count(*) as total from php_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得php岗位的总体平均薪资
    def phpGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from php_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def phpGetMaxSalary(self):
        sql = '''
                select max_salary from php_data
                where max_salary = (select MAX(max_salary) from php_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def phpGetMinSalary(self):
        sql = '''
                select min_salary from php_data
                where min_salary = (select MIN(min_salary) from php_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def phpGetEdu(self):
        sql = '''
                       select education from php_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def phpGetExp(self):
        sql = '''
                   select experience from php_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def phpGetEduForSalary(self):
        sql_0 = '''
                select distinct education from php_data
        '''
        sql_1 = '''
                select AVG(min_salary) from php_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from php_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from php_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def phpGetExpForSalary(self):
        sql_0 = '''
                        select experience from php_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from php_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from php_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from php_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def phpGetSkill(self):
        sql = '''
                select skill from php_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def phpRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        phpSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        phpMin = float(self.phpGetMinSalary())
        phpMax = float(self.phpGetMaxSalary())
        phpAvg = float(self.phpGetAvgSalary())
        phpNum = float(self.phpGetNum())
        # 添加最低薪资分数
        phpSocre.append(phpMin / Min)
        # 添加最高薪资分数
        phpSocre.append(phpMax / Max)
        # 添加平均薪资分数
        phpSocre.append(phpAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from php_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from php_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            phpSocre.append(1 - (Exp / phpNum))
            # 添加学历分数
            phpSocre.append(Edu / phpNum)
            # 添加数量分
            phpSocre.append((phpNum / Num) * 100)
            return json.dumps({'name': 'php', 'value': phpSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================web============================================='''

    def webGetNum(self):
        sql = '''
                select count(*) as total from web_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得web岗位的总体平均薪资
    def webGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from web_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def webGetMaxSalary(self):
        sql = '''
                select max_salary from web_data
                where max_salary = (select MAX(max_salary) from web_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def webGetMinSalary(self):
        sql = '''
                select min_salary from web_data
                where min_salary = (select MIN(min_salary) from web_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def webGetEdu(self):
        sql = '''
                       select education from web_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def webGetExp(self):
        sql = '''
                   select experience from web_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def webGetEduForSalary(self):
        sql_0 = '''
                select distinct education from web_data
        '''
        sql_1 = '''
                select AVG(min_salary) from web_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from web_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from web_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def webGetExpForSalary(self):
        sql_0 = '''
                        select experience from web_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from web_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from web_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from web_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def webGetSkill(self):
        sql = '''
                select skill from web_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def webRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        webSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        webMin = float(self.webGetMinSalary())
        webMax = float(self.webGetMaxSalary())
        webAvg = float(self.webGetAvgSalary())
        webNum = float(self.webGetNum())
        # 添加最低薪资分数
        webSocre.append(webMin / Min)
        # 添加最高薪资分数
        webSocre.append(webMax / Max)
        # 添加平均薪资分数
        webSocre.append(webAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from web_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from web_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            webSocre.append(1 - (Exp / webNum))
            # 添加学历分数
            webSocre.append(Edu / webNum)
            # 添加数量分
            webSocre.append((webNum / Num) * 100)
            return json.dumps({'name': 'web', 'value': webSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================Android============================================='''

    def AndroidGetNum(self):
        sql = '''
                select count(*) as total from Android_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得Android岗位的总体平均薪资
    def AndroidGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from Android_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def AndroidGetMaxSalary(self):
        sql = '''
                select max_salary from Android_data
                where max_salary = (select MAX(max_salary) from Android_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def AndroidGetMinSalary(self):
        sql = '''
                select min_salary from Android_data
                where min_salary = (select MIN(min_salary) from Android_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def AndroidGetEdu(self):
        sql = '''
                       select education from Android_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def AndroidGetExp(self):
        sql = '''
                   select experience from Android_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def AndroidGetEduForSalary(self):
        sql_0 = '''
                select distinct education from Android_data
        '''
        sql_1 = '''
                select AVG(min_salary) from Android_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from Android_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from Android_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def AndroidGetExpForSalary(self):
        sql_0 = '''
                        select experience from Android_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from Android_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from Android_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from Android_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def AndroidGetSkill(self):
        sql = '''
                select skill from Android_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def AndroidRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        AndroidSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        AndroidMin = float(self.AndroidGetMinSalary())
        AndroidMax = float(self.AndroidGetMaxSalary())
        AndroidAvg = float(self.AndroidGetAvgSalary())
        AndroidNum = float(self.AndroidGetNum())
        # 添加最低薪资分数
        AndroidSocre.append(AndroidMin / Min)
        # 添加最高薪资分数
        AndroidSocre.append(AndroidMax / Max)
        # 添加平均薪资分数
        AndroidSocre.append(AndroidAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from Android_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from Android_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            AndroidSocre.append(1 - (Exp / AndroidNum))
            # 添加学历分数
            AndroidSocre.append(Edu / AndroidNum)
            # 添加数量分
            AndroidSocre.append((AndroidNum / Num) * 100)
            return json.dumps({'name': 'Android', 'value': AndroidSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================ios============================================='''

    def iosGetNum(self):
        sql = '''
                select count(*) as total from ios_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得ios岗位的总体平均薪资
    def iosGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from ios_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def iosGetMaxSalary(self):
        sql = '''
                select max_salary from ios_data
                where max_salary = (select MAX(max_salary) from ios_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def iosGetMinSalary(self):
        sql = '''
                select min_salary from ios_data
                where min_salary = (select MIN(min_salary) from ios_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def iosGetEdu(self):
        sql = '''
                       select education from ios_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def iosGetExp(self):
        sql = '''
                   select experience from ios_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def iosGetEduForSalary(self):
        sql_0 = '''
                select distinct education from ios_data
        '''
        sql_1 = '''
                select AVG(min_salary) from ios_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from ios_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from ios_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def iosGetExpForSalary(self):
        sql_0 = '''
                        select experience from ios_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from ios_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from ios_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from ios_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def iosGetSkill(self):
        sql = '''
                select skill from ios_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def iosRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        iosSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        iosMin = float(self.iosGetMinSalary())
        iosMax = float(self.iosGetMaxSalary())
        iosAvg = float(self.iosGetAvgSalary())
        iosNum = float(self.iosGetNum())
        # 添加最低薪资分数
        iosSocre.append(iosMin / Min)
        # 添加最高薪资分数
        iosSocre.append(iosMax / Max)
        # 添加平均薪资分数
        iosSocre.append(iosAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from ios_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from ios_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            iosSocre.append(1 - (Exp / iosNum))
            # 添加学历分数
            iosSocre.append(Edu / iosNum)
            # 添加数量分
            iosSocre.append((iosNum / Num) * 100)
            return json.dumps({'name': 'ios', 'value': iosSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================algorithm============================================='''

    def algorithmGetNum(self):
        sql = '''
                select count(*) as total from algorithm_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得algorithm岗位的总体平均薪资
    def algorithmGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from algorithm_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def algorithmGetMaxSalary(self):
        sql = '''
                select max_salary from algorithm_data
                where max_salary = (select MAX(max_salary) from algorithm_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def algorithmGetMinSalary(self):
        sql = '''
                select min_salary from algorithm_data
                where min_salary = (select MIN(min_salary) from algorithm_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def algorithmGetEdu(self):
        sql = '''
                       select education from algorithm_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def algorithmGetExp(self):
        sql = '''
                   select experience from algorithm_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def algorithmGetEduForSalary(self):
        sql_0 = '''
                select distinct education from algorithm_data
        '''
        sql_1 = '''
                select AVG(min_salary) from algorithm_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from algorithm_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from algorithm_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def algorithmGetExpForSalary(self):
        sql_0 = '''
                        select experience from algorithm_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from algorithm_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from algorithm_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from algorithm_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def algorithmGetSkill(self):
        sql = '''
                select skill from algorithm_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def algorithmRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        algorithmSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        algorithmMin = float(self.algorithmGetMinSalary())
        algorithmMax = float(self.algorithmGetMaxSalary())
        algorithmAvg = float(self.algorithmGetAvgSalary())
        algorithmNum = float(self.algorithmGetNum())
        # 添加最低薪资分数
        algorithmSocre.append(algorithmMin / Min)
        # 添加最高薪资分数
        algorithmSocre.append(algorithmMax / Max)
        # 添加平均薪资分数
        algorithmSocre.append(algorithmAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from algorithm_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from algorithm_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            algorithmSocre.append(1 - (Exp / algorithmNum))
            # 添加学历分数
            algorithmSocre.append(Edu / algorithmNum)
            # 添加数量分
            algorithmSocre.append((algorithmNum / Num) * 100)
            return json.dumps({'name': 'algorithm', 'value': algorithmSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================test============================================='''

    def testGetNum(self):
        sql = '''
                select count(*) as total from test_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得test岗位的总体平均薪资
    def testGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from test_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def testGetMaxSalary(self):
        sql = '''
                select max_salary from test_data
                where max_salary = (select MAX(max_salary) from test_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def testGetMinSalary(self):
        sql = '''
                select min_salary from test_data
                where min_salary = (select MIN(min_salary) from test_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def testGetEdu(self):
        sql = '''
                       select education from test_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def testGetExp(self):
        sql = '''
                   select experience from test_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 50:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def testGetEduForSalary(self):
        sql_0 = '''
                select distinct education from test_data
        '''
        sql_1 = '''
                select AVG(min_salary) from test_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from test_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from test_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def testGetExpForSalary(self):
        sql_0 = '''
                        select experience from test_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from test_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from test_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from test_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 50:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def testGetSkill(self):
        sql = '''
                select skill from test_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def testRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        testSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        testMin = float(self.testGetMinSalary())
        testMax = float(self.testGetMaxSalary())
        testAvg = float(self.testGetAvgSalary())
        testNum = float(self.testGetNum())
        # 添加最低薪资分数
        testSocre.append(testMin / Min)
        # 添加最高薪资分数
        testSocre.append(testMax / Max)
        # 添加平均薪资分数
        testSocre.append(testAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from test_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from test_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            testSocre.append(1 - (Exp / testNum))
            # 添加学历分数
            testSocre.append(Edu / testNum)
            # 添加数量分
            testSocre.append((testNum / Num) * 100)
            return json.dumps({'name': 'test', 'value': testSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================oam============================================='''

    def oamGetNum(self):
        sql = '''
                select count(*) as total from oam_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            last_num = result['total']
            return last_num
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得oam岗位的总体平均薪资
    def oamGetAvgSalary(self):
        sql = '''
                   select ROUND(AVG(avg_salary), 2) as avg_salary from oam_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            return format(result['avg_salary'] or 0, '.2f')
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最高薪资
    def oamGetMaxSalary(self):
        sql = '''
                select max_salary from oam_data
                where max_salary = (select MAX(max_salary) from oam_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Max = result['max_salary']
            return Max
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询最低薪资
    def oamGetMinSalary(self):
        sql = '''
                select min_salary from oam_data
                where min_salary = (select MIN(min_salary) from oam_data)
            '''

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchone()
            Min = result['min_salary']
            return Min
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 取得java学历情况
    def oamGetEdu(self):
        sql = '''
                       select education from oam_data
               '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            education_list = []
            for var in result:
                education_list.append(var['education'])
            edu = dict(Counter(education_list))
            edu_name = []
            edu_value = []

            for var in edu:
                edu_name.append(var)
                edu_value.append(edu[var])

            return json.dumps({'name': edu_name, 'value': edu_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 查询经验要求
    def oamGetExp(self):
        sql = '''
                   select experience from oam_data
           '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 10:
                    del exp[key]
                    continue
            exp_name = []
            exp_value = []
            for var in exp:
                exp_name.append(var)
                exp_value.append(exp[var])

            return json.dumps({'name': exp_name, 'value': exp_value}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    # 薪资与学历的关系
    def oamGetEduForSalary(self):
        sql_0 = '''
                select distinct education from oam_data
        '''
        sql_1 = '''
                select AVG(min_salary) from oam_data
                where education = %s
        '''
        sql_2 = '''
                select AVG(max_salary) from oam_data
                where education = %s
        '''
        sql_3 = '''
                select AVG(avg_salary) from oam_data
                where education = %s
        '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            edu = self.cursor.fetchall()
            edu_list = []
            for var in edu:
                edu_list.append(var['education'])

            # 最小值处理
            min_salary = []
            for var in edu_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in edu_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in edu_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(edu)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': edu_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 经验与薪资
    def oamGetExpForSalary(self):
        sql_0 = '''
                        select experience from oam_data
                '''
        sql_1 = '''
                        select AVG(min_salary) from oam_data
                        where experience = %s
                '''
        sql_2 = '''
                        select AVG(max_salary) from oam_data
                        where experience = %s
                '''
        sql_3 = '''
                        select AVG(avg_salary) from oam_data
                        where experience = %s
                '''
        try:
            self.cursor.execute(sql_0)
            self.connect.commit()
            result = self.cursor.fetchall()
            experience_list = []
            for var in result:
                experience_list.append(var['experience'])
            exp = dict(Counter(experience_list))
            for key in list(exp.keys()):
                if exp[key] < 50:
                    del exp[key]
                    continue
            exp_list = list(exp)

            # 最小值处理
            min_salary = []
            for var in exp_list:
                self.cursor.execute(sql_1, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                min_salary.append(data)

            min_list = []
            for i in min_salary:
                for j in i:
                    min_list.append(round(float(j['AVG(min_salary)']), 2))

            # 最大值
            max_salary = []
            for var in exp_list:
                self.cursor.execute(sql_2, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                max_salary.append(data)

            max_list = []
            for i in max_salary:
                for j in i:
                    max_list.append(round(float(j['AVG(max_salary)']), 2))

            # 平均值
            avg_salary = []
            for var in exp_list:
                self.cursor.execute(sql_3, var)
                self.connect.commit()
                data = self.cursor.fetchall()
                avg_salary.append(data)

            avg_list = []
            for i in avg_salary:
                for j in i:
                    avg_list.append(round(float(j['AVG(avg_salary)']), 2))

            # 整合
            salary_list = []
            for i in range(len(exp_list)):
                data = [min_list[i], avg_list[i], max_list[i]]
                salary_list.append(data)

            return json.dumps({'name': exp_list, 'value': salary_list}, ensure_ascii=False)

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 ：{}".format(e))

    # 查询技术要求
    def oamGetSkill(self):
        sql = '''
                select skill from oam_data
        '''
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            skill = []
            for var in result:
                skill.append(var['skill'])
            return skill

        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}".format(sql, e))

    def oamRadar(self):
        # 分数： 最低薪资分（10分） 最高薪资分  平均薪资分  经验分  学历分  数量分
        oamSocre = []
        Min = float(self.getMinSalary())
        Max = float(self.getMaxSalary())
        Avg = float(self.getAllAvgSalary())
        Num = float(self.getLastNum())
        oamMin = float(self.oamGetMinSalary())
        oamMax = float(self.oamGetMaxSalary())
        oamAvg = float(self.oamGetAvgSalary())
        oamNum = float(self.oamGetNum())
        # 添加最低薪资分数
        oamSocre.append(oamMin / Min)
        # 添加最高薪资分数
        oamSocre.append(oamMax / Max)
        # 添加平均薪资分数
        oamSocre.append(oamAvg / Avg)

        sql_1 = '''
                    select COUNT(num) from oam_data
                    where experience = '1-3年' or  experience ='经验不限' or  experience ='在校/应届'
            '''
        sql_2 = '''
                    select COUNT(num) from oam_data
                    where education = '博士' or  education = '硕士' or education = '本科'
            '''
        try:
            self.cursor.execute(sql_1)
            self.connect.commit()
            result = self.cursor.fetchone()
            Exp = result['COUNT(num)']
            self.cursor.execute(sql_2)
            self.connect.commit()
            result = self.cursor.fetchone()
            Edu = result['COUNT(num)']
            # 添加经验分数
            oamSocre.append(1 - (Exp / oamNum))
            # 添加学历分数
            oamSocre.append(Edu / oamNum)
            # 添加数量分
            oamSocre.append((oamNum / Num) * 100)
            return json.dumps({'name': 'oam', 'value': oamSocre}, ensure_ascii=False)
        except Exception as e:
            self.connect.rollback()
            print(">>>读取数据失败 执行MySQL: {} 时出错：{}", e)

    '''============================================热力图数据======================================================='''
    
    # 获取地区薪资数据（省级）
    def getProvinceSalaryData(self, job_table='', education='', experience='', scale=''):
        """
        获取各省平均薪资数据，用于热力图
        
        :param job_table: 岗位表名，为空时查询所有岗位
        :param education: 学历筛选条件
        :param experience: 经验筛选条件
        :param scale: 公司规模筛选条件
        :return: 省份薪资数据列表，格式为[{"name":"北京","value":15000}, ...]
        """
        # 构建表名
        if not job_table:
            table_name = 'c_data' # 修改为c_data表
        else:
            table_name = job_table + '_data'
        
        # 构建查询条件
        conditions = []
        params = []
        
        if education:
            conditions.append("education = %s")
            params.append(education)
        
        if experience:
            conditions.append("experience = %s")
            params.append(experience)
            
        if scale:
            conditions.append("scale = %s")
            params.append(scale)
            
        where_clause = " AND ".join(conditions) if conditions else ""
        
        # 构建查询SQL - 使用province字段
        try:
            # 首先检查是否存在province字段
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'province'")
            has_province_column = len(self.cursor.fetchall()) > 0
            
            if has_province_column:
                print(f"DEBUG: 使用province字段进行省级查询")
                sql = f'''
                    SELECT 
                        province as province, 
                        AVG(avg_salary) as avg_salary,
                        COUNT(*) as job_count
                    FROM {table_name}
                '''
            else:
                print(f"DEBUG: 未找到province字段，从city字段解析省份")
                sql = f'''
                    SELECT 
                        SUBSTRING_INDEX(city, '-', 1) as province, 
                        AVG(avg_salary) as avg_salary,
                        COUNT(*) as job_count
                    FROM {table_name}
                '''
            
            if where_clause:
                sql += f" WHERE {where_clause}"
                
            sql += " GROUP BY province"
            
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            # 薪资数据
            salary_data = []
            # 岗位数量数据
            job_count_data = []
            
            for row in results:
                province = row['province']
                avg_salary = int(row['avg_salary'])
                job_count = row['job_count']
                
                if province:  # 确保省份名不为空
                    salary_data.append({"name": province, "value": avg_salary})
                    job_count_data.append({"name": province, "value": job_count})
            
            return {"salary": salary_data, "job_count": job_count_data}
            
        except Exception as e:
            self.connect.rollback()
            print(f">>>获取省级薪资数据失败: {e}")
            return {"salary": [], "job_count": []}
    
    # 获取地区薪资数据（城市级）
    def getCitySalaryData(self, province='', job_table='', education='', experience='', scale=''):
        """
        获取特定省份内各城市平均薪资数据，用于热力图
        
        :param province: 省份名称
        :param job_table: 岗位表名，为空时查询所有岗位
        :param education: 学历筛选条件
        :param experience: 经验筛选条件
        :param scale: 公司规模筛选条件
        :return: 城市薪资数据列表，格式为[{"name":"深圳","value":16000}, ...]
        """
        # 构建表名
        if not job_table:
            table_name = 'c_data' # 修改为c_data表
        else:
            table_name = job_table + '_data'
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 检查表是否有province字段
        try:
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'province'")
            has_province_column = len(self.cursor.fetchall()) > 0
            
            if has_province_column and province:
                # 使用province字段查询
                conditions.append("province = %s OR province LIKE %s")
                params.append(province)
                params.append(f"{province}%")  # 模糊匹配，如"浙江省"
                print(f"DEBUG: 使用province字段查询城市数据，province={province}")
            elif province:
                # 直接使用城市名称进行匹配
                conditions.append("city LIKE %s")
                params.append(f"{province}%")
                print(f"DEBUG: 使用city字段模糊匹配province={province}")
        
        except Exception as e:
            print(f">>>检查province字段失败: {e}")
            # 如果出错，使用传统方法
            if province:
                conditions.append("city LIKE %s")
                params.append(f"{province}%")
        
        if education:
            conditions.append("education = %s")
            params.append(education)
        
        if experience:
            conditions.append("experience = %s")
            params.append(experience)
            
        if scale:
            conditions.append("scale = %s")
            params.append(scale)
            
        where_clause = " AND ".join(conditions) if conditions else ""
        
        # 构建查询SQL
        sql = f'''
            SELECT 
                city,
                AVG(avg_salary) as avg_salary,
                COUNT(*) as job_count
            FROM {table_name}
        '''
        
        if where_clause:
            sql += f" WHERE {where_clause}"
            
        sql += " GROUP BY city"
        
        try:
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            print(f"DEBUG: 查询返回城市数据条数: {len(results)}")
            
            # 薪资数据
            salary_data = []
            # 岗位数量数据
            job_count_data = []
            
            for row in results:
                city = row['city'].split('-')[-1] if '-' in row['city'] else row['city']
                avg_salary = int(row['avg_salary'])
                job_count = row['job_count']
                
                if city:  # 确保城市名不为空
                    salary_data.append({"name": city, "value": avg_salary})
                    job_count_data.append({"name": city, "value": job_count})
            
            return {"salary": salary_data, "job_count": job_count_data}
            
        except Exception as e:
            self.connect.rollback()
            print(f">>>获取城市薪资数据失败: {e}")
            return {"salary": [], "job_count": []}
    
    # 获取地区热力图前10排名数据
    def getSalaryRankTop10(self, province='', job_table='', education='', experience='', scale='', metric='salary'):
        """
        获取薪资或岗位数排名前10的地区
        
        :param province: 省份名称，用于筛选省内城市
        :param job_table: 岗位表名，为空时查询所有岗位
        :param education: 学历筛选条件
        :param experience: 经验筛选条件
        :param scale: 公司规模筛选条件
        :param metric: 排序指标，'salary'表示薪资，'job_count'表示岗位数量
        :return: 排名前10的地区数据
        """
        # 构建表名
        if not job_table:
            table_name = 'c_data' # 修改为c_data表
        else:
            table_name = job_table + '_data'
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 检查表是否有province字段
        try:
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'province'")
            has_province_column = len(self.cursor.fetchall()) > 0
            
            # 如果有省份参数，则查询该省份下的城市
            if province and has_province_column:
                conditions.append("province = %s OR province LIKE %s")
                params.append(province)
                params.append(f"{province}%")
                group_by = "city"
                name_field = "city" # 获取城市名
                print(f"DEBUG: 使用province字段查询排名数据，province={province}")
            elif province:
                # 直接使用城市名称进行匹配
                conditions.append("city LIKE %s")
                params.append(f"{province}%")
                group_by = "city"
                name_field = "city" # 获取城市名
                print(f"DEBUG: 使用city字段模糊匹配查询排名, province={province}")
            else:
                # 否则查询所有省份
                if has_province_column:
                    group_by = "province"
                    name_field = "province" # 使用province字段
                    print(f"DEBUG: 使用province字段查询全国排名")
                else:
                    group_by = "SUBSTRING_INDEX(city, '-', 1)"
                    name_field = "SUBSTRING_INDEX(city, '-', 1)" # 解析省份名
                    print(f"DEBUG: 从city字段提取省份信息查询全国排名")
        except Exception as e:
            print(f">>>检查province字段失败: {e}")
            # 如果出错，使用传统方法
            # 如果有省份参数，则查询该省份下的城市
            # 否则查询所有省份
            if province:
                conditions.append("city LIKE %s")
                params.append(f"{province}%")
                group_by = "city"
                name_field = "city" # 获取城市名
            else:
                group_by = "SUBSTRING_INDEX(city, '-', 1)"
                name_field = "SUBSTRING_INDEX(city, '-', 1)" # 获取省份名
        
        if education:
            conditions.append("education = %s")
            params.append(education)
        
        if experience:
            conditions.append("experience = %s")
            params.append(experience)
            
        if scale:
            conditions.append("scale = %s")
            params.append(scale)
            
        where_clause = " AND ".join(conditions) if conditions else ""
        
        # 构建查询SQL
        sql = f'''
            SELECT 
                {name_field} as region_name,
                AVG(avg_salary) as avg_salary,
                COUNT(*) as job_count
            FROM {table_name}
        '''
        
        if where_clause:
            sql += f" WHERE {where_clause}"
            
        sql += f" GROUP BY {group_by}"
        
        # 根据metric参数决定排序方式
        if metric == 'salary':
            sql += " ORDER BY avg_salary DESC"
        else:
            sql += " ORDER BY job_count DESC"
            
        sql += " LIMIT 10"
        
        try:
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            print(f"DEBUG: 查询返回排名数据条数: {len(results)}")
            rank_data = []
            
            for i, row in enumerate(results):
                region_name = row['region_name']
                # 处理从city中提取的城市名称
                if '-' in region_name:
                    region_name = region_name.split('-')[-1]
                
                avg_salary = int(row['avg_salary'])
                job_count = row['job_count']
                
                if region_name:  # 确保地区名不为空
                    rank_data.append({
                        "rank": i + 1,
                        "name": region_name,
                        "salary": avg_salary,
                        "job_count": job_count
                    })
            
            return rank_data
            
        except Exception as e:
            self.connect.rollback()
            print(f">>>获取排名数据失败: {e}")
            return []
            
    # 新增方法：获取省份详细信息（包括城市数据）
    def getProvinceDetail(self, province_name='', job_table='', education='', experience='', scale=''):
        """
        获取省份详细数据，包括省份汇总和城市明细
        
        :param province_name: 省份名称
        :param job_table: 岗位表名，为空时查询所有岗位
        :param education: 学历筛选条件
        :param experience: 经验筛选条件
        :param scale: 公司规模筛选条件
        :return: 省份详细数据，包括省级汇总和城市明细
        """
        # 构建表名
        if not job_table:
            table_name = 'c_data'
        else:
            table_name = job_table + '_data'
        
        # 标准化省份名称，去掉可能的"省"、"市"、"自治区"后缀
        if province_name:
            province_name = province_name.replace('省', '').replace('市', '').replace('自治区', '')
            print(f"DEBUG: 获取省份详情 - {province_name}")
        else:
            print("ERROR: 未指定省份名称")
            return None
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 添加省份条件
        try:
            # 检查表是否有province字段
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'province'")
            has_province_column = len(self.cursor.fetchall()) > 0
            
            if has_province_column:
                # 优先使用province字段
                conditions.append("province = %s OR province LIKE %s")
                params.append(province_name)
                params.append(f"{province_name}%")  # 处理如"浙江省"的情况
                print(f"DEBUG: 使用province字段查询省份 {province_name} 详情")
            else:
                # 尝试从city字段解析省份
                conditions.append("city LIKE %s")
                params.append(f"{province_name}%")
                print(f"DEBUG: 使用city字段模糊匹配省份 {province_name}")
        except Exception as e:
            print(f">>>检查province字段失败: {e}")
            # 如果出错，使用city字段
            conditions.append("city LIKE %s")
            params.append(f"{province_name}%")
        
        if education:
            conditions.append("education = %s")
            params.append(education)
        
        if experience:
            conditions.append("experience = %s")
            params.append(experience)
        
        if scale:
            conditions.append("scale = %s")
            params.append(scale)
            
        where_clause = " AND ".join(conditions) if conditions else ""
        
        try:
            # 1. 获取省级汇总数据
            province_sql = f'''
                SELECT 
                    AVG(avg_salary) as average,
                    MAX(avg_salary) as max_salary,
                    MIN(avg_salary) as min_salary,
                    COUNT(*) as count
                FROM {table_name}
                WHERE {where_clause}
            '''
            
            self.cursor.execute(province_sql, params)
            province_result = self.cursor.fetchone()
            
            if not province_result or province_result['count'] == 0:
                print(f"未找到省份 {province_name} 的数据")
                return None
                
            province_data = {
                "province": province_name,
                "average": int(province_result['average']),
                "max": int(province_result['max_salary']),
                "min": int(province_result['min_salary']),
                "count": province_result['count'],
                "cities": []
            }
            
            # 2. 获取城市详细数据
            city_sql = f'''
                SELECT 
                    city as region,
                    AVG(avg_salary) as value,
                    COUNT(*) as count,
                    MAX(avg_salary) as max_salary,
                    MIN(avg_salary) as min_salary
                FROM {table_name}
                WHERE {where_clause}
                GROUP BY city
            '''
            
            self.cursor.execute(city_sql, params)
            city_results = self.cursor.fetchall()
            
            for city in city_results:
                # 处理城市名称，确保名称合适
                city_name = city['region']
                if '-' in city_name:
                    city_name = city_name.split('-')[-1]
                
                # 确保城市名有"市"后缀
                if not city_name.endswith('市') and not city_name.endswith('区') and not city_name.endswith('县'):
                    city_name = city_name + "市"
                
                province_data["cities"].append({
                    "region": city_name,
                    "province": province_name,
                    "value": int(city['value']),
                    "count": city['count'],
                    "max": int(city['max_salary']),
                    "min": int(city['min_salary'])
                })
            
            print(f"DEBUG: 找到 {len(province_data['cities'])} 个城市数据")
            return province_data
            
        except Exception as e:
            self.connect.rollback()
            print(f">>>获取省份详情数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # 新增方法：获取城市区县数据
    def getCityDistrictData(self, province_name='', city_name='', job_table='', education='', experience='', scale=''):
        """
        获取指定城市的区县级工资数据
        
        :param province_name: 省份名称
        :param city_name: 城市名称
        :param job_table: 岗位表名，为空时查询c_data表
        :param education: 学历筛选条件
        :param experience: 经验筛选条件
        :param scale: 公司规模筛选条件
        :return: 城市区县详细数据
        """
        # 使用c_data表作为数据源
        table_name = 'c_data'
        
        # 标准化省份和城市名称
        if province_name:
            province_name = province_name.replace('省', '').replace('自治区', '')
        
        if city_name:
            city_name = city_name.replace('市', '')
            print(f"DEBUG: 获取城市 {city_name} 的区县数据")
        else:
            print("ERROR: 未指定城市名称")
            return None
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 检查表是否有area字段用于区县划分
        try:
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'area'")
            has_area_column = len(self.cursor.fetchall()) > 0
            
            if not has_area_column:
                print("WARNING: 数据表中不存在area字段，无法查询区县数据")
                return None
                
            # 添加省份条件
            if province_name:
                self.cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'province'")
                has_province_column = len(self.cursor.fetchall()) > 0
                
                if has_province_column:
                    conditions.append("province = %s OR province LIKE %s")
                    params.append(province_name)
                    params.append(f"{province_name}%")
            
            # 添加城市条件
            conditions.append("city = %s OR city LIKE %s")
            params.append(city_name)
            params.append(f"{city_name}%")
            
            if education:
                conditions.append("education = %s")
                params.append(education)
            
            if experience:
                conditions.append("experience = %s")
                params.append(experience)
            
            if scale:
                conditions.append("scale = %s")
                params.append(scale)
                
            where_clause = " AND ".join(conditions) if conditions else ""
            
            # 获取城市汇总数据
            city_sql = f'''
                SELECT 
                    province,
                    city,
                    AVG(avg_salary) as average,
                    MAX(avg_salary) as max_salary,
                    MIN(avg_salary) as min_salary,
                    COUNT(*) as count
                FROM {table_name}
                WHERE {where_clause}
                GROUP BY province, city
            '''
            
            self.cursor.execute(city_sql, params)
            city_result = self.cursor.fetchone()
            
            if not city_result:
                print(f"未找到城市 {city_name} 的数据")
                return None
                
            # 确保城市名称正确
            db_city_name = city_result['city']
            if '-' in db_city_name:
                db_city_name = db_city_name.split('-')[-1]
            
            if not db_city_name.endswith('市'):
                db_city_name += '市'
                
            # 获取省份名称
            db_province = city_result['province'] if 'province' in city_result else province_name
            if db_province and not db_province.endswith('省') and db_province not in ['北京', '上海', '天津', '重庆']:
                db_province += '省'
                
            # 构建结果数据，按照要求的返回结构
            city_data = {
                "level": "district",
                "province": db_province,
                "city": db_city_name,
                "average": int(city_result['average']),
                "max": int(city_result['max_salary']),
                "min": int(city_result['min_salary']),
                "count": city_result['count'],
                "regions": []  # 只保留符合要求的格式
            }
            
            # 获取区县数据
            district_sql = f'''
                SELECT 
                    area as district,
                    AVG(avg_salary) as value,
                    COUNT(*) as count,
                    MAX(avg_salary) as max_value,
                    MIN(avg_salary) as min_value
                FROM {table_name}
                WHERE {where_clause} AND area != '其他' AND area != '其他区'
                GROUP BY area
                HAVING district IS NOT NULL AND district != ''
            '''
            
            self.cursor.execute(district_sql, params)
            district_results = self.cursor.fetchall()
            
            for district in district_results:
                if district['district']:  # 确保区名不为空
                    district_name = district['district']
                    if not district_name.endswith('区') and not district_name.endswith('县'):
                        district_name += '区'
                    
                    # 只保留新格式数据，不再兼容旧格式
                    city_data["regions"].append({
                        "name": district_name,
                        "value": int(district['value']), 
                        "count": district['count'],
                        "max": int(district['max_value']),
                        "min": int(district['min_value'])
                    })
            
            print(f"DEBUG: 找到 {len(city_data['regions'])} 个区县数据")
            return city_data
            
        except Exception as e:
            self.connect.rollback()
            print(f">>>获取城市区县数据失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    # 从文本中提取技能关键词
    def extract_skills_from_text(self, text):
        """从文本中提取技能关键词"""
        # 常见技能关键词列表（可以扩展）
        common_skills = [
            'Java', 'Spring', 'MySQL', 'Redis', 'Python', 'Django', 'Flask', 'pandas',
            'JavaScript', 'HTML', 'CSS', 'Vue', 'React', 'Angular', 'Node.js',
            'C++', 'C#', '.NET', 'PHP', 'Laravel', 'Golang', 'Rust', 'Swift',
            'Docker', 'Kubernetes', 'Linux', 'Git', 'CI/CD', 'AWS', 'Azure',
            'SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'Oracle', 'ElasticSearch',
            'TensorFlow', 'PyTorch', 'Scikit-learn', '机器学习', '深度学习', '人工智能',
            'Android', 'iOS', 'Flutter', 'React Native', 'Hadoop', 'Spark', 'Flink',
            '微服务', 'RESTful', 'GraphQL', 'gRPC', 'WebSocket', '分布式系统'
        ]
        
        # 从文本中提取技能
        found_skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        
        # 如果没有找到任何技能，则返回一些基本技能
        if not found_skills:
            if 'Java' in text:
                found_skills = ['Java', 'Spring', 'MySQL']
            elif 'Python' in text:
                found_skills = ['Python', 'Django', 'MySQL']
            elif '前端' in text or 'web' in text.lower():
                found_skills = ['JavaScript', 'HTML', 'CSS']
            elif '算法' in text:
                found_skills = ['算法', '机器学习', 'Python']
            else:
                found_skills = ['编程', '沟通', '团队协作']
        
        return found_skills

    # 岗位匹配函数
    def match_jobs(self, name, province, city, skills, education, experience, min_salary=0, scale='', priority='match', page=1, page_size=10):
        """
        匹配符合条件的岗位
        :param name: 岗位方向
        :param province: 省份
        :param city: 城市
        :param skills: 技能列表
        :param education: 学历
        :param experience: 工作经验
        :param min_salary: 最低薪资
        :param scale: 公司规模
        :param priority: 匹配优先级
        :param page: 页码，从1开始
        :param page_size: 每页数量
        :return: 匹配的岗位列表和总数量
        """
        try:
            # 使用类的cursor而不是新建连接
            c = self.cursor
            
            # 构建查询条件
            conditions = []
            params = []
            
            # 岗位方向匹配（严格要求匹配岗位方向）
            if name:
                # 更精确的岗位方向匹配，优先匹配完全相同的岗位名称
                if priority == 'match' or priority == 'skill':
                    conditions.append("(name LIKE %s OR (name LIKE %s AND name LIKE %s))")
                    params.extend([f'%{name}%', f'%开发%', f'%{name}%'])
                else:
                    # 对于其他优先级，允许更宽松的匹配
                    conditions.append("(name LIKE %s OR name LIKE %s OR name LIKE %s)")
                    params.extend([f'%{name}%', f'%开发%', f'%工程师%'])
            
            # 地区匹配
            if city:
                if priority == 'area':
                    # 地区优先时，严格匹配城市
                    conditions.append("city = %s")
                    params.append(city)
                else:
                    conditions.append("city LIKE %s")
                    params.append(f'%{city}%')
            elif province:
                if priority == 'area':
                    # 地区优先时，严格匹配省份
                    conditions.append("city LIKE %s")
                    params.append(f'{province}%')
                else:
                    conditions.append("city LIKE %s")
                    params.append(f'%{province}%')
            
            # 学历匹配（低于或等于用户学历）
            edu_levels = {'不限': 0, '中技': 1, '大专': 2, '本科': 3, '硕士': 4, '博士': 5}
            if education and education in edu_levels and edu_levels[education] > 0:
                edu_sql = []
                for edu, level in edu_levels.items():
                    if level <= edu_levels[education]:
                        edu_sql.append("education LIKE %s")
                        params.append(f'%{edu}%')
                if edu_sql:
                    conditions.append(f"({' OR '.join(edu_sql)})")
            
            # 薪资匹配
            if min_salary > 0:
                if priority == 'salary':
                    # 薪资优先时，按平均薪资过滤
                    conditions.append("((min_salary + max_salary) / 2) >= %s")
                    params.append(min_salary)
                else:
                    conditions.append("max_salary >= %s")
                    params.append(min_salary)
            
            # 公司规模匹配
            if scale:
                conditions.append("scale LIKE %s")
                params.append(f'%{scale}%')
            
            # 获取总记录数
            count_query = f"""
                SELECT COUNT(*) as total
                FROM c_data
                WHERE {' AND '.join(conditions)}
            """ if conditions else "SELECT COUNT(*) as total FROM c_data"
            
            c.execute(count_query, params)
            total = c.fetchone()['total']
            
            # 计算分页
            offset = (page - 1) * page_size
            
            # 构建完整查询语句
            if conditions:
                query = f"""
                    SELECT num, name, company, city, area, min_salary, max_salary, education, experience, detail, label, skill, welfare
                    FROM c_data
                    WHERE {' AND '.join(conditions)}
                    LIMIT {page_size} OFFSET {offset}
                """
            else:
                query = f"""
                    SELECT num, name, company, city, area, min_salary, max_salary, education, experience, detail, label, skill, welfare
                    FROM c_data
                    LIMIT {page_size} OFFSET {offset}
                """
            
            c.execute(query, params)
            rows = c.fetchall()
            
            # 处理查询结果
            matched_jobs = []
            for row in rows:
                job_id = row['num']
                job_name = row['name']
                company = row['company']
                city = row['city']
                area = row.get('area', '')  # 区域字段
                min_salary = row['min_salary']
                max_salary = row['max_salary']
                education = row['education']
                experience = row['experience']
                detail = row['detail']
                label = row['label']
                welfare = row.get('welfare', '')  # 福利字段
                
                # 直接使用数据库中的技能字段，而不是通过extract_skills_from_text提取
                skill_text = row.get('skill', '')
                required_skills = [s.strip() for s in skill_text.split() if s.strip()]
                
                # 如果数据库中没有技能列表或为空，则尝试从描述和要求中提取
                if not required_skills:
                    required_skills = self.extract_skills_from_text(detail + " " + label)
                
                # 计算技能匹配度
                matched_skills = []
                for user_skill in skills:
                    for req_skill in required_skills:
                        if user_skill.lower() in req_skill.lower() or req_skill.lower() in user_skill.lower():
                            matched_skills.append(user_skill)
                            break
                
                skill_match_score = len(matched_skills) / max(len(skills), 1) if skills else 0
                
                # 计算地区匹配度
                area_match_score = 1.0 if city and city in city else 0.7
                
                # 计算岗位方向匹配度（更精确的计算）
                if name and name.lower() in job_name.lower():
                    job_match_score = 1.0  # 完全匹配
                elif name and any(term in job_name.lower() for term in [name.lower(), "开发", "工程师"]):
                    job_match_score = 0.8  # 部分匹配
                else:
                    job_match_score = 0.4  # 不太匹配
                
                # 计算综合匹配分数，根据不同优先级调整权重
                match_score = 0
                if priority == 'match':
                    # 综合匹配度优先，平衡各项指标
                    match_score = 0.4 * skill_match_score + 0.3 * area_match_score + 0.3 * job_match_score
                elif priority == 'area':
                    # 地区优先，给地区匹配度更高权重
                    match_score = 0.7 * area_match_score + 0.15 * skill_match_score + 0.15 * job_match_score
                elif priority == 'skill':
                    # 技能优先，给技能匹配度更高权重
                    match_score = 0.7 * skill_match_score + 0.15 * area_match_score + 0.15 * job_match_score
                elif priority == 'salary':
                    # 薪资优先，考虑薪资水平
                    avg_salary = (min_salary + max_salary) / 2
                    salary_score = min(1.0, avg_salary / 50000)  # 假设50000是参考上限
                    match_score = 0.6 * salary_score + 0.2 * skill_match_score + 0.1 * area_match_score + 0.1 * job_match_score
                else:
                    # 默认匹配策略
                    match_score = 0.4 * skill_match_score + 0.3 * area_match_score + 0.3 * job_match_score
                
                # 应用岗位方向过滤器：如果优先级为match且指定了岗位方向但匹配度很低，则排除该岗位
                if priority == 'match' and name and job_match_score < 0.5:
                    continue
                
                # 构建岗位数据结构，包含详细信息
                job_data = {
                    'id': job_id,
                    'name': job_name,
                    'company': company,
                    'city': city,
                    'area': area,
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'education': education,
                    'experience': experience,
                    'detail': detail,
                    'label': label,
                    'welfare': welfare,
                    'skills_required': required_skills,  # 使用数据库中的技能列表
                    'match_score': match_score,
                    'skill_match_score': skill_match_score,  # 单独保存技能匹配度
                    'matched_skills': matched_skills  # 保存匹配的技能列表
                }
                
                matched_jobs.append(job_data)
            
            # 根据匹配度排序
            matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            
            # 返回匹配的岗位和总数
            return matched_jobs, total
            
        except Exception as e:
            print(f"岗位匹配查询错误: {str(e)}")
            return [], 0
    
    # 计算匹配分析数据
    def calculate_match_analysis(self, matched_jobs, user_skills):
        """
        计算岗位匹配分析数据
        :param matched_jobs: 匹配到的岗位列表
        :param user_skills: 用户技能列表
        :return: 匹配分析数据
        """
        if not matched_jobs:
            return {
                'skill_match_percentage': 0,
                'area_match_percentage': 0,
                'avg_salary': 0,
                'skill_stats': {},
                'missing_skills': []
            }
        
        # 计算各项平均匹配度和统计数据
        total_skill_match = 0
        total_jobs = len(matched_jobs)
        total_salary = 0
        skill_occurrence = {}
        
        # 所有岗位要求的技能集合
        all_required_skills = set()
        
        for job in matched_jobs:
            # 累加技能匹配度
            total_skill_match += job.get('skill_match_score', 0)
            
            # 累加薪资计算平均值
            min_salary = job['min_salary']
            max_salary = job['max_salary']
            avg_job_salary = (min_salary + max_salary) / 2
            total_salary += avg_job_salary
            
            # 统计所有岗位中各个技能的出现次数
            for skill in job.get('skills_required', []):
                skill_occurrence[skill] = skill_occurrence.get(skill, 0) + 1
                all_required_skills.add(skill)
        
        # 计算平均值
        avg_skill_match = total_skill_match / total_jobs if total_jobs > 0 else 0
        avg_salary = total_salary / total_jobs if total_jobs > 0 else 0
        
        # 排序技能频率，找出最常见的技能
        sorted_skills = sorted(skill_occurrence.items(), key=lambda x: x[1], reverse=True)
        top_skills = {skill: count for skill, count in sorted_skills[:10]}
        
        # 找出用户缺少的技能（常见技能中用户不具备的）
        user_skills_lower = [s.lower() for s in user_skills]
        missing_skills = []
        
        for skill, count in sorted_skills[:5]:
            skill_lower = skill.lower()
            # 检查用户是否具备此技能（部分匹配也算）
            if not any(user_skill in skill_lower or skill_lower in user_skill for user_skill in user_skills_lower):
                missing_skills.append({
                    'name': skill,
                    'frequency': count,
                    'percentage': (count / total_jobs) * 100 if total_jobs > 0 else 0
                })
        
        # 构建分析结果
        analysis = {
            'skill_match_percentage': avg_skill_match * 100,  # 转为百分比
            'area_match_percentage': 80,  # 假设地区匹配度
            'avg_salary': avg_salary,
            'skill_stats': top_skills,
            'missing_skills': missing_skills
        }
        
        return analysis
