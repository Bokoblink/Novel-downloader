#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件名: one_chapter.py
功能: fw自动抓取小说单章内容并保存为文本文件
作者: Bokoblink
邮箱:juyj1001z@gmail.com
创建日期: 2025-04-15
修改日期: 2025-04-16
版本: v2.0
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class NovelDownloader:

    def __init__(self):
        """初始化配置"""
        # 浏览器驱动路径 (需修改为你的实际路径)
        self.driver_path = 'chromedriver.exe'  # 使用正斜杠避免转义问题

        # 基本配置参数
        self.url = "https://xn--pxtr7m.com/posts/xxxxxxxx"  #替换为章节地址
        self.login_wait = 3  # 登录等待时间(秒)
        self.page_load_wait = 1  # 页面加载等待时间(秒)

        # 初始化浏览器
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.maximize_window()


    def save_chapter(self):
        """保存单个章节内容"""
        try:
            self.driver.get(self.url)
            current_url = self.driver.current_url
            chapter_id = os.path.basename(current_url.rstrip('/'))
            # 获取章节内容
            chapter_title = self.driver.find_element(By.CSS_SELECTOR, "strong.h3").text
            chapter_desc = self.driver.find_element(By.CSS_SELECTOR, "strong.h5").text
            content = self.driver.find_element(By.ID, f"full{chapter_id}").text

            # 尝试获取预警
            try:
                warning_tag = self.driver.find_element(By.CLASS_NAME, "text-center.grayout.warning-tag").text
            except NoSuchElementException:
                warning_tag = None

            # 尝试获取作者的话
            try:
                author_words = self.driver.find_element(By.XPATH,
                                                        "//div[@class='main-text indentation no-selection']/div[@class='text-left grayout']").text
            except NoSuchElementException:
                author_words = None

            # 写入文件
            output_file = f"单章更新.txt"
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n第x章 {chapter_title}\n")
                f.write(f"概要：{chapter_desc}\n")
                if warning_tag:
                    f.write(f"预警：{warning_tag}\n")
                f.write(f"{content}\n")
                if author_words:
                    f.write(f"作者的话：\n{author_words}\n")

            return True
        except Exception as e:
            print(f"保存章节失败: {e}")
            return False


    def run(self):
        try:
            # 访问URL并等待登录
            self.driver.get(self.url)
            print(f"请在 {self.login_wait} 秒内完成登录...")
            time.sleep(self.login_wait)

            print(f"\n开始处理URL: {self.url}")
            self.save_chapter()

        except Exception as e:
            print(f"程序运行出错: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    downloader = NovelDownloader()
    downloader.run()