#!/usr/bin/env python3 - analysis.py
# -*- coding:utf-8 -*-
# Author: 薛骏

import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import wordcloud
import os

MainCharacterNumber = 11    # 主角人数
# 虚词(无意义单词),可自行增加，用于排除无效词以及词云制作
EmptyWords = ['a', 'an', 'the', 'of', 'for', 'to', 'from', 'with', 'on', 'at', 'in',
              'are', 'am', 'is', 'shall', 'was', 'were', 'be', 'been', 'being', '–']


def RebuildScriptData(data, SN):
    # 读取整理后的数据，并构成可使用的数据形式
    # 利用 pandas 简单分析数据
    des = data.describe()
    # 合并除主角之外的其他角色的数据
    otherscripts = SN - round(des.loc['count', 'the Number of Scripts'] * des.loc['mean', 'the Number of Scripts'])
    otherpercentage = 100 - round(des.loc['count', 'the Percentage of Scripts(%)'] * des.loc['mean', 'the Percentage of Scripts(%)'], 2)
    otherwords = 0  # 因为用不到，所以置零
    # 构建 others 的 一维数据
    s = pd.Series({'Character': 'OTHERS', 'the Number of Scripts': otherscripts,
                   'the Percentage of Scripts(%)': otherpercentage, 'the Number of Words': otherwords})
    # 加入到已有数据中
    data = data.append(s, ignore_index=True)
    return data


def ShowScriptData(DataPath, ScriptNumber):
    global MainCharacterNumber
    filename = DataPath + 'TotalStatistics.csv'    # 文件名
    data = pd.read_csv(filename)    # 读取文件
    print(data)    # 显示数据
    scriptdata = RebuildScriptData(data.head(MainCharacterNumber), ScriptNumber)    # 重建台词数据
    return scriptdata    # 返回前11个数据，在最上方可以自行修改


def FilterEmptyWords(words):
    global EmptyWords
    # 获取单词序列
    WordList = list(words['Word'])
    DeleteIndex = []    # 用于存储删除单词的下标
    # 便利寻找无意义的单词
    for i in range(len(WordList)):
        if WordList[i] in EmptyWords:
            DeleteIndex.append(i)
    # 删除数据中无意义单词
    words = words.drop(index=DeleteIndex)
    # 删除数据中无效项
    words = words.dropna(how='any')
    # 重标单词列表前的 index 序号
    words = words.reset_index(drop=True)
    return words


def PrintCommonWords(person, filename):
    # 读取数据
    words = pd.read_csv(filename,  delimiter=',', error_bad_lines=False)
    # 过滤无效单词
    words = FilterEmptyWords(words)
    # 存下并打印该角色最常使用的 20 个单词
    commonwords = words.head(20)
    print('{}:'.format(person))
    print(commonwords, end='\n\n')
    return commonwords


def ShowCommonWords(data, DataPath):
    # 将主角转为 numpy 数组
    characters = np.array(data["Character"])
    charactercommonwords = {}   # 用于存储所有主角的常用词
    # 打印每个主角的常用词，并存入字典
    for person in characters:
        filename = DataPath + r'person\{0}.csv'.format(person.lower())
        commonwords = PrintCommonWords(person, filename)
        charactercommonwords[person] = commonwords
    return charactercommonwords


def DrawBarGraph(character, scriptnumber):
    # 图的大小
    figsize = 12, 5
    # 绘图
    figure, ax = plt.subplots(figsize=figsize)
    # 设置标题字体格式
    font1 = FontProperties(fname=r'C:\Windows\Fonts\STKAITI.TTF', size=14)
    # 构造条形图
    a = plt.bar(character, scriptnumber, label='script')
    # 给条形图上方加上具体数值
    for rect in a:
        height = round(rect.get_height())
        plt.text(rect.get_x()+rect.get_width()/4, height + 50, '%s' % int(height))
    plt.legend()
    # 设置坐标标签大小
    plt.tick_params(labelsize=8)
    # 设置 x 轴标签内容
    plt.xlabel('character')
    # 设置 y 轴标签内容
    plt.ylabel('the Number of Scripts')
    # 设置标题内容
    plt.title(r'主角台词量比较——条形图', FontProperties=font1)
    plt.show()


def DrawPieGraph(character, scriptnumber):
    # 设置标题字体格式
    font1 = FontProperties(fname=r'C:\Windows\Fonts\STKAITI.TTF', size=14)
    # 设置各扇面颜色
    colors = ('lightgreen', 'gold', 'red', 'lightcoral', 'yellow', 'gray', 'pink',
              'lightskyblue', 'brown', 'purple', 'orange', 'cyan')
    # 绘制饼图
    patches, l_text, p_text = plt.pie(tuple(scriptnumber), labels=tuple(character),
                                      colors=colors, autopct='%1.2f%%', shadow=True,
                                      startangle=520)
    # 设置标题内容
    plt.title(r'主角台词量占比——饼图', FontProperties=font1)
    # 使饼图呈圆形
    plt.axis('equal')
    plt.show()


def ScriptAnalysis(SD):
    # 获取绘图所需数据
    character = list(SD['Character'])
    scriptnumber = list(SD['the Number of Scripts'])
    # 绘制柱状图
    DrawBarGraph(character, scriptnumber)
    # 绘制饼图
    DrawPieGraph(character, scriptnumber)


def SeriesWordCloud(SP, CP):
    global EmptyWords
    # 读取剧本合集内容
    with open(SP, 'r', encoding='utf-8') as f:
        txt = f.read()
    # 读取词云遮罩图片
    image = np.array(plt.imread(CP + '.jpg'))
    # 设置词云字体
    font = r'C:\Windows\fonts\comic.ttf'
    # 设置停用词
    sw = set(wordcloud.STOPWORDS)
    for word in EmptyWords:
        sw.add(word)
    # 生成词云
    cloud = wordcloud.WordCloud(scale=4, font_path=font, mask=image, stopwords=sw,
                                background_color='white', max_words=250,
                                random_state=20).generate(txt)
    # 显示词云
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    # 将词云保存
    cloud.to_file(CP + '1.jpg')


def CompareData(SD, SP, CP):
    # 显示台词量的柱状图以及占比饼图
    ScriptAnalysis(SD)
    # 制作词云
    SeriesWordCloud(SP, CP)


def DeleteData(DP):
    filelist = os.listdir(DP)
    for i in filelist:
        filepath = os.path.join(DP, i)
        if os.path.isdir(filepath):
            DeleteData(filepath)
        else:
            os.remove(filepath)
    os.rmdir(DP)


def Analysis():
    global MainCharacterNumber
    # 统计数据
    DataPath, ScriptPath, ScriptNumber = statistics.Statistics()
    # 显示台词量，并返回台词量前11多的角色(主角)
    ScriptData = ShowScriptData(DataPath, ScriptNumber)
    # 显示主角最常用的20个单词
    ShowCommonWords(ScriptData.head(MainCharacterNumber), DataPath)
    # 数据对比
    CompareData(ScriptData, ScriptPath, DataPath[:-5] + 'post')
    # 删除整理后的数据：便于多次运行，若不希望删除，则注释下一语句
    DeleteData(DataPath)


if __name__ == '__main__':
    Analysis()
