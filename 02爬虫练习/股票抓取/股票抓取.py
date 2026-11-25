
import csv
import json
import random
import time

import requests

# ==================== 1. 配置请求参数 ====================

# 百度财经股票讨论接口URL
url = "https://finance.pae.baidu.com/vapi/v1/stocktalklist"

# 请求头（模拟浏览器访问）
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

# Cookie（登录态，需定期更新）
cookies = {
    "BIDUPSID": "E1866DC7FD2C2BAF18171243D039AF84",
    "PSTM": "1763189752",
    "MAWEBCUID": "web_PSXybQOZxvsGSjRSGwVXjpuiRlOafsQnrTyWRnvMYOysfEbtRU",
    "BAIDUID": "38E25368E67FB690B62035658FFEE2CB:FG=1",
    "BDUSS": "FyWEJNQmtpUjhUcEFabmY0djFDMmRXdXVUMzlDTFQyQTZzVUh1MDd1NXhFeVJxSUFBQUFBJCQAAAAAAAAAAAEAAAAAxjgxs8zQ8tSxyq6wywAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGG~GlxhvxpYz",
    "BDUSS_BFESS": "FyWEJNQmtpUjhUcEFabmY0djFDMmRXdXVUMzlDTFQyQTZzVUh1MDd1NXhFeVJxSUFBQUFBJCQAAAAAAAAAAAEAAAAAxjgxs8zQ8tSxyq6wywAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGG~GlxhvxpYz",
    "MCITY": "-75%3A",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "H_WISE_SIDS_BFESS": "63143_67861_68166_68465_68738_69007_69158_69187_69227_69244_69241_69232_69235_69251_69373_69402_69396_69419_69416_69414_69423_69446_69431_69452_69338_69348_69517_69576_69593_69650_69668_69664_69658_69746_69720_69763_69798_69779_69808_69842_69920_69915_69906_69955_69961_70007",
    "BDSFRCVID_BFESS": "dyAOJeCmH4ei3Ov83TD8T9G4P2KK0gOTHllPy_J94MD0ETDVJeC6EG0Ptf8g0KuKgEnYogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0M5",
    "H_BDCLCKID_SF_BFESS": "JbkOVCDKJIP3qn7I5b-_5nkb2lJ8etJXfKn85l7F5lOVOKbNMjbc56vy3-8OLTcxJN4HahkM5h7xObR10brry6c3Xt8j0l3RQeQ-5KQN3KJmfbL9bT3v5fPsQfTk2-biWbRM2MbdJqvP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe4bK-TrBDaOP",
    "BAIDUID_BFESS": "38E25368E67FB690B62035658FFEE2CB:FG=1",
    "H_PS_PSSID": "63143_67861_68166_68465_68738_69007_69158_69187_69227_69244_69241_69235_69251_69373_69419_69416_69414_69423_69446_69431_69452_69593_69650_69746_69720_69763_69798_69779_69808_69842_69920_69915_69906_69955_69961_70007_70026_70051_70022_70098_70037_70057_70056_70117_70130_70146_70157_70164_70220",
    "BA_HECTOR": "8k84800lah2l0k812584ag2kah240n1l0h10026",
    "H_WISE_SIDS": "63143_67861_68166_68465_68738_69007_69158_69187_69227_69244_69241_69235_69251_69373_69419_69416_69414_69423_69446_69431_69452_69593_69650_69746_69720_69763_69798_69779_69808_69842_69920_69915_69906_69955_69961_70007_70026_70051_70022_70098_70037_70057_70056_70117_70130_70146_70157_70164_70220",
    "ZFY": "4jGMXc7AWyYpMo1:BjhW:BSJXp4h7YU:AsrrSXVvFY42Wk:C",
    "ab_sr": "1.0.1_ODEwNjAxNzhlZTU2OTJmZWI2YTA5NzBjOTE0YWZhNWI4NGY3OGM4MDMyMDY2MjRhZjRmMTE0ZGI3YzUzOWE5MzU3NzFhYWRhMDliNzhmYjQ3ZWU0NTg5ZGQ0ZjhmNjJkYTcxMDgyOTk5ODIyN2FmY2MwMTE3ZGJhZjMyNTVhOTUwZmZlMmI5OWM4NDY0YzdmNTdiMzM5ZjZlNWM1ZTUxNw==",
    "ppfuid": "FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGlz0XNorb0vz5CKQS8JxegdGEimjy3MrXEpSuItnI4KDymT2lyQbips1ItIErRL+oahVhxaw/3fSGCUDnH8ryrFqqUTo6WPP4TTQmKEAyd5WBJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFz67xpujr1V+of2ZgvZNzVJUmpzMha9QJygwaQJhnJSof5888Agag7GYPbuhrpUhzFCMUN0p4SXVVUMsKNJv2T2Q0Rs14gDuqHJ3rxHJuOGO4LkPV+7TROLMG0V6r0A++zkWOdjFiy1D/0R8HcRWYvoof6mSAGHJpuboM5joRsCp+HBavJhpxl858h16cMtKQmxzisHOxsE/KMoDNYYE7ucLE22Bi0Ojbor7y6SXfVj7+B4iuZO+f7FUDWABtt/WWQqHKVfXMaw5WUmKnfSR5wwQa+N01amx6X+p+x97kkGmoNOSwxWgGvuezNFuiJQdt51yrWaL9Re9fZveXFsIu/gzGjL50VLcWv2NICayyI8BE9m62pdBPySuv4pVqQ9Sl1uTC//wIcO7QL9nm+0N6JgtCkSAWOZCh7Lr0XP6QztjlyD3bkwYJ4FTiNanaDaDyN+aYIFvoYQvffND5NS2a3TWPC3tx8O/N6iBMjj4Ofj9724h8n7mnXcVqW23AVVnSGk66HDxtjKMU4HPNa0dthF7UsHf7NW9eE+gwuTQSa7GLWfOy9+ap4iFBQsmjpefgOF89jAHLbnVUejtrqqvdeh0/gTYfZ0rcnDTfBJCgA7wmoY7Tjo9rTYHsjSc+LeecoO1Q3Mrq3/V8K23ixqVccD05kuRm4sFZh/o1XJ6o5ZazU62XvOvycqQeNHJHilKXv+Y0q7CT6wHNqzprY+XMxDln8dKB7nefcEun8dlqoZs4uNOo+pkpyckwWP4VbWloC92vUUtZ2lVqKiGsvJKvLgaUA9sPnxLHpdf4XomqPJzwaYMRRvnyvNvptYm/H9TJ82EtrgcP/nqg17T/hHrOFW2byp/ouxpI4lF8dQtOogBfcrGXrDHbdYEoz55OAGISs/kEn2kikYfHcMOTvlvvhFwa2niOwlDexBAHoYSDqUJcXe6HpWGsfMtkPHUjgkj"
}

