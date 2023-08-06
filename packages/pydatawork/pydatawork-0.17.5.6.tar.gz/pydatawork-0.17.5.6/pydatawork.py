
# -*- coding: utf-8 -*-

import os
import shutil
import re
import datetime
import random
import time
import math
import json
import requests # 新电脑刚装上python时，不带这个库，需要自己安装
import urllib.request



# others

# def break_words(stuff):
#     """This function will break up words for us."""
#     words = stuff.split(' ')
#     return words

# def sort_words(words):
#     """Sorts the words.""" # 文档字符串，是注释的一种
#     return sorted(words)

# def print_first_word(words):
#     """Prints the first word after popping it off."""
#     word = words.pop(0)
#     print(word)

# def print_last_word(words):
#     """Print the last word after popping it off."""
#     word = words.pop(-1)
#     print(word)

# def sort_sentence(sentence):
#     """Takes in a full sentence and returns the sorted words"""
#     words = break_words(sentence)
#     return sort_words(words)  # 没懂这个函数

# def print_first_and_last(sentence):
#     """Prints the first and last words of the sentence."""
#     words = break_words(sentence)
#     print_first_word(words)
#     print_last_word(words)

# def print_first_and_last_sorted(sentence):
#     """Sorts the words then prints the first and last one."""
#     words = sort_sentence(sentence)
#     print_first_word(words)
#     print_last_word(words)


# 维护

# 折叠：ctrl + k , ctrl + 1
# 展开：ctrl + k , ctrl + j


# get help
# def hello_jkzhou():
#     """
#     功能：获取pydatawork的使用帮助。
#     """
#     print("\nHi, 感谢你使用pydatawork～")    
#     print("\n1.pydatawork的官方文档中提供了函数说明和一些示例，或许对你有用。\npydatawork官方文档：https://pypi.org/project/pydatawork/")
#     print("\n2.如果你有好的想法或建议，欢迎给我反馈。\n我的邮箱是: zhouqiling.bjfu@foxmail.com")
#     print("\n3.也可以描述你的需求，给pydatawork提出功能建议。\npydatawork功能建议收集表：https://docs.qq.com/form/page/DZVNabWlkRUtldWtJ")
#     print("\n")


def hello_jkzhou(): # 为什么要定义主函数？ @知识卡片
    # 先定义需要用到的函数
    def menu():
        print("\n==pydatawork官方文档==")
        # print("------------------------功能菜单------------------------------------")
        # print("\t\t1.basic functions")
        # print("\t\t2.data processing")
        # print("\t\t3.data analysis")
        # print("\t\t4.查找")
        # print("\t\t5.工作台")
        # print("\t\t6.知识库")
        # print("\t\t7.数据库")
        # print("\t\t8.联系与帮助")
        # print("\t\t0.退出")
        # print("1.basic functions", end="")
        # print("\t2.data processing", end="")
        # print("\t3.data analysis")
        # print("4.查找", end="")
        # print("\t5.工作台", end="")
        # print("\t6.知识库", end="")
        # print("\t7.数据库", end="")
        # print("\t8.联系与帮助")
        # print("0.退出")
        # print("--------------------")
        print("1.basic functions")
        print("2.data processing")
        print("3.data analysis")
        print("4.查找")
        print("5.工作台")
        print("6.知识库")
        print("7.数据库")
        print("8.联系与帮助")
        print("0.退出")
        print("----------------------")

    def basic_functions():
        while True:
            print("basic functions:")
            print("file_split")
            print("get_current_folder_name")
            print("get_file_name")
            print("copy_files")
            print("copy_all_files")
            print("copy_files_by_keyword")
            print("move_files")
            print("move_all_files")
            print("move_files_by_keyword")
            print("rename_by_re") 
            print("rename_by_insert_keyword()")
            print("renamer_folder_numeric_serialize")
            print("\n")

            answer = input("输入 n/N 退出，按 回车 继续...") # @知识卡片 输入时没有指定input的值的类型，所以，当输入的值为空值时，不会报错。如果指定了int，输入空值就会直接报错，无法进入下一步判断。
            if answer == "n" or answer == "N": # 仅当输入n/N直接退出。要继续，直接回车就行
                exit()
            else:
                break # @知识卡片 在这里要继续使用，本质上就是退出当前的循环，所以，直接break

    def data_processing():
        while True:
            print("data processing:")
            print("obsidian_move_md_or_canvas_linked_images")
            print("obsidian_bookmarks_merge_and_deduplicate")
            print("get_weibo")
            print("\n")

            answer = input("输入 n/N 退出，按 回车 继续...") # @知识卡片 输入时没有指定input的值的类型，所以，当输入的值为空值时，不会报错。如果指定了int，输入空值就会直接报错，无法进入下一步判断。
            if answer == "n" or answer == "N": # 仅当输入n/N直接退出。要继续，直接回车就行
                exit()
            else:
                break # @知识卡片 在这里要继续使用，本质上就是退出当前的循环，所以，直接break


    def data_analysis():
        while True:
            print("data analysis:")
            print("game_number_guessing")
            print("get_BMI")
            print("\n")

            answer = input("输入 n/N 退出，按 回车 继续...") # @知识卡片 输入时没有指定input的值的类型，所以，当输入的值为空值时，不会报错。如果指定了int，输入空值就会直接报错，无法进入下一步判断。
            if answer == "n" or answer == "N": # 仅当输入n/N直接退出。要继续，直接回车就行
                exit()
            else:
                break # @知识卡片 在这里要继续使用，本质上就是退出当前的循环，所以，直接break


    def search():
        pass

    def workspaces():
        pass

    def wiki():
        pass

    def database():
        pass

    def get_help():
        print("\nHi, 感谢你使用pydatawork，下面的信息可能对你有用，试试看：")    
        print("1.pydatawork的官方文档中提供了函数说明和一些示例。\npydatawork官方文档：https://pypi.org/project/pydatawork/")
        print("2.如果你有好的想法或建议，欢迎给我反馈。\n我的邮箱是: zhouqiling.bjfu@foxmail.com")
        print("3.也可以描述你的需求，给pydatawork提出功能建议。\npydatawork功能建议收集表：https://docs.qq.com/form/page/DZVNabWlkRUtldWtJ")
        # print("\n")

    while True: # 为什么选择使用while循环。布尔值和while循环用在一起，通常为了实现什么目的。每个对象都有一个布尔值。 @知识卡片
        menu()
        try:
            choice = int(input("请选择：")) 
            if choice in [0,1,2,3,4,5,6,7,8]: # @知识卡片 注意，这里需要提前指定输入数值的范围，别忘了
                if choice == 0:
                    answer=input("确认要退出吗？(y/n)") # 括号里面是提示信息
                    if answer == "y" or answer == "Y": # 兼顾大小写。不能写成"y" or "Y"，这是错误的写法
                        print("谢谢使用！")
                        break # 退出系统。退出循环。
                    else:
                        continue
                elif choice == 1:
                    basic_functions() # 基本功能函数
                elif choice == 2:
                    data_processing() # 数据处理函数
                elif choice == 3:
                    data_analysis() # 数据分析函数
                elif choice == 4:
                    search() # 函数查询
                elif choice == 5:
                    workspaces() # 工作台
                elif choice == 6: 
                    wiki() # 知识库             
                elif choice == 7:
                    database() # 数据库
                elif choice == 8:
                    get_help() # 联系与帮助信息
            else:
                print("输入的数值超出范围...") # @知识卡片 注意与对应的模块对齐

        except ValueError:
            print("输入无效，请重新输入！") # 在选择界面直接回车时，弹出这条，然后重新选择——因为是在无限循环中，所以会直接重新回到 menu()函数，而不用在下方再写一个menu()
            # menu() # 此处不用再写，因为本身就在无限循环的函数中







