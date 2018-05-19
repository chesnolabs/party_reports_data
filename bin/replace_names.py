#!/usr/bin/env python3

import logging
import sys

import tablib

from pib_regexp import *


NAME_COL = 3  # номер стовпця, який відповідає за імена
NAME_COL_TITLE = 'ПІБ (для фіз. осіб)/Назва (для юр. осіб)'

# правильні написання імен
CORRECT_GIVEN = [line.rstrip(",\n") for line in open('correct_given.csv')]
# варіанти імен для автозаміни
SUBSTITUTIONS_GIVEN = dict(
    tablib.Dataset().load(open('substitute_given.csv').read()))
# імена, які вказують на заповнення російською
RU_GIVEN = [line.rstrip(",\n") for line in open('ru_given.csv')]

# правильні написання по батькові
CORRECT_MIDDLE = [line.rstrip(",\n") for line in open('correct_middle.csv')]
# варіанти по батькові для автозаміни
SUBSTITUTIONS_MIDDLE = dict(
    tablib.Dataset().load(open('substitute_middle.csv').read()))
# по батькові, які вказують на заповнення російською
RU_MIDDLE = [line.rstrip(",\n") for line in open('ru_middle.csv')]

# нові автозаміни
GIVEN_NAME_STACK = {}
MIDDLE_NAME_STACK = {}

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', filename='log.txt')
log = logging.getLogger(__name__)


def open_file(file):
    '''
    імпорт файлу у форматі датасету
    '''
    imported_file = tablib.Dataset().load(open(file).read())
    return imported_file


def substitution(imported_file):
    '''
    '''
    if imported_file.headers[NAME_COL] != NAME_COL_TITLE:
        log.error('Неспівпадіння заголовку! Пропуск перевірки.')
        return imported_file

    # створюємо новий датасет, додаємо в нього заголовки з імпортованого файла
    new_data = tablib.Dataset()
    new_data.headers = imported_file.headers

    # по рядку опрацьовуємо імпортований файл
    for row_index in range(imported_file.height):
        row = list(imported_file[row_index])

        if row[8] == 'фізична особа':
            # типові автозаміни
            full_name = standard_name_cleaner(row[NAME_COL])

            # якщо все імʼя у верхньому регістрі - написання з великої
            if full_name.upper() == full_name:
                full_name = full_name.title()

            # розділення ПІБ на частини
            split_name = match_name_parts(full_name)
            # прізвище для обʼєднання пізніше
            family_name = split_name['family_name']
            # первірка імені
            given_name = verify_given_name(
                split_name['given_name'], row_index)
            # перевірка по-батькові
            middle_name = verify_middle_name(
                split_name['middle_name'], row_index)

            # об'єднання ПІБ для запису у файл
            row[NAME_COL] = \
                ' '.join(filter(None, (family_name, given_name, middle_name)))
        # додаємо результат у новий датасет
        new_data.append(row)
    return new_data


def interactive_mode_given(given_name, row_index):
    '''
    пропонує вручну ввести ім'я, якщо не знаходить його в файлах
    '''
    if given_name not in GIVEN_NAME_STACK:
        new_name = input(
            '\a{0}:{1}: "{2}" Введіть правильне імʼя: '
            .format(sys.argv[1], row_index, given_name))

        if new_name:
            GIVEN_NAME_STACK[given_name] = new_name
        else:
            new_name = given_name

    else:
        new_name = GIVEN_NAME_STACK[given_name]

    return new_name


def interactive_mode_middle(middle_name, row_index):
    '''
    пропонує вручну ввести по-батькові, якщо не знаходить його в файлах
    '''
    if middle_name not in MIDDLE_NAME_STACK:
        new_name = input(
            '\a{0}:{1}: "{2}" Введіть правильне по-батькові: '
            .format(sys.argv[1], row_index, middle_name))

        if new_name:
            MIDDLE_NAME_STACK[middle_name] = new_name
        else:
            new_name = middle_name
    else:
        new_name = MIDDLE_NAME_STACK[middle_name]
    return new_name


def verify_given_name(given_name, row_index):
    '''
    перевірка імені
    '''
    if given_name not in CORRECT_GIVEN:
        # автозаміна
        if given_name in SUBSTITUTIONS_GIVEN:
            given_name = SUBSTITUTIONS_GIVEN[given_name]
        elif given_name in RU_GIVEN:
            log.err(
                '{0}:{1} Необхідний переклад усього імені: "{2}"'
                .format(sys.argv[1], row_index, given_name))
        else:
            given_name = interactive_mode_given(given_name, row_index)
    return given_name


def verify_middle_name(middle_name, row_index):
    '''
    перевірка по-батькові
    '''
    if not middle_name:
        return middle_name
    if middle_name not in CORRECT_MIDDLE:
        # автозаміна
        if middle_name in SUBSTITUTIONS_MIDDLE:
            middle_name = SUBSTITUTIONS_MIDDLE[middle_name]
        elif middle_name in RU_MIDDLE:
            log.err(
                '{0}:{1} Необхідний переклад усього імені: {2}'
                .format(sys.argv[1], row_index, middle_name))
        else:
            middle_name = interactive_mode_middle(middle_name, row_index)
    return middle_name


def write_file(tmp, substituted_file):
    '''
    запис датасету в csv-файл
    '''
    with open(tmp, 'w') as f:
        f.write(substituted_file.export('csv'))


if __name__ == "__main__":
    filename = sys.argv[1]

    log.info('Перевірка {}'.format(filename))
    imported_file = open_file(filename)
    substituted_file = substitution(imported_file)

    log.info('Запис {}'.format(filename))
    write_file(filename, substituted_file)

    if GIVEN_NAME_STACK or MIDDLE_NAME_STACK:
        log.info('Таблиці з новими [авто]замінами:')
    if GIVEN_NAME_STACK:
        log.info('Імена')
        log.info('name,replacement')
        for key, value in GIVEN_NAME_STACK.items():
            log.info(','.join((key, value)))

    if MIDDLE_NAME_STACK:
        log.info('по батькові')
        log.info('name,replacement')
        for key, value in MIDDLE_NAME_STACK.items():
            log.info(','.join((key, value)))
