import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import time

url="https://books.toscrape.com/catalogue/page-1.html"

all_books = [] #建立list
page_count = 3 #設定要抓取的頁數

for i in range(page_count):
    print(f"\n正在抓取第{i+1}頁:{url}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.select("h3 a") 
        prices = soup.select("p.price_color") 

        for title, price in zip(titles, prices): #zip：同時走訪兩個清單
            all_books.append({ #list內新增字典
            "title": title["title"],
            "price": price.text
            })
            print(f"書名：{title['title']}  售價：{price.text}")

        next_links = soup.select_one("li.next a") #找li標籤 & next分類 & a標籤的的程式碼 
        if next_links is None: #如果程式碼沒有next_links就停
            break
        url = "https://books.toscrape.com/catalogue/" + next_links["href"] #第一頁中找到的a標籤程式碼href="page-2.html，更新url後第二頁找到的a標籤程式碼href="page-3.html
        time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f"請求失敗:{e}")
        break


print(f"\n共抓取{len(all_books)}樣商品")
