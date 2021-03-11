from tkinter import messagebox as tm
from PIL import Image, ImageTk
from tkinter import font
from mss import mss
from queue import Queue

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tf

import os, mouse, keyboard, traceback, webbrowser
import threading, mss.tools, docx, docx.shared

SLST_CHILL = 0
SLST_SELECTING1 = 1
SLST_SELECTING2 = 2

CHSE_FS = 1
CHSE_OWN = 2

WORK_CHILLING = 0
WORK_WORKING = 1

class GUI:
    sel_state = SLST_CHILL
    work_state = WORK_CHILLING
    extensions = [".docx", ".doc"]

    err_queue = Queue()

    def __init__(self, title, cur_dir):
        self.root = tk.Tk(title)
        self.cur_dir = cur_dir
        self.root.geometry("500x300")
        self.root.title(title)
        self.root.iconbitmap(os.path.join(cur_dir, "res", "icon.ico"))
        self.root.resizable(width=0, height=0)

        #Загрузка картинки
        bg_img = Image.open(os.path.join(cur_dir, "res", 
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
        self.btn_choose1 = ttk.Button(text="✛", style="my.TButton",
            command=choose_point1)
        self.btn_choose1.config(width=2)
        self.btn_choose1.place(x=5,y=5)
        #X и Y
        self.btn_choose1_X_label = ttk.Label(self.root,
            text="X: ")
        self.btn_choose1_X = ttk.Entry(self.root, width=7)
        self.btn_choose1_X_label.place(x=45, y=5)
        self.btn_choose1_X.place(x=60, y=5)

        self.btn_choose1_Y_label = ttk.Label(self.root,
            text="Y: ")
        self.btn_choose1_Y = ttk.Entry(self.root, width=7)
        self.btn_choose1_Y_label.place(x=110, y=5)
        self.btn_choose1_Y.place(x=125, y=5)
        #============================================

        #Выбор для другой точки
        def choose_point2():
            self.sel_state = SLST_SELECTING2
        self.btn_choose2 = ttk.Button(text="✛", style="my.TButton",
            command=choose_point2)
        self.btn_choose2.config(width=2)
        self.btn_choose2.place(x=275,y=175)
        #X и Y
        self.btn_choose2_X_label = ttk.Label(self.root,
            text="X: ")
        self.btn_choose2_X = ttk.Entry(self.root, width=7)
        self.btn_choose2_X_label.place(x=110, y=187)
        self.btn_choose2_X.place(x=125, y=187)

        self.btn_choose2_Y_label = ttk.Label(self.root,
            text="Y: ")
        self.btn_choose2_Y = ttk.Entry(self.root, width=7)
        self.btn_choose2_Y_label.place(x=175, y=187)
        self.btn_choose2_Y.place(x=190, y=187)
        #============================================

        #Выбор размер или фуллскрин
        self.chosen_opt = tk.IntVar()
        def on_fs():
            self.btn_choose1.config(state="disabled")
            self.btn_choose1_X.config(state="disabled")
            self.btn_choose1_Y.config(state="disabled")

            self.btn_choose2.config(state="disabled")
            self.btn_choose2_X.config(state="disabled")
            self.btn_choose2_Y.config(state="disabled")
        on_fs()
        self.full_screen_button = ttk.Radiobutton(text="Весь экран",value=CHSE_FS,
            variable=self.chosen_opt, command=on_fs)

        def on_own():
            self.btn_choose1.config(state="enabled")
            self.btn_choose1_X.config(state="enabled")
            self.btn_choose1_Y.config(state="enabled")

            self.btn_choose2.config(state="enabled")
            self.btn_choose2_X.config(state="enabled")
            self.btn_choose2_Y.config(state="enabled")            
        self.own_rbutton = ttk.Radiobutton(text="Свой выбор",value=CHSE_OWN,
            variable=self.chosen_opt, command=on_own)
        self.full_screen_button.place(x=110,y=85)
        self.own_rbutton.place(x=110, y=105)
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
                self.btn_choose1_X.delete(0, tk.END)
                self.btn_choose1_X.insert(tk.END, str(posx))
                self.btn_choose1_Y.delete(0, tk.END)
                self.btn_choose1_Y.insert(tk.END, str(posy))
                self.sel_state = SLST_CHILL
            elif self.sel_state == SLST_SELECTING2:
                self.btn_choose2_X.delete(0, tk.END)
                self.btn_choose2_X.insert(tk.END, str(posx))
                self.btn_choose2_Y.delete(0, tk.END)
                self.btn_choose2_Y.insert(tk.END, str(posy))
                self.sel_state = SLST_CHILL
        mouse.on_middle_click(on_choose_click)
        #============================================
        
        #Правая сторона программы
        work_frame = ttk.Frame(self.root)
        
        #Сохранение файла
        self.file_label = ttk.Label(work_frame, text="Файл: ")
        self.file_label.grid(row=0, column=1, sticky="w", padx=5)

        self.file_out_path = tk.StringVar()
        self.file_out_path_entry = ttk.Entry(work_frame, textvariable=self.file_out_path)
        self.file_out_path_entry.config(width=28)
        
        self.file_out_path_entry.grid(row=1, column=1, pady=5, padx=5)
        self.save_button = ttk.Button(work_frame, text="Сохранить...", command=self.save_file)
        self.save_button.config(width=15)
        self.save_button.grid(row=2, column=1, padx=5, sticky="nsew")
        #================

        #Ключевая клавиша
        self.key_label = ttk.Label(work_frame, text="Клавиша: ")
        self.key_label.grid(row=3, column=1, sticky="w", padx=5)
        self.key_name = tk.StringVar()
        self.key_name.set("print screen")
        self.key_name_entry = ttk.Entry(work_frame, textvariable=self.key_name)
        self.key_name_entry.grid(row=4, column=1, sticky="nsew", pady=5, padx=5)
        self.key_name_entry.config(state=tk.DISABLED)

        def redefine_button():
            self.key_name.set(keyboard.read_key())
        self.key_button = ttk.Button(work_frame, text="Переназначить", command=redefine_button)
        self.key_button.grid(row=5, column=1, padx=5, sticky="nsew")
        #============================================

        #Ссылка на репозиторий
        self.repo_link = ttk.Label(work_frame, text=
            'https://github.com/alex-\nrusakevich/pris')
        self.repo_link.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
        def open_repo(_):
            webbrowser.open("https://github.com/alex-rusakevich/pris", new=2)
        self.repo_link.bind("<Button-1>", open_repo)

        #Запуск процесса
        self.start_button = ttk.Button(text="Старт!", command=self.start_working)
        self.start_button.place(x=315, y=225, width=175, height=55)

        work_frame.place(x=310, y=5)
        #============================================
        def exception_processing(_):
            if not self.err_queue.empty():
                eq = self.err_queue.get()
                if eq[0] == PermissionError:
                    tm.showerror("Упс!", "Произошла ошибка доступа к файлу. Закройте все программы, в которых используется \""+
                        self.file_out_path.get()+"\" и перезагрузите программу")
                else:
                    tm.showerror("Упс!", "Произошла ошибка "+str(eq[0])+":\n"+str(eq[1])+
                        "\nПерезагрузите программу и попробуйте ещё раз. Если ошибка повторится, пишите на ms.alexander.rusakevich@gmail.com")

                self.err_queue.task_done()
        self.root.bind("<<On error>>", exception_processing)
    
    def back_to_chill(self):
        self.work_state = WORK_CHILLING
        keyboard.unhook_all()
        self.start_button.config(text="Старт!")
        self.change_state("enabled")

    def process(self, err_queue):
        try:
            file_path = self.file_out_path.get().strip()

            #Проверки
            if file_path == "":
                tm.showerror("Ошибка", "Выберите файл")
                self.back_to_chill()
                return
            if not os.path.splitext(file_path)[1] in self.extensions:
                question = tm.askyesno("Предупреждение", "Неправильный тип файла. Хотите создать новый .docx файл с тем же именем?")
                if not question:
                    self.back_to_chill()
                    return
                else:
                    self.file_out_path.set(self.file_out_path.get() + ".docx")
                    file_path += ".docx"
            if not os.path.exists(file_path):
                question = tm.askyesno("Предупреждение", "Файла не существует. Вы хотите создать его?")
                if not question:
                    self.back_to_chill()
                    return
            #============================================

            #Открываем файл
            self.document = docx.Document()

            def really_processing():
                try:
                    screen_path = os.path.join(self.cur_dir, "__TEMP__.png")
                    screen_path = os.path.abspath(screen_path)
                    img = ""
                    #Делаем скриншот
                    if self.chosen_opt.get() == CHSE_OWN:
                        ch1x = int(self.btn_choose1_X.get())
                        ch1y = int(self.btn_choose1_Y.get())
                        ch2x = int(self.btn_choose2_X.get())
                        ch2y = int(self.btn_choose2_Y.get())
                        capture_space = {"top":ch1x, "left":ch1y, 
                            "width": ch2x-ch1x, "height":ch2y-ch1y}
                        with mss.mss() as print_screen:
                            img = print_screen.grab(capture_space)
                        mss.tools.to_png(img.rgb, img.size, output=screen_path)
                    elif self.chosen_opt.get() == CHSE_FS:
                        with mss.mss() as print_screen:
                            img = print_screen.shot(output=screen_path)
                    
                    #Работа с docx и doc файлами
                    section = self.document.sections[0]
                    section.left_margin = docx.shared.Cm(1)
                    section.right_margin = docx.shared.Cm(1)
                    section.top_margin = docx.shared.Cm(1)
                    section.bottom_margin = docx.shared.Cm(1)
                    self.document.add_picture(screen_path, width=section.page_width-section.left_margin-
                        section.right_margin)
                    
                    self.document.save(file_path)
                    os.remove(screen_path)
                except Exception as err:
                    err_queue.put((err.__class__, traceback.format_exc()))
                    self.root.event_generate("<<On error>>")

            keyboard.add_hotkey(self.key_name.get(), really_processing)
        except Exception as err:
            err_queue.put((err.__class__, traceback.format_exc()))
            self.root.event_generate("<<On error>>")

    #Функция для включения и выключения 
    #всех элементов интерфейса, кроме кнопки "Старт"
    def change_state(self, st):
        self.btn_choose1.config(state=st)
        self.btn_choose1_X.config(state=st)
        self.btn_choose1_Y.config(state=st)

        self.btn_choose2.config(state=st)
        self.btn_choose2_X.config(state=st)
        self.btn_choose2_Y.config(state=st)

        self.own_rbutton.config(state=st)
        self.full_screen_button.config(state=st)

        self.key_name_entry.config(state=st)
        self.key_button.config(state=st)

        self.file_out_path_entry.config(state=st)
        self.save_button.config(state=st)

    def start_working(self):
        if self.work_state == WORK_CHILLING:
            self.work_state = WORK_WORKING
            self.start_button.config(text="Стоп")

            # Отключаем всё
            self.change_state("disabled")

            #Создание потока
            self.processing_thread = threading.Thread(target=self.process, args=(self.err_queue,))
            self.processing_thread.start()
        elif self.work_state == WORK_WORKING:
            self.work_state = WORK_CHILLING
            self.change_state("enabled")
            self.start_button.config(text="Старт!")

    def save_file(self):
        self.file_out_path.set(
            tf.asksaveasfilename(filetypes=[("Word-документ (*.docx)", "*.docx"), 
                ("Word-документ устаревшего формата (*.doc)", "*.doc")])
        )
    
    def start(self):
        self.root.mainloop()
