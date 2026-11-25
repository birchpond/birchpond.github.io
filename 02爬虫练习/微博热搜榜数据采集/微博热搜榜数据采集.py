
import requests

# 请求头
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-HK;q=0.5",
    "client-version": "3.0.0",
    "priority": "u=1, i",
    "referer": "https://weibo.com/hot/weibo/102803",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2026.06.10.4",
    "traceparent": "00-2e5b5c012c20d3a076dd9df4b8fff6fb-3e3bf735750968fc-00",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "oyofmWs6noTrr8yjgc8QpBCe"
}

# Cookie信息（需从浏览器中获取有效的登录Cookie）
cookies = {
    "SCF": "AtVakH5ntBIRk-QHeqtrIw9bzUnU62jB-ObrmwQyzeSfWfxtLQRDv-rolMtOxnI3pVySXVsQZzzPAwaYsn5jSzQ.",
    "SINAGLOBAL": "9626632718097.447.1755267824584",
    "ULV": "1775712988621:15:1:1:6983495833024.321.1775712988618:1768898083547",
    "XSRF-TOKEN": "oyofmWs6noTrr8yjgc8QpBCe",
    "PC_TOKEN": "582e12ec54",
    "SUB": "_2A25HLREUDeRhGeFG6lAS8ybOwjuIHXVkQyzcrDV8PUNbmtAbLWuikW9Nfl-29UGTLz1B_naYKpRStq_EXj1oWFYl",
    "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFNhcPaLLOfnYw.HVBOGCfN5JpX5KzhUgL.FoMReKz0e0nE1KM2dJLoI7UoIsvaIsD3",
    "ALF": "02_1783688772",
    "WBPSESS": "EuA_13Fg7hDkis4OlssbW76fiRgfoNyRFcD-NGsQD5XhqetaHSFaMPmA2VUxJWWygbHACaAm04St6Rlbbj_-HAKSO8ncleRb6w9A_L7lG28c9y1L7-ngtn80VMi8Eumd0fQqgnr_iliPWJOw-Ifdpw=="
}

# 微博热搜时间线Ajax接口
url = "https://weibo.com/ajax/feed/hottimeline"

# 请求参数
params = {
    "since_id": "0",
    "refresh": "0",
    "group_id": "102803",
    "containerid": "102803",
    "extparam": "discover|new_feed",
    "max_id": "0",
    "count": "10"
}

# 发送请求获取数据
response = requests.get(url, headers=headers, cookies=cookies, params=params)
res_json = response.json()

# 检查接口是否请求成功
if res_json.get("ok") != 1:
    print("cookie过期，或请求失败")
else:
    # 遍历每条微博
    status_list = res_json.get("statuses", [])
    idx = 0
    for item in status_list:
        idx += 1
        print(f"===== 第{idx}条微博 =====")
        # 发布时间
        create_time = item.get("created_at", "")
        # 微博ID
        mblog_id = item.get("mblogid", "")
        # 发布用户信息
        user_info = item.get("user", {})
        username = user_info.get("screen_name", "")
        user_avatar = user_info.get("avatar_large", "")
        # 微博正文
        content = item.get("text", "")
        # 互动数据：转发、评论、点赞
        total_counter = user_info.get("status_total_counter", {})
        repost = total_counter.get("repost_cnt", 0)
        comment = total_counter.get("comment_cnt", 0)
        like = total_counter.get("like_cnt", 0)
        # 图片
        pic_num = item.get("pic_num", 0)
        pic_infos = item.get("pic_infos", {})
        pic_urls = []
        if pic_infos:
            for val in pic_infos.values():
                pic_urls.append(val["original"]["url"])

        # 打印结果
        print(f"发布用户：{username}")
        print(f"发布时间：{create_time}")
        print(f"微博ID：{mblog_id}")
        print(f"正文内容：{content}")
        print(f"转发：{repost} | 评论：{comment} | 点赞：{like}")
        print(f"图片数量：{pic_num}")
        if pic_urls:
            print(f"原图链接：{pic_urls}")
        print("-" * 60)
