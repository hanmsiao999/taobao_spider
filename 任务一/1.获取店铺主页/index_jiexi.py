#coding:utf-8
import os
import codecs
import re
from lxml import etree
import time
import datetime
from connectMysql import Mymysql

def index_jiexi(shop_ID, html,shop_url,update_time):
 try:
    x = Mymysql()
    x._GetConnect()
    tree  = etree.HTML(html)
    # 有没有进入爱逛街
    guang = tree.xpath(".//a[@class='guang-logo']//text()")
    if len(guang)>0:
        print (shop_ID, guang[0])
        return True

    # noitem
    error  = tree.xpath(".//*[@id='error-notice']/div[2]")
    if len(error) > 0:
        print (shop_ID, "no_item")
        return True
    
    
    
    products = tree.xpath(".//*[starts-with(@href,'//item.taobao.com')]")
    products_item = [] # item_id ,URL,name
    count = 1
    # 1 店铺ID shop_id %s
    shop_id = re.findall("\"shopI[dD]\":(.*?),",html)[0].strip()[1:-1]
    for item in products:
        url = item.get("href")
        item_id = re.findall("id=(\d+)",url)
        if len(item_id)==0:
            continue
        # 产品ID
        item_id = item_id[0]
        name = item.xpath("string(.)")
        # 产品名称
        name = re.sub("[\r\n\t ]*","",name)
        name= name.replace("\xc2\xa0", "")
        name = name.replace("'","")
        if len(name)==0:
            name=""
        name = name.strip()[:100]
        
        # 产品相对顺序
        sequence = count
       
        #print [shop_id,item_id,url,name,sequence]

        # 日期
        sql = "insert  ignore into shop_homepage(shop_id,product_id,product_name,sequence,update_time) values ('%s','%s','%s',%d,'%s')" % (shop_id,item_id,name,sequence,update_time)
        #print sql
        try:
           x.ExecNonQuery(sql)
           count+=1
        except Exception as ex:
                print (ex)
                print (sql)
                print ("=============================")
                continue
           

    x.EndSql()
    if count<10:
        print (shop_ID,":",shop_id,":",u"主页产品",":",count,shop_url)

    alipay_Authentication = tree.xpath(".//span[@class='id-time J_id_time']/text()")
    if not alipay_Authentication:
        alipay_Authentication = '0000-00-00'
    else:
        alipay_Authentication = alipay_Authentication[0]
    return alipay_Authentication
 except Exception as ex:
     print (ex)
     save_path = os.path.join("re_jiexi","%s_index" % (shop_ID))
     f = codecs.open(save_path,"w+",encoding="utf-8")
     f.write(html)
     f.close()
     x.EndSql()
     return False
   
