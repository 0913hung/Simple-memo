import tkinter as tk
import json

class Example(tk.Frame):
	def __init__(self, root):
		tk.Frame.__init__(self, root)
		#tk.Frame.overrideredirect(True)
		b1 = tk.Button(self,border=0,bg='cornflowerblue', font=('Arial', 10),fg='white', text="Close", command = self.close)
		b1.place(x=110, y=5)
		b2 = tk.Button(self,border=0,bg='cornflowerblue', font=('Arial', 10),fg='white', text="Full", command = self.toggle_fill)
		b2.place(x=77, y=5)
		b3 = tk.Button(self,border=0,bg='cornflowerblue', font=('Arial', 10),fg='white', text="Save", command = self.save)
		b3.place(x=37, y=5)
		b4 = tk.Button(self,border=0,bg='cornflowerblue', font=('Arial', 10),fg='white', text="New", command = self.newWin)
		b4.place(x=0, y=5)
		#self.count = 0
		self.win_list=[]
		self.value_list=[]
		self.size_list=[]
		self.create()
		self.overrideredirect=False
		
		
	def create(self):
		with open("memo_content.txt", "r") as data:
			data=json.load(data)
			for i in data:
				self.newWindow(i)
				

	def newWindow(self,value):
		window = tk.Toplevel(self, bg='yellow')
		window.title('')
		#window.geometry('100x70+0+0')
		
		
		#if width<300:
		#	width=300
		window.geometry(value['size'])
		label = tk.Text(window, bg='yellow', font=('Arial', 14), width=20, height=5)
		label.pack(side="top", fill="both", expand=True)
		label.insert(tk.END,value['data'])
		#label.bind("<B3-Motion>", lambda event,label=window:self.move_me(event,label))
		#window.bind("<B3-Motion>",self.move_me)
		#window.bind("<Button-3>", self.getlocation)
		self.value_list.append(label)
		self.win_list.append(window)
		
	
	def toggle_fill(self):
		value=self.overrideredirect
		for i in self.win_list:
			if value:
				i.overrideredirect(False)
				self.overrideredirect=False
			else:
				i.overrideredirect(True)
				self.overrideredirect=True
				
	def save(self):		
		value=[]
		with open("memo_content.txt", "w") as data:
			for i,j in zip(self.value_list,self.win_list):
				try:
					value.append({"data":i.get("1.0", "end"),"size":j.geometry()})
				except:
					pass
			data.write(json.dumps(value))
	
	def newWin(self):
		self.newWindow({'data':'','size':''})
	
	def close(self):
		self.save()
		root.destroy()
	
	def getlocation(self,event):
		widget=event.widget
		self.x=widget.master.winfo_x()
		self.y=widget.master.winfo_y()
		print('location:')
		print(self.x,self.y)
		
	def move_me(self, event):
		label=event.widget
		x = event.x+self.x
		y = event.y+self.y
		location='+{}+{}'.format(x,y)
		label.master.geometry(location)
		#print(self.x,self.y)
		print(location)
		#print(label.master.geometry())

			

if __name__ == "__main__":
	root = tk.Tk()
	
	root.geometry('170x40+1770+860')
	root.attributes('-topmost', 'true')
	root.overrideredirect(True)
	Example(root).pack(side="top", fill="both", expand=True)
	root.mainloop()

