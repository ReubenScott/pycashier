#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# python 2.x 导入包
import Tkinter as tk
import ttk

root = tk.Tk()
root.title('测试')



tree = ttk.Treeview(root, columns=['1', '2', '3'] , show='headings')


# show = "headings" 显示第一行标题，同时把第一列隐藏起来
#   show = "tree", 第一列也会被显示出来，   同时把第一行的列标题隐藏起来  
# height 的单位是字符，本例里可以显示 10行
  
tree.column('1', width=100 ,anchor= 'center')  #指定这一列的宽度和对齐方式
tree.column('2', width=100 ,anchor= 'center')
tree.column('3', width=100 ,anchor= 'center')

tree.heading('1', text='姓名') #显示这一列标题
tree.heading('2', text='学号')
tree.heading('3', text='性别')

# python2.x  unicode 编码 （中文乱码的问题 ）
li = [ u'王记 ' ,'12' , u' 男 ']
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
tree.insert('', 'end', values =li )
td=tree.insert('', 'end', values =li )

print type(td) , td

'''

#y滚动条
yscrollbar = tk.Scrollbar(tree, orient ='vertical', command=tree.yview)
tree.configure(yscrollcommand=yscrollbar.set )
yscrollbar.pack(side='right', fill= 'y' )

#x滚动条
xscroll = tk.Scrollbar(tree, orient ='horizontal', command=tree.xview)
tree.configure(xscrollcommand=xscroll.set )
xscroll.pack(side='bottom', fill= 'x' )
'''

tree.pack()

root.mainloop()
