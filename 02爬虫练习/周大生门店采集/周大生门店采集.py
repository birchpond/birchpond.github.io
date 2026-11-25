
import json
import random
import time

import pandas as pd
import requests

# ==================== 1. 配置请求参数 ====================

# 周大生官网门店查询接口URL
url = "https://www.chowtaiseng.com/dupusearch"

# 请求头（模拟浏览器AJAX请求）
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://www.chowtaiseng.com/Retailnetwork/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# Cookie（网站会话标识，需定期更新）
cookies = {
    "acw_tc": "0a05830e17797619651047520e32ae568248293617056f3fdbe687f364965d",
    "think_lang": "zh-cn",
    "PHPSESSID": "972ce218866e6e3e02c76b2df19fc629",
    "Hm_lvt_e1bfb956a372b4617e2a9917b65f6c78": "1779761966",
    "HMACCOUNT": "C0562A90DC7EFAC9",
    "qimo_seosource_4b2b51b0-3316-11ec-9d5c-cdb4d343a0b6": "%E7%AB%99%E5%86%85",
    "qimo_seokeywords_4b2b51b0-3316-11ec-9d5c-cdb4d343a0b6": "",
    "qimo_xstKeywords_4b2b51b0-3316-11ec-9d5c-cdb4d343a0b6": "",
    "href": "https%3A%2F%2Fwww.chowtaiseng.com%2F",
    "accessId": "4b2b51b0-3316-11ec-9d5c-cdb4d343a0b6",
    "pageViewNum": "1",
    "Hm_lpvt_e1bfb956a372b4617e2a9917b65f6c78": "1779763518",
}

# ==================== 2. 解析城市数据 ====================
# 读取 cityList.json，将其整理为 [{省份: [城市1, 城市2, ...]}, ...] 的结构
# cityList.json 格式：{"编码": "名称", ...}
#   - 编码以 "0000" 结尾的是省份
#   - 编码以 "00" 结尾（但非 "0000"）的是该省份下的城市

with open("cityList.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 解析省份-城市层级关系
city_datas = []
current_province = None

for code, name in raw_data.items():
    if code.endswith("0000"):
        # 新省份
        current_province = {name: []}
        city_datas.append(current_province)
    elif current_province is not None:
        if code.endswith("00"):
            # 城市添加到当前省份下
            province_keys = list(current_province.keys())
            province_name = province_keys[0]
            current_province[province_name].append(name)

print(f"城市数据解析完成，共 {len(city_datas)} 个省份")

# ==================== 3. 遍历城市采集门店数据 ====================

# 存储所有门店数据
dupu_datas = {"店铺名": [], "地址": []}

for data in city_datas:
    for province, citys in data.items():
        for city in citys:
            print(f"正在采集：{province} - {city}")

            # 更新Cookie中的时间戳
            cookies["Hm_lpvt_e1bfb956a372b4617e2a9917b65f6c78"] = str(int(time.time()))

            # 请求参数：cid=42（门店分类），city=城市名，province=省份名
            params = {
                "cid": "42",
                "catesearch": "",
                "city": city,
                "province": province,
            }

            # 发送GET请求
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            dict_datas = json.loads(response.text)

            # 解析门店数据
            try:
                for item in dict_datas["data"]:
                    dupu_name = item["title"]      # 门店名称
                    dupu_address = item["summary"]  # 门店地址
                    dupu_datas["店铺名"].append(dupu_name)
                    dupu_datas["地址"].append(dupu_address)
                    print(f"  店铺名: {dupu_name}, 地址: {dupu_address}")
                    print("  " + "-" * 60)
            except:
                print(f"  数据异常：{dict_datas}")

            # 随机延时3~5秒，防止被封
            time.sleep(random.uniform(3, 5))

# ==================== 4. 保存数据到CSV ====================

df = pd.DataFrame(dupu_datas)
df.to_csv("dupu_datas.csv", index=False, encoding="utf-8")
print(f"\n采集完成！共获取 {len(dupu_datas['店铺名'])} 家门店，已保存到 dupu_datas.csv")
