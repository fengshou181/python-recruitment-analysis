import datahandle
from spider import bosszp_spider

# 爬数据的时候，先把数据清洗模块的代码（本页13--14行）注释掉，然后再运行；
# 清洗数据的时候，把数据爬虫模块的代码（本页8--9行）注释掉，然后再运行。

#数据爬虫
spider = bosszp_spider.Spider()
spider.run()


#数据清洗
# handle = datahandle.DataHandle()
# handle.run()
