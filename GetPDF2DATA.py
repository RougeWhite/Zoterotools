# -*- coding:utf-8 -*-
#                 ____                                       _____  __         
#                /\  _`\                                    /\___ \/\ \        
#                \ \ \L\_\  __  __     __      ___          \/__/\ \ \ \___    
#                 \ \ \L_L /\ \/\ \  /'__`\  /' _ `\           _\ \ \ \  _ `\  
#                  \ \ \/, \ \ \_\ \/\ \L\.\_/\ \/\ \         /\ \_\ \ \ \ \ \ 
#                   \ \____/\ \____/\ \__/.\_\ \_\ \_\        \ \____/\ \_\ \_\
#                    \/___/  \/___/  \/__/\/_/\/_/\/_/  _______\/___/  \/_/\/_/
#                                                      /\______\               
#                                                      \/______/  
'''
@FileName  :GetPDF2DATA.py

@Time      :2022/7/18 13:16

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :由于Zotero可以快速下载论文到本地，但是并不支持将pdf下载到想要的目录，使用使用本转移工具+OneDrive自动同步，可以实现一些无缝操作
'''

# TODO 获取old文件夹内全部pdf文件
# TODO 获取new文件夹内目录文件tmp
# TODO 如果old文件夹中有同名文件，并且日期相同，则认为文件已经转移，否则转移文件到new下
# TODO


import os
import shutil
from glob import glob
from tkinter import *
import hashlib
import time
import re

# root = Tk()  # 创建窗口对象的背景色
#
# root.mainloop()
LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("Zotero处理工具 v1.0 作者：Guan_Jh")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('365x260+777+410')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="Zotero文件位置：例如 E:\zotero\storage")
        self.init_data_label.grid(row=0, column=0, sticky='w')
        self.init_data_Text = Text(self.init_window_name, width=50, height=1)  # 原始数据录入框
        self.init_data_Text.insert(1.0, "E:\zotero\storage")
        self.init_data_Text.grid(row=1, column=0, rowspan=1, columnspan=10)

        self.result_data_label = Label(self.init_window_name, text="转移位置：例如 E:\OneDrive\论文\PDFfromOther")
        self.result_data_label.grid(row=3, column=0, sticky='w')
        self.result_data_Text = Text(self.init_window_name, width=50, height=1)  #处理结果展示
        self.result_data_Text.insert(1.0, "E:\OneDrive\论文\PDFfromOther")
        self.result_data_Text.grid(row=4, column=0, rowspan=1, columnspan=10)

        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=9, column=0, sticky='w')
        self.log_data_Text = Text(self.init_window_name, width=50, height=9)  # 日志框
        self.log_data_Text.grid(row=10, column=0, columnspan=10)



        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="开始转移", bg="lightblue", width=10,command=self.chick)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=8, column=5)


    def chick(self):
        PDF_Path_Input = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        New_Path_Input = self.result_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        PDF_Path = PDF_Path_Input.decode()
        New_Path = New_Path_Input.decode()
        # print(New_Path)
        PDF_Path_Vaild = re.search('.*:\\.*', PDF_Path)
        New_Path_Vaild = re.search('.*:\\.*', New_Path)
        if PDF_Path_Vaild and New_Path_Vaild:
            self.write_log_to_Text("路径有效")
            self.GetPDF2Data(PDF_Path, New_Path)
        else:
            if PDF_Path_Vaild:
                self.write_log_to_Text("第二个输入路径无效")
            else:
                self.write_log_to_Text("第一个输入路径无效")



    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


    def mycopyfile(self,srcfile, dstpath):  # 复制函数
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)  # 创建路径
            shutil.copy(srcfile, dstpath + fname)  # 复制文件
            self.write_log_to_Text("复制文件\n %s \n到\n %s" % (srcfile, dstpath + fname))
            # print("复制文件\n %s \n到\n %s" % (srcfile, dstpath + fname))


    def text_create(self,path,name, msg):
        full_path = path + name
        f = open(full_path, 'w')
        f.write(msg)
        # file.close()

    def GetPDF2Data(self,PDF_Path,New_Path_Input):
        # PDF_Path = "E:\zotero\storage"    # 需要转移的PDF路径
        New_Path = New_Path_Input+"\\"
        # New_Path = "E:\\OneDrive\\论文\\PDFfromOther\\"    # 转移后的路径
        Dir_Name = New_Path+"Toc_Config"    # 目录配置名称
        self.write_log_to_Text("读取Toc_Config配置文件。。。")
        if os.path.exists(Dir_Name) ^ 1:
            self.write_log_to_Text("初次使用将新建配置文件")
            self.write_log_to_Text("配置文件请不要删除，否则将导致严重后果")
            self.text_create(New_Path , 'Toc_Config', '配置文件请不要删除，否则将导致严重后果,')

    #     获取路径下全部pdf文件
        for root, dirs, files in os.walk(PDF_Path):
            for File_Name in files:
                File_Name_List = File_Name.split(".")
                File_Name_Suffix = File_Name_List[len(File_Name_List)-1]
                if File_Name_Suffix == "pdf":
                    PDF_File_Path = os.path.join(root, File_Name)
                    # print(os.path.join(root, File_Name))
                    PDF_NAME = os.path.basename(PDF_File_Path)   # PDF名称
                    # print(PDF_NAME)
                    PDF_TIME = time.strftime("%Y-%m-%d", time.localtime(os.stat(PDF_File_Path).st_mtime))  # PDF 生成日期
                #   获取目录内的数据，并判断是否存在
                    f = open(Dir_Name)
                    lines = f.read()
                    line_list = lines.split(",")
                    tmp_a = 0
                    for i in line_list:
                        if i == "\n" + PDF_TIME + "-----" + PDF_NAME:
                            self.write_log_to_Text("PDF文件已存在\n"+PDF_NAME)
                            # print("PDF文件已存在\n"+PDF_NAME)
                            break
                        else:
                            tmp_a = tmp_a + 1
                            if len(line_list) == tmp_a:
                                f = open(Dir_Name, "a")
                                # 写入配置名称
                                f.write("\n" + PDF_TIME + "-----" + PDF_NAME + ",")
                                # 复制文件
                                src_file_list = glob(PDF_File_Path + '*')  # glob获得路径下所有文件，可根据需要修改
                                for srcfile in src_file_list:
                                    self.mycopyfile(srcfile, New_Path)
                    f.close()
        # print("转移完成")
        self.write_log_to_Text("转移完成")

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()