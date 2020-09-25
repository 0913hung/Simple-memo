import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
import json
import os
import getpass


class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.win_list = [] #contain a list of Toplevel object
        self.memo_list = [] #contain a list of Label object
        self.hidden = False

        self.overrideredirect = False
        self._offsetx = 0
        self._offsety = 0
        self.counter = 0
        self.create()

    def create(self):
        print(os.path.exists("memo_content"))
        try:
            with open("memo_content", "r") as data:            
                data = json.load(data)
                if not len(data)==0:
                    for i in data:
                        self.new_window(i)
                else:
                    raise Exception()
        except:
            if not os.path.exists("memo_content"):
                with open("memo_content", "w"):pass
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
        button_frame.pack(side='bottom', expand=False)

        memo = tk.Text(mainFrame, bg='yellow', border=0, font=('Arial', value['font_size']), width=1, height=1)
        memo.pack(fill="both", expand=True)
        memo.insert(tk.END, value['data'])
        memo.bind("<B3-Motion>", lambda event, window=window: self.dragwin(event, window))

        window.bind("<Enter>", lambda event, button_frame=button_frame: self.show(event, button_frame))
        window.bind("<Leave>", lambda event, button_frame=button_frame, window=window: self.hide(event, button_frame, window))
        window.bind("<Button-3>", self.clickwin)

        close = tk.Button(button_frame, command=lambda window=window: self.delete(window))
        new = tk.Button(button_frame, command=self.new_blank_window)
        save = tk.Button(button_frame, command=self.save)
        front_increse = tk.Button(button_frame, command=lambda memo=memo: self.font_changer(memo, 1))
        front_decrest = tk.Button(button_frame, command=lambda memo=memo: self.font_changer(memo, -1))

        close.configure(width=4, border=0, bg='cornflowerblue', font=('Arial', 8), fg='white', text="Del")
        new.configure(width=4, border=0, bg='cornflowerblue', font=('Arial', 8), fg='white', text="New")
        save.configure(width=4, border=0, bg='cornflowerblue', font=('Arial', 8), fg='white', text="Save")
        front_increse.configure(width=2, border=0, bg='cornflowerblue', font=('Arial', 8), fg='white', text="+")
        front_decrest.configure(width=2, border=0, bg='cornflowerblue', font=('Arial', 8), fg='white', text="-")

        new.pack(side='left', padx=1)
        save.pack(side='left', padx=1)
        front_increse.pack(side='left', padx=1)
        front_decrest.pack(side='left', padx=1)
        close.pack(side='left', padx=1)

        self.memo_list.append(memo)
        self.win_list.append(window)

        memo = tk.Label(button_frame, text="X")
        save.pack(side='left', padx=1)

        grip = tk.ttk.Sizegrip(window)
        grip.place(relx=1.0, rely=1.0, anchor="se")
        grip.lift(memo)
        grip.bind("<B1-Motion>", lambda event, window=window: self.on_motion(event, window))

    def delete(self, memo):
        message = tk.messagebox.askquestion('Delete', 'Confirm delete', icon='warning')
        if message == 'yes':
            memo.destroy()
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

    def show(self, event, button_frame):
        button_frame.pack(side='bottom', expand=False)
        self.hidden = False

    def hide(self, event, button_frame, window):
        self.hidden = True

        def a(self, button_frame, window):
            if self.hidden:
                button_frame.forget()
                window.attributes('-topmost', False)
                self.hidden = True

        window.after(100, lambda self=self, button_frame=button_frame, window=window: a(self, button_frame, window))

    def save(self):
        values = []
        with open("memo_content", "w") as data:
            for i, j in zip(self.memo_list, self.win_list):
                value = i.get("1.0", "end")
                if value and value != "\n":
                    font_size = i['font'].split(' ')
                    values.append({"data": i.get("1.0", "end"), "size": j.geometry(), "font_size": font_size[1]})
            data.write(json.dumps(values))

    def new_blank_window(self):
        self.new_window({'data': '', 'size': '160x86+953+513', 'font_size': 14})

    def close(self):
        self.save()
        root.destroy()

    def dragwin(self, event, window):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        window.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

USER_NAME = getpass.getuser()
def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)

if __name__ == "__main__":
    add_to_startup()
    root = tk.Tk()
    root.overrideredirect(True)
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
