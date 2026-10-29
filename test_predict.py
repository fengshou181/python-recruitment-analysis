#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试薪资预测模型的预测功能
"""

import sys
import time
import traceback
from salary_model import SalaryPredictor

def test_prediction():
    """测试模型预测功能"""
    print("开始测试薪资预测模型...")
    
    try:
        # 创建预测器实例
        predictor = SalaryPredictor()
        
        # 加载模型
        print("正在加载模型...")
        if not predictor.load_model():
            print("模型加载失败，请确认已经训练并保存了模型文件")
            return False
            
        print("模型加载成功！")
        
        # 设置测试用例
        test_cases = [
            {
                'name': "北京Python开发工程师",
                'province': '北京市',
                'city': '北京市',
                'area': '朝阳区',
                'scale': '1000-9999人',
                'education': '本科',
                'experience': '3-5年',
                'skill': 'Python Django Flask 数据分析 爬虫'
            },
            {
                'name': "上海Java工程师",
                'province': '上海市',
                'city': '上海市',
                'area': '浦东新区',
                'scale': '500-999人',
                'education': '硕士',
                'experience': '5-10年',
                'skill': 'Java SpringBoot Mybatis 微服务'
            },
            {
                'name': "深圳前端工程师",
                'province': '广东省',
                'city': '深圳市',
                'area': '南山区',
                'scale': '100-499人',
                'education': '大专',
                'experience': '1-3年',
                'skill': 'Javascript Vue React 前端开发'
            }
        ]
        
        # 测试不同职位的预测
        for i, test_case in enumerate(test_cases):
            print(f"\n测试用例 #{i+1}: {test_case['name']}")
            print("-" * 40)
            print(f"城市: {test_case['city']}")
            print(f"学历: {test_case['education']}")
            print(f"经验: {test_case['experience']}")
            print(f"规模: {test_case['scale']}")
            print(f"技能: {test_case['skill']}")
            
            # 执行预测
            start_time = time.time()
            prediction = predictor.predict_salary(test_case)
            elapsed = time.time() - start_time
            
            print("\n预测结果:")
            print(f"薪资范围: {prediction['min_salary']:,} ~ {prediction['max_salary']:,} 元/月")
            print(f"平均薪资: {prediction['avg_salary']:,} 元/月")
            print(f"置信度: {prediction['confidence']:.2f}")
            print(f"预测耗时: {elapsed:.3f} 秒")
            print("-" * 40)
            
        print("\n全部测试完成！")
        return True
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        print("错误详情:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prediction()
    if not success:
        sys.exit(1) 