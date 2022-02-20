
#!/usr/bin/env python     
# -*- coding: UTF-8 -*- 

import sys
import os
import io
import time
import re
import base64
import Tkinter as tk
import tkFont
import ttk
from decimal import Decimal

#from Tkinter import *
#from PIL import Image  
#import Image
import memory_pic  # 无需像原博客那样一个个导入
import agent.payagent


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
  reload(sys)
  sys.setdefaultencoding(defaultencoding)
    

# 小数点后位数
NUMBER_OF_DECIMAL_PLACES = 2


def btn_def(num1, num2):
    num = int(num1) + int(num2)
    messagebox.showinfo('结果', '%d' % num)  
    

def digital_check(content): 
 
  if content.endswith('.') and content.count('.') <= 1:
    content = content[0:-1]
  
  #以下是整数和小数正确的正则表达式 
  regInt = '^0$|^[1-9]\d*$'#不接受09这样的为整数
  regFloat = '^0\.\d+$|^[1-9]\d*\.\d+$'
  #接受0.00、0.360这样的为小数，不接受00.36，思路:若整数位为零,小数位可为任意整数，但小数位数至少为1位，若整数位为自然数打头，后面可添加任意多个整数，小数位至少1位

  regIntOrFloat = regInt + '|' + regFloat  #整数或小数
  patternIntOrFloat = re.compile(regIntOrFloat)  #创建pattern对象，以便后续可以复用
  
  #if patternIntOrFloat.search(content) or re.search(patternIntOrFloat,content) or re.search(regIntOrFloat,content) or (content==""):
  if re.search(patternIntOrFloat,content) or (content==""):
    return True
  else:
    return False

