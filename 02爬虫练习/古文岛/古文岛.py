
import requests
from lxml import etree

# 1 确定url - 古诗文网《黄帝内经》目录页
url = 'https://www.gushiwen.cn/guwen/book_1bf1210e9d1f.aspx'

# 定义请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# 2 发送请求，获取目录页HTML
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
html = response.text

# 3 解析数据，逐章采集并写入TXT文件
idx = 1
with open('皇帝内经全文.txt', 'a', encoding='utf-8') as file:
    tree = etree.HTML(html)
    bookconts = tree.xpath('//div[@class="bookcont"]')

    for bookcont in bookconts:
        spans = bookcont.xpath('./div[2]/span')
        for span in spans:
            # 获取章节详情页链接
            hrefs = span.xpath('./a/@href')
            if not hrefs:
                continue
            links = 'https://www.gushiwen.cn/' + hrefs[0]

            # 发送请求，获取详情页数据
            response = requests.get(links, headers=headers)
            response.encoding = 'utf-8'
            detail_html = response.text

            # 解析详情页数据
            print(f'正在解析第{idx}章：{links}')
            idx += 1
            detail_tree = etree.HTML(detail_html)
            title_list = detail_tree.xpath('//div[@class="sons"]//h1/span/b/text()')
            title = title_list[0]
            content_elements = detail_tree.xpath('//div[@class="contson"]/p')
            content_list = []
            for element in content_elements:
                texts = element.xpath('.//text()')
                if texts:
                    text_str = ''.join(texts)
                    content_list.append(text_str + '\n')

            # 如果没有p标签，直接从div中获取所有文本
            if not content_list:
                content_list = detail_tree.xpath('//div[@class="contson"]//text()')

            content_text = ''.join(content_list)

            # 写入数据到txt文件中
            file.write(title + '\n' + content_text + '\n\n')
