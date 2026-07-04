import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import time

url="https://books.toscrape.com/catalogue/page-1.html"

all_books = []
page_count = 2

for i in range(page_count):
    print(f"\n正在抓取第{i+1}頁:{url}")
    try:

        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        titles = soup.select("h3 a")
        prices = soup.select("p.price_color")

        for title, price in zip(titles, prices):
            all_books.append({
            "title": title["title"],
            "price": price.text
            })
            print(f"書名：{title['title']}  售價：{price.text}")

        next_links = soup.select_one("li.next a")
        if next_links is None:
            break
        url = "https://books.toscrape.com/catalogue/" + next_links["href"]
        time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f"請求失敗:{e}")
        break

print(f"\n共抓取{len(all_books)}樣商品")
