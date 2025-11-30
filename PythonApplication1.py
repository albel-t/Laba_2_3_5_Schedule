import tkinter as tk
from PIL import ImageTk, Image
import os
import sys

from tkinter import ttk

import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from laba_logging import *
InitLogFile()


InitFile(__file__)

from main import *


'''
    # Настраиваем заголовки столбцов для второй таблицы
    table2.heading('col1', text='№')
    table2.heading('col2', text='Предмет')
    table2.heading('col3', text='Тип Зан.')
    table2.heading('col4', text='Преподаватель')
    table2.heading('col5', text='Аудитория')
    
    # Настраиваем ширину столбцов
    table2.column('col1', width=10)
    table2.column('col2', width=120)
    table2.column('col3', width=10)
    table2.column('col4', width=120)
    table2.column('col5', width=40)
'''




class TableWindow:
    def __init__(self, new_window, table1, table2):
        self.new_window = new_window
        self.new_window.title("Таблицы с изменяемыми цветами")
        self.new_window.geometry("1200x700")
        self.new_window.minsize(1200, 700)
        self.groupid1 = 0
        self.groupid2 = 0
        # Цветовые палитры
        # self.colors1 = ['#FF0000', '#00FF00', '0000FF']
        self.label1 = None
        self.frame1 = None
        self.table1 = None

        self.separator = None
        
        self.label2 = None
        self.frame2 = None
        self.table2 = None
 
        self.listtable1 = table1
        self.listtable2 = table2

        self.parity = 0



        # Создаем таблицы
        self.create_tables()
        


        # Создаем кнопки для изменения цветов
        self.create_buttons(table1, table2)
    
    def create_tables(self): #, listtable1: list[schedule], listtable2: list[schedule]
        # # Создаем фрейм для первой таблицы
        # if self.current_table1 != None:
            
        # if self.current_table2 != None:

        table1data = self.listtable1[self.groupid1]
        table2data = self.listtable2[self.groupid2]
        if self.frame1 == None:
            self.frame1 = tk.Frame(self.new_window)
        self.frame1.pack(pady=20, padx=10, fill='both', expand=True)
        
        
        # Первая таблица
        if self.table1 == None:
            self.table1 = ttk.Treeview(self.frame1, columns=('col1', 'col2', 'col3', 'col4', 'col5'), show='headings', height=12)
        
        # Настраиваем заголовки столбцов
        col_name = ["День недели", "№", 'Предмет', 'Тип Зан.', 'Преподаватель', 'Аудитория']
        for i in range(5):
            self.table1.heading(f'col{i+1}', text=col_name[i])
            self.table1.column(f'col{i+1}', width=len(col_name[i]))
        
        # Заполняем первую таблицу данными
        table2data = self.fill_table(self.table1, table2data, table1data)
        self.table1.pack(fill='both', expand=True)
                # Заголовок для первой таблицы
        if self.label1 == None:
            self.label1 = tk.Label(self.frame1, text=table1data.group, font=('Arial', 14, 'bold'))
        else:
            self.label1.destroy()
            self.label1 = tk.Label(self.frame1, text=table1data.group, font=('Arial', 14, 'bold'))
        self.label1.pack(pady=(0, 10))


        # Разделитель между таблицами
        if self.separator == None:
            self.separator = ttk.Separator(self.new_window, orient='horizontal')
        self.separator.pack(fill='x', padx=20, pady=20)
        


        # Создаем фрейм для второй таблицы
        if self.frame2 == None:
            self.frame2 = tk.Frame(self.new_window)
        self.frame2.pack(pady=20, padx=10, fill='both', expand=True)
        
        # Вторая таблица
        if self.table2 == None:
            self.table2 = ttk.Treeview(self.frame2, columns=('col1', 'col2', 'col3', 'col4', 'col5'), show='headings', height=12)
        
        # Настраиваем заголовки столбцов
        for i in range(5):
            self.table2.heading(f'col{i+1}', text=f'Колонка {i+1}')
            self.table2.column(f'col{i+1}', width=120)
        
        # Заполняем вторую таблицу данными
        table1data = self.fill_table(self.table2, table1data, table2data)
        self.table2.pack(fill='both', expand=True)

                # Заголовок для первой таблицы
                # Заголовок для второй таблицы
        if self.label2 == None:
            self.label2 = tk.Label(self.frame2, text=table2data.group, font=('Arial', 14, 'bold'))
        else:
            self.label2.destroy()
            self.label2 = tk.Label(self.frame2, text=table2data.group, font=('Arial', 14, 'bold'))
        self.label2.pack(pady=(0, 10))

    def fill_table(self, table, table_data_check, table_data: schedule):
        """Заполняет таблицу данными с белым фоном"""
        # Очищаем таблицу
        for item in table.get_children():
            table.delete(item)
        
        # Настраиваем белый цвет по умолчанию
        # table.tag_configure('white', background='white')
        
        # Заполняем таблицу
        print("--------------- наполенние ---------------------")
        print(table_data.days_even.keys())
        print(table_data_check.days_even.keys())
        count = 0
        if self.parity :
            week = table_data.days_even
            week_check = table_data_check.days_even
        else:
            week = table_data.days_uneven
            week_check = table_data_check.days_uneven
        for d in week.keys():
            print(week[d].pairs.keys())
            for p in week[d].pairs.keys():
                week[d].pairs[p].check(week_check[d].pairs[p])
                if p == "1":
                    week_day = d
                    count += 1
                else:
                    week_day = ''
                values = [week_day, p, week[d].pairs[p].lesson
                          , week[d].pairs[p].type
                          , week[d].pairs[p].teacher
                          , week[d].pairs[p].auditory]
                print(values)
                colors = {"Identical" : ['green3', 'green2'], 
                          "Similar" : ['LightGoldenrod2', 'khaki1'],
                          "Different" : ['coral1', 'salmon']} 
                if discrepancy_to_show[week[d].pairs[p].discrepancy]:
                    this_tag = week[d].pairs[p].discrepancy
                else:
                    this_tag = 'White'
                table.insert('', 'end', values=values, tags= this_tag + str(count%2))

        table.tag_configure('Identical0', background='green3')
        table.tag_configure('Identical1', background='green2')
        table.tag_configure('Similar0', background='LightGoldenrod2')
        table.tag_configure('Similar1', background='khaki1')
        table.tag_configure('Different0', background='coral1')
        table.tag_configure('Different1', background='salmon')
        table.tag_configure('White0', background='White')
        table.tag_configure('White1', background='light gray')
        return table_data_check
    '''
    PaleGreen2 / green2
    tan1 / khaki1
    coral1 / salmon

    '''
    # def change_colors_table1(self):

    # def change_colors_table2(self):

    
    # def change_colors_both(self):
    
    # def change_colors(self, table, color_palette):

    # def reset_colors(self):

    def create_buttons(self, listtable1: list[schedule], listtable2: list[schedule]):
        """Создает кнопки для управления цветами"""
        button_frame = tk.Frame(self.new_window)
        button_frame.pack(pady=10)
        self.groups = []
        self.groups1 = []
        for i in listtable1:
            self.groups.append(i.group)        
        for i in listtable2:
            self.groups1.append(i.group)

        self.file_combobox_group1 = ttk.Combobox(self.new_window, values=self.groups, state="readonly", font=(20), cursor="hand2")
        self.file_combobox_group1.place(relx=1, rely=0.4, height=30, width=100, anchor="ne")
        self.file_combobox_group1.bind("<<ComboboxSelected>>", self.on_group_selected)


        self.file_combobox_group2 = ttk.Combobox(self.new_window, values=self.groups1, state="readonly", font=(20), cursor="hand2")
        self.file_combobox_group2.place(relx=1, rely=0.9, height=30, width=100, anchor="ne")
        self.file_combobox_group2.bind("<<ComboboxSelected>>", self.on_group_selected1)

        close_btn = tk.Button(button_frame, text="Закрыть", 
                             command=self.new_window.destroy, font=('Arial', 10), bg='#333', fg='white')
        close_btn.pack(side='left', padx=5)

        remake_btn = tk.Button(button_frame, text="пересоздать", 
                             command=self.create_tables, font=('Arial', 10), bg='#333', fg='white')
        remake_btn.pack(side='left', padx=5)

        self.click_parity = tk.Button(button_frame, text="ченетная", 
                             command=self.on_button_click_parity, font=('Arial', 10), bg='#333', fg='white')
        self.click_parity.pack(side='left', padx=5)
    # self.selected_group = ''
    # self.selected_group1 = ''

    def on_group_selected(self, event):
        # Обработчик выбора файла
        self.selected_group = self.file_combobox_group1.get()
        if self.selected_group:
            print(f"выбран файл: {self.selected_group}")
        self.groupid1 = self.groups.index(self.selected_group)
        self.create_tables()


    def on_group_selected1(self, event):
        # Обработчик выбора файла
        self.selected_group1 = self.file_combobox_group2.get()
        if self.selected_group1:
            print(f"выбран файл: {self.selected_group1}")
        self.groupid2 = self.groups1.index(self.selected_group1)
        self.create_tables()

    def on_button_click_parity(self):          # кнопка выбора 2
        print("переключение")
        if self.parity == 0:
            self.click_parity.config(text="четная")
            self.parity = 1
        else:
            self.click_parity.config(text="ченетная")
            self.parity = 0