# 请求参数：code=股票代码，name=股票名称，pn=页码（每页10条）
params = {
    "from_smart_app": "0",
    "code": "000651",          # 格力电器股票代码
    "name": "格力电器",
    "market": "ab",
    "finance_type": "stock",
    "method": "taglist",
    "rn": "10",                # 每页条数
    "pn": "0",                 # 页码偏移量
    "sub_tab": "all",
    "finClientType": "pc"
}

# ==================== 2. 采集数据并保存 ====================

# 打开CSV文件，写入表头
with open('格力电器1.csv', 'a', encoding='utf-8', newline='') as wf:
    writer = csv.writer(wf)
    writer.writerow(['作者', '时间', '平台', '内容'])

    # 循环翻页采集，共采集200页
    for i in range(200):
        # 设置当前页码：pn 每页递增10
        params['pn'] = i * 10

        # 发送GET请求
        response = requests.get(url, headers=headers, cookies=cookies, params=params)

        # 将响应JSON文本转为字典
        datas = json.loads(response.text)

        # 解析每条讨论数据
        for data in datas['Result']['list']:
            author = data["author"]['name']              # 作者昵称
            date = data['create_show_time']              # 发布时间
            provider = data['provider']                  # 来源平台
            # 讨论内容
            content_items = data['content']['items']
            content = content_items[0]['data']

            # 写入CSV并打印
            writer.writerow([author, date, provider, content])
            print('已保存数据：', author, date, provider, content)

        # 随机延时3~5秒，防止被封
        time.sleep(random.uniform(3, 5))

        print('第', i, '页数据已保存完成')
        print('-' * 50)