# Basic Functions

# 重命名，正则，关键词替换，批量重命名
def rename_by_re(path: str, pattern: str, keyword: str):
    """
    功能：按正则表达式匹配进行文件重命名或批量重命名。（先通过正则表达式匹配要替换的部分，再进行关键词替换。注意：pattern参数也可当普通参数使用，用于匹配一个具体的词。））

    参数：

    path：一个路径，可以是文件路径或文件夹路径。

    pattern：正则表达式匹配模式。如可用pattern = "[\u4e00-\u9fa5]+"匹配文件名中的全部中文；可用pattern = "呼呼"匹配文件名中的“呼呼”这两个具体的字符。

    keyword：用于替换的关键词。
    """

    def rename_file(filepath,pattern,keyword):
        filename = os.path.basename(filepath)
        # 使用正则表达式进行替换
        new_filename = re.sub(pattern, keyword,filename)
        # 构建新文件的完整路径
        new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
        # 重命名文件
        os.rename(filepath, new_filepath)
        print(f"renaming: {filename} to {new_filename}")

    path = path
    pattern = pattern
    keyword = keyword
    
    if os.path.isfile(path):
        filepath = path
        rename_file(filepath,pattern,keyword)

    elif os.path.isdir(path):
        # 遍历目录下的所有文件
        for filename in os.listdir(path):
            # 构建文件的完整路径
            filepath = os.path.join(path, filename)
            # 判断是否为文件
            if os.path.isfile(filepath):
                rename_file(filepath,pattern,keyword)
            else:
                continue