# 弹窗  预支付
class PopupDialog(tk.Toplevel):

  def __init__(self, master=None, **kw):
    tk.Toplevel.__init__(self, master, **kw)
    
    global token      # 预支付接口  服务器返回 Token  

    # todo 调用预支付接口 客户端提供参数： 商品明细： 会员号， 商品条码 , 数量 ，金额       
    rs = agent.payagent.prePayment()        
    print rs
    token = rs 
    print "Token: ",  token
    
    self.title('结算 金额单位（元）') 
    # 设置图片 修改tkinter窗口的红色图标'Tk'
    #ckw.iconbitmap('../favicon.ico')
    
    #设置屏幕正中      
    width, height = self.master.master.maxsize()
    width = width/4
    height = height/4    
    screenwidth = self.master.winfo_screenwidth()
    screenheight = self.master.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)   
    

    ckw = tk.LabelFrame(self, padx=0, pady=5) 
    #frame5 = tk.LabelFrame(root,bd=2,relief="ridge",text="英語",width=380,height=70,foreground="purple")

    # 第一行（两列）
    tk.Label(ckw, text='应付总额：').grid(row=0, column=0,  sticky='wens')
    tk.Label(ckw, text=self.master.mainPage.totalbar.orgtotal.get() ).grid(row=0, column=1,  sticky='wens') 
    
    tk.Label(ckw, text='剩余应付：').grid(row=1, column=0,  sticky='wens')
    tk.Label(ckw, text=self.master.mainPage.totalbar.curtotal.get(), font=('Arial', 15, 'bold') ).grid(row=1, column=1,  sticky='wens')    
    
    tk.Label(ckw, text='付款方式：').grid(row=2, column=0,  sticky='wens')      
    # 创建 付款方式下拉列表   Payment method drop-down list
    self.numbervv = tk.StringVar()
    self.chosen_payment_label = ttk.Combobox(ckw, textvariable=self.numbervv, state='readonly' )
    self.chosen_payment_label['values'] = (u"现金", u"银行卡", u"微信", u"支付宝")    # 设置下拉列表的值
    self.chosen_payment_label.grid(row=2, column=1,  sticky='wens')      # 设置其在界面中出现的位置   column代表列    row 代表行
    self.chosen_payment_label.current(0)     # 设置下拉列表默认显示的值， 0为 numberChosen['values'] 的下标值
    #self.numbervv.set(u"银行卡")
    # 绑定切换事件
    self.chosen_payment_label.bind("<<ComboboxSelected>>", self.payment_selected)     
    
        
    tk.Label(ckw, text='支付金额：').grid(row=3, column=0,  sticky='wens')   
    #通过register方法转换为validatecommand选项能接收的函数
    check_auto_change = self.register(self.amount_checksum)      
    self.paidin = tk.StringVar()
    paidin_entry = tk.Entry(ckw, textvariable=self.paidin ,validate='key', validatecommand=(check_auto_change,'%P'))
    paidin_entry.focus() # 当程序运行时,光标默认会出现在该文本框中  
    paidin_entry.grid(row=3, column=1,  sticky='wens')   
    
    # 应找金额：, font=('Arial', 15, 'bold'), bg='green'  , fg='red'
    tk.Label(ckw, text='应找金额：').grid(row=4, column=0,  sticky='wens') 
    self.change = tk.StringVar()    
    tk.Label(ckw, textvariable=self.change, font=('Arial', 15, 'bold'), fg='red' ).grid(row=4, column=1,  sticky='wens') 
    #self.change.set(self.master.mainPage.totalbar.curtotal.get())    


    # 交易备注
    tk.Label(ckw, text='交易备注：').grid(row=5, column=0,  sticky='wens') 
    self.remark = tk.StringVar()    
    tk.Entry(ckw, textvariable=self.remark).grid(row=5, column=1,  sticky='wens')   

    # Grid 分配比例
    ckw.columnconfigure(0, weight=1)
    ckw.columnconfigure(1, weight=1)
  
    ckw.grid(row=0, column=0, columnspan=3, sticky='wens')
    
    
    # 
    tk.Button(self, text="收款过账 Enter", command=self.confirm_posting).grid(row=1, column=0, sticky='wens')
    tk.Button(self, text="返回修改 Esc", command=self.cancel_pay).grid(row=1, column=1, sticky='wens')
    tk.Button(self, text="本单作废 F12", command=self.cancel_pay).grid(row=1, column=2, sticky='wens')
          
    # Grid 分配比例
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

    #self.rowconfigure(0, weight=200)
    #self.rowconfigure(1, weight=2)
    #self.rowconfigure(2, weight=1)    

    self.geometry(size)  
    self.transient(master)   
    # 窗口关闭事件
    self.protocol("WM_DELETE_WINDOW", self.cancel_pay)
    
    #TODO 父窗口不然修改   # 这一句很重要！！！  
    #self.master.wait_window(self) 
    self.resizable(0,0)
    #self.attributes("-toolwindow", 1)
    
    # 绑定 
    self.bind('<Return>', lambda event: self.confirm_posting())  # 回车
    self.bind('<Escape>', lambda event: self.cancel_pay())  # Esc 
    self.bind('<F12>', lambda event: self.cancel_pay())  # F12 
    
      
  # 输入金额校验    
  def amount_checksum(self, content):    
    if content.endswith('.') and content.count('.') <= 1 :
      content = content[0:-1]    
    
    #以下是整数和小数正确的正则表达式 
    regInt = '^0$|^[1-9]\d*$'#不接受09这样的为整数
    regFloat = '^0\.\d+$|^[1-9]\d*\.\d+$'
    #接受0.00、0.360这样的为小数，不接受00.36，思路:若整数位为零,小数位可为任意整数，但小数位数至少为1位，若整数位为自然数打头，后面可添加任意多个整数，小数位至少1位
  
    regIntOrFloat = regInt + '|' + regFloat  #整数或小数
    patternIntOrFloat = re.compile(regIntOrFloat)  #创建pattern对象，以便后续可以复用
    
    #if patternIntOrFloat.search(content) or re.search(patternIntOrFloat,content) or re.search(regIntOrFloat,content) or (content==""):   
    
    if (re.search(patternIntOrFloat,content) or (content=="")) and len(content.partition('.')[2]) <= NUMBER_OF_DECIMAL_PLACES : 
      # 修改应找金额  '%.2f' % 变量  四舍五入   
      self.change.set(round(float(0 if content == "" else content) - float(self.master.mainPage.totalbar.curtotal.get()) , NUMBER_OF_DECIMAL_PLACES))          
      return True
    else:
      return False    
      
    
  # 绑定事件 切换付款方式
  def payment_selected(self, event):
    print(self.chosen_payment_label.get())
    print(self.numbervv.get())

  # Confirm Posting
  def confirm_posting(self):
    # 显式地更改父窗口参数
    #self.parent.name = self.name.get()
    #self.parent.age = self.age.get()
    # 显式地更新父窗口界面
    #self.parent.l1.config(text=self.parent.name)
    #self.parent.l2.config(text=self.parent.age)
      
    if self.change.get() != "" and float(self.change.get()) >= 0: 
      #TODO 提交数据        
      # need to post data to server  
      
      # todo 调用预支付接口 客户端提供参数： 商品明细： 会员号， 商品条码 , 数量 ，金额       
      rs = agent.payagent.payment(token)           
      
      # 解锁主窗口
      self.master.master.attributes("-disabled",False)
      self.destroy() # 销毁窗口
        
        
  # print(u'你关闭窗口: ')
  def cancel_pay(self):   
    '''    
    # 解除 输入框  锁定
    edit_entry_dict = self.master.mainPage.entrypage.children    
    #  一定要是一个tuple 类型数据 否则会提
    for k in edit_entry_dict.iterkeys():
      item_entry = edit_entry_dict[k]
      if isinstance(item_entry, tk.Entry):       
        item_entry.config(state='normal')      
    ''' 
    # 解锁主窗口
    self.master.master.attributes("-disabled",False)    
    self.destroy()
    

    
    
