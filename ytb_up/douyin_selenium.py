# -*- encoding: utf-8 -*-
'''
@File    :   auto_publish.py
@Time    :   2022/04/25 21:25:30
@Author  :   DongDongGe 
@Version :   1.0
@Contact :   412719702@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   自动发布模块
'''
from selenium import webdriver
import random
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
driver = webdriver.Chrome(options=options)


def publish_douyin(video_abs_path, title, describe):

    # 进入创作者页面，并上传视频
    driver.get("https://creator.douyin.com/creator-micro/home")
    time.sleep(5)
    driver.find_element_by_xpath('//*[text()="发布视频"]').click()
    time.sleep(5)
    driver.find_element_by_xpath(
        '//input[@type="file"]').send_keys(video_abs_path)

    # 等待视频上传完成
    while True:
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//*[text()="重新上传"]')
            break
        except Exception as e:
            print("视频还在上传中···")

    print("视频已上传完成！")

    time.sleep(5)
    # 输入视频描述(标题)
    try:
        driver.find_element_by_xpath(
            '//div[@aria-autocomplete="list"]//br').send_keys(title + describe)
    except Exception as e:
        driver.find_element_by_xpath(
            '//div[@aria-autocomplete="list"]//br').send_keys(describe)
    # 人工进行检查并发布
    # time.sleep(3)
    # # 点击发布
    driver.find_element_by_xpath('//button[text()="发布"]').click()


def autoo_publish_weixin_shipinghao(video_abs_path, title, describe):

    # 进入微信视频号创作者页面，并上传视频
    driver.get("https://channels.weixin.qq.com/post/create")
    time.sleep(5)
    driver.find_element_by_xpath(
        '//input[@type="file"]').send_keys(video_abs_path)

    # 检查视频是否上传完成
    while True:
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//*[text()="取消上传"]')
            print("视频还在上传中···")
        except Exception as e:
            break

    while True:
        time.sleep(3)
        try:
            driver.find_element_by_xpath('//*[text()="正在处理文件"]')
            print("视频还在上传中···")
        except Exception as e:
            break

    print("视频已上传完成！")

    # 输入视频描述
    # driver.find_element_by_xpath('//*[@data-placeholder="添加描述"]').send_keys(describe+"#情感文案 #情感语录 #文案 #语录 #情感 @微信时刻 @微信创作者 #人人都是创作者")
    try:
        driver.find_element_by_xpath(
            '//*[@data-placeholder="添加描述"]').send_keys(title+describe)
    except Exception as e:
        driver.find_element_by_xpath(
            '//*[@data-placeholder="添加描述"]').send_keys(describe)

    # 点击发布
    try:
        # 保存草稿，如果要直接发布，则将「保存草稿」改为「发表」
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="保存草稿"]')))
        element.send_keys(Keys.ENTER)
        time.sleep(5)
        print(">>>>>{}发布完成>>>>>".format(video_abs_path))
        # 点击首页按钮，刷新页面，直接刷新页面会提示「是否要重新加载此网站」，不会破解
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="menuBar"]/li[1]/a')))
        element.send_keys(Keys.ENTER)
        time.sleep(5)
    except Exception as e:
        print(e)


def main_wx(video_abs_path, title):
    "自动发布微信视频号"
    title = title.replace("@抖音小助手", "")
    title = title.replace("@DOU+小助手", "")

    # 要添加的话题和 @的人
    describe = "#情感文案 #情感语录 #文案 #语录 #情感 @微信时刻 @微信创作者 #人人都是创作者"

    autoo_publish_weixin_shipinghao(video_abs_path, title, describe)


def main_dou_yin(video_abs_path, title):
    """自动发布抖音"""

    # 要添加的话题和 @的人
    describe = " #上热门 #dou上热门 #我要上热门 @抖音小助手 @DOU+小助手"

    publish_douyin(video_abs_path, title, describe)


if __name__ == "__main__":
    f_name = "情感深夜"
    i = 0
    for fn in os.listdir("media/{}".format(f_name)):
        try:
            abs_dir = os.path.abspath("__file__")
            dir_anme = os.path.dirname(abs_dir)
            video_path = os.path.join("media/{}".format(f_name), fn)
            # 得到绝对路径
            video_abs_path = os.path.join(dir_anme, video_path)
            # 文件名称就是视频标题
            file_name, ext = os.path.splitext(fn)

            # 抖音自动发布
            # main_dou_yin(video_abs_path, file_name)  # 要发布视频号，就先将这行代码注释掉
            # 视频号自动发布
            main_wx(video_abs_path, file_name)  # 要发布抖音，就先将这行代码注释掉

            # 删除已发布的视频
            # os.remove(video_abs_path)
        
            i += 1
            # 连续发布｜保存多少个视频就停止
            if i >= 10:
                break
            # 设置间隔20～30分钟发布一个
            # time.sleep(random.randint(1200, 1800))

            # 视频号，可以先保存草稿，自己手动发布，时间间隔可以设置短一点，甚至不设置间隔
            time.sleep(random.randint(60, 120))
        except Exception as e:
            pass
