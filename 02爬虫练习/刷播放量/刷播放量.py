
import time

from DrissionPage import ChromiumPage

# 需要刷播放量的B站视频链接列表
video_urls = [
    'https://www.bilibili.com/video/BV17uMi6HE5g/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1C6M46uEeS/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1TKT76mEPK/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1FVTi6dEUJ/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1bHER6HEr1/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1jkEE6wE9a/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1uLVh66Ezp/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1oDVc6NEVf/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1175y6zELt/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1H75b6sEAL?spm_id_from=333.788.videopod.sections&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1x99xBDEAn/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1k7oYBuEcR/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1AVdmBLEVp/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1cUdnBiE9B/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1rLQnBWELn/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1X3QgBjEBk/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV18dDsBUEds/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1N5DrBQE18/?spm_id_from=333.1365.list.card_archive.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1tAXKBFEGm/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1V9QyB1EAm/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1iHwjzFEJ3/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1duPpzJEJF/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV157A8zPE4Z/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV18DAkzFE4w/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV12i6YBMEFo/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1Vv6EBCE28/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1efkeBFEC5/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1sqrjB4ENP/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV12TquBFEJ9/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1iyB5BAEmB/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1VLBtBhEvg/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1npmuBLE7L/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1kR2yBjE4s/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
    'https://www.bilibili.com/video/BV1AJ2xBbEH2/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1vHUaBMEvR/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1AwbBzqELU/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1skbbzEEr5/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1sbtqzKEiW/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1RUtAzsEH7/?spm_id_from=333.1387.homepage.video_card.click',
    'https://www.bilibili.com/video/BV1VLBtBhEvg/?spm_id_from=333.1387.homepage.video_card.click&vd_source=e8c82dbee7398418e4e6f0ad3df44a90',
]

# 循环1000轮，每轮访问所有视频链接，每个链接停留30秒
for i in range(1000):
    # 每轮创建一个新的浏览器实例
    driver = ChromiumPage()

    # 依次访问每个视频链接，停留30秒以增加播放量
    for video_url in video_urls:
        driver.get(video_url)
        time.sleep(30)

print("完成")
