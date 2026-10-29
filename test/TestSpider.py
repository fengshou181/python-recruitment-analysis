import random
import re
import urllib.error
import urllib.request


import bs4
import pymysql


"""正则表达式匹配规则"""
find_link = re.compile(r'<a href="(.*?)">')  # 详情链接匹配规则

find_img_src = re.compile(r'<img.*src="(.*?)"', re.S)  # 图片地址匹配规则 re.S保留换行符

find_title = re.compile(r'<span class="title">(.*)</span>')  # 影片名称匹配规则

find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # 影片评分匹配规则

find_judge = re.compile(r'<span>(\d*)人评价</sapn>')  # 评价人数匹配规则

find_inq = re.compile(r'<span class="inq">(.*)</span>')  # 概况匹配规则

find_bd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 相关信息匹配规则


def main():

    url = "https://movie.douban.com/top250?start="

    data_list = getData(url)
    saveData(data_list)


def getData(target_url):
    datalist = []

    """获取10次链接"""
    for i in range(0, 100):
        url = target_url + str(i * 25)

        """保存页面原始数据"""
        html = askUrl(url)

        """逐一解析页面"""
        soup = bs4.BeautifulSoup(html, "html.parser")
        for value in soup.find_all('div', class_="item"):
            data = []

            """将值转化为字符串"""
            value = str(value)

            """正则表达式匹配"""
            link = re.findall(find_link, value)[0]  # 0为匹配重复对象的第一条
            data.append(link)

            imgSrc = re.findall(find_img_src, value)[0]
            data.append(imgSrc)

            title = re.findall(find_title, value)  # 名称可能有多个
            if len(title) == 2:
                cn_title = title[0]  # 添加中文名
                data.append(cn_title)
                en_title = title[1].replace("/", "")  # 添加外文名
                data.append(en_title)
            else:
                data.append(title[0])
                data.append(" ")  # 无外文名留空

            rating = re.findall(find_rating, value)[0]
            data.append(rating)

            judge_num = re.findall(find_judge, value)
            data.append(judge_num)

            inq = re.findall(find_inq, value)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(find_bd, value)[0]
            bd = re.sub(r"<br(\s+)?/>(\s+)?", "", bd)
            data.append(bd.strip())  # strip去掉前后空格

            """处理好的一部电影信息存入列表"""
            datalist.append(data)
    print(datalist)
    return datalist


def askUrl(target_url):
    """伪装浏览器"""
    head = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"
    }
    """获取网站回应"""
    request = urllib.request.Request(target_url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("UTF-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


def saveData(data_list):
    print(data_list)
    connect = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                              password='123456', database='spiderdatabase',
                              charset='utf8')
    print('-------------链接数据库成功-------------')
    cursor = connect.cursor()

    for data in data_list:
        for index in range(len(data)):
            data[index] = str(data[index])
        sql = '''insert into movie250 (
                info_link,pic_link,cname,ename,socre,rated,instroduction,info)
                values (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        try:
            cursor.execute(sql, data)
            connect.commit()
        except Exception as e:
            connect.rollback()

            print("插入数据失败 执行MySQL: %s 时出错：%s" % (sql, e))

    print('-------------数据存储成功-------------')
    cursor.close()
    connect.close()
    return


if __name__ == "__main__":
    main()
