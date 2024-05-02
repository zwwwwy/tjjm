import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import urllib3

urllib3.disable_warnings()

df = pd.DataFrame(
    columns=[
        "工作名称",
        "单位名称",
        "需求学历",
        "工作城市",
        "薪资",
        "日期",
        "大类",
        "小类",
        "工作经验",
        "招聘人数",
        "工作性质",
        "专业要求",
        "工作地点",
    ]
)


base = "https://job.rc114.com/"

for i in tqdm(range(1, 78)):
    url = f"https://job.rc114.com/JobSearchCate.aspx?Page={i}"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
        "Referer": "http://www.baidu.com/",
        "Connection": "close",
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

        u = sub_soup.find(class_="jobname").find("a")["href"]
        sub_response = requests.get(base + u, headers=headers)

        sub_soup = BeautifulSoup(sub_response.text, "html.parser")
        hlJobCateBig = sub_soup.find(id="hlJobCateBig")
        hlJobCateSmall = sub_soup.find(id="hlJobCateSmall")
        jobItem = sub_soup.find(class_="JobItem")

        if not jobItem:
            time.sleep(1)
            continue

        cate1 = jobItem.find(id="hlJobCateBig").text
        cate2 = jobItem.find(id="hlJobCateSmall").text

        expr = jobItem.find(string="工作经验：")
        if expr:
            expr = expr.parent.next_sibling.strip()
        else:
            expr = "nan"
        num = jobItem.find(string="招聘人数：")
        if num:
            num = num.parent.next_sibling.strip()
        else:
            num = "nan"
        attr = jobItem.find(string="工作性质：")
        if attr:
            attr = attr.parent.next_sibling.strip()
        else:
            attr = "nan"
        zyyq = jobItem.find(string="专业要求：")
        if zyyq:
            zyyq = zyyq.parent.next_sibling.strip()
        else:
            zyyq = "nan"
        gzdd = jobItem.find(string="工作地点：")
        if gzdd:
            gzdd = gzdd.parent.next_sibling.strip()
        else:
            gzdd = "nan"

        tmp = {
            "工作名称": jobname,
            "单位名称": unitname,
            "需求学历": edu,
            "工作城市": workcity,
            "薪资": salary,
            "日期": date,
            "大类": cate1,
            "小类": cate2,
            "工作经验": expr,
            "招聘人数": num,
            "工作性质": attr,
            "专业要求": zyyq,
            "工作地点": gzdd,
        }
        df = df._append(tmp, ignore_index=True)

df.to_excel("job_detail.xlsx", index=False)
