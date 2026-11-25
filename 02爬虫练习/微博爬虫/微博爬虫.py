
import os
import random
import re
import time
from urllib.parse import quote

import pandas as pd
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# ==================== 1. 初始化配置 ====================

keyword = "人机恋"          # 搜索关键词
max_pages = 5              # 搜索结果翻页数
max_comment_pages = 10     # 每条微博最多采集的评论页数

# 配置浏览器选项
co = ChromiumOptions()
co.set_argument('--no-sandbox')  # 禁用沙箱
page = ChromiumPage(co)

# requests会话
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://m.weibo.cn/',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/plain, */*'
}

# 存储所有采集结果
results = []

# ==================== 2. 登录微博并同步Cookie ====================

print("正在打开微博首页...")
page.get('https://weibo.com')

print("请在打开的浏览器中完成登录（扫码或账号登录）。")
print("程序将自动检测登录状态...")

# 循环检测是否登录成功（检测Cookie中是否有 SUB）
while True:
    cookies_list = page.cookies()
    cookies = {}
    for c in cookies_list:
        cookies[c['name']] = c['value']
    if 'SUB' in cookies:
        print("检测到登录成功！")
        break
    time.sleep(2)

# 跳转到移动端首页，确保Cookie对移动端接口有效
print("正在同步移动端Cookie...")
page.get('https://m.weibo.cn')
time.sleep(2)

# 将浏览器Cookie同步到requests session
cookies_list = page.cookies()
cookies = {}
for c in cookies_list:
    cookies[c['name']] = c['value']
session.cookies.update(cookies)
# 更新XSRF-TOKEN到请求头（如果存在）
if 'XSRF-TOKEN' in cookies:
    headers['X-XSRF-TOKEN'] = cookies['XSRF-TOKEN']
print("Cookie获取成功。")

# ==================== 3. 搜索话题并获取微博列表 ====================

print(f"开始搜索话题: {keyword}")
base_url = "https://m.weibo.cn/api/container/getIndex"

# 关键词URL编码，防止中文导致header编码错误
encoded_keyword = quote(keyword)

for page_num in range(1, max_pages + 1):
    print(f"正在爬取第 {page_num} 页微博列表...")

    params = {
        'containerid': f'100103type=1&q={keyword}',
        'page_type': 'searchall',
        'page': page_num
    }

    try:
        # 必须带上Referer，且中文必须编码
        headers['Referer'] = f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{encoded_keyword}"
        resp = session.get(base_url, params=params, headers=headers)

        if resp.status_code != 200:
            print(f"请求失败: {resp.status_code}")
            continue

        data = resp.json()
        if data.get('ok') != 1:
            print("当前页无数据或接口限制")
            break

        data_obj = data.get('data', {})
        cards = data_obj.get('cards', [])

        # ==================== 4. 处理每条微博 ====================
        for card in cards:
            if card.get('card_type') != 9:  # 9是微博正文
                continue

            mblog = card.get('mblog', {})

            # 提取微博基本信息
            mid = mblog.get('id')
            blog_user_obj = mblog.get('user', {})
            blog_user = blog_user_obj.get('screen_name')
            blog_text = mblog.get('text')            # 可能含HTML标签
            comments_count = mblog.get('comments_count')
            blog_like = mblog.get('attitudes_count')  # 点赞数
            blog_repost = mblog.get('reposts_count')   # 转发数

            print(f"发现微博: {mid} by {blog_user}, 评论数: {comments_count}")

            # ==================== 5. 获取该微博的评论 ====================
            if comments_count > 0:
                # 调用评论接口获取评论
                comment_url = "https://m.weibo.cn/comments/hotflow"
                comment_params = {
                    'id': mid,
                    'mid': mid,
                    'max_id_type': 0
                }

                page_count = 0
                while page_count < max_comment_pages:
                    try:
                        headers['Referer'] = f"https://m.weibo.cn/detail/{mid}"
                        resp = session.get(comment_url, params=comment_params, headers=headers)

                        if resp.status_code != 200:
                            break

                        c_data = resp.json()
                        if c_data.get('ok') != 1:
                            break

                        data_data = c_data.get('data', {})
                        comments = data_data.get('data')
                        if not comments:
                            comments = []

                        if not comments:
                            break

                        # ==================== 6. 保存每条评论数据 ====================
                        for c in comments:
                            c_user_obj = c.get('user', {})
                            c_user = c_user_obj.get('screen_name')
                            c_text = c.get('text')                    # 含HTML
                            c_like = c.get('like_count', 0)
                            c_reply = c.get('total_number', 0)        # 回复该评论的数量

                            # 清洗HTML标签
                            clean_blog_text = re.sub(r'<[^>]+>', '', str(blog_text))
                            clean_comment_text = re.sub(r'<[^>]+>', '', str(c_text))

                            results.append({
                                '微博ID': mid,
                                '博主': blog_user,
                                '微博内容': clean_blog_text,
                                '微博点赞': blog_like,
                                '微博转发': blog_repost,
                                '评论用户': c_user,
                                '评论内容': clean_comment_text,
                                '评论点赞': c_like,
                                '评论回复数': c_reply
                            })

                        # 获取下一页的 max_id
                        max_id = data_data.get('max_id')
                        if max_id == 0 or not max_id:
                            break

                        comment_params['max_id'] = max_id
                        page_count += 1
                        time.sleep(random.uniform(1, 2))

                    except Exception as e:
                        print(f"获取评论出错: {e}")
                        break
            else:
                # 即使没评论也保存微博本身的信息
                clean_blog_text = re.sub(r'<[^>]+>', '', str(blog_text))
                results.append({
                    '微博ID': mid,
                    '博主': blog_user,
                    '微博内容': clean_blog_text,
                    '微博点赞': blog_like,
                    '微博转发': blog_repost,
                    '评论用户': "N/A",
                    '评论内容': "无评论",
                    '评论点赞': 0,
                    '评论回复数': 0
                })

        # 随机延时，防止封号
        time.sleep(random.uniform(2, 4))

    except Exception as e:
        print(f"搜索页出错: {e}")

# ==================== 7. 保存数据到Excel ====================

if not results:
    print("没有爬取到数据。")
else:
    df = pd.DataFrame(results)
    df.to_excel("weibo_comments.xlsx", index=False)
    print(f"数据已保存到 weibo_comments.xlsx, 共 {len(df)} 条记录。")
