# coding:utf-8
import os
import codecs
from lxml import etree
import re
from connectMysql import Mymysql
import datetime
import uuid
from util import get_pic_md5


def main_page_jiexi(product_id, content, update_time,item_dict,thread_name):
    try:
        x = Mymysql()
        x._GetConnect()

        # 属性插入:
        tree = etree.HTML(content)
        attributes = tree.xpath(".//ul[@class='attributes-list']/li/text()")
        attributes = [item.split(":") for item in attributes]
        for item in attributes:
            if item:
                detail_id = uuid.uuid1()
                index_name = item[0].strip()
                index_value = item[1].strip().replace("'", "")
                sql = """
                          insert into product_detail_information(detail_id,product_id,index_name,index_value,update_time)
                          values('%s','%s','%s','%s','%s')
                      """ % (detail_id, product_id, index_name, index_value, update_time)
                try:
                    x.ExecNonQuery(sql)
                except Exception as ex:
                    print("attributes jiexi error", ex)
                    print(sql)
                    print("=============================")
                    return False
        # 左上角图片插入
        imgs_left = tree.xpath(".//ul[@id='J_UlThumb']/li//img")
        count = 1
        for item in imgs_left:
            src = item.get("src")
            if not src:
                src = item.get("data-src")
            src = "http:" + src
            src = src.replace("50x50", "400x400")
            if not src.endswith("jpg"):
                continue
            from_who = position = 1
            sequence = count
            pic_md5 = get_pic_md5(src, product_id)
            sql = """
                              insert into image(product_id,img_src,position,sequence,update_time,from_who,pic_md5)
                                          values('%s','%s','%s','%s','%s','%s','%s')
                              """ % (product_id, src, position, sequence, update_time, from_who,pic_md5)
            try:
                x.ExecNonQuery(sql)
                count += 1
            except Exception as ex:
                print("left_img jiexi error",ex)
                print(sql)
                print("=============================")
                continue

        # size 插入
        code = tree.xpath(".//ul[@class='J_TSaleProp tb-clearfix']//span/text()")
        for item in code:
            Size_ID = uuid.uuid1()
            Size = item.replace("'", "")
            Size = item.replace("\\", "")
            sql = """
                             insert into  size(product_id,size_id, size,update_time) values('%s','%s','%s','%s')
                  """ % (product_id, Size_ID, Size, update_time)
            try:
                x.ExecNonQuery(sql)
            except Exception as ex:
                    print('size jiexi error',ex)
                    print(sql)
                    print("=============================")
                    return False

        # color 插入
        color = tree.xpath(".//ul[@class='J_TSaleProp tb-img tb-clearfix']//a")
        count = 1
        for item in color:
            src = item.get("style")
            img_id = ""
            if src:  # 有图片
                src = "http:" + re.findall("\((.*?)\)", src)[0]
                src = src.replace("30x30", "400x400")
                if not src.endswith("jpg"):
                    continue
                from_who = 1
                position = 3
                sequence = count
                pic_md5 = get_pic_md5(src, product_id)
                sql = """
                          insert into image(pic_md5,product_id,img_src,position,sequence,update_time,from_who)
                                      values('%s','%s','%s','%s','%s','%s','%s')
                          """ % (pic_md5, product_id, src, position, sequence, update_time, from_who)
                try:
                    x.ExecNonQuery(sql)
                    count += 1
                except Exception as ex:
                    print("color imagejiexi error",ex)
                    print(sql)
                    print("=============================")
                    continue

            color_id = uuid.uuid1()
            color = item.xpath(".//span/text()")[0]
            sql = """
                          insert into color(product_id,img_id,color_id,color,update_time)
                                      values('%s','%s','%s','%s','%s')
                          """ % (product_id, img_id, color_id, color, update_time)
            try:
                x.ExecNonQuery(sql)
            except Exception as ex:
                print("colortext jiexi error",ex)
                print(sql)
                print("=============")
                continue
        # 3 产品名称
        product_name = tree.xpath(".//h3[@class='tb-main-title']")
        if not product_name:
            product_name = ""
        else:
            product_name = product_name[0].get("data-title")
        product_name = product_name.replace("'", "")
        item_dict['product_name'] = product_name

        # 产品简述
        product_profile = tree.xpath(".//*[@id='J_Title']/p/text()")
        product_profile = product_profile[0] if product_profile else ""
        product_profile = product_profile.replace("'", "")
        item_dict['product_profile'] = product_profile



        return "ok"





    except Exception as ex:
        print(product_id, "main_page_jiexi", "error:", ex)
        file_save = os.path.join("jiexi", product_id + "_" + "1" + ".html")
        f = codecs.open(file_save, "a+", encoding="utf-8")
        f.write(content)
        f.close()
        return False