# 重命名
def rename_by_insert_keyword(path, index:int=-1,keyword:str=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
    """
    功能：在文件名的指定位置插入关键词，进行文件重命名或批量重命名。需要给定一个路径（文件或文件夹），给定一个位置索引（从0开始），给定一个关键词（字符串），程序会对其中的文件（忽略子文件夹）进行重命名或批量重命名，命名方式为：把keyword添加到原文件名的指定位置。index和keyword有默认值，默认在文件名的后缀插入当前时间戳。

    参数：

    path：一个路径（文件或文件夹）。

    index：一个位置索引（从0开始。前缀位置索引为0，后缀位置索引为-1）。默认为-1。
    
    keyword：一个关键词（字符串）。默认为当前时间戳(格式为：2023-07-07_18-17-13)。
    """

    path = path
    index = index
    keyword = keyword

    # 检查输入参数的值是否正确——只需要验证“可设为默认值的参数的值”，以便提醒用户
    def default_value_prompt(path,index,keyword):
        # 判断path是否输入  （这里不做判断，系统也会自动判断。因为path在函数中是必须输入的参数，少了，会报错。）
        if path is None:
            print("请输入路径")
            return
        
        # 处理keyword和index参数的默认值
        # if keyword is None : # 因为，当keyword和index为默认值的时候，默认值也是个具体的值，这已经在函数定义中写具体了，所以，这里不能用None，因为肯定不是None。keyword如果没有专门输入，那keyword的值应为：keyword=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if keyword == datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") : 
            if index == -1:
                # keyword和index都使用默认值，将当前时刻的时间戳添加到文件名的后缀部分
                print("由于未提供keyword和index参数，默认将当前时刻的时间戳添加到文件名的后缀部分（keyword的默认值为当前时间戳，index的默认值为-1）")
            else:
                # keyword使用默认值，当前的时间戳
                print("由于未提供keyword参数，keyword默认已设置为当前时间戳")
        else:
            if index == -1:
                # index使用默认值，-1
                index = -1
                print("由于未提供index参数，index默认已设置为-1")

        # # 验证keyword参数类型是否正确   （参数的数据类型，已经在函数定义中指定，不需要在这里再次验证）


    def file_rename(path):
        # 单个文件重命名
        directory, filename = os.path.split(path)
        name, extension = os.path.splitext(filename)  # @知识卡片 filename是包含后缀的
        
        # 考虑原文件名本身的长度，与index对比，确保index的值在有效范围
        # 先考虑正向，同时考虑长度
        if int(index) >= 0: # 为正时
            if abs(index) < len(name): # 长度有效时继续
                # 区分正负，写法不一样
                if index == 0: # 前缀
                    new_name = keyword + "_" + filename  # @知识卡片 filename是包含后缀的
                    new_path = os.path.join(directory, new_name)
                    os.rename(path, new_path)
                    print(f"renaming: {filename} 为 {new_name}")

                elif int(index) > 0:
                    new_name = name[:index] + "_" + keyword + "_" + name[index:] + extension
                    new_path = os.path.join(directory, new_name)
                    os.rename(path, new_path)
                    print(f"renaming: {filename} 为 {new_name}")
            else:
                print("index的值超出范围")

        else: # 为负时
            if -abs(index) >= -len(name): # 长度有效时继续
                if index == -1: # 后缀
                    new_name = name + "_" + keyword + extension  # @知识卡片 filename是包含后缀的
                    new_path = os.path.join(directory, new_name)
                    os.rename(path, new_path)
                    print(f"renaming: {filename} 为 {new_name}")

                else:
                    new_name = name[:index+1] + "_" + keyword + "_" + name[index+1:] + extension
                    new_path = os.path.join(directory, new_name)
                    os.rename(path, new_path)
                    print(f"renaming: {filename} 为 {new_name}")
            else:
                print("index的值超出范围")


    # 参数验证    
    default_value_prompt(path, keyword, index)

    # 重命名
    if os.path.isfile(path):
        file_rename(path)
    elif os.path.isdir(path):
        # 文件夹中的文件批量重命名
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                file_rename(file_path)
            else:
                continue # 不遍历子文件夹；直接进入下一个处理，而不是打断循环
    # 找不到文件
    else:
        print("无效路径，请检查输入路径")




# 文件备份

def file_backup():
    pass



# 分割

def file_split():
    """
    功能：对文件夹中的文件按指定数量进行拆分。（会忽略文件夹，只处理文件）。如，文件夹中有1000张图片，可将其拆分为10个小文件夹，每个文件夹100张图片，文件夹编号为1-10。

    参数：无需提前输入参数，执行后，根据终端中的提示进行输入。

    path = input("请输入原始文件路径:")  # 输入待分割的原始文件所在路径。

    folderPath = input("请输入要输出的路径:")  # 输入分割后的结果存放路径。

    number = int(input("请输入每个文件夹中文件数:"))  # 每个文件夹中的文件数。
    """

    path = input("请输入原始文件路径:\n")  # 输入原始文件路径
    folderPath = input("请输入要输出的路径:\n")  # 输入要输出的路径
    path = path.strip("\"")  # 去除路径两端的引号
    folderPath = folderPath.strip("\"")  # 去除路径两端的引号

    number = int(input("请输入每个文件夹中文件数:\n"))  # 每个文件夹中的文件数
    file_list = os.listdir(path)  # 原始文件名称列表
    Number = math.ceil(len(file_list) / number)  # 目标文件夹数量

    # 从0号文件夹开始，使用此处的设置
    # folderNumber = -1 #起始文件夹id ，-1是因为0 % 任意数 = 0
    # sort_folder_number = [x for x in range(0,Number)]

    # 从1号文件夹开始，使用此处的设置
    folderNumber = 0 # 起始文件夹id ，移动文件时，考虑到第一个文件的索引是0，由于将文件移动到哪个文件夹这个环节涉及到数学计算及判断（判断取余数的结果是否为0），索引，为保证第一个文件能存到1号文件夹，这里的初始id设置0，而不能直接设成1，在数学判断后，id会变成0+1=1。（0 % 任意数 = 0）
    sort_folder_number = [x for x in range(1,Number+1)] # 这里可以是从1开始，不必从0开始，如果从0开始，会建立一个0号文件夹

    # 创建文件夹
    for foldernumber in sort_folder_number:
        new_folder_path = os.path.join(folderPath, '%s' % foldernumber)  # 新文件夹路径为 'folderPath\number' 。
        """
        @知识卡片
        这行代码的作用是将文件夹路径和文件夹编号拼接起来，形成新的文件夹路径。`os.path.join()` 函数用于拼接路径，它接受多个参数，并根据操作系统的不同使用适当的路径分隔符进行拼接。在这里，`folderPath` 是用户输入的输出路径，`'%s' % foldernumber` 是文件夹编号，通过字符串格式化将其转换为字符串。通过调用 `os.path.join(folderPath, '%s' % foldernumber)`，将输出路径和文件夹编号拼接在一起，得到新的文件夹路径 `new_folder_path`。例如，如果 `folderPath` 是 `/path/to/output`，`foldernumber` 是 `0`，那么 `new_folder_path` 将是 `/path/to/output/0`。这样就可以根据文件夹编号创建不同的文件夹路径。
        """
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)  # 创建新文件夹
            print("新建了一个名为" + str(foldernumber) + "的文件夹，路径为" + new_folder_path)

    # 分包
    for i in range(0, len(file_list)):
        old_file = os.path.join(path, file_list[i])  # 原始文件路径
        if os.path.isdir(old_file):
            '''如果路径是文件夹，程序将跳过它'''
            print('图片不存在，路径为' + old_file + '，它是一个文件夹')
            pass
        elif not os.path.exists(old_file):
            '''如果路径不存在，程序将跳过它'''
            print('图片不存在，路径为' + old_file)
            pass
        else:
            '''定义文件夹编号，与每个文件夹处理图片的数量相关'''
            if (0 == (i % number)):  # @ 知识卡片 第一个i=0, 0 % 任意数 = 0,所以，folderNumber = 0，加1后为1，第一个文件会移动到1号文件夹中;如果每个文件夹中20个，索引0-19会存到1；上面虽然建立了0号文件夹，但0号文件夹不存东西。
                folderNumber += 1  # 增加文件夹编号
            """
            @知识卡片
            这段代码用于确定每个文件应该被移动到哪个文件夹中。
            首先，`(i % number)` 是计算 `i` 除以 `number` 的余数。如果余数为 0，表示 `i` 是 `number` 的倍数。然后，`(0 == (i % number))` 是判断 `(i % number)` 是否等于 0。如果等于 0，表示 `i` 是 `number` 的倍数。
            如果 `(i % number)` 等于 0，即 `i` 是 `number` 的倍数，那么 `folderNumber` 的值会加 1。这样，每当遍历到一个是 `number` 的倍数的文件时，`folderNumber` 的值就会增加，从而确定下一个文件应该被移动到的文件夹编号。
            例如，如果 `number` 是 5，那么当 `i` 的值为 0、5、10、15 等时，`(i % number)` 的值都为 0，此时 `folderNumber` 的值会加 1。这样就可以确保每个文件夹中的文件数不超过 `number`，并且文件按照顺序被分配到不同的文件夹中。
            """

            new_file_path = os.path.join(folderPath, '%s' % (folderNumber))  # 新文件路径
            if not os.path.exists(new_file_path):
                break
            shutil.move(old_file, new_file_path)  # 移动文件
            print(old_file + '成功移动到' + new_file_path)

    print(f"分割完毕：已将文件分到 {Number} 个文件夹，每个文件夹 {number} 个文件")




