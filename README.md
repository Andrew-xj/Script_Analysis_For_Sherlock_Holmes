
程序说明
============================================================
  
# 功能描述  
本程序实现的是一个简易版本的台词分析程序，对数据源进行台词量和
词频统计，最后输出对比图像以及剧本词云。  
  
# 开发环境  

## 程序语言  
Python 3.5+  
  
## 第三方库  
pandas		0.24.0    
numpy		1.16.1  
matplotlib	3.0.2  
wordcloud	1.5.0  
pip 命令安装即可  
  
# 项目结构简介  

## 流程图  
![analysis.py](https://github.com/Andrew-xj/Script_Analysis_For_Sherlock_Holmes/tree/master/image/analysis.py)  
![statistics.py](https://github.com/Andrew-xj/Script_Analysis_For_Sherlock_Holmes/tree/master/image/statistics.py)  
  
## 模块目录  
..\code\analysis.py  
..\code\statistics.py  
  
## 修改参数
替换“..\script\”目录下的台词数据集  
analysis.py 中对分析结果的限定，根据注释自行修改  
  
# 测试DEMO  
直接运行analysis.py文件即可，有现成测试。
