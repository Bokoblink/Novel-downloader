# Novel-downloader

## ⚠️ 法律与道德声明

1. **工具性质**  
   本项目代码仅为**个人学习网络爬虫技术**而创建，不涉及任何商业用途。所有功能需**用户手动授权**（包括但不限于登录、输入验证码等操作）。
2. **数据获取**  
   - 使用者应确保已获得目标网站的**明确书面授权**  
   - 禁止批量爬取（建议单次请求间隔≥30秒）  
   - 获取内容需在24小时内删除（参考《民法典》第1036条）
3. **责任豁免**  
   开发者不对以下行为负责：  
   - 用户违反目标网站《服务条款》的行为  
   - 因爬取导致的账号封禁/法律纠纷  
   - 任何形式的二次传播或商用  




## 使用说明

### 一、爬取整篇文章内容

1. 打开novel_downloader.py

1. 用 pip 和 requirements.txt 文件安装所有依赖项，注意selenium版本会导致代码运行报错

   ```
   pip install -r requirements.txt
   ```

3. 安装浏览器驱动，根据自己浏览器的版本，到官网下载对应驱动，并且把'chromedriver.exe'引号内改成自己驱动的本地保存地址 xxx/xxx/chromedriver.exe

   ```python
   self.driver_path = 'chromedriver.exe'
   ```

4. 找到以下代码，把'https://xxxx.com/'引号内地址改为目标网站主页地址

   ```python
   self.driver.get('https://xxxx.com/')
   ```

5. 运行文件，待浏览器打开后返回编辑器输入文章主页URL地址，多个地址用空格分隔，回车确认

6. 若含边限文章，需要在打开网页后30s内手动登录账号



### 二、爬单章内容

1. 打开one_chapter.py

2. 用 pip 和 requirements.txt 文件安装所有依赖项，注意selenium版本会导致代码运行报错

   ```
   pip install -r requirements.txt
   ```

3. 安装浏览器驱动，根据自己浏览器的版本，到官网下载对应驱动，并且把'chromedriver.exe'引号内改成自己驱动的本地保存地址 xxx/xxx/chromedriver.exe

   ```python
   self.driver_path = 'chromedriver.exe'
   ```

4. 找到以下代码，把"https://xxxx/posts/xxxxxxxx"引号内地址改为目标章节地址

   ```python
   self.url = "https://xxxx/posts/xxxxxxxx"
   ```

5. 若含边限文章，需要在打开网页后30s内手动登录账号

   

## 异常情况

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

   文章与主页域名不一致，把文章主页地址域名保持一致后重新操作

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
   
   

## 目录结构

```
novel_downloader/  
├── .gitattributes
├── .gitignore
├── novel_downloader.py       //爬取整篇文章内容 
├── one_chapter.py            //爬单章内容打开
├── requirements.txt 		  //依赖库清单
└── README.md      		      // help 
```
