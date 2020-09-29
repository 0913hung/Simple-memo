import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
import json
import os
import getpass
from photo import *
import base64
from io import BytesIO


class Example(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)

		self.win_list = [] #contain a list of Toplevel object
		self.memo_list = [] #contain a list of Label object
		self.hidden = []
		
		if os.path.isdir('D:\\'):
			self.path="D:\\memo_data"
		else:
			self.path=r'C:\Users\%s\desktop\memo_data' % getpass.getuser()

		self.overrideredirect = False
		self._offsetx = 0
		self._offsety = 0
		self.counter = 0
		self.create()
		
		

	def create(self):
		try:
			with open(self.path, "r") as data:
				data = json.load(data)
				if data:
					for i in data:
						self.new_window(i)
				else:
					print('no data')
					self.new_blank_window()
		except:
			with open(self.path, "w"):pass
			self.new_blank_window()

	def new_window(self, value):
		window = tk.Toplevel(self, bg='yellow')
		window.title('Memo')
		window.overrideredirect(True)
		window.geometry(value['size'])

		# outter frame, contain all component
		mainFrame = tk.Frame(window, bg='yellow')
		mainFrame.pack(fill="both", expand=True)

		# bottom frame, contain all bottom
		button_frame = tk.Frame(mainFrame, height=115)
		#button_frame.pack(side='bottom', expand=False)

		memo = tk.Text(mainFrame, bg='yellow', border=0, font=('Arial', value['font_size']), width=1, height=1)
		memo.pack(fill="both", expand=True)
		memo.insert(tk.END, value['data'])
		memo.bind("<B3-Motion>", lambda event, window=window: self.dragwin(event, window))
		#memo.bind("<Control-s>", self.save)
		
		
		self.memo_list.append(memo)
		self.win_list.append(window)
		self.hidden.append(False)
		
		

		window.bind("<Enter>", lambda event, button_frame=button_frame,window=window: self.show(event, button_frame,window))
		window.bind("<Leave>", lambda event, button_frame=button_frame, window=window: self.hide(event, button_frame, window))
		window.bind("<Button-3>", self.clickwin)
		
		
		
		icon_delete = tk.PhotoImage(data=code_delete)
		icon_new= tk.PhotoImage(data=code_new)
		icon_save= tk.PhotoImage(data=code_save)
		icon_bigger= tk.PhotoImage(data=code_bigger)
		icon_smaller= tk.PhotoImage(data=code_smaller)
		icon_close= tk.PhotoImage(data=code_close)

		close = tk.Button(button_frame, command=lambda window=window,memo=memo: self.delete(window,memo))
		new = tk.Button(button_frame, command=self.new_blank_window)
		
		save = tk.Button(button_frame, command=self.save)
		front_increse = tk.Button(button_frame, command=lambda memo=memo: self.font_changer(memo, 1))
		front_decrest = tk.Button(button_frame, command=lambda memo=memo: self.font_changer(memo, -1))
		close_all = tk.Button(button_frame, command=self.close)
		
		
		
		close.configure(border=0, bg='yellow',image=icon_delete)
		close.image=icon_delete
		new.configure(border=0, bg='yellow',image=icon_new)
		new.image=icon_new
		save.configure(border=0, bg='yellow',image=icon_save)
		save.image=icon_save
		front_increse.configure(border=0, bg='yellow',image=icon_bigger)
		front_increse.image=icon_bigger
		front_decrest.configure(border=0, bg='yellow',image=icon_smaller)
		front_decrest.image=icon_smaller
		close_all.configure(border=0, bg='yellow',image=icon_close)
		close_all.image=icon_close

		new.pack(side='left')
		save.pack(side='left')
		front_increse.pack(side='left')
		front_decrest.pack(side='left')
		close.pack(side='left')
		close_all.pack(side='left')


		memo = tk.Label(button_frame, text="X")
		save.pack(side='left')

		grip = tk.ttk.Sizegrip(window)
		grip.place(relx=1.0, rely=1.0, anchor="se")
		grip.lift(memo)
		grip.bind("<B1-Motion>", lambda event, window=window: self.on_motion(event, window))

	def delete(self, window,memo):
		message = tk.messagebox.askquestion('Delete', 'Confirm delete', icon='warning')
		if message == 'yes':
			window.destroy()
			index=self.win_list.index(window)
			self.win_list.remove(window)
			self.memo_list.remove(memo)
			self.hidden[index]=None
			
			if len(self.win_list) ==0:
				root.destroy()
			else:
				self.save()
		else:
			return

	def font_changer(self, memo, value):
		size = memo['font'].split(' ')
		size = int(size[1]) + value
		memo['font'] = ('Arial', size)

	def on_motion(self, event, window):
		x1 = window.winfo_pointerx()
		y1 = window.winfo_pointery()
		x0 = window.winfo_rootx()
		y0 = window.winfo_rooty()
		window.geometry("%sx%s" % ((x1 - x0), (y1 - y0)))
		return

	def show(self, event, button_frame,window):
		index=self.win_list.index(window)
		button_frame.pack(side='bottom', expand=False)
		self.hidden[index] = False

	def hide(self, event, button_frame, window):
		index = self.win_list.index(window)
		self.hidden[index] = True

		def a(self, button_frame, window):
			if self.hidden[index]:
				button_frame.forget()
				window.attributes('-topmost', False)
				self.hidden[index]= True

		window.after(50, lambda self=self, button_frame=button_frame, window=window: a(self, button_frame, window))

	def save(self):
		values = []
		with open(self.path, "w") as data:
			for i, j in zip(self.memo_list, self.win_list):
				value = i.get("1.0", "end")
				if value and value != "\n":
					font_size = i['font'].split(' ')
					values.append({"data": i.get("1.0", "end"), "size": j.geometry(), "font_size": font_size[1]})
			data.write(json.dumps(values))

	def new_blank_window(self):
		self.new_window({'data': '', 'size': '160x86+953+513', 'font_size': 14})

	def close(self):
		message = tk.messagebox.askquestion('Close', 'Confirm Close', icon='warning')
		if message == 'yes':
			self.save()
			root.destroy()
		else:
			return

	def dragwin(self, event, window):
		x = self.winfo_pointerx() - self._offsetx
		y = self.winfo_pointery() - self._offsety
		window.geometry('+{x}+{y}'.format(x=x, y=y))

	def clickwin(self, event):
		self._offsetx = event.x
		self._offsety = event.y

USER_NAME = getpass.getuser()
def add_to_startup():
	file_path = r'D:\Users\%s\desktop' % USER_NAME
	bat_path = r'D:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
	if not os.path.isdir(bat_path):
		bat_path=r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
		file_path = r'C:\Users\%s\desktop' % USER_NAME
	with open(bat_path + '\\' + "memo.bat", "w+") as bat_file:
		bat_file.write(r'start "" "%s\memo.exe"' % file_path)

if __name__ == "__main__":
	add_to_startup()
	root = tk.Tk()
	root.overrideredirect(True)
	Example(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
