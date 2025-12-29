import requests
from bs4 import BeautifulSoup
from time import sleep


for count in range(1, 8):
    sleep(3)
    url = f"https://scrapingclub.com/exercise/list_basic/?page=1{count}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml") #html.parser
    
    data = soup.find_all("div", class_="w-full rounded border") #первоначальный поиск div, нужный class_="w-full rounded border" find_all
    for i in data:
        name = i.find("h4").text.replace("\n", "") # имя товара 
        price = i.find("h5").text #цена
        url_img = "https://scrapingclub.com" + i.find("img", class_="card-img-top img-fluid").get("src") #ссылка на картинку
        print(f"{name}\n{price}\n{url_img}\n\n")