class CasherHeader(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)
    #justify定义多行文本如何对齐。可取值有：LEFT, RIGHT, 或 CENTER。   
    storeLab = tk.Label(self, text="店名:", **kw)   
    termnoLab = tk.Label(self, text="终端号:", **kw)   # Device No
    cashiernoLab = tk.Label(self, text="收银员：", **kw)   # Cashier
    worktimeLab = tk.Label(self, text="时间：", **kw)   
                         
    storename = tk.StringVar()
    storename.set('XXXX商店名称')  # TODO 
    termnoText = tk.StringVar()
    termnoText.set('3FDC28EA')   #  TODO
    cashierno = tk.StringVar()
    cashierno.set('0001')   #  TODO
    #timevar = tk.StringVar()
    #timevar.set(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))   #  TODO 时间可更新
    
       
    storenameLab = tk.Label(self, textvariable=storename, font=('Microsoft YaHei', 9, 'normal', 'underline'), **kw)  # TODO  underline  , font=('Arial', 10, 'bold', 'underline')
    termnoTextLab = tk.Label(self, textvariable=termnoText, **kw)
    cashiernoTextLab = tk.Label(self, textvariable=cashierno, **kw)
    #timeTextLab = tk.Label(self, textvariable=timevar)
    self.clockLab = tk.Label(self, font=('Microsoft YaHei', 9, 'bold'), bg="black", fg="white", relief='flat', justify='left')
      
                          
    #按扭停靠在窗口的哪个位置left: 左,top: 上,right: 右,botton: 下
    storeLab.pack(side='left', fill='x', expand='yes')  
    storenameLab.pack(side='left', fill='x', expand='yes')  
    termnoLab.pack(side='left', fill='x', expand='yes')  
    termnoTextLab.pack(side='left', fill='x', expand='yes')  
    cashiernoLab.pack(side='left', fill='x', expand='yes')  
    cashiernoTextLab.pack(side='left', fill='x', expand='yes')  
    worktimeLab.pack(side='left', fill='x', expand='yes')  
    self.clockLab.pack(side='left', fill='x', expand='yes')  
    
    self.tick() 
    #self.grid()
    #self.grid(row=0, column=0, sticky='wens')
    self.pack(fill='x', expand='no')
    
  # 更新系统时钟
  def tick(self):
    global local_time
    # 从运行程序的计算机上面获取当前的系统时间
    #time2 = time.strftime('%H:%M:%S')
    currunt_time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 如果时间发生变化，代码自动更新显示的系统时间
    if currunt_time != local_time:
      local_time = currunt_time
      self.clockLab.config(text=currunt_time)
      # calls itself every 200 milliseconds
      # to update the time display as needed
      # could use >200 ms, but display gets jerky      
    self.clockLab.after(200, self.tick)
    
    
'''
 会员栏目
'''    
class MemberBar(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)
    membernoLab = tk.Label(self, text="会员编号：", relief='sunken') 
    memnameLab = tk.Label(self, text="会员名称：", relief='flat')   
    memtypeLab = tk.Label(self, text="会员类型：", relief='flat')   
    menoffLab = tk.Label(self, text="享受折扣：", relief='ridge')   
    menbalanceLab = tk.Label(self, text="账户余额：", relief='ridge')   
    bonusLab = tk.Label(self, text="会员积分：", relief='ridge')   
  

    membernoLab.pack(side='left')
    memnameLab.pack(side='left')
    memtypeLab.pack(side='left')
    
    self.pack(fill='x', expand='no')  