# 文件对比


def copy_files_by_keyword(raw_data_path,working_path):
    """
    功能：根据文件名中的关键词复制文件。

    参数：

    raw_data_path：原始数据所在路径。（不会复制子文件夹，也不会遍历子文件夹）。
    
    working_path：工作路径，提取出来的文件将存放到该路径。

    keyword（不是参数）：指文件名中包含的关键词，不是参数，程序运行后，在命令行中根据提示按需输入。
    """

    # 原始数据文件夹
    raw_data_path = raw_data_path
    # 给定工作路径，或基础路径，用于制作结果文件夹路径
    working_path = working_path

    # 根据keyword制作目标路径——复制文件存放的位置
    keyword = str(input("请输入要复制的文件包含的关键词:\n"))

    # 判断结果文件夹是否已存在，不依赖上一步，如果此处发现目标文件夹不存在，可以现场新建一个
    result_path = working_path + "/" + str(keyword)
    if os.path.exists(result_path) == False:
        os.mkdir(result_path)

    # 提取raw_path中的文件列表，获取列表里面的文件，再根据文件名制作文件当前的完整路径——这一串操作都是为了制作路径
    every_file_list_path = os.listdir(raw_data_path)
    for i in every_file_list_path:
        file_path = os.path.join(raw_data_path, i)  # 使用os.path.join()函数拼接路径
        if os.path.isfile(file_path):  # 判断是否为文件
            if str(keyword) in i:
                print(f"找到名称中包括 {keyword} 的文件")
                shutil.copy(file_path, result_path)
                print(f"copying: {i} to {result_path}")
            else:
                continue 

    print(f"名称中包括 {keyword} 的文件已提取（复制）完毕") 




