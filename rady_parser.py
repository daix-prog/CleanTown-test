import requests
import xlsxwriter
from bs4 import BeautifulSoup
from time import sleep

list_card_url = []

# Сбор ссылок на карточки товаров
for count in range(1, 8):
    try:
        sleep(3)
        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        print(f"Обрабатываю страницу {count}: {url}")
        
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="w-full rounded border")
        
        if not data:
            print(f"Не найдены карточки товаров на странице {url}")
            continue
        
        for i in data:
            card_url = "https://scrapingclub.com" + i.find("a").get("href")
            list_card_url.append(card_url)
    except Exception as e:
        print(f"Ошибка при обработке страницы {url}: {e}")
        continue

print(f"Собрано {len(list_card_url)} ссылок на карточки товаров.")

# Сбор данных из каждой карточки товара
def array():
    for card_url in list_card_url:
        try:
            sleep(3)
            response = requests.get(card_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            data = soup.find("div", class_="my-8 w-full rounded border")
            
            if not data:
                print(f"Не удалось найти данные для URL: {card_url}")
                continue
            
            name = data.find("h3", class_="card-title").text
            price = data.find("h4", class_="my-4 card-price").text
            text = data.find("p", class_="card-description").text
            url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top").get("src")
            
            yield name, price, url_img, text
        except Exception as e:
            print(f"Ошибка при обработке карточки {card_url}: {e}")
            continue

# Запись данных в Excel
def writer(parametr):
    try:
        book = xlsxwriter.Workbook(r"E:\parsing_test.xlsx")
        page = book.add_worksheet("rosap")
        
        row = 0
        column = 0
        
        page.set_column("A:A", 20)
        page.set_column("B:B", 20)
        page.set_column("C:C", 50)
        page.set_column("D:D", 50)
        
        for item in parametr:
            if len(item) != 4:
                print(f"Некорректная структура данных: {item}")
                continue
            page.write(row, column, item[0])
            page.write(row, column+1, item[1])
            page.write(row, column+2, item[2])
            page.write(row, column+3, item[3])
            row += 1
        
        book.close()
        print("Данные успешно записаны в файл.")
    except Exception as e:
        print(f"Ошибка при записи в Excel: {e}")

# Вызов функций
writer(array())