# 主窗体
class MainPage(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master, **kw)
    
    #订单
    OrderBox(self)
    
    #帮助
    helpBar(self, bg="black", fg="white", relief='flat', justify='left')
    
    #输入栏
    self.entrypage = EntryPage(self, bg="black", fg="white", relief='flat', justify='left')
    
    #状态栏
    Statusbar(self, bg="black", fg="white", relief='flat', justify='left')
    
    #合计
    self.totalbar = Totalbar(self, bg="black", fg="white", relief='flat', justify='left', font=('Arial', 15, 'bold'))
    
    # Grid 分配比例  主页面 
    self.columnconfigure(0, weight=6)
    self.columnconfigure(1, weight=4)
    self.columnconfigure(2, weight=1)

    self.rowconfigure(0, weight=200)
    self.rowconfigure(1, weight=2)
    self.rowconfigure(2, weight=1)
    
    self.pack(fill='both', expand='yes')
    
    


class OrderBox(tk.Frame):
  def __init__(self, master=None,**kw):
    tk.Frame.__init__(self, master,**kw)
  
    global spreadsheet
    spreadsheet = ttk.Treeview(self, columns=['ordinal', 'barcode', 'name','unit','specs','sale_price','member_price','preferential_price','sold_price','volume','amount'] , show='headings')    
    
    # show = "headings" 显示第一行标题，同时把第一列隐藏起来
    #   show = "tree", 第一列也会被显示出来，   同时把第一行的列标题隐藏起来  
    # height 的单位是字符，本例里可以显示 10行
      
    spreadsheet.column('ordinal', width=30 ,anchor= 'center')  #指定这一列的宽度和对齐方式
    spreadsheet.column('barcode', width=200 ,anchor= 'center')
    spreadsheet.column('name', width=300 ,anchor= 'center')
    spreadsheet.column('unit', width=30 ,anchor= 'center')
    spreadsheet.column('specs', width=100 ,anchor= 'center')
    spreadsheet.column('sale_price', width=50 ,anchor= 'center')
    spreadsheet.column('member_price', width=50 ,anchor= 'center')
    spreadsheet.column('preferential_price', width=50 ,anchor= 'center')
    spreadsheet.column('sold_price', width=50 ,anchor= 'center')
    spreadsheet.column('volume', width=30 ,anchor= 'center')
    spreadsheet.column('amount', width=100 ,anchor= 'center')
    
    #显示列标题 
    spreadsheet.heading('ordinal', text='序号')              # 序号      ordinal
    spreadsheet.heading('barcode', text='商品编号')          # 商品编号  barcode  
    spreadsheet.heading('name', text='商品名称')             # 商品名称  name
    spreadsheet.heading('unit', text='单位')                 # 单位      unit
    spreadsheet.heading('specs', text='规格')                # 规格      specs
    spreadsheet.heading('sale_price', text='零售价')         # 零售价    sale_price
    spreadsheet.heading('member_price', text='会员价')       # 会员价    member_price
    spreadsheet.heading('preferential_price', text='特价')     # 特价    discounted_price      special offer
    #spreadsheet.heading('discount_rate', text='折扣%')          # 折扣%    discount rate
    spreadsheet.heading('sold_price', text='实售价')         # 实售价    sold_price
    spreadsheet.heading('volume', text='数量')               # 数量      volume
    spreadsheet.heading('amount', text='金额')               # 金额      amount
                
    
    #for i in range(10):
    #    tree.insert('',i,values=('a'+str(i),'b'+str(i),'c'+str(i)))
    spreadsheet.bind("<Double-1>", self.onDBClick)
    # 鼠标滚轮绑定
    self.master.master.bind("<MouseWheel>", self.OnMouseWheel)
    #tree.bind("<MouseWheel>", self.OnMouseWheel)
    
    '''
    
    '''    
    #y滚动条
    yscrollbar = tk.Scrollbar(spreadsheet, orient ='vertical', command=spreadsheet.yview)
    spreadsheet.configure(yscrollcommand=yscrollbar.set )
    yscrollbar.pack(side='right', fill= 'y' )
    
    #x滚动条
    xscroll = tk.Scrollbar(spreadsheet, orient ='horizontal', command=spreadsheet.xview)
    spreadsheet.configure(xscrollcommand=xscroll.set )
    xscroll.pack(side='bottom', fill= 'x' )
    
    spreadsheet.pack(fill='both', expand='yes')   

    #tree.grid(row=0, column=0, sticky='wens')
    
    #helpLab = tk.Label(self, text="结算 +", relief='sunken', justify = 'left'  )     
    #helpLab.grid(row=0, column=1, sticky='wens')
    
    self['borderwidth']='1px'
    
    #self.pack(fill='both', expand='yes')
    self.grid(row=0, column=0, columnspan=2, sticky='wens')
    
    
  def onDBClick(self, event):
      item = tree.selection()[0]
      print "you clicked on ", tree.item(item, "values")
      
  # 鼠标 滚轮    
  def OnMouseWheel(self, event):
      tree.yview("scroll", -1*(event.delta/120), "units")
      #tree.yview_scroll(-1*(event.delta/120), "units")
      return "break"
    
    
    
