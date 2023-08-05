**注意：尚未完成迁移**

# 史学家
《群星》模组，在游戏中自动记录数据，并将其编纂为 HTML 格式的史书。

_五帝三皇神圣事，骗了无涯过客。_

## 当前内容
+ 基本信息

   国家名称，政府名称，政府个性，主流思潮，起源，母星名称，母星类别，母星系名称，创始物种
+ 经济史

  各类资源的储量及月收入
+ 人口史
  
  各物种人口数量
+ 科技史

  研究点数月收入
+ 外交史
  
  我国与其它国家的关系及相互评价

## 未来计划
+ 外交史
  
  我国与其它国家的外交操作与事件
+ 科技史
  
  获得科技的名称、描述及获得时间。
+ 军事史
  - 战争细节
  - 海军、陆军组织
+ 富语义地图
+ 其它
  - 星球地方志
  - 领袖传记
  - 各事件（局势，异常现象，考古等等）的描述

## 已知问题
再次进入游戏时，日期可能会早于上次退出的日期，因此同一日期的数据可能被记录多次。重复的数据将会据某一主码被去除（通常是日期）。对于物种人口数量，由于可能多个物种名称相同，主码必须为 `(日期，物种名称，物种数量)`。这将造成一些问题。例如，如果两个名称相同的物种在同一天数量也相同，那么这两条记录会被视为属于同一物种，从而其中的一条记录将被错误地去除；此外，如果在两次游戏的同一天，一个物种的数量不同，那么这两条记录会被视为属于两个物种，从而被错误地同时保留。


## 环境要求
Python 3
  - jinja2
  - pyecharts
  - pandas

<!-- 如有问题，请参考[使用指南](史学家模组使用指南.md)。 -->
  
## 使用
正确使用本模组需要运行两个 Python 脚本（运行方法稍后详细说明）：
+ **每次退出游戏后，运行 `src` 文件夹中的 `extract_history.py`**，这会从游戏日志中提取数据并写入结构化的数据文件；
+ **想要生成史书时，运行 `src` 文件夹中的 `compile_history.py`**，这会从 `extract_history.py` 生成的数据文件中读取数据并编译出 HTML 文档。
  
生成的数据文件和 HTML 文档会被保存到本文件夹下的一个单独的文件夹中，该文件夹的名称作为一个参数需要在运行脚本的时候指定（若不指定则为默认值 `MemoryGrain`）。因此，**玩家的每个国家须对应一个独有的文件夹**，即，**对于一个国家，假设希望将其相关文件保存在名为 `地球联合国` 的文件夹中，则第一次运行 `extract_history.py` 前，应保证本文件夹下没有名为 `地球联合国` 的文件夹；每次为该国家运行脚本时，该参数都应为 `地球联合国`**。文件夹 `地球联合国` 将会在第一次运行 `extract_history.py` 时被自动创建。

以下介绍运行脚本的方法。
#### 运行 `extract_history.py`
在本文件夹下的终端运行命令
```sh
python ./src/extract_history.py -o '地球联合国'
```
生成的数据文件将被存储到 `./地球联合国/data`。
#### 运行 `compile_history.py`
在本文件夹下的终端运行命令
```sh
python ./src/compile_history.py -o '地球联合国'
```
生成的史书将被存储到 `./地球联合国/output`。

**注意：如果玩家某次退出游戏后没有运行 `extract_history.py`，那么其信息会在玩家再次进入游戏时 _丢失_，因为每次进入游戏后游戏日志都会被覆盖。**

## 贡献方式
欢迎对模组创作的任何贡献，包括代码（Stellaris modding API 或 Python）编写、对史书内容或排版的设计等。如有兴趣可以提出 issue，发送邮件至 `zhukaiwensq@outlook.com` 或在 QQ 上联系 3387572450。
