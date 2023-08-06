
pydatawork功能建议收集表：
https://docs.qq.com/form/page/DZVNabWlkRUtldWtJ



pydatawork content summary：Mon Jul 3 21:52:47 CST 2023
- basic functions
- data processing
- data analysis



# pydatawork测试环境：python 3.7.2

pydatawork中所用到的库：

```python
import os
import shutil
import re
import datetime
import random
import time
import math
import json
import requests # 需要单独安装
import urllib.request
```

requests非python自带的库，需要单独安装，否则无法正常运行pydatawork：

```shell
pip install requests 
或 
pip3 install requests
```



# Basic Functions

## rename_by_re() 通过正则表达式匹配实现文件重命名或批量重命名——先匹配，再用关键词替换匹配部分 （v 0.17.5.3）

###### Sat Jul 8 21:29:29 CST 2023

```python
def rename_by_re(path: str, pattern: str, keyword: str):
    """
    功能：按正则表达式匹配进行文件重命名或批量重命名。（先通过正则表达式匹配要替换的部分，再进行关键词替换。注意：pattern参数也可当普通参数使用，用于匹配一个具体的词。）

    参数：

    path：一个路径，可以是文件路径或文件夹路径(文件夹中的子文件夹不处理)。

    pattern：正则表达式匹配模式。如可用pattern = "[\u4e00-\u9fa5]+"匹配文件名中的全部中文字符；可用pattern = "呼呼"匹配文件名中的“呼呼”这两个具体的字符。

    keyword：用于替换的关键词。
    """
```

使用示例1：匹配某一类全部字符串。（将 呼呼hhh-积极一回81871.jpg 中的中文替换成zzz。）

```python
import pydatawork as dw

path = r"/home/jkzhou/Desktop/pydatawork/test_data/rename_by_re"
pattern = "[\u4e00-\u9fa5]+" # 匹配文件名中的全部中文字符
keyword = "zzz"

dw.rename_by_re(path,pattern,keyword)
```

输出结果：
```text
renaming: 呼呼hhh-积极一回81871.jpg to zzzhhh-zzz81871.jpg
```


使用示例2：匹配某个具体字符串。（将 呼呼hhh-积极一回81871.jpg 中的“呼呼”替换成zzz。）

```python
import pydatawork as dw

path = r"/home/jkzhou/Desktop/pydatawork/test_data/rename_by_re"
pattern = "呼呼" # 精准匹配关键词“呼呼”
keyword = "zzz"

dw.rename_by_re(path,pattern,keyword)
```

输出结果：
```text
renaming: 呼呼hhh-积极一回81871.jpg to zzzhhh-积极一回81871.jpg
```



## rename_by_insert_keyword() 在文件名的指定位置插入关键词（默认为当前时间戳），实现重命名或批量重命名 (v 0.17.4.4)

###### Fri Jul 7 16:06:42 CST 2023

```python
def rename_by_insert_keyword(path, index:int=-1,keyword:str=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
    """
    功能：在文件名的指定位置插入关键词，进行文件重命名或批量重命名。需要给定一个路径（文件或文件夹），给定一个位置索引（从0开始），给定一个关键词（字符串），程序会对其中的文件（忽略子文件夹）进行重命名或批量重命名，命名方式为：把keyword添加到原文件名的指定位置。index和keyword有默认值，默认在文件名的后缀插入当前时间戳。

    参数：

    path：一个路径（文件或文件夹）。

    index：一个位置索引（从0开始。前缀位置索引为0，后缀位置索引为-1）。默认为-1。
    
    keyword：一个关键词（字符串）。默认为当前时间戳(格式为：2023-07-07_18-17-13)。
    """
```



## file_split() 文件分割：按指定数量对文件夹中的文件进行拆分 （v 0.17.3.0）

###### Mon Jul 3 21:21:23 CST 2023

