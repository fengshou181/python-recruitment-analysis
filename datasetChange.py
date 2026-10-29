# import pymysql
#
# class MySql(object):
#     def __init__(self):
#         self.connect = pymysql.connect(
#             host="127.0.0.1",
#             port=3306,
#             user="root",
#             password="123456",
#             database="spiderdatabase",
#             charset="utf8"
#         )
#         self.cursor = self.connect.cursor()
#
#     def __del__(self):
#         self.cursor.close()
#         self.connect.close()
#
#     def close(self):
#         self.cursor.close()
#         self.connect.close()
#
#     def update_provinces(self):
#         # 城市 => 省份 映射
#         city_to_province = {
#             "北京": "北京市",
#             "上海": "上海市",
#             "广州": "广东省",
#             "深圳": "广东省",
#             "杭州": "浙江省",
#             "天津": "天津市",
#             "西安": "陕西省",
#             "苏州": "江苏省",
#             "武汉": "湖北省",
#             "厦门": "福建省",
#             "长沙": "湖南省",
#             "成都": "四川省",
#             "郑州": "河南省",
#             "重庆": "重庆市",
#             "佛山": "广东省",
#             "合肥": "安徽省",
#             "济南": "山东省",
#             "青岛": "山东省",
#             "南京": "江苏省",
#             "东莞": "广东省",
#             "福州": "福建省"
#         }
#
#         # 只更新 province 为 NULL 的记录
#         for city, province in city_to_province.items():
#             sql = """
#                 UPDATE c_data
#                 SET province = %s
#                 WHERE city = %s AND province IS NULL
#             """
#             self.cursor.execute(sql, (province, city))
#             print(f"已更新 city = {city} 的 province => {province}")
#
#         self.connect.commit()
#         print("✅ 所有符合条件的记录已更新完成。")
#
# if __name__ == "__main__":
#     db = MySql()
#     db.update_provinces()
#     db.close()
import pymysql


class MySql(object):
    def __init__(self):
        # 建议从配置文件或环境变量读取敏感信息，这里为了方便直接写入
        self.connect = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123456",
            database="spiderdatabase",
            charset="utf8"
        )
        self.cursor = self.connect.cursor()
        print("🎉 数据库连接成功！")

    def __del__(self):
        self.cursor.close()
        self.connect.close()
        print("💨 数据库连接已断开。")

    def close(self):
        """主动关闭连接"""
        self.cursor.close()
        self.connect.close()
        print("💨 数据库连接已主动关闭。")

    def unify_city_names(self):
        """
        统一 c_data 表中的 city 字段，为不规范的城市名称加上“市”后缀。
        这是一个真正“一劳永逸”的解决方案。
        """
        print("\n🚀 开始执行 city 字段统一化任务...")

        # 定义一些常见的不需要加后缀的词，防止例如“朝阳区”变成“朝阳区市”
        # 你可以根据你的数据情况扩充这个列表
        ignore_suffixes = ['市', '省', '区', '县', '盟', '旗', '自治州']

        try:
            # 1. 找出所有不重复的城市名，提高效率
            self.cursor.execute("SELECT DISTINCT city FROM c_data")
            all_cities = [item[0] for item in self.cursor.fetchall()]

            update_count = 0
            # 2. 遍历所有城市名，找出需要更新的
            for city_name in all_cities:
                if not city_name:  # 跳过空字符串或NULL
                    continue

                # 检查是否以忽略的后缀结尾
                needs_update = True
                for suffix in ignore_suffixes:
                    if city_name.endswith(suffix):
                        needs_update = False
                        break

                # 3. 如果需要更新，则执行 UPDATE 操作
                if needs_update:
                    new_city_name = city_name + '市'
                    sql = "UPDATE c_data SET city = %s WHERE city = %s"
                    self.cursor.execute(sql, (new_city_name, city_name))
                    update_count += self.cursor.rowcount  # 累加受影响的行数
                    print(f"  - [更新] 将 '{city_name}' 标准化为 '{new_city_name}'")

            # 4. 如果有更新，则提交事务
            if update_count > 0:
                self.connect.commit()
                print(f"\n✅ 数据清洗完成！共更新了 {update_count} 条记录。")
            else:
                print("\n✅ 数据检查完成，所有 city 字段都已是标准格式，无需更新。")

        except Exception as e:
            print(f"\n❌ 执行出错: {e}")
            print("   操作已回滚，数据库未做任何更改。")
            self.connect.rollback()


if __name__ == "__main__":
    db = MySql()

    # 执行城市名称统一化
    db.unify_city_names()

    # 完成后关闭连接
    db.close()