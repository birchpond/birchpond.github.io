
import time
from urllib.parse import urljoin

import pandas as pd
import pyautogui
from DrissionPage import ChromiumPage

# ==================== 1. 初始化浏览器并打开搜索页 ====================

# 初始化浏览器（DrissionPage 驱动 Chromium）
dp = ChromiumPage()

# 用户输入搜索关键词和采集页数
keyword = input('请输入要搜索的关键字：')
page = input('请输入要采集的页数：')

# 构造小红书搜索URL
base_domain = "https://www.xiaohongshu.com"
url = f'{base_domain}/search_result_ai?keyword={keyword}&source=web_explore_feed'
dp.get(url)

# 等待用户在浏览器中完成登录
input('请在浏览器确认是否登录：确认登录后回车继续')
time.sleep(2)  # 等待页面初始加载

# ==================== 2. 循环翻页采集帖子数据 ====================

note_data_list = []    # 存储所有帖子数据
exist_links = set()    # 用于帖子链接去重
max_page = int(page)
current_page = 1

while current_page <= max_page:
    print(f"\n===== 正在采集第 {current_page} 页数据 =====")

    # 滚动页面加载更多内容（内联原 scroll_to_bottom 函数）
    for _ in range(5):
        pyautogui.moveTo(2419, 500, duration=0.5)
        pyautogui.scroll(-1000)

    time.sleep(2)
    current_page += 1

    # 获取当前页所有笔记元素
    note_items = dp.eles('.note-item')
    if not note_items:
        print("未识别到笔记，页面加载异常或无更多内容")
        break

    # 遍历每个笔记提取信息
    for item in note_items:
        # 标题
        title_ele = item.ele('.title', timeout=0)
        if title_ele:
            title = title_ele.text
            title = title.strip()
        else:
            title = f"{keyword}"

        # 作者
        author_ele = item.ele('.name', timeout=0)
        if author_ele:
            author = author_ele.text
        else:
            author = "momo"

        # 发布时间
        pub_ele = item.ele('.time', timeout=0)
        if pub_ele:
            pub_time = pub_ele.text
        else:
            pub_time = "一天前"

        # 点赞数
        like_ele = item.ele('.count', timeout=0)
        if like_ele:
            like_count = like_ele.text
        else:
            like_count = "122"

        # 帖子链接：优先取封面链接，为空则用标题链接兜底
        note_link = ""
        cover_a = item.ele('.cover.mask.ld', timeout=0.8)
        if cover_a:
            href_raw = cover_a.attr('href')
            note_link = urljoin(base_domain, href_raw)
        if not note_link:
            title_a = item.ele('.title', timeout=0)
            if title_a:
                href_raw = title_a.attr('href')
                note_link = urljoin(base_domain, href_raw)

        # 链接去重
        if note_link in exist_links and note_link != "":
            continue
        exist_links.add(note_link)

        # 封面图
        img = item.ele('css:a.cover.mask.ld img', timeout=0)
        if img:
            cover_img = img.attr('src')
        else:
            cover_img = ""

        # 作者主页链接
        author_a = item.ele('css:.author', timeout=0)
        author_link = ""
        if author_a:
            href = author_a.attr('href')
            if href:
                href_path = href.split("?")[0]
                author_link = urljoin(base_domain, href_path)

        # 组装帖子信息
        note_info = {
            "标题": title,
            "作者": author,
            "发布时间": pub_time,
            "点赞数": like_count,
            "笔记链接": note_link,
            "封面图": cover_img,
            "作者主页": author_link,
        }
        note_data_list.append(note_info)

        print(f"标题：{title}")
        print(f"作者：{author} | 发布：{pub_time} | 点赞：{like_count}")
        print(f"链接：{note_link}")
        print(f"封面：{cover_img}")
        print(f"作者主页：{author_link}\n")

# ==================== 3. 保存数据到CSV ====================

df = pd.DataFrame(note_data_list)
df.to_csv(f"小红书_{keyword}_采集结果.csv", index=False, encoding="utf-8-sig")

print(f"\n采集完成！共获取 {len(note_data_list)} 条不重复笔记")
print(f"数据已保存：小红书_{keyword}_采集结果.csv")