```python
def file_split():
    """
    功能：对文件夹中的文件按指定数量进行拆分。（会忽略文件夹，只处理文件）。如，文件夹中有1000张图片，可将其拆分为10个小文件夹，每个文件夹100张图片，文件夹编号为1-10。

    参数：无需提前输入参数，执行后，根据终端中的提示进行输入。

    path = input("请输入原始文件路径:")  # 输入待分割的原始文件所在路径。

    folderPath = input("请输入要输出的路径:")  # 输入分割后的结果存放路径。

    number = int(input("请输入每个文件夹中文件数:"))  # 每个文件夹中的文件数。
    """
```



## move_files_by_keyword() 按文件名中关键词移动文件，灵活提取文件 (v 0.17.1.2)

###### Sun Jul 2 24:35:12 CST 2023

```python
def move_files_by_keyword(raw_data_path,working_path):
    """
    功能：根据文件名中的关键词移动文件。

    参数：

    raw_data_path：原始数据所在路径。（不会移动子文件夹，也不会遍历子文件夹）。

    working_path：工作路径，提取出来的文件将存放到该路径。

    keyword（不是参数）：指文件名中包含的关键词，不是参数，程序运行后，在命令行中根据提示按需输入。
    """
```



## copy_files_by_keyword() 按文件名中关键词复制文件，灵活提取文件 (v 0.17.1.2)

###### Sun Jul 2 24:28:40 CST 2023

```python
def copy_files_by_keyword(raw_data_path,working_path):
    """
    功能：根据文件名中的关键词复制文件。

    参数：

    raw_data_path：原始数据所在路径。（不会复制子文件夹，也不会遍历子文件夹）。
    
    working_path：工作路径，提取出来的文件将存放到该路径。

    keyword（不是参数）：指文件名中包含的关键词，不是参数，程序运行后，在命令行中根据提示按需输入。
    """
```

使用示例：

```python
import pydatawork as dw

raw_data_path = r"/home/test_data/copy_files_by_keyword/data"
working_path = r"/home/test_data/copy_files_by_keyword/working"

dw.copy_files_by_keyword(raw_data_path,working_path)
```

输出结果：
```text
请输入要复制的文件包含的关键词:
11
找到名称中包括 11 的文件
copying: 111.zip to /home/test_data/copy_files_by_keyword/working/11
名称中包括 11 的文件已提取（复制）完毕
```



## get_current_folder_name() 给定一个路径，返回当前文件夹名 (v 0.1.26)

###### Mon Jun 26 24:23:48 CST 2023
```python
def get_current_folder_name(path):
    """
    功能：输入一个路径，返回当前文件夹名。

    参数：

    path：一个路径，可以是文件夹路径，也可以是文件路径。
    """
```



## get_file_name() 给定一个路径，返回文件名  (v 0.1.32)

###### Mon Jun 26 24:24:45 CST 2023
```python
def get_file_name(path):
    """
    功能：输入一个路径，返回文件名。（当path为文件夹路径，返回的值为空值。）

    参数：

    path：一个路径，可以是文件夹路径，也可以是文件路径。
    """
```



## copy_files() 复制当前文件夹中（不包括子文件夹）指定类型的文件 （v 0.1.23） 

###### Sun Jun 25 06:19:50 CST 2023

```python
def copy_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹中(不包括子文件夹)指定类型的文件复制到目标文件夹。

    参数：

    folder_path：待整理文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """
```



## move_files() 移动当前文件夹中（不包括子文件夹）指定类型的文件 （v 0.1.23） 

###### Sun Jun 25 06:17:26 CST 2023

```python
def move_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹中（不包括子文件夹)指定类型的文件移动到目标文件夹。

    参数：

    folder_path：待整理文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """
```



## copy_all_files() 复制文件夹及子文件夹下指定类型的全部文件 （v 0.1.22）

###### Sun Jun 25 06:05:29 CST 2023

```python
def copy_all_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹及其子文件夹中指定类型的全部文件复制到目标文件夹。

    参数：

    folder_path：待整理文件夹，可包含多层级子文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """
```



## move_all_files() 移动文件夹及子文件夹下指定类型的全部文件 （v 0.1.22）

###### Sun Jun 25 05:01:22 CST 2023

