#coding:utf-8
#1.获取店铺主页
import sys
sys.path.append("..")
import warnings
warnings.filterwarnings("ignore")
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from lxml import etree
import codecs
from selenium import webdriver
import time,re,os
import random
import queue
import threading
from good_jiexi import good_jiexi
import datetime


lock = threading.Lock()

#开启线程数
thread_num = 1
#登录信息保存文件名
#cookie_list = ["../user_data","../user_data_02"]
cookie_list = ["../user_data"]


class crawl(threading.Thread):
    def __init__(self,**kwargs):
        threading.Thread.__init__(self)
        #self.start_PhantomJS()
        self.shop_time = 0
        self.cookie_path = cookie_list.pop() if cookie_list else None
        if self.cookie_path:
           self.cookie_path = os.path.abspath(self.cookie_path)
        self.start_chrome()
        
            

    def __del__(self):
        self.f_log.close()

    def start_chrome(self):
        try:
            self.driver.quit()
        except Exception as ex:
            pass
        hromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        hromeOptions.add_experimental_option("prefs",prefs)
        hromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        hromeOptions.add_argument("user-data-dir=%s" % self.cookie_path)
        self.driver = webdriver.Chrome(executable_path="../chromedriver",chrome_options=hromeOptions)
        self.driver.get("http://www.taobao.com")
        self.driver.add_cookie({'name':"thw","value":"cn","path":"/","domain":".taobao.com"})

        
    def dirver_set(self):
        self.driver.set_page_load_timeout(20)
        self.driver.set_window_size(1124, 850)

       
    def get_main_page(self,url):
        try:
            self.driver.get(url)
            return True
        except Exception as ex:
            print (ex)
            print (self.name+":再次获取")
            return False

           
    def roll_bottom(self):
        #print ("开始滚轮")
        increment = random.randint(2000,4000)
        distance = 0
        last_time = 0
        length = []
        while True:
          distance = distance + increment # 目标位置
          js = "var q=document.body.scrollTop=%s;return q" % (distance)
          self.driver.execute_script(js)
          time.sleep(1.4)

          js = "return document.body.scrollTop"
          this_time = self.driver.execute_script(js)
          #print last_time,this_time
          length.append(len(self.driver.page_source))
          if len(length)>5 and length[-1]==length[-2]==length[-3]==length[-4]==length[-5]:
              break
          if this_time > last_time:
              last_time = this_time
          else:
              break

    def find_all_link(self, html):
        link = re.findall("href=\"//(\S+\.taobao\.com/\S+\?search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+\.taobao\.com/search.htm)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search.htm\?search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        return False

        
    def main_method(self, item,update_time):
        try:
          shop_ID = re.findall("\d+",item)[0]
          url = "https:"+item
          print (self.name, url)
          #time.sleep(1000)
          begin_time = time.time()
          # 访问商品主页
          if self.get_main_page(url)==False:# 获取店铺主页面
             self.f_log.write("浏览器崩溃 重启浏览器\n")
             self.start_chrome()
             self.f_log.write("浏览器重启成功\n")
             return False
          time.sleep(1)

          #print "123"
          if "noshop.htm" in self.driver.current_url or "guang.taobao.com" in self.driver.current_url or "tmall" in self.driver.current_url:
              self.f_log.write("%s:%s:%s\n"%(shop_ID,self.driver.current_url ,"不存在"))
              return "ok"

          # 点击所有宝贝
          all_links = self.find_all_link(self.driver.page_source)
          if not all_links:
              self.f_log.write("shop %s: all_links unfound\n" % (shop_ID))
              print ("shop %s: all_links unfound\n" % (shop_ID))
          url = "https://" + all_links
          if self.get_main_page(url)==False:# 获取店铺主页面
             self.f_log.write("浏览器崩溃 重启浏览器\n")
             self.start_chrome()
             self.f_log.write("浏览器重启成功\n")
             return False



          # 滚到首页底部
          page = 1
          self.roll_bottom()
          error_time = 0
          #result = good_jiexi(shop_ID, shop_ID, self.driver.page_source, page, update_time, self.name)
          page += 1
          while True:
              try:
                 result = good_jiexi(shop_ID, shop_ID, self.driver.page_source, page, update_time, self.name)
                 ele = WebDriverWait(self.driver, 10,1).until(lambda d: d.find_element_by_xpath(".//a[@class='J_SearchAsync next']"),self.driver)
                 ele.click()
                 error_time = 0
              except Exception as ex:
                  #print (ex)
                  try:
                      self.driver.find_element_by_xpath(".//a[@class='disable']")
                      return 'ok'
                  except Exception as ex:
                      #print (ex)
                      input("下一页不存在,请输入用户名或者密码:%s:%s" % (self.driver.title,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                      if error_time<300:
                          error_time += 1
                          self.roll_bottom()
                          time.sleep(3)
                          continue
                      else:
                          self.f_log.write("shop_Id:%s error \n" % (shop_ID))
                          return False

        except Exception as ex:
           print (ex,self.name)
           return False
    
    def run(self):
        log_path = os.path.join("log", self.name + ".log")
        while True:
         try:
           self.f_log = codecs.open(log_path, "a+", encoding="utf-8")
           if user_list.empty():
                print ('break')
                break
           item = user_list.get()
           global update_time

           re = self.main_method(item, update_time)
           if re == 'ok':
               global lock
               lock.acquire() 
               f = codecs.open("has_craw_shop.txt","a+",encoding="utf-8")
               f.write("%s|%s\n" % (item,update_time))
               f.close()
               now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               print (item+":"+self.name+":"+now+":done")
               self.f_log.write(item+":"+self.name+":"+now+":done\n")
               lock.release() 
           self.shop_time += 1
           time.sleep(3)
           if self.shop_time >20:
              self.f_log.write(self.name + ":restart driver \n")
              self.driver.quit()
              self.start_chrome()
              #self.start_PhantomJS()
              time.sleep(5)
              self.shop_time = 0
              self.f_log.write(self.name + ":restart succeed\n")

         except Exception as ex:
           print ('main_method',ex)
         finally:
             self.f_log.close()


import threading
lock = threading.Lock()
get_lock = threading.Lock()
update_time = datetime.datetime.now().strftime("%Y-%m-%d")

url_file = os.path.join("../all_url.csv")
f = open(url_file, "r+")
results = f.readlines()
f.close()

results = [item[:-1] for item in results]  # 总url

if not os.path.isfile("has_craw_shop.txt"):
   f = open("has_craw_shop.txt", "w+")
   f.close()
f = codecs.open("has_craw_shop.txt", "r+", encoding="utf-8")
IDS = f.readlines()
f.close()
IDS = [item.split(":")[0] for item in IDS]

user_list = queue.Queue()
ip_list = queue.Queue()
print("put ing~")
for item in results:
 if item not in IDS:
     # user_list.put("//shop71221132.taobao.com")
     user_list.put(item)
     # break

print("put finish")

print("this time will crawl %s shops" % (str(user_list._qsize())))

a = time.time()
ths = []
for i in range(thread_num):
 ths.append(crawl())

for th in ths:
 time.sleep(2)
 th.start()

while len(ths):
 thread = ths.pop()
 if thread.isAlive():
     thread.join()
     b = time.time()

print('all end')