data_directory = "D:\\projects\\VisualStudioCode\\Laba_2_3_5_Schedule\\data"
selected_file = "D:\\projects\\VisualStudioCode\\Laba_2_3_5_Schedule\\data\\iait_17-18-1.06.02.xls"
selected_file1 = "D:\\projects\\VisualStudioCode\\Laba_2_3_5_Schedule\\data\\iait_17-18-1.09.22.xls"
def create_window():
    # Создаем новое окно
    new_window = tk.Toplevel()
    TableWindow(new_window, parsing(selected_file), parsing(selected_file1))

'''//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''

def get_files_in_directory(directory="."):
    # Возвращает список файлов в указанной директории
    if not os.path.exists(directory):
        return []
    
    try:
        items = os.listdir(directory)
        return [item for item in items if os.path.isfile(os.path.join(directory, item))]
    except PermissionError:
        return []

def on_file_selected(event):
    # Обработчик выбора файла
    global selected_file
    selected_file = data_directory + "\\" + file_combobox.get()
    if selected_file:
        print(f"выбран файл: {selected_file}")

def on_file_selected1(event):
    # Обработчик выбора файла
    global selected_file1
    selected_file1 = data_directory + "\\" + file_combobox1.get()
    if selected_file1:
        print(f"выбран файл: {selected_file1}")

x1 = 0
x2 = 0
x3 = 0
discrepancy_to_show = {'Identical' : 0, 'Similar' : 0, 'Different' : 0}
def on_button_click2():          # кнопка выбора 2
    print("Сравнить сходства")
    global x1
    if x1 == 0:
        btn2.config(background="lightgreen")
        x1 =+ 1
        discrepancy_to_show['Identical'] = 1
    else:
        btn2.config(background="lightsteelblue")
        x1 = 0
        discrepancy_to_show['Identical'] = 0
    
def on_button_click3():          # кнопка выбора 3
    print("Сравнить различия")
    global x2
    if x2 == 0:
        btn3.config(background="lightgreen")
        x2 =+ 1
        discrepancy_to_show['Similar'] = 1
    else:
        btn3.config(background="lightsteelblue")
        x2 = 0
        discrepancy_to_show['Similar'] = 0
    
def on_button_click4():          # кнопка выбора 4
    print("Сравнить несоотствие")
    global x3
    if x3 == 0:
        btn4.config(background="lightgreen")
        x3 =+ 1
        discrepancy_to_show['Different'] = 1
    else:
        btn4.config(background="lightsteelblue")
        x3 = 0
        discrepancy_to_show['Different'] = 0

# окно
window = tk.Tk()
window.title("название_окна")
window.geometry("602x220") # размеры окна
# window.minsize(605, 270)
# window.maxsize(1920, 1080)

# Загрузка и установка фонового изображения
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "gradient\\gradient_1920_1080.png") # путь к фону
file_path1 = os.path.join(current_dir, "gradient\\button.png") # путь к кнопке
print(f"путь к изображению фона {file_path}")
print(f"путь к изображению кнопки {file_path1}")
bg_image = Image.open(file_path)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_image1 = Image.open(file_path1)
bg_photo1 = ImageTk.PhotoImage(bg_image1)

# фон
canvas = tk.Canvas(window, width=bg_image.width, height=bg_image.height)
canvas.pack(fill="both", expand=True)

# Добавление фонового изображения на Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Сохраняем ссылку на изображение
window.photo = bg_photo
window.photo = bg_photo1

# Получаем список файлов в текущей директории
files = get_files_in_directory(data_directory)

# виджеты
btn1 = tk.Button(canvas, image=bg_photo1, cursor="hand2", command=create_window, activebackground="lightgreen", background="#c1fdc0") # кнопка
btn1.place(relx=0.7, rely=0.5, anchor="nw")

tk.Label(window, text=" Выберите файл для сранения ", font=(20), background="lightsteelblue1").place(anchor="sw", relx=0, rely=0.1)

file_combobox = ttk.Combobox(window, values=files, state="readonly", font=(20), cursor="hand2")
file_combobox.place(relx=0, rely=0.1, height=30, width=300, anchor="nw")
file_combobox.bind("<<ComboboxSelected>>", on_file_selected)

tk.Label(window, text=" Выберите файл для сранения ", font=(20), background="lightsteelblue1").place(anchor="se", relx=1, rely=0.1)

file_combobox1 = ttk.Combobox(window, values=files, state="readonly", font=(20), cursor="hand2")
file_combobox1.place(relx=1, rely=0.1, height=30, width=300, anchor="ne")
file_combobox1.bind("<<ComboboxSelected>>", on_file_selected1)

btn2 = tk.Button(canvas, text="Указать сходства", cursor="hand2", command=on_button_click2, activebackground="lightgray", background="lightsteelblue", font=(20)) # кнопка
btn2.place(relx=0.3, rely=0.5, anchor="s")

btn3 = tk.Button(canvas, text="Указать различия", cursor="hand2", command=on_button_click3, activebackground="lightgray", background="lightsteelblue", font=(20)) # кнопка
btn3.place(relx=0.3, rely=0.6, anchor="center")

btn4 = tk.Button(canvas, text="Указать несоответствие", cursor="hand2", command=on_button_click4, activebackground="lightgray", background="lightsteelblue", font=(20)) # кнопка
btn4.place(relx=0.3, rely=0.7, anchor="n")

window.mainloop() # это запуск, он должен быть в конце