```python
def move_all_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹及其子文件夹中指定类型的全部文件移动到目标文件夹。

    参数：

    folder_path：待整理文件夹，可包含多层级子文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """
```

示例：
```Python
import pydatawork as dw 

folder_path = "/home/jkzhou/Desktop/pydatawork/test_data/move_all_files/folder_path"
target_folder = "/home/jkzhou/Desktop/pydatawork/test_data/move_all_files/target_folder"
file_type_list = [".jpg",".zip",".png",".gz",".whl",".md"]

dw.move_all_files(folder_path,target_folder,file_type_list)
```



## rename_folder_numeric_serialize() 文件夹从左到右比较，按数值从小到大排序，再从1开始进行序列化重命名（v 0.1.6）

###### Sun Jun 18 22:37:01 CST 2023

```python
def rename_folder_numeric_serialize(path):
    """
    功能：给定一个文件夹路径，获取其中子文件夹的名字，根据子文件夹的名字，从左到右进行比较，按数值从小到大对子文件夹排序，再从1开始对子文件夹进行序列化重命名。

    参数：

    path：文件夹路径。
    """
```



# Data Processing

## obsidian_bookmarks_merge_and_deduplicate() obsidian中surfing插件产生的书签整理：先合并，再去重 （v 0.1.31）

###### Mon Jun 26 22:50:45 CST 2023

```python
def obsidian_bookmarks_merge_and_deduplicate(original_bookmarks_path,result_path):
    """
    功能：用于处理surfing插件产生的bookmarks。先合并多个bookmarks（只有1个也能正常使用），再对合并后的bookmarks去重，最后得到一个最全、不重复的bookmarks。

    参数：

    original_bookmarks_path：一个路径，路径下存放bookmarks文件，json格式，可以是1个或多个json文件。

    result_path：一个路径，用于存放最终结果。
    """
```



## obsidian_move_md_or_canvas_linked_images() 提取obsidian中.md文档、.canvas文档中链接的图片，实现附件管理、库空间管理、笔记归档 (v 0.1.24)

###### Sat Jun 24 18:37:16 CST 2023

```python
def obsidian_move_md_or_canvas_linked_images(images_path,folder_path,target_folder):
    """
    功能：指定相关路径，提取obsidian中.md文档、.canvas文档中链接的图片，实现附件管理、库空间管理、笔记归档。

    参数：

    images_path：图片附件所在的文件夹。通常是笔记库的附件文件夹。

    folder_path：待整理的md、canvas文档所在文件夹（可包括多层级子文件夹，会遍历）。通常临时建立一个文件夹,将待整理的笔记存进去。

    target_folder：提前准备的文件夹，可以建在任意位置，用于存放提取出来的图片。
    """
```

示例及说明：在自己的代码中提前准备好三个路径，然后调用函数

```python
import pydatawork as dw 

images_path = "/home/jkzhou/Desktop/手机笔记同步-附件"
folder_path = "/home/jkzhou/Desktop/file"
target_folder = "/home/jkzhou/Desktop/file/附件"

dw.obsidian_move_md_or_canvas_linked_images(images_path,folder_path,target_folder)
```



## get_weibo() 微博图片获取（v 0.1.2）

###### Sun Jun 18 17:10:46 CST 2023

```python
def get_weibo(path,id,weibo_name):
    """
    功能：获取某个微博的全部图片及正文。

    参数：

    path: 内容存放路径。

    id: 微博id。（id获取方法：以梅西的微博id为例。在网页版微博上找到梅西的微博，查看链接，链接为 https://weibo.com/u/5934019851 ，链接中u后面的数字即为id ,梅西微博的id为 5934019851。）

    weibo_name: 内容存放路径下一个自定义的文件夹名。
    """
```

示例：获取梅西的微博id，获取其微博内容

```python
import pydatawork as dw 

path="/home/Desktop/pydatawork"
id="5934019851" # 梅西的微博id。在网页版微博上找到梅西的微博，查看链接，链接为 https://weibo.com/u/5934019851 ，链接中u后面的数字即为id ,梅西微博的id为 5934019851。
weibo_name="mx"

dw.get_weibo(path,id,weibo_name)
```