# 输入栏目
class EntryPage(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)
    
    tk.Label(self, text="输入条码：", **kw).pack(side='left', fill='both', expand='yes')
    
    #通过register方法转换为validatecommand选项能接收的函数  focusout
    #search_goods_reg = self.register(self.search_goods)        
    #nameEntered = tk.Entry(self, validate='key', validatecommand=(search_goods_reg,'%P'))
    
       
    #tk.Label(self, textvariable=self.orgtotal, relief='flat', bg='black', fg='white', font=('Arial', 20, 'bold')).grid(row=0, column=2, sticky='wens')    
    
    
    self.goods_code = tk.StringVar()    
    nameEntered = tk.Entry(self, textvariable=self.goods_code)
    nameEntered.focus() # 当程序运行时,光标默认会出现在该文本框中    
    nameEntered.pack(side='left', fill='both', expand='yes')    
    
    tk.Label(self, text="商品：", **kw).pack(side='left', fill='both', expand='yes')
    self.goods_name = tk.StringVar()    
    goods_name_lable = tk.Label(self, textvariable=self.goods_name, relief='flat', bg='black', fg='white'  )
    goods_name_lable.pack(side='left', fill='both', expand='yes')
    tk.Label(self, text="数量：", **kw).pack(side='left', fill='both', expand='yes')
    tk.Entry(self).pack(side='left', fill='both', expand='yes')
    
    # 给文件加下划线
    underline_font = tkFont.Font(goods_name_lable, goods_name_lable.cget("font"))
    underline_font.configure(underline=True)
    goods_name_lable.configure(font=underline_font)    
    
    #print underline_font.cget('family'), underline_font.cget('size'), underline_font.cget('weight')
    #="times", size=30, weight=NORMAL

   # membernoLab.pack(side='left')  
   # memnameLab.pack(side='left')  
   # memtypeLab.pack(side='left')      
    
    self.grid(row=1, column=0,  sticky='wens')
    
    # 绑定 回车 查询条码
    #给输入框绑定按键监听事件<Key>为监听任何按键 <Key-x>监听其它键盘，如大写的A<Key-A>、回车<Key-Return>
    nameEntered.bind('<Key-Return>', self.search_goods)    
    #self.master.master.bind("<F10>", self.search_goods)    
    
  # 通过条形码查询商品
  def search_goods(self, event=None):
    # todo 调用查询接口
    rs = agent.payagent.search_goods_by_code(self.goods_code.get())    
    if rs != None:
      # 商品编号 商品名称 单位 规格 零售价 会员价 折扣
      goods_barcode, goods_name, unit, specs, sale_price, member_price, discount = rs
      self.goods_name.set(goods_name)  
      ordinal = len(spreadsheet.get_children()) + 1
      # 实售价 数量 金额  （需要计算的） sold_price   volume   Amount
      sold_price = Decimal(sale_price * discount).quantize(Decimal('0.00'))
      volume = 1
      amount = sold_price * volume  
            
      print ordinal, goods_barcode, goods_name, unit, specs, sale_price, member_price, discount, sold_price, volume, amount
      
      # 需要插入一行标识
      add_flag = True
      sheet = spreadsheet.get_children()
      for i in sheet:
        # 判断条码是否已经存在  
        if goods_barcode == spreadsheet.item(i,'values')[1]:
          add_flag = False
          # 序号 商品编号 商品名称 单位 规格 零售价 会员价 折扣 实售价 数量 金额
          sold_price = spreadsheet.item(i,'values')[8]
          volume = spreadsheet.item(i,'values')[9]
          print 'old volume ' , volume , sold_price
          # TODO 更新数量  录入数量 未取值 
          volume = int(volume) + 1
          amount = Decimal(sold_price) * volume       
          spreadsheet.set(i, column='volume', value=volume)
          spreadsheet.set(i, column='amount', value=amount)
          
      if add_flag:
        spreadsheet.insert('','end',values=(ordinal, goods_barcode, goods_name, unit, specs, sale_price, member_price, discount, sold_price, volume, amount )  )  
        
        # python2.x  unicode 编码 （中文乱码的问题 ）
        #li = [ '12', u'王记 ', u' 男 ', u'王记 ' ,'12' , ' 11 ','12', '13 ', '9.9', '1 ' ,'12' ]
        #spreadsheet.insert('', 'end', values =li )
    
        
      # 添加成功清除条形码
      self.goods_code.set("")   
      
      # 计算合计
      total_volume = 0
      total_sale_amount = 0
      total_amount = 0      
      for k in spreadsheet.get_children():      
        sale_price = spreadsheet.item(k,'values')[5]
        amount = spreadsheet.item(k,'values')[10]
        volume = spreadsheet.item(k,'values')[9]
        total_volume += int(volume)
        total_sale_amount += Decimal(sale_price) * int(volume) 
        total_amount += Decimal(amount)
        print k , sale_price, volume, amount
        
      print 'total: ', len(spreadsheet.get_children()), total_volume , total_amount , k 
      
      # 更新合计
      self.master.totalbar.orgtotal.set(total_sale_amount)     
      self.master.totalbar.curtotal.set(total_amount)      
      
    
