import pandas as pd
import numpy as np

index = ['2022-06-20']
columns = ['今日花费（元）', '早上起床时间（小时）', '晚上睡觉时间（小时）', '中午午睡时间（小时）', '躺尸时间（小时）', '聊天次数', '水果', '白水饮用（ml）', '看纸质书的时间（小时）', '其他']

initial = pd.DataFrame(index = pd.to_datetime(index), columns = columns)

initial['今日花费（元）'] = 5
initial['早上起床时间（小时）'] = 7
initial['晚上睡觉时间（小时）'] = 22.2
initial['中午午睡时间（小时）'] = 2
initial['躺尸时间（小时）'] = 5
initial.聊天次数 = 0
initial.水果 = ''
initial['白水饮用（ml）'] = 1500
initial['看纸质书的时间（小时）'] = 0
initial.其他 = ''

initial.to_csv('diary.csv')
