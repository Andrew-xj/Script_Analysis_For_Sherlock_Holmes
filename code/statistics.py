#!/usr/bin/env python3 - statistics.py
# -*- coding:utf-8 -*-
# Author: 薛骏

import os

ScriptPath = ''             # Script 路径
FilePathList = []           # 文件路径列表
Person_ScriptNumber = {}    # 每名角色的台词量
Person_Word_Number = {}     # 每名角色的用词词频
Person_WordsNumber = {}     # 每名角色的单词数
PersonNumber = 0            # 角色数
ScriptNumber = 0            # 台词总量
DataPath = ''               # 整理完的 Data 的路径


def GetFileList():
    global ScriptPath, DataPath
    # 获取当前文件路径
    FilePath = os.path.abspath(__file__)
    # 获得数据源文件路径，此处用已知路径替代
    ScriptPath = FilePath[:-18] + 'script'
    # ScriptPath = input("请输入包含台词文件的文件夹路径")
    # 生成用于存放整理完的数据的路径：默认与代码所在文件夹同一目录下
    DataPath = FilePath[:-18] + 'data\\'
    os.makedirs(DataPath)
    # 得到所有台词的文件名
    Files = os.listdir(ScriptPath)
    FileList = []
    # 去除多于的文件名，并生成文件名列表
    for file in Files:
        if file[-3:] == 'txt':
            FileList.append(ScriptPath + '\\' + file)
    # 用于生成词云，所有剧本合集，自行修改(若无置为空字符串)
    ScriptPath += r'\raw_data\All_Episodes.txt'
    return FileList


def FormatPunctuation(content):
    # 遍历，将所有中文标点替换成英文标点
    ch = '，。？《》；：’‘“”（）【】！'
    en = ''',.?<>;:''""()[]!'''
    for i in range(len(ch)):
        content.replace(ch[i], en[i])
    return content


def DeleteEmptyLine(content):
    lines = []
    for line in content:
        if len(line) != 0:
            lines.append(line)
    return lines


def ScriptNumber(content):
    # 统计每个人的台词数量，并存入字典 Person_ScriptNumber 中
    global Person_ScriptNumber
    for line in content:
        script = line.split(':')
        if script[0] in Person_ScriptNumber.keys():
            Person_ScriptNumber[script[0]] += 1
        else:
            Person_ScriptNumber[script[0]] = 1


def WordFrequency(content):
    # 统计每个人所用单词的词频，同时获得其在剧中的所有台词的单词总数
    # 分别存入字典 Person_Word_Number, Person_WordsNumber 中
    global Person_Word_Number, Person_WordsNumber
    for line in content:
        script = line.split(':')    # 角色与台词分段
        # 统计单词词频
        if script[0] not in Person_Word_Number.keys():
            Person_Word_Number[script[0]] = {}
        else:
            words = script[1].lower().split(' ')    # 英文单词分词
            for word in words:
                if word == '':
                    continue
                else:
                    word = word.strip(''',.!?'"<>''')   # 去除标点
                    if word in Person_Word_Number[script[0]].keys():
                        Person_Word_Number[script[0]][word] += 1
                    else:
                        Person_Word_Number[script[0]][word] = 1


def StatisticsLine(content):
    # 1 统计每个人的台词量
    ScriptNumber(content)
    # 2 统计每个人用词的词频
    WordFrequency(content)


def StatisticsFile(FilePath):
    # 用 with open() 函数打开文件，字符编码：utf-8
    with open(FilePath, 'r', encoding='utf-8') as f:
        # 读取文件中的内容
        content = f.read()
        # 将所有标点转化为英文标点
        content = FormatPunctuation(content)
        # 去除内容中的空白行
        content = content.split('\n')
        content = DeleteEmptyLine(content)
        # 统计台词内容，其中第一行为该集的标题（若直接是台词内容，则无需切片）
        StatisticsLine(content[1:])


def Update_Words(name, person):
    # 更新同人异名的词频库
    global Person_Word_Number
    for word in Person_Word_Number[person]:
        if word in Person_Word_Number[name].keys():
            Person_Word_Number[name][word] += Person_Word_Number[person][word]
        else:
            Person_Word_Number[name][word] = Person_Word_Number[person][word]


def Update_Name(NameList):
    # 更新同人异名
    global Person_ScriptNumber
    DelNameList = []
    # 更新台词字典
    for person in Person_ScriptNumber.keys():
        for names in NameList:
            if person in names and person != names[0]:
                Person_ScriptNumber[names[0]] += Person_ScriptNumber[person]
                # 更新词频库
                Update_Words(names[0], person)
                DelNameList.append(person)
                break
    # 删除其他名字
    for name in DelNameList:
        del Person_ScriptNumber[name]
        del Person_Word_Number[name]
    # 对两个字典进行排序
    Person_ScriptNumber = dict(sorted(Person_ScriptNumber.items(), key=lambda x: x[1], reverse=True))
    for key in Person_Word_Number.keys():
        Person_Word_Number[key] = dict(sorted(Person_Word_Number[key].items(), key=lambda x: x[1], reverse=True))