#  状态栏
class Statusbar(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)

    tk.Label(self, text="流水号：", **kw).pack(side='left', fill='both', expand='yes')
    tk.Label(self, text='need to do something', **kw).pack(side='left',fill='both', expand='yes')
    tk.Label(self, text="网络状况：", **kw).pack(side='left',fill='both', expand='yes')
    
    tk.Label(self, text='need to do something', **kw).pack(side='left',fill='both', expand='yes')    
    
    
    
    
    tk.Label(self, text="挂单：", **kw).pack(side='left',fill='both', expand='yes')
    tk.Label(self, text='need to do something', **kw).pack(side='left',fill='both', expand='yes')               
    
    self.grid(row=2, column=0, sticky='wens')    
    

#  合计栏
class Totalbar(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)   

    tk.Label(self, text="原价\n合计", **kw).grid(row=0, column=0, sticky='wens')    
    tk.Label(self, text=":", **kw).grid(row=0, column=1, sticky='wens')        
    self.orgtotal = tk.StringVar()
    tk.Label(self, textvariable=self.orgtotal, relief='flat', bg='black', fg='white', font=('Arial', 20, 'bold')).grid(row=0, column=2, sticky='wens')    
    
    tk.Label(self, text="应收\n合计", **kw).grid(row=0, column=3, sticky='wens')    
    tk.Label(self, text=":", **kw).grid(row=0, column=4, sticky='wens')    
    self.curtotal = tk.StringVar()    
    tk.Label(self, textvariable=self.curtotal , relief='flat',bg='black', fg='red', font=('Arial', 20, 'bold')).grid(row=0, column=5, sticky='wens')    
    
    #TODO  TEST  delete  
    self.orgtotal.set(0.00)     
    self.curtotal.set(0.00)      
     
    
    # Grid 分配比例
    self.columnconfigure(0, weight=2)   # 原价
    self.columnconfigure(1, weight=1)   #  :
    self.columnconfigure(2, weight=4)   # 金额 
    self.columnconfigure(3, weight=2)   # 应收
    self.columnconfigure(4, weight=1)   #  :  
    self.columnconfigure(5, weight=4)   # 金额 


    self.rowconfigure(0, weight=1)
    
    ''' 
    self.rowconfigure(0, weight=200)
    self.rowconfigure(1, weight=2)
    self.rowconfigure(2, weight=1)
    '''
    
    self.grid(row=1, column=1, rowspan=2, sticky='wens')    
    
    

