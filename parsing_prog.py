import requests
from bs4 import BeautifulSoup
from time import sleep

def get_url():
    for count in range(1, 8):  
        # Проходим по страницам с 1 по 7
        sleep(3)  
        # Задержка между запросами во избежание блокировки
        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"  
        # Формируем URL страницы
        response = requests.get(url) 
        # отправляем запрорс на сайт
        soup = BeautifulSoup(response.text,"lxml") 
        # разбираем страницу
        data = soup.find_all("div", class_="w-full rounded border") 
        # первоначальный поиск div, нужный class_="w-full rounded border" find_all (список из всех карточек товара)
    
    for i in data: 
        # цикл (берем каждую отдельную карту в переменную i )
     card_url = "https://scrapingclub.com" + i.find("a").get("href") 
     # в теге 'a' в атрибуте 'href' лежит ссылка (дополняем её базовым доменом)
     yield card_url
     
 
def array(): 
     for card_url in get_url(): 
         # проходимся по всему смуску ссылок
         response = requests.get(card_url) 
         # делаем отдельно запрос на карту товара 
         sleep(3) 
         # Задержка между запросами во избежание блокировки
         soup = BeautifulSoup(response.text,"lxml") 
         # разбираем страницу
         data = soup.find("div", class_="my-8 w-full rounded border")
         # поиск div, нужный class_="my-8 w-full rounded border" find_all (вся информация которая хранится в этой карте)
         name = data.find("h3", class_="card-title").text
         price = data.find("h4", class_="my-4 card-price").text
         text = data.find("p", class_="card-description").text
         url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top").get("src")
         yield name, price, url_img, text
