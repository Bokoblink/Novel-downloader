# Novel-downloader

1. 爬取整篇文章内容打开novel_downloader.py，爬单章内容打开one_chapter.py

1. 用 pip 和 requirements.txt 文件安装所有依赖项，注意selenium版本会导致代码运行报错

   ```
   pip install -r requirements.txt
   ```

3. 安装浏览器驱动，根据自己浏览器的版本，到官网下载对应驱动，并且把驱动的地址改成自己的驱动保存地址 xxx/xxx/chromedriver.exe

   ```python
   self.driver_path = 'chromedriver.exe'
   ```

3. 运行文件，待浏览器打开后返回编辑器输入fw文章主页URL地址，多个地址用空格分隔，回车确认

4. 若含边限文章，需要在打开网页后30s内手动登录账号



# 异常情况

1. 登录未完成，页面就自动跳转至文章主页：

   延长登录等待时间后重新操作。

   找到

   ```python
   self.login_wait = 30  # 登录等待时间(秒)
   ```

   修改为

   ```python
   self.login_wait = 60  # 登录等待时间(秒)
   ```

   重新运行。

2. 登录成功，但仍无法爬取边限文章，页面就自动跳转至文章主页后显示为未登录状态：

   文章与主页域名不一致，把文章主页地址域名均改为https://xn--pxtr7m.com/后重新操作

3. 文章章节超过500，文章爬取不完整：

   修改最大抓取章节数。

   找到

   ```python
   self.max_chapters = 500  # 最大抓取章节数
   ```

   修改最大章节数，使其>文章实际章节数

4. 部分章节的章节内容未爬取完整，或章节获取失败报错：

   考虑网速问题，延长页面加载等待时间

   找到

   ```python
   self.page_load_wait = 1  # 页面加载等待时间(秒)
   ```

   增大参数值，使页面加载时间充足



# 目录结构

```
novel_downloader/  
├── .gitattributes
├── .gitignore
├── novel_downloader.py       //爬取整篇文章内容 
├── one_chapter.py            //爬单章内容打开
├── requirements.txt 		  //依赖库清单
└── README.md      		      // help 
```