# 帮助栏
class helpBar(tk.Frame):
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master)   
    self['background']='black'   
     
    tk.Label(self, text="结算 +           ", **kw).pack()       
    tk.Label(self, text="挂单 F8          ", **kw).pack()      
    tk.Label(self, text="取单 F9          ", **kw).pack()      
    tk.Label(self, text="删除 Del         ", **kw).pack()      
    tk.Label(self, text="全清 F12         ", **kw).pack()      
    tk.Label(self, text="赠品 F5          ", **kw).pack()      
    tk.Label(self, text="改数量 F1        ", **kw).pack()      
    tk.Label(self, text="改单位 F2        ", **kw).pack()      
    tk.Label(self, text="改单价 F3        ", **kw).pack()      
    tk.Label(self, text="改顾客 F4        ", **kw).pack()      
    tk.Label(self, text="读会员卡 Home    ", **kw).pack()      
    tk.Label(self, text="顾客退货 F10     ", **kw).pack()      
    tk.Label(self, text="开钱箱 F6        ", **kw).pack()      
    tk.Label(self, text="锁屏 CtrL + L    ", **kw).pack()      
    tk.Label(self, text="重打小票 Ctrl + P", **kw).pack()      
    tk.Label(self, text="单项打折 Ctrl + X", **kw).pack()      
    tk.Label(self, text="全部打折 Ctrl + A", **kw).pack()      
    tk.Label(self, text="新建顾客 Ctrl + Z", **kw).pack()  
    
    self.grid(row=0, column=2,  rowspan=3, sticky='wens')
    
    
# 版权    
class Copyright(tk.Frame):
  def __init__(self, master=None,**kw):
    tk.Frame.__init__(self, master)    
    copyright = tk.Label(self, text='Copyright © 2019 xxxx Systems Corporation. All rights reserved.  Tel：400-xxxx-xxxx  Email: suport@sss.com', **kw)
    copyright.pack()    
    self.pack(side='bottom')      
    

class Application(tk.Frame):
    
  def __init__(self, master=None, **kw):
    tk.Frame.__init__(self, master, **kw )
    header = CasherHeader(bg="black", fg="white")  # 台头信息
    MemberBar()  # 台头信息
    #Copyright(top,height=120,width=60,relief=RIDGE, bg='#ff3399',bd=5,borderwidth=4) , 
    self.mainPage = MainPage()
    Copyright(bg="black", fg="white")
    #self.pack(fill='both', expand='yes')
    #header.tick()  
    #self.grid()
    self.pack(padx=0, pady=0)
    
    # python Tkinter 全屏显示
    self.state = False
    self.master.bind("<F11>", self.toggle_fullscreen)
    #self.master.bind("<Escape>", self.end_fullscreen)  
    
    #结算
    self.master.bind("<F2>", self.checkout)       
    
    
  # 窗口全屏 
  def toggle_fullscreen(self, event=None):
    self.state = not self.state  # Just toggling the boolean
    self.master.attributes("-fullscreen", self.state)     

  def end_fullscreen(self, event=None):
    self.state = False
    self.master.attributes("-fullscreen", False)
      
  # 结算
  def checkout(self, event=None):
    ''' 
    #锁定输入框    
    edit_entry_dict = self.mainPage.entrypage.children    
    #  一定要是一个tuple 类型数据 否则会提
    for k in edit_entry_dict.iterkeys():
      item_entry = edit_entry_dict[k]
      if isinstance(item_entry, tk.Entry):       
        item_entry.config(state='disabled')  
    '''                   
    # 打开结算窗口     
    PopupDialog(self)         
    # 禁用主窗口
    self.master.attributes("-disabled",True)   
    #设置主窗口 must be normal, iconic, withdrawn, or zoomed   
    #self.master.state(newstate='zoomed')  


