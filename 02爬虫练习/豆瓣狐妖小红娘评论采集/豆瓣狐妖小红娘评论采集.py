
import random
import time

import pandas as pd
import requests
from lxml import etree

# ==================== 1. 配置请求参数 ====================

# 豆瓣电影《狐妖小红娘》长评页面URL
# subject ID: 26435736
url = "https://movie.douban.com/subject/26435736/reviews"

# 请求头（模拟浏览器访问）
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://movie.douban.com/subject/26435736/reviews?sort=hotest&start=20",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

# Cookie（豆瓣登录态，需定期更新）
cookies = {
    "bid": "vk5JqDDnh7I",
    "_pk_id.100001.4cf6": "0080df312b3ffb81.1763782331.",
    "ll": "\"118318\"",
    "_vwo_uuid_v2": "DF9F7F7F3D58AEE19F39DF6107E25445A|c872b33285ea0423f7e95c3cb684320c",
    "dbcl2": "\"250171040:8Wy1sbv4hbs\"",
    "push_noty_num": "0",
    "push_doumail_num": "0",
    "__utmv": "30149280.25017",
    "ct": "y",
    "__utmz": "223695111.1768885404.7.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search",
    "ck": "eU40",
    "ap_v": "0,6.0",
    "frodotk_db": "\"50e588131120a7d3f2b098393361f779\"",
    "__utma": "223695111.751770581.1763782332.1768834001.1768885404.7",
    "__utmc": "223695111",
    "__utmb": "30149280.10.10.1768885390",
    "_pk_ref.100001.4cf6": "%5B%22%22%2C%22%22%2C1768885404%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3D%E7%8B%90%E5%A6%96%E5%B0%8F%E7%BA%A2%E5%A8%98%22%5D",
    "_pk_ses.100001.4cf6": "1",
    "__utmt": "1"
}

# 用于存储所有评论数据
datas = []

# ==================== 2. 循环翻页采集 ====================

# 豆瓣每页20条评论，start参数从0开始，每次递增20
# 共采集401/20+1≈21页
for i in range(0, 401, 20):
    print(f"正在处理第 {i // 20 + 1} 页评论...")

    # 翻页参数：sort=hotest按热度排序，start=偏移量
    params = {
        "sort": "hotest",
        "start": str(i)
    }

    # 发送GET请求获取页面HTML
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    html = response.text

    # 使用lxml解析HTML
    tree = etree.HTML(html)

    # 提取评论列表中的每一条评论
    divs = tree.xpath('//div[@class="review-list  "]/div')
    for div in divs:
        # 作者昵称
        name = div.xpath('./div/header/a[@class="name"]/text()')[0]
        # 投票/回应数（去除"回应"文字）
        vote = div.xpath('./div/div/div[3]/a[@class="reply "]/text()')[0]
        if "回应" in vote:
            vote = vote.replace("回应", "")
        # 发布日期
        date = div.xpath('./div/header/span[@class="main-meta"]/text()')[0]

        # 评论内容：获取 short-content 下所有文本节点并拼接
        # 兼容包含 <p class="spoiler-tip"> 的情况，忽略 <p> 和 <a> 标签内文字
        content_list = div.xpath('.//div[@class="short-content"]/text()')
        # 去除每段文本首尾空白，存入新列表
        stripped_list = []
        for t in content_list:
            stripped_list.append(t.strip())
        # 拼接成完整字符串
        content = "".join(stripped_list)
        # 清理换行和括号
        content = content.replace("\n", "")
        content = content.replace("(", "")
        content = content.replace(")", "")

        print(name, vote, date, content)
        print('-' * 50)
        datas.append([name, vote, date, content])

        # 暂停1~3秒，避免触发豆瓣的 too many requests 限制
        time.sleep(random.uniform(1, 3))

# ==================== 3. 保存数据到Excel ====================

df = pd.DataFrame(datas, columns=['发帖人', '投票数', '日期', '评论内容'])
df.to_excel('douban_reviews.xlsx', index=False)
print(f"采集完成！共获取 {len(datas)} 条评论，已保存到 douban_reviews.xlsx")