def move_files_by_keyword(raw_data_path,working_path):
    """
    功能：根据文件名中的关键词移动文件。

    参数：

    raw_data_path：原始数据所在路径。（不会移动子文件夹，也不会遍历子文件夹）。

    working_path：工作路径，提取出来的文件将存放到该路径。

    keyword（不是参数）：指文件名中包含的关键词，不是参数，程序运行后，在命令行中根据提示按需输入。
    """

    # 原始数据文件夹
    raw_data_path = raw_data_path
    # 给定工作路径，或基础路径，用于制作结果文件夹路径
    working_path = working_path

    # 根据keyword制作目标路径——复制文件存放的位置
    keyword = str(input("请输入要移动的文件包含的关键词:\n"))

    # 判断结果文件夹是否已存在，不依赖上一步，如果此处发现目标文件夹不存在，可以现场新建一个
    result_path = working_path + "/" + str(keyword)
    if os.path.exists(result_path) == False:
        os.mkdir(result_path)

    # 提取raw_path中的文件列表，获取列表里面的文件，再根据文件名制作文件当前的完整路径——这一串操作都是为了制作路径
    every_file_list_path = os.listdir(raw_data_path)
    for i in every_file_list_path:
        file_path = os.path.join(raw_data_path, i)  # 使用os.path.join()函数拼接路径
        if os.path.isfile(file_path):  # 判断是否为文件
            if str(keyword) in i:
                print(f"找到名称中包括 {keyword} 的文件")
                file_path = raw_data_path + "/" + i
                shutil.move(file_path, result_path)
                print(f"moving: {i} to {result_path}")
            else:
                continue 

    print(f"名称中包括 {keyword} 的文件已提取（移动）完毕") 




def get_current_folder_name(path):
    """
    功能：输入一个路径，返回当前文件夹名。

    参数：

    path：一个路径，可以是文件夹路径，也可以是文件路径。
    """

    # 判断路径是文件夹路径还是文件路径
    if os.path.isdir(path):
        # 如果是文件夹路径
        current_folder_name = os.path.basename(path)
    else:
        # 如果是文件路径
        current_folder_name = os.path.basename(os.path.dirname(path))
    return current_folder_name




def get_file_name(path):
    """
    功能：输入一个路径，返回文件名。（当path为文件夹路径，返回的值为空值。）

    参数：

    path：一个路径，可以是文件夹路径，也可以是文件路径。
    """

    # 判断路径是文件夹路径还是文件路径
    if os.path.isdir(path):
        # 如果是文件夹路径
        file_name = None
    else:
        # 如果是文件路径
        file_name = os.path.basename(path)
    return file_name




def move_all_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹及其子文件夹中指定类型的全部文件移动到目标文件夹。

    参数：

    folder_path：待整理文件夹，可包含多层级子文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，递归调用函数来遍历它
        if os.path.isdir(file_path):
            move_all_files(file_path, target_folder, file_type_list)
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其移动到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Moving {file} to {target_folder}")
                    shutil.move(file_path, target_folder)
            else:
                continue




def copy_all_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹及其子文件夹中指定类型的全部文件复制到目标文件夹。

    参数：

    folder_path：待整理文件夹，可包含多层级子文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，递归调用函数来遍历它
        if os.path.isdir(file_path):
            copy_all_files(file_path, target_folder, file_type_list)
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其复制到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Copying {file} to {target_folder}")
                    shutil.copy(file_path, target_folder)
            else:
                continue




def move_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹中（不包括子文件夹)指定类型的文件移动到目标文件夹。

    参数：

    folder_path：待整理文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，忽略
        if os.path.isdir(file_path):
            continue
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其移动到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Moving {file} to {target_folder}")
                    shutil.move(file_path, target_folder)
            else:
                continue




