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
		
		
	def create(self):
		with open("memo_content.txt", "r") as data:
			data=json.load(data)
			for i in data:
				self.newWindow(i)
				

	def newWindow(self,value):
		window = tk.Toplevel(self, bg='yellow')
		
		width=window.winfo_reqwidth()
		height=window.winfo_reqheight()
		
		#if width<300:
		#	width=300
		window.geometry(value['size'])
		label = tk.Text(window, bg='yellow', font=('Arial', 14))
		label.pack(side="top", fill="both", expand=True)
		label.insert(tk.END,value['data'])
		self.value_list.append(label)
		self.win_list.append(window)
		
	
	def toggle_fill(self):
		for i in self.win_list:
			#print(i.geometry())
			#print(i.overrideredirect())
			if not i.overrideredirect():
				i.overrideredirect(True)
			else:
				i.overrideredirect(False)
				
	def save(self):		
		value=[]
		with open("memo_content.txt", "w") as data:
			for i,j in zip(self.value_list,self.win_list):				
				value.append({"data":i.get("1.0", "end"),"size":j.geometry()})
			data.write(json.dumps(value))
	
	def newWin(self):
		self.newWindow({'data':'','size':''})
	
	def close(self):
		self.save()
		root.destroy()
		

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry('170x40+1770+860')
	root.attributes('-topmost', 'true')
	root.overrideredirect(True)
	Example(root).pack(side="top", fill="both", expand=True)
	root.mainloop()

