import mysql
from wordcloud import WordCloud
from PIL import Image

from matplotlib import pyplot as plt


class Cloud:
    def __init__(self):
        # 实例化数据库对象
        print(">>>链接数据库")
        self.__sql = mysql.MySql()

    def __del__(self):
        print(">>>词云生成成功")

    '''首页'''

    # 生成热门岗位词云图
    def popularJobs(self):
        text = self.__sql.getJobName()
        Str = str(text).replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\热门岗位.jpg')

    # 总体福利热词
    def welfareCloud(self):
        text = self.__sql.getWelfare()
        Str = str(text).replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\福利待遇.jpg')

    '''java'''

    def javaSkillCloud(self):
        text = self.__sql.javaGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\Java技术热词.jpg')

    '''python'''

    def pythonSkillCloud(self):
        text = self.__sql.pythonGetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\Python技术热词.jpg')

    '''c/c++'''

    def cSkillCloud(self):
        text = self.__sql.cGetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\C C++技术热词.jpg')

    '''c#/.net'''

    def c23SkillCloud(self):
        text = self.__sql.c23GetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\C23技术热词.jpg')

    '''u3due'''

    def u3dUeSkillCloud(self):
        text = self.__sql.u3dUeGetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\u3dUe技术热词.jpg')

    '''PHP'''

    def phpSkillCloud(self):
        text = self.__sql.phpGetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\php技术热词.jpg')

    '''PHP'''

    def webSkillCloud(self):
        text = self.__sql.webGetSkill()
        Str = str(text).replace('Python', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\web技术热词.jpg')

    '''Android'''

    def AndroidSkillCloud(self):
        text = self.__sql.AndroidGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\Android技术热词.jpg')

    '''ios'''

    def iosSkillCloud(self):
        text = self.__sql.iosGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\ios技术热词.jpg')


    '''algorithm'''

    def algorithmSkillCloud(self):
        text = self.__sql.algorithmGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\algorithm技术热词.jpg')

    '''test'''


    def testSkillCloud(self):
        text = self.__sql.testGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\test技术热词.jpg')


    '''oam'''


    def oamSkillCloud(self):
        text = self.__sql.oamGetSkill()
        Str = str(text).replace('Java', '').replace("'", '').replace(",", '')
        wc = WordCloud(
            scale=1,
            background_color='white',
            font_path=r'C:\Windows\Fonts\msyh.ttc',
            min_font_size=1,
            max_font_size=60,
            width=750,
            height=400
        )
        wc.generate_from_text(Str)
        plt.axis('off')
        wc.to_file(r'd:\oam技术热词.jpg')