def copy_files(folder_path, target_folder, file_type_list):
    """
    功能：将待整理文件夹中(不包括子文件夹)指定类型的文件复制到目标文件夹。

    参数：

    folder_path：待整理文件夹。

    target_folder：目标文件夹。

    file_type_list：一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类。
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，忽略
        if os.path.isdir(file_path):
            continue
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其复制到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Copying {file} to {target_folder}")
                    shutil.copy(file_path, target_folder)
            else:
                continue



def rename_folder_numeric_serialize(path):
    """
    功能：给定一个文件夹路径，获取其中子文件夹的名字，根据子文件夹的名字，从左到右进行比较，按数值从小到大对子文件夹排序，再从1开始对子文件夹进行序列化重命名。

    参数：

    path：文件夹路径。
    """

    # 定义一个函数，将输入的字符串按照数字和非数字的部分进行分割，并将数字部分转换为整数
    def split_key(s): # 【一个字符串一个字符串处理】
        parts = [] # 初始化一个空列表，用于存储分割后的字符串
        current_part = "" # 初始化一个空字符串，用于存储当前正在处理的部分
        for c in s: # 遍历字符串中的每个字符
            if c.isalnum(): # 如果当前字符是字母或数字
                current_part += c # 将其添加到 current_part 变量中
            else: # 如果当前字符是非字母和数字的符号
                if current_part: # 如果 current_part 不为空
                    if current_part.isdigit(): # 如果 current_part 是数字
                        current_part = int(current_part) # 将其转换为整数
                    parts.append(current_part) # 将 current_part 添加到 parts 列表中
                    current_part = "" # 将 current_part 重置为空字符串
        if current_part: # 如果 current_part 不为空
            if current_part.isdigit(): # 如果 current_part 是数字
                current_part = int(current_part) # 将其转换为整数
            parts.append(current_part) # 将 current_part 添加到 parts 列表中
            # print(parts)
            # exit()
        return parts # 返回分割后的字符串列表
        
    # 定义文件夹路径
    images_path = path

    # 获取images_path下的所有子文件夹
    subfolders = [f.path for f in os.scandir(images_path) if f.is_dir()]

    # 对子文件夹按名字进行递增排序 @ 知识卡片 键函数。把subfolders中的每个元素，传给split_key按规则进行处理，并返回一个键，按返回的键进行排序。
    subfolders.sort(key=split_key)

    # 对排序后的子文件夹从1开始序列化，序列化的值加在原文件名末尾，以_进行拼接
    for i, folder in enumerate(subfolders, start=1): # 遍历排序后的子文件夹，从1开始序列化 @ 知识卡片
        new_name = f"{folder}_{i}" # 将序列化的值加在原文件名末尾，以_进行拼接
        os.rename(folder, new_name) # 重命名文件夹 @ 知识卡片
        print(os.path.basename(new_name)) # 打印重命名后的文件夹名字，不包括路径








# Data Processing


def obsidian_move_md_or_canvas_linked_images(images_path,folder_path,target_folder):
    """
    功能：指定相关路径，提取obsidian中.md文档、.canvas文档中链接的图片，实现附件管理、库空间管理、笔记归档。

    参数：

    images_path：图片附件所在的文件夹。通常是笔记库的附件文件夹。

    folder_path：待整理的md、canvas文档所在文件夹（可包括多层级子文件夹，会遍历）。通常临时建立一个文件夹,将待整理的笔记存进去。

    target_folder：提前准备的文件夹，可以建在任意位置，用于存放提取出来的图片。
    """

    # 001-图片文件夹:原始库的附件文件夹路径
    images_path = images_path
    # 002-文件夹路径：准备移动归档的文件夹，里面包含.md和.canvas格式的文件
    folder_path = folder_path
    # 003-图片移动的目标文件夹：通常，在002中建立一个文件夹，用于存放图片即可
    target_folder = target_folder

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
            # 将md文件打印出来
                print(file)
            # 处理markdown文档
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    # 查找文档中的图片
                    images = re.findall(r"\!\[\[(.*?)\]\]", content) # @@知识卡片 正则匹配
                    # exit()
                    for image_name in images:
                        # 在images文件夹中查找对应图片
                        for image_root, _, image_files in os.walk(images_path):
                            if image_name in image_files:
                                # 移动图片到指定文件夹
                                shutil.move(os.path.join(image_root, image_name), os.path.join(target_folder, image_name))
                                # 打印移动过程
                                print(f"moving:{os.path.join(image_root, image_name)}--->{os.path.join(target_folder, image_name)}")
            # exit()

            # 处理canvas文档
            elif file.endswith(".canvas"):
                # 将canvas文件打印出来
                print(file)
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read() # @知识卡片 不必非用json的读取方式
                    # 查找文档中的图片
                    # images = re.findall(r'"file":"(.*?\.png)"', content) # @知识卡片 匹配形如"file":"Pasted image 20230531214326.png"的字符串，得到的是绝对路径
                    images = re.findall(r'"file":"(.*?)"', content) # @知识卡片 匹配形如"file":"Pasted image 20230531214326.png"的字符串，得到的是绝对路径。不用指定png、jpeg等格式。
                    # print(images)
                    for file_path in images:
                        # print(file_path)
                        image_name = os.path.basename(file_path) #  @知识卡片 从绝对路径中提取文件名。Pasted image 20230531214326.png
                        # 在images文件夹中查找对应图片
                        for image_root, _, image_files in os.walk(images_path):
                            if image_name in image_files:
                                # 移动图片到指定文件夹
                                shutil.move(os.path.join(image_root, image_name), os.path.join(target_folder, image_name))
                                # 打印移动过程
                                print(f"moving:{os.path.join(image_root, image_name)}--->{os.path.join(target_folder, image_name)}")

    # 统计附件整理情况
    images_list = os.listdir(target_folder)
    num_images = len(images_list)

    print(f"\n已整理{num_images}个附件！")




def obsidian_bookmarks_merge_and_deduplicate(original_bookmarks_path,result_path):
    """
    功能：用于处理surfing插件产生的bookmarks。先合并多个bookmarks（只有1个也能正常使用），再对合并后的bookmarks去重，最后得到一个最全、不重复的bookmarks。

    参数：

    original_bookmarks_path：一个路径，路径下存放bookmarks文件，json格式，可以是1个或多个json文件。

    result_path：一个路径，用于存放最终结果。
    """

    # 当次处理结果文件夹
    result_path = result_path
    # 待处理书签文件夹：里面包括多个书签文件，仅包含1个也行
    original_bookmarks_path = original_bookmarks_path

    # 获取去重后的bookmarks：输入1个书签路径,返回去重后的书签
    def get_no_duplicates_bookmarks(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            bookmarks = data["bookmarks"]
            categories = data["categories"]

        # 去重
        unique_data = []
        urls = set()
        for bookmark in bookmarks:
            url = bookmark["url"]
            if url not in urls:
                unique_data.append(bookmark)
                urls.add(url)
        # 构造新的json字典并写入到result.json文件中
        new = {"bookmarks": unique_data, "categories": categories}

        # 统计原始json中书签的个数、去重后的新书签数量和重复书签数量的统计
        num_original = len(data["bookmarks"])
        num_new = len(urls)
        num_duplicates = num_original - num_new

        print(f"原始json中书签的个数: {num_original}")
        print(f"去重后的新书签数量: {num_new}")
        print(f"重复书签数量: {num_duplicates}")

        return new

    # json文件合并 @知识卡片 两个数据格式相同的字典合并
    def merge_json_files(original_bookmarks_path, result_path):
        data = {"bookmarks": [], "categories": []}
        for file_name in os.listdir(original_bookmarks_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(original_bookmarks_path, file_name)
                with open(file_path, 'r') as f:
                    file_data = json.load(f)
                    # print(file_data) # file_data是字典
                data["bookmarks"].extend(file_data["bookmarks"])
                data["categories"].extend(file_data["categories"])
        # 合并结果存为：temp-surfing-bookmark.json
        with open(os.path.join(result_path, "temp-surfing-bookmark.json"), 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(
            f"Merged {len(os.listdir(original_bookmarks_path))} files into {result_path}")

    # 调用
    merge_json_files(original_bookmarks_path, result_path)


    # 合并后再去重一次:单个去重，得到 surfing-bookmark.json
    final_bookmarks = get_no_duplicates_bookmarks(os.path.join(
        result_path, "temp-surfing-bookmark.json"))  # final_bookmarks是一个完整的标签内容

    with open(os.path.join(result_path, "surfing-bookmark.json"), 'w') as f:
        json.dump(final_bookmarks, f, indent=2,
                ensure_ascii=False)  # 这里写final_bookmarks

    print("书签合并与去重完毕！")




def get_weibo(path,id,weibo_name):
    """
    功能：获取某个微博的全部图片及正文。

    参数：

    path: 内容存放路径。

    id: 微博id。

    weibo_name: 内容存放路径下一个自定义的文件夹名。

    示例：获取梅西的微博id，获取其微博内容。

    import pydatawork as dw 

    path="/home/Desktop/pydatawork"

    id="5934019851" # 梅西的微博id。在网页版微博上找到梅西的微博，查看链接，链接为 https://weibo.com/u/5934019851 ，链接中u后面的数字即为id ,梅西微博的id为 5934019851。

    weibo_name="mx"

    dw.get_weibo(path,id,weibo_name)
    """
    path = path
    id = id # 在微博上获取

    proxy_addr = "122.241.72.191:808"
    weibo_name = weibo_name # 可以自定义名字

    def use_proxy(url, proxy_addr):
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
        return data

    def get_containerid(url):
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        for data in content.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
        return containerid

    def get_userInfo(id):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")

    def get_weibo(id, file):
        global pic_num
        pic_num = 0
        i = 1
        while True:
            url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
            weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url) + '&page=' + str(i)
            try:
                data = use_proxy(weibo_url, proxy_addr)
                content = json.loads(data).get('data')
                cards = content.get('cards')
                if (len(cards) > 0):
                    for j in range(len(cards)):
                        print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")
                        card_type = cards[j].get('card_type')
                        if (card_type == 9):
                            mblog = cards[j].get('mblog')
                            attitudes_count = mblog.get('attitudes_count')
                            comments_count = mblog.get('comments_count')
                            created_at = mblog.get('created_at')
                            reposts_count = mblog.get('reposts_count')
                            scheme = cards[j].get('scheme')
                            text = mblog.get('text')
                            if mblog.get('pics') != None:
                                # print(mblog.get('original_pic'))
                                # print(mblog.get('pics'))
                                pic_archive = mblog.get('pics')
                                for _ in range(len(pic_archive)):
                                    pic_num += 1
                                    print(pic_archive[_]['large']['url'])
                                    imgurl = pic_archive[_]['large']['url']
                                    img = requests.get(imgurl)
                                    # f = open(path + weibo_name + '\\' + str(pic_num) + str(imgurl[-4:]),'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）# 原始代码
                                    f = open(os.path.join(path, weibo_name, str(pic_num) + str(imgurl[-4:])), 'ab') # 存储图片，多媒体文件需要参数b（二进制文件）
                                    f.write(img.content)  # 多媒体存储content
                                    f.close()

                            with open(file, 'a', encoding='utf-8') as fh:
                                fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                                fh.write("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                                    created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                                    attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                                    reposts_count) + "\n")
                    i += 1
                else:
                    break
            except Exception as e:
                print(e)
                i += 1  # 添加这一行
                pass

    # # 在指定路径下，先建立一个名为weibo的文件夹
    # if os.path.isdir(os.path.join(path,"weibo")):
    #     pass
    # else:
    #     os.mkdir(os.path.join(path,"weibo"))

    if os.path.isdir(os.path.join(path,weibo_name)):
        pass
    else:
        os.mkdir(os.path.join(path,weibo_name))
    file = os.path.join(path, weibo_name, weibo_name + ".txt")

    get_userInfo(id)
    get_weibo(id, file)
    print("微博数据获取完毕")
    # 该程序最初来源：http://www.omegaxyz.com/2018/02/13/python_weibo/






# Data Analysis


def game_number_guessing(number=100):
    """
    游戏规则：指定一个整数，确定数字的范围；根据提示猜数字，直到猜中。

    参数：

    number：大于1的整数，默认为100，指要猜的数字在100以内。

    用法1：若不设定参数，可以写成 game_number_guessing() ，这时默认值为100。

    用法2：自定义参数，可以写成 game_number_guessing(number=200)，这时，数字范围设定为在200以内。
    """

    # 自定义数字的范围，不局限于100以内
    # x = int(input("输入一个数字，限定一个范围："))
    x = int(number)

    # 每次程序运行执行该行代码的时候，都会产生一个 指定范围内 的随机整数，并赋值给 answer 变量
    answer = random.randint(1, x)

    # 游戏设置
    print("\nloading...")
    time.sleep(0.5)
    print("猜数字游戏加载中")
    time.sleep(1)
    print("ok...")
    time.sleep(0.5)
    print("加载完毕")
    time.sleep(0.5)
    print("start...")
    time.sleep(0.5)
    print("游戏已开局")
    time.sleep(0.5)
    user = input("设定你的游戏角色名字(若暂不设定，可按回车跳过)：")
    if user:
        print("角色名设定完毕...")
        time.sleep(0.5)
        print("gogogo...")
        time.sleep(0.5)
    else:
        print("skiping...")
        time.sleep(0.5)

    num = 1
    while True:

        aa = int(input("\n输入答案："))
        time.sleep(0.25)

        if aa == answer:
            print("猜对了！")
            break
        elif aa < answer:
            print("大一点")
        else:
            print("小一点")
        num = num + 1
    
    # 输出结果
    if user:
        print(f"\nhi，{user}，你一共猜了{num}次。")
    else:
        print(f"\nhi，无名氏，你一共猜了{num}次。")



def get_BMI(height,weight):
    """
    功能：用于BMI测量。BMI（身体质量指数）是一种计算一个人体重是否健康的方法，基于身高和体重的比例来计算。如果 bmi 小于 18.5，说明体重过轻；如果 bmi 在 18.5 和 24.9 之间说明体重在正常范围；如果 bmi 在 24.9 和 29.9 之间说明体重过重；如果大于 29.9 说明肥胖。

    参数：

    height：身高（m）（注意，单位为米）。

    weight：体重（kg）（注意，单位为千克）。

    调用示例：dw.get_BMI(height=1.75,weight=73)。
    """

    # height = float(input("输入身高（米）："))
    # weight = float(input("输入体重（千克）："))

    height = float(height) 
    weight = float(weight)
    bmi = weight / (height * height)  #计算BMI指数
    suggested_weight_lower =  (height * height) * 18.5
    suggested_weight_higher =  (height * height) * 24.9

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y.%m.%d %H:%M:%S")
    
    print("本次BMI测量时间：" + formatted_time) # 使用加号，格式更自由 @ 知识卡片
    print("身高：",height,"m") # @知识卡片 每个逗号会被打印成一个空格，基础打印
    print("体重：",weight,"kg")
    # print("BMI(身体质量指数):",bmi)
    print("BMI(身体质量指数)：%0.2f" % (bmi)) # @知识卡片 保留两位小数，格式化打印

    if bmi < 18.5:
        print("当前BMI健康状态评价：体重过轻")
    elif 18.5 <= bmi < 24.9:
        print("当前BMI健康状态评价：体重在正常范围")
    elif 24.9 <= bmi < 29.9:
        print("当前BMI健康状态评价：体重过重")
    else:
        print("当前BMI健康状态评价：体重超重")

    # print(f"建议体重保持在{suggested_weight_lower}至{suggested_weight_higher}之间")
    print("正常体重范围：建议体重保持在 %0.2f kg 至 %0.2f kg 之间\n(注意：男女有别，请结合自身实际情况判断自己的体重状态)" % (suggested_weight_lower,suggested_weight_higher))





