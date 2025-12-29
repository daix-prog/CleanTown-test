import xlsxwriter
from parcer.parsing_prog import array  # Импортируем массив данных из модуля 

def writer(parametr):
    # Создаем новый Excel-файл по указанному пути
    book = xlsxwriter.Workbook(r"E:\parsing_test")
    # Добавляем лист с названием "rosap"
    page = book.add_worksheet("rosap")

    row = 0    # Начинаем с первой строки
    column = 0  # Начинаем с первого столбца

    # Устанавливаем ширину столбцов
    page.set_column("A:A", 20)  # Столбец A шириной 20
    page.set_column("B:B", 20)  # Столбец B шириной 20
    page.set_column("C:C", 50)  # Столбец C шириной 50
    page.set_column("D:D", 50)  # Столбец D шириной 50

    # Записываем данные в файл
    for item in parametr:
        page.write(row, column, item[0])      # Запись в столбец A
        page.write(row, column+1, item[1])    # Запись в столбец B
        page.write(row, column+2, item[2])    # Запись в столбец C
        page.write(row, column+3, item[3])    # Запись в столбец D
        row += 1  # Переход на следующую строку

    book.close()  # Закрываем книгу (сохраняем файл)

# Вызываем функцию, передавая ей импортированный массив данных
writer(array)