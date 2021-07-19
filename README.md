# B.N.P
Schrödinger’s Bank Note Printer
`薛定谔式印钞机`  在特定的二级市场行情下，以运气为原材料，输出💴💴💴RMB!

## 项目简介
本项目是作者在2020年下半年业余时间开发的量化交易试验程序。还有很多不完善的地方。偶尔还会更新。
您可以在此代码基础上任意修改，作为个人使用。如再次公开请附带上LICENSE文件，包含原作者信息。
作者对A股二级市场的熟悉程度还不够(其实完全不懂)，如有大神看到，还请多多指导！
合作开发联系: z_nolan@126.com
有意思的工作也可以推荐，反内卷，反996, F**K THE CAPITALISM!

## 安装指南
#### 0. 完善config配置

#### 1. pip install -r requirements.txt

#### 2. TA-Lib安装
参考 [官方文档](https://mrjbq7.github.io/ta-lib/install.html)

#### 3. 链接到site-packages
python -m site 查看site-packages路径
创建软链接，示例
ln -s /path/to/bnp_v0.1 /path/to/site-packages/bnp

## 代码说明
algo目录下的test文件可用于测试算法。
scripts下的脚本可直接用于crontab配置定时执行。
添加订阅用户：修改bnp_v0.1/settings/SUBSCRIBER文件，每行一个，邮箱+空格+用户名备注

## 客户端
可在终端执行，用于********
安装方法：
pip install alpha_stock
试用Token: 60f583d6069b92789ffd2691  (有效期至2021.10.16，你不买也可以直接问我要，反正也没啥用！)

使用方法示例：
stock --help    # 查看帮助
stock recommend --help  # 查看参数的帮助
stock recommend -a 8    # 算法8今日的推荐
stock expectation   # 前几日的模拟收益
stock statistic -d 10   # 10日内股票的推荐次数统计
天黑之后才能用，不然没数据。更多参数请自行探索~


LET'S MAKE MORE MONEY!
