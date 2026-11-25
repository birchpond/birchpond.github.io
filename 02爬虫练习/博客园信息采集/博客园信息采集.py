
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 基础网址（博客园首页文章列表分页）
url_root = 'https://www.cnblogs.com/sitehome/p/'

# 请求头
headers = {
    "Referer": "https://www.cnblogs.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# 构建链接 - 爬取第2-10页的文章数据
urls = []
for i in range(2, 10):
    urls.append(url_root + f'{i}')

print("开始爬取博客园信息...")
print(f"目标页面：{len(urls)}个")

# 循环每个url，获取信息
all_data = []
page_num = 0

for url in urls:
    page_num += 1
    print(f'正在爬取: 第{page_num}页, url: {url}')

    # 发送请求获取页面
    re = requests.get(url, headers=headers)

    # 判断是否爬取成功
    if re.status_code != 200:
        print('error!')
        continue

    soup = BeautifulSoup(re.text, "html.parser")

    # 找到文章列表
    articles = soup.find('div', id='post_list', class_='post-list').find_all('article', class_='post-item')

    # 解析每篇文章的信息
    for article in articles:
        author, comment, recomment, views = '', 0, 0, 0  # 创建初始值
        infos = article.find_all('a')

        for info in infos:
            if 'post-item-title' in str(info):
                href = info['href']
                title = info.get_text()
            if 'post-item-author' in str(info):
                author = info.get_text().strip()
            if 'icon_comment' in str(info):
                comment = info.get_text().strip()
            if 'icon_digg' in str(info):
                recomment = info.get_text().strip()
            if 'icon_views' in str(info):
                views = info.get_text().strip()

        all_data.append([href, title, author, comment, recomment, views])

print(f'爬取完成，共爬取{len(urls)}个页面')
print(f'获取到{len(all_data)}篇文章信息')

# 写入 Excel
df = pd.DataFrame(all_data, columns=['href', 'title', 'author', 'comment', 'recomment', 'views'])
df.to_excel('文章信息爬取结果.xlsx', index=True)

print("数据已保存到 '文章信息爬取结果.xlsx'")
