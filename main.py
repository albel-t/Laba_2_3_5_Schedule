import sys
import os
import xlrd
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from laba_logging import *

InitFile(__file__)


class pair:
    def __init__(self, lesson, type, teacher, auditory):
        self.lesson = lesson
        self.type = type
        self.teacher = teacher
        self.auditory = auditory
    def check(self, pair):
        if self.lesson == pair.lesson:
            if(self.type == pair.type) and (self.teacher == pair.teacher) and (self.auditory == pair.auditory):
                self.discrepancy = "Identical"
                pair.discrepancy = "Identical"
                print("сравнение - Identical")
            else:
                self.discrepancy = "Similar"
                pair.discrepancy = "Similar"
                print("сравнение - Similar")

        else:
            self.discrepancy = "Different"
            pair.discrepancy = "Different"
            print("сравнение - Different")

    def tostr(self):
        return f"pair {self.lesson}, {self.type}, {self.teacher}, {self.auditory}"


class day:
    def __init__(self):
        self.pairs = {}
    def add_pair(self, num, lesson, type, teacher, auditory):
        self.pairs[num] = pair(lesson, type, teacher, auditory)
        # print(f"add_pair {num}, {lesson}, {type}, {teacher}, {auditory}")
        # print(f"self.pairs[num] {self.pairs[num].tostr()}")
        # print(f"self.pairs.keys() {self.pairs.keys()}")
    def tostr(self):
        tmp = 'day'
        for i in self.pairs.keys():
            tmp += f"\n{i} - {self.pairs[i].tostr()}"
        return tmp

class schedule:
    def __init__(self, group, year, semester):
        self.group = group
        self.year = year
        self.semester = semester
        self.days_even = {}
        self.days_uneven = {}
        
    def add_day(self, week_day, day, ev):
        if ev:
            self.days_even[week_day] = copy.deepcopy(day)         
        else: 
            self.days_uneven[week_day] = copy.deepcopy(day)   
    def print_data(self):
        print(f"check days days_even: {self.days_even.keys()}")
        for i in self.days_even.keys():
            print(f"day {i}  / {self.days_even[i].tostr()}")
        print(f"check days days_uneven: {self.days_uneven.keys()}")
        for i in self.days_uneven.keys():
            print(f"day {i}  / {self.days_uneven[i].tostr()}")
# iait_17-18-1.09.22
def parsing(path = 'D:\\projects\\VisualStudioCode\\Laba_2_3_5_Schedule\\data\\iait_17-18-1.06.02.xls'):
    # Открытие файла
    print("parsing...")
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    group = ''
    schedules = []
    tmp_schedule = schedule(sheet.cell_value(4, 0), '0', '0')
    last_week_day = ""
    # Чтение данных
    count = 0
    day_ev = day()
    day_nev = day()
    for row in range(4, sheet.nrows):
        count += 1
        for col in range(1, sheet.ncols):
            print(sheet.cell_value(row, col), end="|")
        print('', end="\n")
        # print(f"new str {sheet.cell_value(row, 0)}|{sheet.cell_value(row, 1)}|{sheet.cell_value(row, 2)}")

        if(sheet.cell_value(row, 1) != ""):
            last_week_day = sheet.cell_value(row, 1)


        print(f"{row} of {(sheet.nrows)-1}")
        if(sheet.cell_value(row, 2) == "") or (row >= (sheet.nrows-1)):
            while (6 >= count):
                day_ev .add_pair(str(count), '', '', '', '')
                day_nev.add_pair(str(count), '', '', '', '')
                count += 1
            # print(f"end of day: \n{str(day_ev.pairs['1'].lesson)}\n{str(day_nev.pairs['1'].lesson)}")
            tmp_schedule.add_day(last_week_day, day_ev, 0)
            tmp_schedule.add_day(last_week_day, day_nev, 1)
            day_ev .pairs.clear()
            day_nev.pairs.clear()
            count = 0
        else:
            while (int(sheet.cell_value(row, 2)) > count):
                day_ev .add_pair(str(count), '', '', '', '')
                day_nev.add_pair(str(count), '', '', '', '')
                count += 1
            day_ev .add_pair(str(count), sheet.cell_value(row, 3), sheet.cell_value(row, 5), sheet.cell_value(row, 6), sheet.cell_value(row, 7))
            day_nev.add_pair(str(count), sheet.cell_value(row, 10), sheet.cell_value(row, 12), sheet.cell_value(row, 13), sheet.cell_value(row, 14))



        if(sheet.cell_value(row, 0) != '') or (row == sheet.nrows-1):
            # print(f"old | new group: {group}|{sheet.cell_value(row, 0)}")
            if group != "":
                print("group: " + group)
                for day_name in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']:
                    if day_name not in tmp_schedule.days_even.keys():
                        for i in range(1, 7):
                            day_ev .add_pair(str(i), '', '', '', '')
                            day_nev.add_pair(str(i), '', '', '', '')
                        tmp_schedule.add_day(day_name, day_ev, 0)
                        tmp_schedule.add_day(day_name, day_nev, 1)
                        day_ev .pairs.clear()
                        day_nev.pairs.clear()
                schedules.append(tmp_schedule)
                tmp_schedule.print_data()
                tmp_schedule = schedule(group, '0', '0')
                count = 0
            group = sheet.cell_value(row, 0)





        # for col in range(1, sheet.ncols):
            # print(f'[{row}][{col}] - [{sheet.cell_value(row, col)}]')
    return schedules
    '''
    # Для pandas
    pip install pandas openpyxl xlrd

    # Или только нужные компоненты
    pip install pandas
    pip install openpyxl  # для .xlsx файлов
    pip install xlrd      # для старых .xls файлов
    '''
parsing()