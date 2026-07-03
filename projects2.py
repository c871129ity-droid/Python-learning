import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import time

url = "https://www.ptt.cc/bbs/Gossiping/index.html"

headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"cookie":"over18=1"
}

all_titles =[]
page_count = 3

for i in range(page_count):
    print(f"\n正在抓{i+1}頁:{url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        arts = soup.select("div.r-ent div.title a")

        for art in arts:
            title = art.get_text(strip=True)
            all_titles.append(title)
            print(title)
        
        paging_links = soup.select("div.btn-group-paging a")
        prev_path = paging_links[1]["href"]
        prev_url = "https://www.ptt.cc" + prev_path

        time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f"請求失敗:{e}")
        break

print(f"總共抓取{len(all_titles)}篇")