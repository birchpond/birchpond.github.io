

import random
import time
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ==================== 第一部分：爬取豆瓣电影Top250 ====================

# 豆瓣Top250目标URL和请求头
base_url = "https://movie.douban.com/top250"
headers = {
    "referer": "https://movie.douban.com/top250",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}
params = {"start": "0", "filter": ""}

# 用于收集所有电影数据
movie_lists = []

# 共10页，每页25条，通过修改 start 参数翻页
for i in range(10):
    print("正在爬取第{}页数据...".format(i + 1))
    params["start"] = str(i * 25)

    # 请求页面
    response = requests.get(url=base_url, headers=headers, params=params)
    response.encoding = "utf-8"
    html = response.text

    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(html, "lxml")
    ol_element = soup.find("ol", class_="grid_view")
    movie_list = ol_element.find_all("li")

    for movie in movie_list:
        movie_rank = movie.find("em").text.strip()

        pic_div = movie.find('div', class_="pic")
        img_tag = pic_div.find("img")
        movie_name = img_tag.get('alt').strip()

        bd_div = movie.find("div", class_="bd")
        p_tag = bd_div.find('p')
        movie_bd = p_tag.get_text(strip=True).strip()

        movie_score = movie.find('span', class_="rating_num").text.strip()

        span_list = bd_div.find_all('span')
        movie_num = span_list[3].text.strip()

        print(f"{movie_rank}：{movie_name}, {movie_bd}, {movie_score},{movie_num}")
        print('-' * 30)

        # 将数据添加到列表中
        movie_lists.append({
            '电影排名': movie_rank,
            '电影名称': movie_name,
            '电影演员': movie_bd,
            '评分': movie_score,
            '评价人数': movie_num
        })

    # 随机延迟，避免被反爬
    time.sleep(random.uniform(2, 4))

# 保存原始数据到CSV
movie_df = pd.DataFrame(movie_lists)
movie_df.to_csv("douban_top250.csv", index=False, encoding="utf-8",
                columns=['电影排名', '电影名称', '电影演员', '评分', '评价人数'])
print("原始数据保存完成：douban_top250.csv")


# ==================== 第二部分：数据清洗与字段拆分 ====================

# 读取刚才保存的CSV
csv_file = "douban_top250.csv"
movie_df = pd.read_csv(csv_file, encoding="utf-8")

# "电影演员"字段原始格式示例：
# "导演: 张三 主演: 李四/2023/中国大陆/剧情"
# 需要从中拆分出导演、主演、上映年份、上映国家、电影类型

# 提取导演：匹配 "导演: xxx 主演" 之间的内容
director_list = []
for x in movie_df['电影演员']:
    match = re.search(r'导演: (.*?)主演', x)
    if match:
        director_list.append(match.group(1).strip())
    else:
        director_list.append(None)
movie_df['电影导演'] = director_list
print(movie_df['电影导演'])

# 提取主演：匹配 "主演: xxx." 之间的内容
actor_list = []
for x in movie_df['电影演员']:
    match = re.search(r'主演: (.*?)\.', x)
    if match:
        actor_list.append(match.group(1).strip())
    else:
        actor_list.append(None)
movie_df['电影主演'] = actor_list

# 提取上映国家：按 "/" 分割，倒数第二段
country_list = []
for x in movie_df['电影演员']:
    country = x.split('/')[-2].strip()
    country_list.append(country)
movie_df['上映国家'] = country_list

# 提取上映年份：匹配4位数字年份
year_list = []
for x in movie_df['电影演员']:
    match = re.search(r'\d{4}', x)
    if match:
        year_list.append(match.group())
    else:
        year_list.append(None)
movie_df['上映年份'] = year_list

# 提取电影类型：按 "/" 分割，最后一段
type_list = []
for x in movie_df['电影演员']:
    movie_type = x.split('/')[-1].strip()
    type_list.append(movie_type)
movie_df['电影类型'] = type_list

# 删除原始的"电影演员"列
movie_df.drop(columns=['电影演员'], inplace=True)

# 清洗"评价人数"字段，去掉"人评价"文字
movie_df['评价人数'] = movie_df['评价人数'].str.replace('人评价', '')

print(movie_df.head())

# 保存清洗后的数据到新CSV
movie_df.to_csv('douban_top250_new.csv', index=False, encoding="utf-8")
print("清洗后数据保存完成：douban_top250_new.csv")
