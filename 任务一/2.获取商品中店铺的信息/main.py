#coding:utf-8
import sys
sys.path.append("..")
from selenium.webdriver.support.ui import WebDriverWait
import codecs
import re,time,os,queue
from selenium import webdriver
import threading
from connectMysql import Mymysql
from shop_service_jiexi import shop_service_jiexi
from refund_jiexi import refund_jiexi
import datetime

#配置线程数 
thread_num = 3
class crawl(threading.Thread):
    def __init__(self,**kwargs):
        threading.Thread.__init__(self)
        self.driver =None
        self.start_chrome()
        #self.start_PhantomJS()
        self.shop_time = 0
        log_path = os.path.join("log",self.name+".log")
        self.f_log = codecs.open(log_path,"a+",encoding="utf-8")

    def __del__(self):
        self.f_log.close()

    def start_chrome(self):
        if self.driver!=None:
           self.driver.quit()
        hromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        hromeOptions.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(executable_path="../chromedriver",chrome_options=hromeOptions)
        self.shop_time = 0
        self.dirver_set()
        self.driver.get("http://www.taobao.com")
        self.driver.add_cookie({'name':"thw","value":"cn","path":"/","domain":".taobao.com"})
        
    def start_PhantomJS(self):
        if self.driver!=None:
           self.driver.quit()
        self.cap = webdriver.DesiredCapabilities.PHANTOMJS
        self.cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
        self.cap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(executable_path="../phantomjs",
                                          desired_capabilities=self.cap,service_log_path="%s.txt" % name)
        self.shop_time = 0
        self.dirver_set()
        self.driver.add_cookie({'name':"thw","value":"cn","path":"/","domain":".taobao.com"})
        self.driver.get("http://www.taobao.com")

    def dirver_set(self):
        self.driver.set_page_load_timeout(60)
        self.driver.set_window_size(1124, 850)
        #self.back_to_main_land()
        time.sleep(3)

        
    def get_main_page(self,url):
        try:
            self.driver.get(url)
            return True
        except Exception as ex:
            print (ex)
            print (self.name+":get main page error")
            return False

              
           
    def isElementExist(self,xpath):
        flag=True
        browser=self.driver
        try:
            ele = browser.find_element_by_xpath(xpath)
            return flag
        except:
            flag=False
            return flag

    def isElementsExist(self,xpath):
        flag=True
        browser=self.driver
        try:
            ele = browser.find_elements_by_xpath(xpath)
            return ele
        except:
            flag=False
            return flag

    
    def main_method(self, shop_product):
        try:
          shop_url = shop_product[0][0]
          shop_id = re.findall("\d+",shop_url)[0]
          product_id = shop_product[1]
          update_time = shop_product[0][1].strip()
          url = "https://item.taobao.com/item.htm?id=%s" % (product_id)
          self.f_log.write(self.name+":"+url+"\n")
          error_time = 0
          # 访问商品主页
          while self.get_main_page(url)==False:# 获取主页面
              self.get_main_page(url)
              error_time+=1
              if error_time>3:
                  self.f_log.write("浏览器崩溃 重启浏览器\n")
                  self.driver.quit()
                  self.start_chrome()
                  time.sleep(5)
                  self.f_log.write("浏览器重启成功\n")
          time.sleep(2)
          while "error" in self.driver.current_url :
              self.f_log.write(product_id+":counter error\n")
              time.sleep(20)
              self.driver.refresh()
              time.sleep(3)
          if "noitem" in self.driver.current_url or "fktz.php" in self.driver.current_url :
              self.f_log.write("商品%s no item \n " % product_id)
              return False

          # 点击专享服务
          distance = 0
          for i in range(3):
              try:
                 ele = WebDriverWait(self.driver,15,1).until(lambda d: d.find_element_by_xpath(".//li[@id='J_ServiceTab']"),self.driver)       
                 ele.click()
                 time.sleep(1)
                 WebDriverWait(self.driver,15,1).until(lambda d: d.find_element_by_xpath(".//ul[@class='service-list-items']"),self.driver)       
              except Exception as ex:
                 self.f_log.write("%s:%s:%s:%s:%s\n" % (self.name,shop_id,product_id,"专享服务寻找失败", i))
                 #self.driver.save_screenshot(shop_id+".jpg")
    
                 distance += 150 # 目标位置
                 js = "var q=document.body.scrollTop=%s;return q" % (distance)
                 self.driver.execute_script(js)
                 time.sleep(1)
         
          if  not self.isElementExist(".//ul[@class='service-list-items']"):
                 self.f_log.write("%s:%s:%s:%s\n"  %(self.name,shop_id,product_id,"未找到专享服务内容"))
                 return False
          other_name = ""
          #  1 专享服务解析
          re1 = shop_service_jiexi(shop_id,self.driver.page_source,update_time)
          if re1==False:
             other_name+="1_"


          # 2 退货纠纷
          # 点击累计评论
          # for i in range(5):
          #     try:
          #        ele = WebDriverWait(self.driver,15,1).until(lambda d: d.find_element_by_xpath(".//*[@id='J_TabBar']/li[2]/a"),self.driver)
          #        ele.click()
          #        time.sleep(1)
          #        if "加载中..."  in self.driver.page_source:
          #           self.f_log.write(product_id+":累计评论正在加载\n")
          #           time.sleep(2)
          #           continue
          #
          #        if "请求不成功"  in self.driver.page_source:
          #           self.f_log.write(product_id+":累计请求不成功\n")
          #           return False
          #
          #        if self.isElementExist(".//div[@class='kg-rate-wd-filter-bar']"):
          #           break
          #
          #     except Exception as ex:
          #        # 下滚两百
          #        self.f_log.write("%s:%s:%s\n" % (self.name,product_id,"累计评论点击失败 下滚200"))
          #        distance += 200 # 目标位置
          #        js = "var q=document.body.scrollTop=%s;return q" % (distance)
          #        self.driver.execute_script(js)
          #        time.sleep(1)
          #
          # if  not self.isElementExist(".//div[@class='kg-rate-wd-filter-bar']"):
          #        self.f_log.write("%s:%s:%s\n" % (self.name,product_id,"未找到吧台"))
          #        return False
          # # 4 点击售后信息
          # distance = 0
          # for i in range(5):
          #     try:
          #         ele = WebDriverWait(self.driver, 10,1).until(lambda d: d.find_element_by_xpath(".//li[@data-kg-rate-tab='refund']"),self.driver)
          #         ele.click()
          #         #time.sleep(2)
          #         #if self.isElementExist(".//div[@data-kg-rate-tab='refund']"):
          #         #    break
          #         if "请求不成功"  in self.driver.page_source:
          #           self.f_log.write(product_id+":售后信息请求不成功\n")
          #           return False
          #         WebDriverWait(self.driver, 10,1).until(lambda d: d.find_element_by_xpath(".//tr[@class='J_KgRate_RefundSummary_TR']"),self.driver)
          #         break
          #     except Exception as ex:
          #         if "请求不成功"  in self.driver.page_source:
          #            self.f_log.write(product_id+":请求不成功\n")
          #            return False
          #         self.f_log.write("%s:%s:%s\n" %("product_id:",product_id,"未找到售后信息, 重新点击累计评论"))
          #         self.f_log.write("%s:%s:%s\n" % (self.name,product_id,"累计评论点击失败 下滚200"))
          #         distance += 200 # 目标位置
          #         js = "var q=document.body.scrollTop=%s;return q" % (distance)
          #         self.driver.execute_script(js)
          #         time.sleep(1)
          #         ele = WebDriverWait(self.driver,20,1).until(lambda d: d.find_element_by_xpath(".//*[@id='J_TabBar']/li[2]/a"),self.driver)
          #         ele.click() # 点击累计评论
          #         time.sleep(3)
          #
          # if  not self.isElementExist(".//tr[@class='J_KgRate_RefundSummary_TR']"):
          #        self.f_log.write("%s:%s:%s\n" % (self.name,product_id,"最终未找到售后信息"))
          #        return False
          # else:
          #     re4 = refund_jiexi(shop_id,self.driver.page_source,update_time)
          #     if re4==False:
          #        other_name+="4"
          #
          #     # 最终保存
          if other_name == "":
             return "ok"
          else:
              new_name = other_name+"_"+str(product_id)+".html"
              new_name = os.path.join("jiexi",new_name)
              f = codecs.open(new_name,"w+",encoding="utf-8")
              f.write(self.driver.page_source)
              f.close()
              return False
        except Exception as ex:
           print (ex)
           self.f_log.write("main_method %s:%s\n" % (str(ex),self.name))
           return False
    
    def run(self):
        while True:
         try:
           if shop_product_queue.empty():
              self.f_log.write("%s:%s:%s\n" %(self.name,'break',str(time.time() - a)))
              break
           shop_product = shop_product_queue.get(timeout=20)
           self.f_log.write("%s:%s:%s\n" %(shop_product[0][0],":begin:",self.name))
           re = self.main_method(shop_product)
           if re == 'ok':
               update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               global lock
               lock.acquire() 
               f = codecs.open("has_craw.txt","a+",encoding="utf-8")
               f.write("%s|%s\n" % (shop_product[0][0],update_time))
               f.close()
               print (shop_product[0][0]+":"+self.name+":done",update_time.strip())
               lock.release() 
               self.f_log.write(shop_product[0][0]+":"+self.name+":done\n")
           self.shop_time += 1
           if self.shop_time >30:
              self.f_log.write(self.name + ":重启浏览器\n")
              self.driver.quit()
              self.start_chrome()
              time.sleep(5)
              self.f_log.write(self.name + ":重启浏览器成功\n")
         except Exception as ex:
                print ("fucntion run",ex,self.name)


