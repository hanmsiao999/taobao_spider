#coding:utf-8
from selenium import webdriver
import time
import os
import shutil

#登录信息的保存文件名
file_name = "user_data"
# 删除已经保存的用户名
if os.path.exists(file_name):
    shutil.rmtree(file_name)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--user-data-dir=%s" % file_name)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.taobao.com")
a = input("please login")
cookie= driver.get_cookies()
# 将页面滚动条拖到底部
js = "window.scrollTo(0,document.body.scrollHeight)"
driver.execute_script(js)
time.sleep(5)
# 将滚动条移动到页面的顶部
js = "window.scrollTo(0,10)"
driver.execute_script(js)
time.sleep(5)
print(cookie)
print(driver.title)


