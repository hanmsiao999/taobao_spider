#coding:utf-8
import os
import codecs
import re
from lxml import etree
import time
import datetime


def index_jiexi(shop_ID, html,shop_url):
    tree  = etree.HTML(html)
    # 有没有进入爱逛街
    guang = tree.xpath(".//a[@class='guang-logo']//text()")
    if len(guang)>0:
        print shop_ID, guang[0]
        return True

    # noitem
    error  = tree.xpath(".//*[@id='error-notice']/div[2]")
    if len(error) > 0:
        print shop_ID, "no_item"
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
        
        
        # 产品相对顺序
        sequence = count
       
        #print [shop_id,item_id,url,name,sequence]

        # 日期
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d")


f = codecs.open("1659426597_index",encoding="utf-8")
html = f.read()
f.close()
index_jiexi(1000, html,"1000")
