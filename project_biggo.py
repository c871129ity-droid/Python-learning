from selenium import webdriver                                    # 匯入 webdriver，這是操控瀏覽器的核心工具
from selenium.webdriver.common.by import By                        # 匯入 By，用來指定「用什麼方式」找網頁元素
from selenium.webdriver.support.ui import WebDriverWait             # 匯入 WebDriverWait，用來設定「最多等幾秒」
from selenium.webdriver.support import expected_conditions as EC    # 匯入 EC，裡面裝著各種「等待條件」
from selenium.webdriver.common.keys import Keys                    # 匯入 Keys，用來模擬鍵盤按鍵（像 Enter）
import time                                                         # 匯入 time，讓程式可以暫停幾秒
import csv                                                          # 匯入 csv，用來把資料寫成 CSV 檔案
import os                                                           # 匯入 os，用來組合檔案存放的路徑
import random                                                       # 匯入 random，用來產生隨機停頓秒數，避免被當機器人

driver = webdriver.Chrome()                # 打開一個 Chrome 瀏覽器視窗，driver 就是這個瀏覽器的遙控器
driver.implicitly_wait(10)                 # 全域設定：找不到元素時，最多耐心等待 10 秒再放棄

url = "https://biggo.com.tw/"              # 目標網站：BigGo 比價網首頁
driver.get(url)                            # 讓瀏覽器前往這個網址

wait = WebDriverWait(driver, 10)           # 建立一個「顯性等待器」，之後可以指定等特定元素出現，最多等 10 秒
search_box = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.SearchBar_input__VuqN4"))
    # 等到搜尋框（class 是 SearchBar_input__VuqN4）出現在畫面上為止
)
search_box.send_keys("Marshall KilBurn III 奶油白")   # 模擬打字，在搜尋框輸入商品關鍵字
search_box.send_keys(Keys.ENTER)                   # 模擬按下 Enter 鍵，送出搜尋

time.sleep(random.uniform(2, 4))           # 隨機停頓 2-4 秒，等搜尋結果頁載入，也避免請求太規律被偵測成機器人

# ── 填寫價格區間 ──────────────────────────────
min_price_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='最低價格']")
# 找到「最低價格」輸入框：這個 input 沒有 class，用 placeholder 屬性當作辨識依據
max_price_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='最高價格']")
# 找到「最高價格」輸入框，做法相同

min_price_input.clear()                    # 先清空這個輸入框，避免殘留舊的數字
min_price_input.send_keys("3000")         # 輸入最低價格 25000 元

max_price_input.clear()                    # 清空最高價格輸入框
max_price_input.send_keys("15000")         # 輸入最高價格 60000 元

# ── 按下 Go 按鈕套用篩選 ──────────────────────
go_button = driver.find_element(By.CSS_SELECTOR, "button[class*='CustomPrice_go-button']")
# 找「Go」按鈕：用 [class*='...'] 做部分比對，因為 class 後面那段雜湊值可能隨時改變
go_button.click()                          # 模擬點擊，套用剛剛輸入的價格區間篩選
time.sleep(random.uniform(2, 3))           # 隨機停頓，等篩選後的結果重新載入完成

all_results = []                           # 準備一個空清單，之後每一支符合條件的手機資料都會加進這裡
seen_links = set()                         # set：專門記錄「已經抓過的商品連結」，天生不會有重複值，用來防止重複收錄

page_num = 1                               # 目前頁數，從第 1 頁開始
MAX_pages = 2                             # 設定只抓前 2 頁就停止，避免抓太多頁被網站封鎖

while page_num <= MAX_pages:               # 條件式迴圈：頁數還沒超過上限就繼續跑
    print(f"正在抓第 {page_num} 頁，目前已收集 {len(all_results)} 筆不重複資料")
    # 印出目前進度，方便你邊執行邊確認程式有沒有正常運作

    cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='product-content-wrap']")
    # 找出這一頁畫面上所有「商品卡片」，find_elements 找不到也不會報錯，只會回傳空清單

    for card in cards:                     # 逐一走訪每一張商品卡片
        try:                               # 用 try 包起來，避免某張卡片格式異常時讓整支程式當掉
            title_el = card.find_element(By.CSS_SELECTOR, "div[class*='product-title'] a")
            # 在這張卡片「裡面」找標題的 a 標籤，確保抓到的標題跟這張卡片一致
            price_el = card.find_element(By.CSS_SELECTOR, "div[class*='product-price']")
            # 在同一張卡片裡面找價格區塊，這樣標題和價格保證是同一支手機的資料

            link = title_el.get_attribute("href")   # 取出這個商品連結，href 屬性內容通常是獨一無二的

            if link in seen_links:                   # 檢查這個連結是不是已經抓過了
                continue                              # 抓過的話，跳過這張卡片，繼續下一張
            seen_links.add(link)                      # 沒抓過的話，記錄進 seen_links，避免之後重複收錄

            all_results.append({                      # 把這支手機的資料整理成一個字典，加進總清單
                "title": title_el.get_attribute("title"),   # 商品名稱藏在 title 屬性裡
                "price": price_el.text.strip(),             # 價格是卡片裡的純文字，去掉前後空白
                "href": link                                 # 商品連結
            })
        except Exception:                  # 如果這張卡片找元素時出錯（例如結構跟別的不同）
            continue                        # 就跳過這張，不影響其他卡片繼續處理

    next_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '下一頁')]")
    # 用 XPath 找「文字內容包含『下一頁』」的按鈕，因為這個按鈕的 class 是共用樣式，不夠獨特
    if not next_buttons:                    # 如果清單是空的，代表找不到下一頁按鈕
        print("已是最後一頁")
        break                               # 沒有下一頁了，跳出迴圈

    next_buttons[0].click()                 # 點擊下一頁按鈕，前往下一頁
    time.sleep(random.uniform(2, 4))        # 隨機停頓，等下一頁的內容載入完成
    page_num += 1                           # 頁數計數器加 1，準備進入下一輪迴圈

BASE_DIR = os.path.dirname(__file__)        # 取得這支程式檔案所在的資料夾路徑
csv_path = os.path.join(BASE_DIR, "biggo_result.csv")   # 組合出 CSV 檔案要存放的完整路徑

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:   # 用寫入模式開啟 CSV 檔案
    writer = csv.writer(f)                                          # 建立 CSV 寫入工具
    writer.writerow(["品名", "售價", "連結"])                        # 先寫入標題列，共 3 欄
    for item in all_results:                                        # 走訪收集到的每一筆商品資料
        writer.writerow([item["title"], item["price"], item["href"]])   # 依序把 3 個欄位寫成一列

print(f"儲存成功{csv_path}")                # 印出提示，確認檔案儲存完成
driver.quit()                               # 關閉瀏覽器，釋放資源，程式結束前一定要做這件事
