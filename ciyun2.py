import pandas as pd
import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取Excel文件
file_path = 'Data.xlsx'  # 替换为你的实际文件路径
df = pd.read_excel(file_path)

# 确保数据中包含 skill 列
if 'skill' not in df.columns:
    raise ValueError("Excel 文件中没有 'skill' 列")

# 提取 skill 列的数据并将其转换为字符串
skill_data = df['skill'].astype(str)

# 统计每个技能词汇的出现频率
word_count = Counter()


# 辅助函数：过滤标点符号和单一阿拉伯数字
def filter_words(words):
    filtered_words = []
    for word in words:
        # 去除标点符号和单一数字
        if re.match(r'^[\u4e00-\u9fa5]+$', word):  # 仅保留中文字符
            filtered_words.append(word)
        elif not word.isdigit():  # 不是单一数字
            filtered_words.append(word)
    return filtered_words


# 遍历每一行的技能数据
for text in skill_data:
    # 对文本进行jieba分词
    words = jieba.lcut(text)

    # 过滤标点符号和单一阿拉伯数字
    filtered_words = filter_words(words)

    # 统计分词结果
    for word in filtered_words:
        if word.strip():  # 只统计非空白的词
            word_count[word] += 1

# 使用wordcloud库生成词云图
wordcloud = WordCloud(
    font_path='msyh.ttc',  # Windows系统下指定微软雅黑字体路径，Mac或Linux可以使用其他字体
    width=2400,
    height=1800,
    background_color='white',
).generate_from_frequencies(word_count)

# 保存图像到本地，并设置DPI为300，避免留白
output_image_path = 'skill_wordcloud_output.png'
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.tight_layout(pad=0)  # 通过紧凑布局减少留白

# 保存图像，设置DPI为300
plt.savefig(output_image_path, dpi=300)

# 显示生成的词云图
plt.show()

print(f"词云图已保存至: {output_image_path}")
