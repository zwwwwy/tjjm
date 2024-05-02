import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
    },
)

driver.get("https://kns.cnki.net/kns8/defaultresult/index")
time.sleep(1)
driver.find_element(By.ID, "txt_search").send_keys("人工智能")
driver.find_element(By.CLASS_NAME, "search-btn").click()
time.sleep(20)

k = 0
result_lst = []
while True:
    trs = driver.find_elements(By.XPATH, "//table[@class='result-table-list']/tbody/tr")
    for tr in trs:
        try:
            pubtime = tr.find_element(By.XPATH, "./td[@class='date']").text
        except:
            continue
        if int(pubtime[:4]) > 2023 or int(pubtime[:4]) < 2014:
            continue
        else:
            k += 1
        order = tr.find_element(By.XPATH, "./td[@class='seq']").text
        title = tr.find_element(By.XPATH, "./td[@class='name']").text
        try:
            data = tr.find_element(By.XPATH, "./td[@class='data']").text
        except:
            data = None
        try:
            author = tr.find_element(By.XPATH, "./td[@class='author']").text
        except:
            author = None
        source = tr.find_element(By.XPATH, "./td[@class='source']").text
        try:
            quote = tr.find_element(By.XPATH, "./td[@class='quote']").text
        except:
            quote = None
        try:
            download = tr.find_element(By.XPATH, "./td[@class='download']").text
        except:
            download = None
        result_lst.append(
            {
                "序号": order,
                "题目": title,
                "作者": author,
                "来源": source,
                "发表时间": pubtime,
                "发表类别": data,
                "被引": quote,
                "下载": download,
            },
        )
        print(f"第{k}条数据爬取成功")
    try:
        next = driver.find_element(By.ID, "PageNext").click()
        time.sleep(1.5)
        html = driver.page_source
    except:
        print("没有下一页了")
        break

driver.quit()

df = pd.DataFrame(result_lst)
df.to_csv("./data/爬取的知网论文数据.csv", index=False)
