# -*- config: utf-8 -*-
# @File  : test.py.py
# @Auther: Hxp
# @Date  : 2020/11/24 : 10:28
# @
for i in range(1,10):
    print(i)
print()
# import tkinter as tk
#
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.li = ['C', 'python', 'php', 'html', 'SQL', 'java']
#         self.movie = ['CSS', 'jQuery', 'Bootstrap']
#         self.pack()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")
#
#         self.list = tk.Listbox(self)
#         for item in self.li:  # 第一个小部件插入数据
#             self.list.insert(0, item)
#         self.list.pack()
#
#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")
#
#     def say_hi(self):
#         print("hi there, everyone!")
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()
#
# # li = ['C', 'python', 'php', 'html', 'SQL', 'java']
# # movie = ['CSS', 'jQuery', 'Bootstrap']
# # listb = Listbox(root)  # 创建两个列表组件
# # listb2 = Listbox(root)
# # for item in li:  # 第一个小部件插入数据
# #     listb.insert(0, item)
# #
# # for item in movie:  # 第二个小部件插入数据
# #     listb2.insert(0, item)