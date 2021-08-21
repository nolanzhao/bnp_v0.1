# B.N.P
一个简单的量化交易试验代码


## 项目说明
您可以在此代码基础上任意修改，作为个人使用。如再次公开请附带上LICENSE文件，包含原作者信息。


## 安装指南
#### 0. 完善config配置

#### 1. 安装Python依赖库
```bash
pip install -r requirements.txt
```

#### 2. TA-Lib安装
参考 [官方文档](https://mrjbq7.github.io/ta-lib/install.html)

#### 3. 链接到site-packages
```bash
python -m site  # 查看site-packages路径
```

创建软链接，示例
```bash
ln -s /path/to/bnp_v0.1 /path/to/site-packages/bnp
```


## 代码说明
algo目录下的test文件可用于测试算法。

scripts下的脚本可直接用于crontab配置定时执行。

添加订阅用户：修改bnp_v0.1/settings/SUBSCRIBER文件，每行一个，邮箱+空格+用户名备注


## 客户端
可在终端执行，用于********

#### 安装方法：
```bash
pip install alpha_stock
```
试用Token: 60f583d6069b92789ffd2691  (有效期至2021.10.16)

#### 使用方法示例：
```bash
stock --help    # 查看帮助
stock recommend --help  # 查看参数的帮助
stock recommend -a 8    # 算法8今日的推荐
stock expectation   # 前几日的模拟收益
stock statistic -d 10   # 10日内股票的推荐次数统计
```
更多参数请自行探索~


LET'S MAKE MORE MONEY!
