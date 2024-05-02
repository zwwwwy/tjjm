import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=["工作名称", "单位名称", "需求学历", "工作城市", "薪资", "日期"])

for i in range(1, 78):
    url = f"https://job.rc114.com/JobSearchCate.aspx?Page={i}"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
        "Connection": "keep-alive",
        "Referer": "http://www.baidu.com/",
    }

    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    joblist = soup.find_all(class_="joblist")


    for i in joblist:
        sub_soup = BeautifulSoup(str(i), "html.parser")
        jobname = sub_soup.find(class_="jobname").get_text().strip()
        unitname = sub_soup.find(class_="unitname").get_text().strip()
        edu = sub_soup.find(class_="edu").get_text().strip()
        workcity = sub_soup.find(class_="workcity").get_text().strip()
        salary_tag = sub_soup.find(class_="salary")
        salary = salary_tag.get_text().strip()
        date = salary_tag.find_next_sibling("li").get_text().strip()
        tmp = {"工作名称": jobname, "单位名称": unitname, "需求学历": edu, "工作城市": workcity, "薪资": salary, "日期": date}
        df = df._append(tmp, ignore_index=True)


df.to_excel("job.xlsx", index=False)