#登陆页面
class LoginPage(tk.Frame):

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)    
    
    self.master.title('Welcome to Mofan Python')
    
    #设置屏幕正中      
    width, height = self.master.maxsize()
    width = width/3
    height = height/3    
    screenwidth = self.master.winfo_screenwidth()
    screenheight = self.master.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)    
    self.master.geometry(size)
    
    print width ,  height
    
    # welcome image
    
    def get_pic(pic_code):  
      image = open('new_app.gif', 'wb+')
      image.write(base64.b64decode(memory_pic.welcome_gif))      
      #image = open(memory_pic.welcome_gif, 'wb')    
      #image.write(base64.b64decode(pic_code))
      image.close()
    
    # 在这里使用图片 icon.ico
    #os.remove('icon.ico')    

    canvas = tk.Canvas(self, height= height/2, width=500)
    # Escape / raw string literal
    get_pic('welcome_gif') 
    #self.image_file = image_file  # to prevent the image garbage collected.
    
    bin_img_data = base64.b64decode(memory_pic.welcome_gif)
    #file_like = io.BytesIO(bin_img_data)
    #file_like.read()    
    #img = Image.open(file_like)
    #with open('welcome.gif', 'rb') as f: 
    #  data = f.read()
    #self.image_file = tk.PhotoImage(format="gif", data=data)          
    self.image_file = tk.PhotoImage(file=r'new_app.gif')
    image = canvas.create_image(0,0, anchor='nw', image=self.image_file)
    canvas.grid(row=0, column=0, columnspan=2, pady=5, sticky='wens')    
    os.remove('new_app.gif')    
    
    # user information
    tk.Label(self, text='User name: ').grid(row=1, column=0, pady=5, sticky='ens')  #.place(x=50, y= 150)
    
    var_usr_name = tk.StringVar()
    var_usr_name.set('example@python.com')
    entry_usr_name = tk.Entry(self, textvariable=var_usr_name)
    entry_usr_name.grid(row=1, column=1, pady=5, sticky='wens')   # .place(x=160, y=150)
    
    tk.Label(self, text='Password: ').grid(row=2, column=0, pady=5, sticky='ens')    #.place(x=50, y= 190)    
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(self, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.grid(row=2, column=1, pady=5, sticky='wens')   #.place(x=160, y=190)    
    
    
    def usr_login():
      usr_name = var_usr_name.get()
      usr_pwd = var_usr_pwd.get()
      
      
      # 如登陆成功， 关闭当前页面跳转 
      self.master.destroy()          
      # 主页面
      app = Application(relief='ridge', bg='black') 
      app.master.title('Sample application')
      app.master['background']='black'
      app.master['bd']='0px'
    
      
      #通过register方法转换为validatecommand选项能接收的函数
      #check_amount_fun = app.master.register(digital_check)  
                    
      '''    
      # 插入表格数据
      for i in range(10):
        #tree.insert('',i,values=('a'+str(i),'b'+str(i),'c'+str(i)))  
        tree.insert('','end',values=('a'+str(i),'b'+str(i),'c'+str(i)))  
      
      ''' 
      
      '''   '''
      # 全屏 方法一
      w, h = app.master.maxsize()
      app.master.geometry("{}x{}+0+0".format(w-15, h-75))   
      # app.master.geometry("{}x{}".format(w-15, h-40)) 
      # app.master.attributes("-topmost",True)    
      
      '''  
      # 全屏 方法三
      app.master.attributes("-fullscreen", True)
      '''
            
      #rbFenxi = tk.Button(app.master, text="结算", command = lambda: btn_def(e1.get(), e2.get()))      
      app.mainloop()


    
    # login and sign up button
    btn_login = tk.Button(self, text='Login', command=usr_login)
    btn_login.grid(row=3, column=0, columnspan=2, pady=5, sticky='wens')
    btn_sign_up = tk.Button(self, text='Sign up')
    btn_sign_up.grid(row=4, column=0, columnspan=2, pady=5, sticky='wens')  
    
    
    # Grid 分配比例
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=10)    
    self.pack()
    #self.createWidgets()    
  
        
  def say_hi(self):
    print "hi there, everyone!"

  def createWidgets(self):
    self.QUIT = tk.Button(self)
    self.QUIT["text"] = "QUIT"
    self.QUIT["fg"]   = "red"
    self.QUIT["command"] =  self.quit

    self.QUIT.pack({"side": "left"})

    self.hi_there = tk.Button(self)
    self.hi_there["text"] = "Hello",
    self.hi_there["command"] = self.say_hi

    self.hi_there.pack({"side": "left"})




if __name__ == "__main__":    
  # 本地时间
  local_time = ''
  
  #root = Tk()
  #root.title('my window')
  #root.geometry('300x300')
  loginPage = LoginPage()
  loginPage.mainloop()
  #root.destroy()  
  
  ''' 

 
  '''


