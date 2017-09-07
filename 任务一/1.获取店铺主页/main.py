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
from index_jiexi import index_jiexi
from rate_jiexi import rating_jiexi
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
        #self.driver.add_cookie({'name':"thw","value":"cn","path":"/","domain":".taobao.com"})

        
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

        
    def main_method(self, item,update_time):
        try:
          
          shop_ID = re.findall("\d+",item)[0]
          url = "https:"+item
          print (self.name, url)
          #time.sleep(1000)
          begin_time = time.time()
          # 访问商品主页
          if self.get_main_page(url)==False:# 获取主页面
             self.f_log.write("浏览器崩溃 重启浏览器\n")
             self.start_chrome()
             self.f_log.write("浏览器重启成功\n")
             return False
          time.sleep(1)
          #print "123"
          if "noshop.htm" in self.driver.current_url or "guang.taobao.com" in self.driver.current_url or "tmall" in self.driver.current_url:
              self.f_log.write("%s:%s:%s\n"%(shop_ID,self.driver.current_url ,"不存在"))
              return "ok"

          try:
              ele = WebDriverWait(self.driver, 10,1).until(lambda d: d.find_element_by_xpath(".//a[starts-with(@href,'//rate.taobao.com')]"),self.driver)
          except Exception as ex:
              self.f_log.write("%s:%s\n" % (url,":rating框未出现"))
              return False

          text = ele.text
          if "未收到评价" in self.driver.page_source:
              self.f_log.write("%s:%s:%s:%s\n" %(shop_ID,text,self.name, "无内容"))
              return "ok"
          #rate_url = ele.get_attribute("href")
          
        
          
          # 滚到首页底部
          self.roll_bottom()  
       
          # 解析页面商品阶段
          re_1 = index_jiexi(shop_ID, self.driver.page_source,url,update_time)
          if re_1 == False:
              self.f_log.write("%s:%s\n" %(shop_ID, "界面解析失败"))
              return False
            
          self.f_log.write("%s:%s:%s\n" % (shop_ID,"主页面解析完成:",self.name))
          print (shop_ID,"主页面解析完成:",self.name)
          if time.time() - begin_time <20:
             time.sleep(20-(time.time() - begin_time))
        
          try:
              #ele = WebDriverWait(self.driver, 60,1).until(lambda d: d.find_element_by_xpath(".//span[@class='shop-rank']/a"),self.driver)
              ele.click()
              handle_1,handle_2 = self.driver.window_handles
              self.driver.close()
              self.driver.switch_to.window(handle_2)
              #self.driver.save_screenshot(shop_ID+".jpg")
              #print shop_ID,url,"评价页面已点击:",self.name
          except Exception as ex:
              print (shop_ID,url,"未找到评价页面:",self.name)
              self.driver.save_screenshot(shop_ID+".jpg")
        
                  
          for i in range(3):
             try:
                if "login.taobao.com" in self.driver.current_url or "sec.taobao" in self.driver.current_url:
                    self.f_log.write("%s:%s:%s\n" % ( self.name, shop_ID, '登录出现'))
                    return False
                WebDriverWait(self.driver, 15,1).until(lambda d: d.find_element_by_xpath(".//div[@class='info-block info-block-first']//ul/li[2]"),self.driver)
                WebDriverWait(self.driver, 15,1).until(lambda d: d.find_element_by_xpath(".//*[@id='chart-name']"),self.driver)
                break
             except Exception as ex:
                if i == 2:
                    self.f_log.write("%s:%s:%s\n" % (shop_ID,"日期地域最终未出现",self.name))
                    return False
                self.f_log.write("%s:%s\n" %  (shop_ID,"日期地域未出现"))
                self.driver.save_screenshot(shop_ID+".jpg")
                if "login.taobao.com" in self.driver.current_url or "sec.taobao" in self.driver.current_url:
                    self.f_log.write("%s:%s:%s\n" % ( self.name, shop_ID, '登录出现'))
                    return False
          # 等待 30天
          try:
              for i in range(5):
                  if "加载中..." in self.driver.page_source:
                      time.sleep(2)
                  else:
                      break
              WebDriverWait(self.driver, 10,1).until(lambda d: d.find_element_by_xpath(".//table[@class='tb-rate-table']/tbody/tr"),self.driver)
          except Exception as ex:
              self.f_log.write("%s:%s:%s\n" % (shop_ID,"30天近况始终未出现:",self.name))
              self.driver.save_screenshot(shop_ID+"_30days"+".jpg")
              return False
              
          
          # 解析店铺评价页面
          re_2 = rating_jiexi(shop_ID, self.driver.page_source,update_time,re_1)
          if  re_2=="ok":
             return "ok"
          else:
             self.f_log.write("%s:%s\n" % (shop_ID,":评价页面解析失败"))
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
               f = codecs.open("../has_craw_shop.txt","a+",encoding="utf-8")
               f.write("%s|%s\n" % (item,update_time))
               f.close()
               now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               print (item+":"+self.name+":"+now+":done")
               self.f_log.write(item+":"+self.name+":"+now+":done\n")
               lock.release() 
           self.shop_time += 1
           time.sleep(5)
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





# 统一更新日期
update_time = datetime.datetime.now().strftime('%Y-%m-%d')
url_file = os.path.join("../all_url.csv")
f = open(url_file,"r+")
results = f.readlines()
f.close()
results = [item[:-1] for item in results] # 总url

if not os.path.isfile("../has_craw_shop.txt"):
    f = open("../has_craw_shop.txt", "w+")
    f.close()
f = codecs.open("../has_craw_shop.txt","r+",encoding="utf-8")
IDS = f.readlines()
f.close()
IDS = [item.strip().split("|")[0] for item in IDS]
user_list = queue.Queue()
for item in results:
    if item not in IDS:
        #print item
        user_list.put(item)
        #break


        

print ("this time will crawl %s shops" % str(user_list._qsize()))
assert thread_num<=len(cookie_list)
ths = []
for i in range(thread_num):
    ths.append(crawl())
    
for th in ths:
    time.sleep(2)
    th.start()
    
a = time.time()
while len(ths):
    thread = ths.pop()
    if thread.isAlive():
        thread.join()
b = time.time()
print ("functions run:",b-a)
print ('all done') 
    
    

    