lock = threading.Lock()
shop_product_queue = queue.Queue()
# 获取带爬商品ID 列表
x = Mymysql()
x._GetConnect()


#target:
f = codecs.open("../has_craw_shop.txt","r+",encoding="utf-8")
shop_infos = f.readlines()
f.close()
shop_infos = [item.strip().split("|") for item in shop_infos]


# has crawl
if not os.path.exists("has_craw.txt"):
    f = open("has_craw.txt","w+")
    f.close()
f = codecs.open("has_craw.txt","r+",encoding="utf-8")
has_crawl_IDS = f.readlines()
f.close()
has_crawl_IDS = [str(item.strip().split("|")[0]) for item in has_crawl_IDS]

for item in shop_infos: # shop_id
    if item[0] not in has_crawl_IDS:
       #shop_id = '60857518'
       shop_url = item[0]
       shopID = re.findall("\d+",shop_url)[0]
       sql = """
              select product_id from shop_homepage
              where shop_id='%s'  limit 2
             """ % (shopID)
       
       result = x.ExecQuery(sql)
       if len(result)>=2:
          shop_product_queue.put([item,result[1][0]])
          #break
       else:
           print (sql)
           #f = codecs.open("go_to_down_load.txt","a+",encoding="utf-8")
           #f.write(shop_url+"\n")
           #f.close()
           #print (shopID,u"主页下没有商品")
x.EndSql()

#print ("loading done")
#time.sleep(1000)
ths = []
for i in range(thread_num):
    ths.append(crawl())
a = time.time()
print ("Begin at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print ("This time will crawl %s products" % (str(shop_product_queue._qsize())))
for th in ths:
    time.sleep(2)
    th.start()


while len(ths):
    thread = ths.pop()
    if thread.isAlive():
        thread.join()
print (u'all done') 

    

    