来源：非原创
原作者：XYJISAW
参考链接：https://www.omegaxyz.com/2018/02/13/python_weibo/




# Data Analysis

## game_number_guessing() 猜数字游戏：自定义数字的范围，输入自己猜的数字，并根据计算机的提示调整，直至猜对 （v 0.1.37）

###### Sat Jul 1 01:42:58 CST 2023

```python
def game_number_guessing(number=100):
    """
    游戏规则：指定一个整数，确定数字的范围；根据提示猜数字，直到猜中。

    参数：

    number：大于1的整数，默认为100，指要猜的数字在100以内。

    用法1：若不设定参数，可以写成 game_number_guessing() ，这时默认值为100。

    用法2：自定义参数，可以写成 game_number_guessing(number=200)，这时，数字范围设定为在200以内。
    """
```

使用示例1：

```python
import pydatawork as dw

dw.game_number_guessing(number=200) # 将数字范围调整成200
```

使用示例2：

```python
import pydatawork as dw

dw.game_number_guessing() # 使用默认值100
```



## get_BMI() 输入身高（m）、体重(kg)，进行身体质量指数（BMI）测量，了解当前身体健康状态，获得体重管理建议 （V 0.1.36）

###### Fri Jun 30 19:50:03 CST 2023

```python
def get_BMI(height,weight):
    """
    功能：用于BMI测量。BMI（身体质量指数）是一种计算一个人体重是否健康的方法，基于身高和体重的比例来计算。如果 bmi 小于 18.5，说明体重过轻；如果 bmi 在 18.5 和 24.9 之间说明体重在正常范围；如果 bmi 在 24.9 和 29.9 之间说明体重过重；如果大于 29.9 说明肥胖。

    参数：

    height：身高（m）（注意，单位为米）。

    weight：体重（kg）（注意，单位为千克）。
    """
```

使用示例1：

```python
import pydatawork as dw

dw.get_BMI(height=1.75,weight=73) # 调用函数，通过关键词参数输入值
```

使用示例2:

```python
import pydatawork as dw

height = float(1.75)
weight = float(73)

dw.get_BMI(height,weight)
```

测量结果示例：
```text
本次BMI测量时间：2023.06.30 20:20:34
身高： 1.75 m
体重： 73.0 kg
BMI(身体质量指数)：23.84
当前BMI健康状态评价：体重在正常范围
正常体重范围：建议体重保持在 56.66 kg 至 76.26 kg 之间
(注意：男女有别，请结合自身实际情况判断自己的体重状态)
```



# about pydatawork

## hello_jkzhou() 获得帮助（v 0.1.7）

###### Sun Jun 18 23:34:45 CST 2023

```python
def hello_jkzhou():
    """
    获取pydatawork的使用教程。
    """
```


## pypi维护指令

```shell
cd 到pydatawork文件夹
python3 setup.py sdist bdist_wheel # 打包
twine check dist/* # 检查
twine upload dist/* # 上传，需要输入帐号密码

```



## 查看pydatawork是否有更新

```shell
pip3 list --outdated
```



## pydatawork升级方法（先卸载，再安装）

```shell
# 卸载指令
pip3 uninstall pydatawork 
或 
pip uninstall pydatawork 

# 安装指令
pip3 install pydatawork 
或 
pip install pydatawork 
```



## pydatawork 导入方式
```shell
import pydatawork # 标准导入方式
import pydatawork as dw # 推荐使用此方式，更简洁
```



## pydatawork安装
```shell
# 安装指令
pip3 install pydatawork 
或 
pip install pydatawork
```



## 关于pydatawork

数据工作相关的分享、梳理，主要目的是辅助个人开展数据处理、数据分析工作。

推荐始终使用最新版。

要升级使用最新的安装包，比较稳定可靠的一种方式是，先卸载旧的，再重装。

发布时间：Thu Jun 15 13:23:43 CST 2023
