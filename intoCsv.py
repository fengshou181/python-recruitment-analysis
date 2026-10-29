import mysql
import pandas


class IntoCsv:

    def __init__(self):
        # 实例化数据库对象
        print(">>>链接数据库")
        self.__sql = mysql.MySql()

    def run(self):
        self.__dataToCsv()

    # 将原始数据转换为csv文件 Data.csv 同时清除重复项
    def __dataToCsv(self):
        # 从数据库获取原始数据
        algorithm_data = self.__sql.readAlgorithmData()
        android_data = self.__sql.readAndroidData()
        c_data = self.__sql.readCData()
        c23_data = self.__sql.readC23Data()
        ios_data = self.__sql.readIosData()
        java_data = self.__sql.readJavaData()
        oam_data = self.__sql.readOamData()
        php_data = self.__sql.readPhpData()
        python_data = self.__sql.readPythonData()
        test_data = self.__sql.readTestData()
        u3due_data = self.__sql.readU3dueData()
        web_data = self.__sql.readWebData()

        data_list = [algorithm_data, android_data, c_data, c23_data, ios_data, java_data, oam_data, php_data,
                     python_data, test_data, u3due_data, web_data]
        name_list = ["algorithm", "android", "c", "c23", "ios", "java", "oam", "php", "python", "test", "u3due", "web"]
        # 将数据转换为dataframe格式

        for var in data_list:
            data = pandas.DataFrame(var)
            # 设置数据索引
            data_1 = data.set_index('num', drop=True)
            # 写入csv
            name = "csv/" + name_list[data_list.index(var)] + ".csv"
            pandas.DataFrame.to_csv(data_1, name, encoding='utf-8')
            print(">>>数据转换csv格式成功")

