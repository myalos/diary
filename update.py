"""
    作者 myalos
    时间 2022-06-20
    功能 用csv来写日记
    版本 1.0.0
"""
import datetime
import numpy as np
import pandas as pd
import pyttsx3
import os

VERSION = 'RELEASE'

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

columns = ['今日花费（元）', '早上起床时间（小时）', '晚上睡觉时间（小时）', '中午午睡时间（小时）', '躺尸时间（小时）', '聊天次数', '水果', '白水饮用（ml）', '看纸质书的时间（小时）', '其他']
# 配置文件
if VERSION != 'RELEASE':
    engine = pyttsx3.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.kyoko')
    engine.say('マスター')
    engine.say(f'今日は{year}年{month}月{day}日です')
    engine.runAndWait()

    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.meijia')
    engine.setProperty('volume', 0.9)
    engine.say('今天辛苦啦！来记录一下今天的生活吧~')
    engine.runAndWait()

# 工具函数
def check_24(string) -> bool:
    """
        功能 检查字符串是否是小时:分钟 这样的格式
        输入 字符串
        输出 检查结果
    """
    if ':' not in string:
        return False
    str_list = string.split(':')
    if len(str_list) != 2 or len(str_list[0]) > 2 or len(str_list[1]) > 2:
        return False
    try:
        a, b = int(str_list[0]), int(str_list[1])
    except ValueError:
        return False
    if a > 47 or b > 59:
        return False
    return True

def check_goodslist(string) -> bool:
    """
        功能 检查描述东西的字符串格式是否正确
        输入 字符串
        输出 检查结果
    """
    str_list = string.split(',')
    for item_str in str_list:
        item_list = item_str.split('*')
        if len(item_list) > 2:
            return False
        goodsname = item_list[0]
        goodscount = item_list[1] if len(item_list) == 2 else 1
        try:
            goodscount = int(goodscount)
        except ValueError:
            return False
    return True

def voice(string) -> None:
    """
        功能: 用人声将string读出来
        输入: 要读的字符串
    """
    global VERSION
    if VERSION == 'RELEASE':
        return
    global engine
    engine.say(string)
    engine.runAndWait()


diary_path = 'diary.csv'
while True:
    try:
        table = pd.read_csv(diary_path, index_col=0, parse_dates=[0])
        print('成功读入日记')
        break
    except FileNotFoundError:
        print('默认日记没有找到，请输入日记所在位置，输入退出就会退出程序')
        voice('默认日记没有找到，请输入日记所在位置，输入退出就会退出程序')
        input_str = input('请输入：\n')
        if input_str == '退出':
            exit()
        elif input_str.endswith('csv'):
            diary_path = input_str
        else:
            # 不能用os.path.join 因为join是会加个/符号
            diary_path = input_str + '.csv'

new_index = datetime.datetime(year, month, day)
table.loc[new_index] = [np.nan] * table.shape[1]

print('请输入今日花费的金额：（元）')
while True:
    try:
        money = float(input(''))
        table.loc[new_index, columns[0]] = money
        break
    except ValueError:
        print('输入内容有问题，请输入合理的数')
        voice('输入内容有问题，请输入合理的数')

print('请输入今日起床的时间：（24小时制）格式是  小时:分钟')
while True:
    getup_time = input('')
    if not check_24(getup_time):
        print('输入内容的格式有问题，请输入格式  小时:分钟')
        voice('输入内容的格式有问题，请重新输入')
        continue
    hour, minute = int(getup_time.split(':')[0]), int(getup_time.split(':')[1] )
    table.loc[new_index, columns[1]] = f'{hour:02d}:{minute:02d}'
    break

print('请输入今日晚上睡觉时间: （24小时制）格式是小时:分钟')
while True:
    sleep_time = input('')
    if not check_24(getup_time):
        print('输入内容的格式有问题，请输入格式小时:分钟')
        voice('输入内容的格式有问题，请重新输入')
        continue
    hour, minute = int(getup_time.split(':')[0]), int(getup_time.split(':')[1] )
    table.loc[new_index, columns[2]] = f'{hour:02d}:{minute:02d}'
    break

print('请输入今日午睡时长：（分钟）')
while True:
    try:
        midsleep_time = int(input(''))
        table.loc[new_index, columns[3]] = midsleep_time
        break
    except ValueError:
        print('输入内容有问题，请输入合理的整数')
        voice('输入内容的格式有问题，请重新输入')

print('请输入今日躺尸时间：（分钟）')
while True:
    try:
        ts_time = int(input(''))
        table.loc[new_index, columns[4]] = ts_time
        break
    except:
        print('输入内容有问题，请输入合理的整数')
        voice('输入内容的格式有问题，请重新输入')

print('请输入今天聊天次数：')
while True:
    try:
        lt_time = int(input(''))
        table.loc[new_index, columns[5]] = lt_time
        break
    except:
        print('输入内容有问题，请输入合理的整数')
        voice('输入内容的格式有问题，请重新输入')

print('请输入今天吃的水果，格式是水果名*个数,用逗号来分隔')
while True:
    fruit = input('')
    if not check_goodslist(fruit):
        print('水果输入的格式有问题，请重新输入，格式是水果名*个数,用逗号来分隔')
        voice('输入内容的格式有问题，请重新输入')
        continue
    table.loc[new_index, columns[6]] = fruit
    break

print('请输入今天白水饮用量（ml）：')
while True:
    try:
        water = int(input(''))
        table.loc[new_index, columns[7]] = water
        break
    except ValueError:
        print('输入内容有问题，请输入合理的整数')
        voice('输入内容的格式有问题，请重新输入')

print('请输入今天看纸质书的时间（分钟）：')
while True:
    try:
        read_time = int(input(''))
        table.loc[new_index, columns[8]] = read_time
        break
    except ValueError:
        print('输入内容有问题，请输入合理的数')
        voice('输入内容的格式有问题，请重新输入')

print('请输入要额外记录的内容：')
extra_str = input('')
table.loc[new_index, columns[9]] = extra_str
if VERSION != 'RELEASE':
    engine.say('早点休息，明天继续加油鸭！')
    engine.runAndWait()

table.to_csv('diary.csv')
