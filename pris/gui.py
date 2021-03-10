import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os, mouse
from tkinter import font

SLST_CHILL = 0
SLST_SELECTING1 = 1
SLST_SELECTING2 = 2

CHSE_FS = 1
CHSE_OWN = 2

class GUI:
    sel_state = SLST_CHILL

    def __init__(self, title):
        self.root = tk.Tk(title)
        self.root.geometry("500x300")
        self.root.title(title)
        self.root.resizable(width=0, height=0)

        #Загрузка картинки
        bg_img = Image.open(os.path.join("res", 
            "bg_border.png"))
        bg_img = ImageTk.PhotoImage(bg_img)

        lab_img = tk.Label(self.root, image=bg_img)
        lab_img.photo = bg_img
        lab_img.place(x=5,y=5)

        style = ttk.Style()
        style.configure("my.TButton", font=("Helvetica", 18))
        #============================================

        #Выбор для одной точки
        def choose_point1():
            self.sel_state = SLST_SELECTING1
        btn_choose1 = ttk.Button(text="✛", style="my.TButton",
            command=choose_point1)
        btn_choose1.config(width=2)
        btn_choose1.place(x=5,y=5)
        #X и Y
        btn_choose1_X_label = ttk.Label(self.root,
            text="X: ")
        btn_choose1_X = ttk.Entry(self.root, width=7)
        btn_choose1_X_label.place(x=45, y=5)
        btn_choose1_X.place(x=60, y=5)

        btn_choose1_Y_label = ttk.Label(self.root,
            text="Y: ")
        btn_choose1_Y = ttk.Entry(self.root, width=7)
        btn_choose1_Y_label.place(x=110, y=5)
        btn_choose1_Y.place(x=125, y=5)
        #============================================

        #Выбор для другой точки
        def choose_point2():
            self.sel_state = SLST_SELECTING2
        btn_choose2 = ttk.Button(text="✛", style="my.TButton",
            command=choose_point2)
        btn_choose2.config(width=2)
        btn_choose2.place(x=275,y=175)
        #X и Y
        btn_choose2_X_label = ttk.Label(self.root,
            text="X: ")
        btn_choose2_X = ttk.Entry(self.root, width=7)
        btn_choose2_X_label.place(x=110, y=187)
        btn_choose2_X.place(x=125, y=187)

        btn_choose2_Y_label = ttk.Label(self.root,
            text="Y: ")
        btn_choose2_Y = ttk.Entry(self.root, width=7)
        btn_choose2_Y_label.place(x=175, y=187)
        btn_choose2_Y.place(x=190, y=187)
        #============================================

        #Выбор размер или фуллскрин
        self.chosen_opt = tk.IntVar()
        def on_fs():
            btn_choose1.config(state="disabled")
            btn_choose1_X.config(state="disabled")
            btn_choose1_Y.config(state="disabled")

            btn_choose2.config(state="disabled")
            btn_choose2_X.config(state="disabled")
            btn_choose2_Y.config(state="disabled")
        on_fs()
        full_screen_rbutton = ttk.Radiobutton(text="Весь экран",value=CHSE_FS,
            variable=self.chosen_opt, command=on_fs)

        def on_own():
            btn_choose1.config(state="enabled")
            btn_choose1_X.config(state="enabled")
            btn_choose1_Y.config(state="enabled")

            btn_choose2.config(state="enabled")
            btn_choose2_X.config(state="enabled")
            btn_choose2_Y.config(state="enabled")            
        own_rbutton = ttk.Radiobutton(text="Свой выбор",value=CHSE_OWN,
            variable=self.chosen_opt, command=on_own)
        full_screen_rbutton.place(x=110,y=85)
        own_rbutton.place(x=110, y=105)
        self.chosen_opt.set(1)
        #============================================

        #Подсказки
        hint_lbl1 = ttk.Label(text="В режиме выбора области нажмите на кнопку \"✛\",\n"+
                                   "чтобы кликом средней кнопки мыши(колесиком)\n"+
                                   "выбрать угол для прямоугольника, который\n"+
                                   "обрежет всё, что вне его границ.")
        hint_lbl1.place(x=10, y=220)
        #============================================

        #Выбираем позицию с помощью клика средней кнопки мыши
        def on_choose_click():
            posx, posy = mouse.get_position()
            if self.sel_state == SLST_SELECTING1:
                btn_choose1_X.delete(0, tk.END)
                btn_choose1_X.insert(tk.END, str(posx))
                btn_choose1_Y.delete(0, tk.END)
                btn_choose1_Y.insert(tk.END, str(posy))
                self.sel_state = SLST_CHILL
            elif self.sel_state == SLST_SELECTING2:
                btn_choose2_X.delete(0, tk.END)
                btn_choose2_X.insert(tk.END, str(posx))
                btn_choose2_Y.delete(0, tk.END)
                btn_choose2_Y.insert(tk.END, str(posy))
                self.sel_state = SLST_CHILL
        mouse.on_middle_click(on_choose_click)
        #============================================

    def start(self):
        self.root.mainloop()