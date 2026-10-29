# -*- coding: utf-8 -*-
"""数据分析 筛选组合批量采集：6 组 (经验×学历) × 82 城，逐组调 cdp_reader"""
import subprocess
import sys

CITIES = ('北京 上海 广州 深圳 杭州 成都 武汉 西安 南京 苏州 长沙 重庆 郑州 天津 合肥 青岛 '
          '济南 东莞 佛山 福州 厦门 哈尔滨 长春 沈阳 大连 呼和浩特 石家庄 太原 乌鲁木齐 '
          '兰州 银川 南昌 贵阳 昆明 南宁 海口 无锡 南通 常州 徐州 盐城 扬州 镇江 泰州 '
          '温州 嘉兴 绍兴 金华 台州 湖州 泉州 烟台 潍坊 临沂 济宁 泰安 威海 淄博 珠海 '
          '中山 惠州 汕头 江门 洛阳 新乡 保定 廊坊 唐山 绵阳 芜湖 柳州 桂林 赣州 九江 '
          '襄阳 宜昌 株洲 岳阳 包头 吉林 大庆 齐齐哈尔').split()

# experience: 105=1-3年, 106=3-5年, 107=5-10年; degree: 203=本科, 202=大专
COMBOS = [
    'experience=105&degree=203', 'experience=106&degree=203', 'experience=107&degree=203',
    'experience=105&degree=202', 'experience=106&degree=202', 'experience=107&degree=202',
]

for i, combo in enumerate(COMBOS, 1):
    print(f'===== 组合 {i}/{len(COMBOS)}: {combo} =====', flush=True)
    cmd = [sys.executable, 'spider/cdp_reader.py', '--keyword', '数据分析', '--auto',
           '--cities'] + CITIES + [
           '--pages-per-city', '1', '--pages', '200', '--delay-min', '8', '--delay-max', '13',
           '--rest-every', '30', '--rest-min', '60', '--rest-max', '120',
           '--filter-arg', combo]
    subprocess.run(cmd)
print('===== 全部组合完成 =====', flush=True)
