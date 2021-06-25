# tkinter+scoket 实现局域网单聊（服务端）

from socket import *
from tkinter import Frame, Button, END, Tk, messagebox, scrolledtext, Entry, Label
import time
import threading


# 获取ip的窗口
class InputIPdialog(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.ip = Label(self, text="输入服务器IP")
		self.ip.grid(row=0, column=0, columnspan=2)

		self.ipInput = Entry(self, width=20)
		self.ipInput.grid(row=1, column=1)
		self.ipInput.bind("<KeyPress-Return>", self.ok)

		self.ipInput.bind("<KeyPress-Return>", self.ok)

		self.okbtn = Button(self, text='确定', command=self.setIP).grid(row=2, column=0, columnspan=2)
		self.grid()

	def setIP(self):
		global servername
		servername = self.ipInput.get()
		# 销毁窗口
		ipRootFrame.destroy()

	def ok(self, event):
		if event.keysym == "Return":
			self.setIP()


class Application(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		# 显示聊天窗口
		self.textEdit = scrolledtext.ScrolledText(self, width=50, height=15)
		self.textEdit.grid(row=0, column=0, rowspan=1, columnspan=4)
		# 定义标签，改变字体颜色
		self.textEdit.tag_config('red', foreground='#003366')
		self.textEdit.tag_config('blue', foreground='#CC3333')
		self.textEdit.tag_config('text', foreground='#444444')

		# 编辑窗口
		self.inputText = Entry(self, width=40)
		self.inputText.grid(row=1, column=0, columnspan=1)
		# 定义快捷键，按下回车即可发送消息
		self.inputText.bind("<KeyPress-Return>", self.textSendReturn)
		# 发送按钮
		self.btnSend = Button(self, text='send', width=10, command=self.textSend)
		self.btnSend.grid(row=1, column=3)
		# 开启一个线程用于接收消息并显示在聊天窗口
		t = threading.Thread(target=self.getInfo)
		t.start()

	def textSend(self):
		# 获取Text的所有内容
		str = self.inputText.get()
		if str != "":
			# 显示发送时间和发送消息
			timemsg = "小红 " + time.strftime('%m-%d %H:%M:%S', time.localtime()) + '\n'
			self.textEdit.config(state='normal')
			self.textEdit.insert(END, timemsg, 'blue')
			self.textEdit.insert(END, str + '\n', 'text')
			# 将滚动条拉到最后显示最新消息
			self.textEdit.see(END)
			self.textEdit.config(state='disabled')
			# 删除输入框的内容
			self.inputText.delete(0, END)
			# 发送数据到服务端
			sendMessage = bytes(str, encoding='utf8')
			# 发送输入的数据
			connectionSocket.send(sendMessage)

		else:
			messagebox.showinfo('警告', "不能发送空白信息！")

	def getInfo(self):
		while True:
			print("开始监听")
			recMsg = connectionSocket.recv(1024).decode("utf-8") + '\n'
			print("本次监听结束")
			revTime = '小蓝 ' + time.strftime('%m-%d %H:%M:%S', time.localtime()) + '\n'
			# 通过设置state属性设置textEdit可编辑
			self.textEdit.config(state='normal')
			self.textEdit.insert(END, revTime, 'red')
			self.textEdit.insert(END, recMsg, 'text')
			# 将滚动条拉到最后显示最新消息
			self.textEdit.see(END)
			# 通过设置state属性设置textEdit不可编辑
			self.textEdit.config(state='disabled')

	def textSendReturn(self, event):
		if event.keysym == "Return":
			self.textSend()


servername = ''

serverPort = 12000
ipRootFrame = Tk()

ipDialog = InputIPdialog(ipRootFrame)
ipDialog.mainloop()

root = Tk()
root.title("小红")

serverSocket = socket(AF_INET, SOCK_STREAM)

try:
	# 绑定端口
	serverSocket.bind((servername, serverPort))
	# 定义最大连接数
	serverSocket.listen(1)
	print('等待连接....')
	# 接受请求则建立一个连接
	connectionSocket, addr = serverSocket.accept()
except:
	messagebox.showinfo('未知错误', '检查服务器地址是否错误！')
	exit()

app = Application(master=root)

app.mainloop()
