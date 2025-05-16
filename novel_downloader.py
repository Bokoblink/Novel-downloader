#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件名: novel_downloader.py
功能: fw自动抓取小说内容并保存为文本文件
作者: Bokoblink
邮箱:juyj1001z@gmail.com
创建日期: 2025-04-09
修改日期: 2025-04-16
版本: v3.3
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
        self.start_urls = []  # 改为存储多个URL的列表
        self.max_chapters = 500  # 最大抓取章节数
        self.login_wait = 30  # 登录等待时间(秒)
        self.page_load_wait = 1  # 页面加载等待时间(秒)

        # 初始化浏览器
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.maximize_window()

    def get_author(self):
        """获取作者信息（优先尝试XPath，其次CLASS_NAME，都没有则返回None）"""
        selectors = [
            (By.XPATH, "(//div[@class='h5'])[2]/div[1]/a"),  # 优先尝试的选择器1
            (By.CLASS_NAME, "majia")  # 备选选择器2
        ]

        for by, value in selectors:
            try:
                return self.driver.find_element(by, value).text
            except NoSuchElementException:
                continue

        print("获取作者信息失败：所有选择器均未找到元素")
        return ""

    def get_novel_info(self):
        """获取小说基本信息
        返回包含标题、简介、作者和详细描述的字典
        如果详细描述获取不到，则返回'无'
        """
        print("正在获取小说基本信息...")
        try:
            # 获取标题、简介等信息
            title = self.driver.find_element(By.CSS_SELECTOR, "a.font-1").text
            short_desc = self.driver.find_element(By.XPATH, "(//div[@class='h5'])[1]").text
            author = self.get_author()  # 调用优化后的方法
            if author is None:
                return None

            # 获取tag
            tag_father_element = self.driver.find_element(By.XPATH, "(//div[@class='h5'])[2]/div[3]")
            a_tags = tag_father_element.find_elements(By.TAG_NAME, 'a')
            texts = [a.text for a in a_tags]
            tags = " - ".join(texts)

            # 获取详细描述，如果获取不到则返回"无"
            try:
                long_desc = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.main-text.text-center.no-selection"
                ).text
            except NoSuchElementException:
                print("获取小说文案失败")

            return {
                'title': title,
                'short_desc': short_desc,
                'author': author,
                'tags': tags,
                'long_desc': long_desc
            }
        except NoSuchElementException as e:
            print(f"获取小说基本信息失败: {e}")
            return None

    def save_chapter(self, file_path, chapter_count, chapter_id):
        """保存单个章节内容"""
        try:
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
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"\n\n第{chapter_count}章 {chapter_title}\n")
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

    def process_novel(self, url):
        """处理单个小说"""
        try:
            # 1. 访问首页
            self.driver.get(url)

            # 2. 获取并保存小说基本信息
            novel_info = self.get_novel_info()
            if not novel_info:
                return False

            output_file = f"{novel_info['title']}BY{novel_info['author']}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"《{novel_info['title']}》\n")
                f.write(f"一句话简介：{novel_info['short_desc']}\n")
                f.write(f"作者：{novel_info['author']}\n")
                f.write(f"tags：{novel_info['tags']}\n")
                f.write(f"文案：\n{novel_info['long_desc']}\n\n")
                f.write("=== 小说内容开始 ===\n\n\n")

            # 3. 开始阅读
            try:
                self.driver.find_element(By.LINK_TEXT, "开始阅读").click()
                time.sleep(self.page_load_wait)
            except NoSuchElementException:
                print("未找到'开始阅读'按钮")
                return False

            # 4. 循环抓取章节
            chapter_count = 1
            while chapter_count <= self.max_chapters:
                current_url = self.driver.current_url
                chapter_id = os.path.basename(current_url.rstrip('/'))

                if not chapter_id.isdigit():
                    print(f"无效章节ID: {chapter_id}")
                    break

                # print(f"正在处理第 {chapter_count} 章 (ID: {chapter_id})...")

                if self.save_chapter(output_file, chapter_count, chapter_id):
                    chapter_count += 1

                # 尝试跳转下一章
                try:
                    self.driver.find_element(By.LINK_TEXT, "下一章").click()
                    time.sleep(self.page_load_wait)
                except NoSuchElementException:
                    print("已到达最后一章")
                    break

            # 5. 完成处理
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write("\n=== 小说内容结束 ===")

            print(f"完成！共保存 {chapter_count - 1} 章内容到 {output_file}")
            return True

        except Exception as e:
            print(f"处理小说时出错: {e}")
            return False

    def run(self):
        """主运行方法"""
        try:
            # 获取用户输入的多个URL
            print("请输入小说首页URL(多个URL用空格分隔):")
            urls = input().strip().split()
            if not urls:
                print("未输入任何URL")
                return

            # 访问第一个URL并等待登录
            self.driver.get('https://xn--pxtr7m.com/')
            print(f"请在 {self.login_wait} 秒内完成登录...")
            time.sleep(self.login_wait)

            # 处理每个URL
            for url in urls:
                print(f"\n开始处理URL: {url}")
                self.process_novel(url)

        except Exception as e:
            print(f"程序运行出错: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    downloader = NovelDownloader()
    downloader.run()