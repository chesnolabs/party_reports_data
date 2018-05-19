#!/usr/bin/env python3

import tablib, sys
from pib_regexp import *

NAME_COL = 3 #номер стовпця, який відповідає за імена
CORRECT_GIVEN = [line.rstrip(",\n") for line in open('correct_given.csv')] #імпортуємо файл з правильним написанням імен
SUBSTITUTIONS_GIVEN = tablib.Dataset().load(open('substitute_given.csv').read()) #імпортуємо файл з варіантами імен, на які має відбутися заміна
CORRECT_MIDDLE = [line.rstrip(",\n") for line in open('correct_middle.csv')] #імпортуємо файл з правильним написанням імен
SUBSTITUTIONS_MIDDLE = dict(tablib.Dataset().load(open('substitute_middle.csv').read())) #імпортуємо файл з варіантами імен, на які має відбутися заміна


def open_file(file): #імпортуємо файл у форматі датасету
    imported_file = tablib.Dataset().load(open(file).read())
    return imported_file


def substitution(imported_file):
    new_data = tablib.Dataset() #створюємо новий датасет, додаємо в нього заголовки з імпортованого файла
    new_data.headers = imported_file.headers
    for row_index in range(imported_file.height): #по рядку опрацьовуємо імпортований файл
        row = list(imported_file[row_index])
        if row[8] == 'фізична особа':
            full_name = standard_name_cleaner(row[NAME_COL]) #робимо типову автозаміну
            if full_name.upper() == full_name:
                full_name = full_name.title() #якщо все слово пишеться заглавними літерами, замінюємо на написання з великої
            split_name = match_name_parts(full_name) #використовуємо регулярний вираз з підключеного модуля для розділення ПІБ
            family_name = split_name['family_name'] #прізвище
            given_name = replace_given_name(split_name['given_name']) #ім'я
            middle_name = replace_middle_name(split_name['middle_name']) #по-батькові
            row[NAME_COL] = ' '.join(filter(None, (family_name, given_name, middle_name))) #об'єднуємо прізвище, ім'я і по-батькові
        new_data.append(row) #додаємо результат у новий датасет
    return new_data

def interactive_mode_given(given_name): #пропонує вручну ввести ім'я, якщо не знаходить його в файлах
    given_name = input('Зараз ' + given_name + " А як має бути? Введіть правильне ім'я: ")
    return given_name
    
def interactive_mode_middle(middle_name): #пропонує вручну ввести по-батькові, якщо не знаходить його в файлах
    middle_name = input('Зараз ' + middle_name + " А як має бути? Введіть правильне по-батькові: ")
    return middle_name

def replace_given_name(given_name): #автозаміна імен
    if given_name not in CORRECT_GIVEN:
        given_name = given_name.title() #пишемо всі імена з великої літери
        if given_name in SUBSTITUTIONS_GIVEN:
            given_name = SUBSTITUTIONS_GIVEN[given_name] #автозаміна
        else:
            given_name = interactive_mode_given(given_name)
    return given_name
    
def replace_middle_name(middle_name): #автозаміна по-батькові
    if not middle_name:
        return middle_name
    if middle_name not in CORRECT_MIDDLE:
        middle_name = middle_name.title() #пишемо всі імена з великої літери
        if middle_name in SUBSTITUTIONS_MIDDLE:
            middle_name = SUBSTITUTIONS_MIDDLE[middle_name] #автозаміна
        else:
            middle_name = interactive_mode_middle(middle_name)
    return middle_name

def write_file(tmp, substituted_file): #записуємо датасет у csv-файл
    with open(tmp, 'w') as f:
        f.write(substituted_file.export('csv'))

imported_file = open_file('2017/ОБ/5_donations.csv')
#imported_file = open_file(sys.argv[1])
substituted_file = substitution(imported_file)
write_file('2017/ОБ/5_tmp.csv', substituted_file)
#write_file(sys.argv[2], substituted_file)
