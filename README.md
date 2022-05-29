# visualization
互联网行业分析，数据源于前程无忧招聘网站，数据分析基于Hadoop+Spark平台，数据大屏基于Echarts

### 数据源
基于多线程爬取。各个城市的精度data/BaiduMap_cityCenter.txt来源于百度地图开放平台，crawler/cityInfo.py含爬取前程无忧各个城市的编号，爬取的岗位关键字在data/job.csv，爬取代码crawler/qcwy.py，结果为/data/data.csv

### 数据分析
数据分析是基于spark平台，数据储存在hdfs上，开发环境是Jupyter,由于我的分布式平台是在虚拟机搭建的，所以本项目的各个模块（爬虫、数据分析、数据大屏）是分离的，将/data/data.csv上传至hdfs，分析代码位于/visual.ipynb，分析结果保存为json文件，将分析结果文件保存至data/。

### 数据大屏
因为数据均保存为静态数据，因此可以忽略数据爬取和数据分析这一部分代码，直接打开visual/index.html

### [预览](https://zyoungbright.github.io/visualization/visual/index.html)