def RepeatedName():
    # 去除同名异人问题(根据不同剧本自行修改)
    # 名字表：列表中的每个元组代表一个角色
    #        每个元组中的元素代表该角色的不同名字，其中第一个作为最终保留下来的名字
    NameList = [('SHERLOCK', 'SHERLOCK HOLMES', 'HOLMES', "SHERLOCK's VOICE", "YOUNG SHERLOCK's VOICE"),
                ('JOHN', 'JOHN WATSON', 'WATSON', "JOHN's VOICE"),
                ('MORIARTY', 'JIM MORIARTY', 'JIM', 'M', "JIM's VOICE", "MORIARTY's VOICE"),
                ('MYCROFT', 'MYCROFT HOLMES', "MYCROFT's VOICE", 'M/MYCROFT'),
                ('MRS HUDSON', 'HUDSON'), ('MOLLY', 'MOLLY COPPER'),
                ('MARY', 'MARY MORSTAN', 'MORSTAN', 'MRS WATSON'),
                ('IRENE', 'IRENE ADLER', 'ADLER'),
                ('EURUS', 'EURUS HOLMES', "EURUS's VOICE", "ADULT EURUS")]
    # 更新字典中的姓名
    Update_Name(NameList)


def Number():
    # 统计角色在剧中的单词总数
    global Person_WordsNumber, Person_ScriptNumber
    for person in Person_Word_Number.keys():
        Person_WordsNumber[person] = 0
        for word in Person_Word_Number[person].keys():
            Person_WordsNumber[person] += Person_Word_Number[person][word]
    # 对字典进行排序
    Person_WordsNumber = dict(sorted(Person_WordsNumber.items(), key=lambda x: x[1], reverse=True))


def Delete():
    # 删除无效数据：键对应的值为 0 或 空
    global Person_ScriptNumber, Person_Word_Number, Person_WordsNumber
    a = list(Person_ScriptNumber.keys())
    b = list(Person_Word_Number.keys())
    c = list(Person_WordsNumber.keys())
    aa, bb, cc = [], [], []
    for i in range(-1, -len(a), -1):
        if Person_ScriptNumber[a[i]] != 0:
            break
        aa.append(a[i])
    for i in range(-1, -len(b), -1):
        if Person_Word_Number[b[i]] == {}:
            bb.append(b[i])
    for i in range(-1, -len(c), -1):
        if Person_WordsNumber[c[i]] != 0:
            break
        cc.append(c[i])
    for d in aa:
        del Person_ScriptNumber[d]
    for d in bb:
        del Person_Word_Number[d]
    for d in cc:
        del Person_WordsNumber[d]


def SumUp():
    # 统计总角色数，总台词量
    global PersonNumber, ScriptNumber, Person_ScriptNumber
    PersonNumber = len(Person_ScriptNumber.keys())
    ScriptNumber = eval('+'.join(map(str, Person_ScriptNumber.values())))


def CreateDataFiles():
    # 生成数据文件(在 code 同目录下的 data 文件夹中)：
    #       TotalStatistics.csv
    #       person 文件夹（其中包括各个角色对应的每个单词的词频）
    global Person_ScriptNumber, Person_Word_Number, Person_WordsNumber, DataPath, ScriptNumber
    # 生成 TotalStatistics.csv
    file1 = DataPath + 'TotalStatistics.csv'
    with open(file1, 'w', encoding='utf-8') as f1:
        f1.write("{0},{1},{2},{3}\n".format('Character', 'the Number of Scripts', 'the Percentage of Scripts(%)', 'the Number of Words'))
        for person in Person_ScriptNumber.keys():
            try:
                f1.write("{0},{1},{2:.2f},{3}\n".format(person, Person_ScriptNumber[person],
                                                        Person_ScriptNumber[person]/ScriptNumber*100,
                                                        Person_WordsNumber[person]))
            except KeyError:
                continue
    # 生成 person 文件夹
    path = DataPath + 'person\\'
    os.makedirs(path)
    for name in Person_Word_Number.keys():
        filename = path + name.lower() + '.csv'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("{0},{1}\n".format('Word', 'Number'))
                for word in Person_Word_Number[name].keys():
                    f.write('{0},{1}\n'.format(word, Person_Word_Number[name][word]))
        except FileNotFoundError:
            continue


def Statistics():
    global FilePathList, PersonNumber, ScriptNumber, DataPath, ScriptPath
    # 获得数据集的文件名列表
    FilePathList = GetFileList()
    for path in FilePathList:
        # 统计数据
        StatisticsFile(path)
    # 检查同人异名
    RepeatedName()
    # 统计每个人台词的单词总数
    Number()
    # 去除无效数据
    Delete()
    # 统计总数
    SumUp()
    # 生成数据文件
    CreateDataFiles()
    return DataPath, ScriptPath, ScriptNumber
