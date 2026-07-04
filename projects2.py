import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import time

url = "https://www.ptt.cc/bbs/Gossiping/index.html"

headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"cookie":"over18=1" #設定cookie
}

all_titles =[] #建立list
page_count = 3 #設定要抓取的頁數

for i in range(page_count): #for ... in rage()
    print(f"\n正在抓{i+1}頁:{url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        arts = soup.select("div.r-ent div.title a") #找div標籤 & r-ent分類 & div標籤 & title分類 & a標籤

        for art in arts:
            title = art.get_text(strip=True) #只取得a標籤程式碼的文字 strip=True去除多餘空白
            all_titles.append(title)
            print(title)
        
        paging_links = soup.select("div.btn-group-paging a")#找div標籤 & btn-group-paging分類 & a標籤 
        prev_path = paging_links[1]["href"] #找到的a標籤共有四個，要找的標的為第二個，所以為 paging_links[1] ，如果要找的標的為第一個，應為paging_links[0]
        url = "https://www.ptt.cc" + prev_path

        time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f"請求失敗:{e}")
        break

print(f"總共抓取{len(all_titles)}篇")
