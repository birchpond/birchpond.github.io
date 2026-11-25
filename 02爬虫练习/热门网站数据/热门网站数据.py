
import requests
from lxml import etree
import pandas as pd
import openpyxl

# 配置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 用于存储所有网站分类的数据，格式为：{"旅游网站": [ {...}, {...} ], ...}
site_datas = {}

# 1 请求首页的HTML内容
start_page = 'https://top.chinaz.com/hangyemap.html'
response = requests.get(start_page, headers=headers)
start_html = response.text

# 2 解析首页的热门网站分类及链接
first_etrees = etree.HTML(start_html)
urls = first_etrees.xpath('//div[@class="TopMapHot mb20"]/ul')

for ul in urls:
    for li in ul.xpath('./li'):
        site_name = li.xpath('./a/text()')[0]
        site_url = li.xpath('./a/@href')[0]
        print(site_name, site_url)
        site_datas[site_name] = []  # 构建存储数据的字典

        # 3 请求每个网站分类的HTML内容
        lists_html = requests.get(site_url, headers=headers).text

        # 4 解析每个网站分类的网站名、网站链接、网站排名、网站得分
        second_etree = etree.HTML(lists_html)
        for li in second_etree.xpath('//ul[@class="listCentent"]/li'):
            data_temp_dict = {}  # 创建临时字典:存储每个列表项的数据

            # 拼接详细页的链接地址
            list_url = "https://top.chinaz.com" + li.xpath('./div[@class="leftImg"]/a/@href')[0]
            data_temp_dict['网站'] = li.xpath('./div[2]/h3/a/text()')[0]
            data_temp_dict['排名'] = li.xpath('./div[3]/div/strong/text()')[0]
            data_temp_dict['得分'] = li.xpath('./div[3]/div/span/text()')[0][3:]  # 去掉前3个字符（"得分："）

            # 5 请求每个网站的详情页
            detail_html = requests.get(list_url, headers=headers).text

            # 6 解析详情页: 百度权重、360权重、APPPC排名、关键词数、APPPC反向PR
            three_etree = etree.HTML(detail_html)
            for ul in three_etree.xpath('//ul[@class="wkdate_tul"]'):
                data_temp_dict['百度权重'] = ul.xpath('./li[1]/div/comdiv/text()')[0]
                data_temp_dict['360权重'] = ul.xpath('./li[2]/div/comdiv/text()')[0]
                # 获取APPPC排名（可能为空，需要判断）
                appc_rank_list = ul.xpath('./li[3]/div/comdiv/a/text()')
                if len(appc_rank_list) > 0:
                    data_temp_dict['APPPC排名'] = appc_rank_list[0]
                else:
                    data_temp_dict['APPPC排名'] = ''
                data_temp_dict['关键词数'] = ul.xpath('./li[4]/div/comdiv/text()')[0]
                data_temp_dict['APPPC反向PR'] = ul.xpath('./li[5]/div/a/comdiv/text()')[0]

                site_datas[site_name].append(data_temp_dict)
                print(data_temp_dict)

# 7 保存数据到Excel文件
if site_datas:  # 确保有数据才保存
    # 使用openpyxl创建Excel工作簿，逐个分类创建sheet
    wb = openpyxl.Workbook()
    # 删除默认创建的空sheet
    wb.remove(wb.active)

    for category_name, data_list in site_datas.items():
        if data_list:  # 确保当前分类有数据
            # 创建对应分类的sheet
            ws = wb.create_sheet(title=category_name)
            # 获取所有字段名（作为表头）
            field_names = list(data_list[0].keys())
            # 写入表头
            col_idx = 1
            for field_name in field_names:
                ws.cell(row=1, column=col_idx, value=field_name)
                col_idx += 1
            # 写入数据行
            row_num = 2
            for data in data_list:
                col_num = 1
                for field_name in field_names:
                    ws.cell(row=row_num, column=col_num, value=data[field_name])
                    col_num += 1
                row_num += 1
            print(f"已将{category_name}分类写入到对应的 sheet 中")

    wb.save('热门网站数据.xlsx')
    print("所有数据成功写入Excel文件！")
else:
    print("没有获取到任何数据，无法创建Excel文件")
