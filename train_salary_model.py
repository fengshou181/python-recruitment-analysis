#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
薪资预测模型训练脚本
用法: python train_salary_model.py [--visualize] [--limit 数据量]
"""

import argparse
import os
import sys
import logging
from salary_model import visualize_data, MySql, SalaryPredictor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('salary_model_training')

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="训练薪资预测模型")
    parser.add_argument("--visualize", action="store_true", help="是否仅生成数据可视化图表")
    parser.add_argument("--limit", type=int, default=None, help="从数据库获取的数据量限制，设为0表示不限制")
    return parser.parse_args()

def custom_main(data_limit=None):
    """自定义main函数实现，支持数据量限制参数"""
    print("开始薪资预测模型训练流程")
    
    try:
        # 1. 连接数据库并获取数据
        print("从数据库获取数据...")
        db = MySql()
        df = db.get_salary_data(limit=data_limit)
        db.close()
        
        if df.empty:
            logger.error("获取的数据为空，请检查数据库连接或查询条件")
            return False
            
        print(f"获取到 {len(df)} 条数据记录")
        
        # 2. 数据基本信息
        print("\n数据基本信息:")
        print(f"数据规模: {df.shape[0]} 行, {df.shape[1]} 列")
        print("数据类型:")
        print(df.dtypes)
        print("缺失值统计:")
        print(df.isnull().sum())
        
        # 3. 数据可视化
        try:
            visualize_data(df)
        except Exception as e:
            logger.warning(f"数据可视化过程中出现问题: {str(e)}，但继续进行模型训练")
        
        # 4. 创建模型并训练
        predictor = SalaryPredictor()
        metrics = predictor.train(df)
        
        # 5. 保存模型
        predictor.save_model()
        
        print("训练完成!")
        
        # 6. 测试模型预测
        test_input = {
            'province': '北京市',
            'city': '北京市',
            'area': '朝阳区',
            'scale': '1000-9999人',
            'name': 'Python开发工程师',
            'education': '本科',
            'experience': '3-5年',
            'skill': 'Python Django Flask 数据分析 爬虫'
        }
        
        # 重新加载模型以验证保存和加载功能
        predictor = SalaryPredictor()
        if predictor.load_model():
            try:
                prediction = predictor.predict_salary(test_input)
                print("\n测试预测结果:")
                print(f"预估薪资区间: {prediction['min_salary']} ~ {prediction['max_salary']} 元/月")
                print(f"平均薪资: {prediction['avg_salary']} 元/月")
                print(f"置信度: {prediction['confidence']}")
            except Exception as e:
                logger.error(f"预测过程出现问题: {str(e)}")
        else:
            logger.error("模型加载失败，无法进行预测测试")
            
        return True
        
    except Exception as e:
        logger.error(f"训练过程发生异常: {str(e)}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    data_limit = args.limit if args.limit != 0 else None
    
    # 如果仅需要可视化数据，则只执行可视化步骤
    if args.visualize:
        print(f"仅执行数据可视化，数据量限制: {data_limit if data_limit else '不限'}")
        try:
            db = MySql()
            df = db.get_salary_data(limit=data_limit)
            db.close()
            visualize_data(df)
            print("数据可视化完成")
        except Exception as e:
            logger.error(f"数据可视化过程中出现问题: {str(e)}")
            sys.exit(1)
    else:
        # 执行完整的模型训练流程
        print(f"执行完整模型训练流程，数据量限制: {data_limit if data_limit else '不限'}")
        
        # 使用自定义main函数，传递数据限制参数
        success = custom_main(data_limit=data_limit)
        if not success:
            sys.exit(1) 