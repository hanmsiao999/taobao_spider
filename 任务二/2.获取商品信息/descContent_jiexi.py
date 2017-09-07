import os
import codecs
from lxml import etree
import re
from connectMysql import Mymysql
import json
import uuid
from util import get_pic_md5


def descContent_jiexi(product_id, content, update_time, item_dict,thread_name):
    try:
        x = Mymysql()
        x._GetConnect()
        content = content.replace("var desc='", "")
        content = content.replace("';", "")
        tree = etree.HTML(content)
        imgs = tree.xpath(".//img")
        count = 1
        for img in imgs:
            src = img.get("src")
            if not src or not src.endswith("jpg"):
                continue
            src = src.replace("50x50", "400x400")

            from_who = 1
            position = 2
            sequence = count
            pic_md5 = get_pic_md5(src,product_id)
            sql = """
                              insert into image(product_id,img_src,position,sequence,update_time,from_who,pic_md5)
                                          values('%s','%s','%s','%s','%s','%s','%s')
                              """ % ( product_id, src, position, sequence, update_time, from_who,pic_md5)
            try:
                x.ExecNonQuery(sql)
                count += 1

            except Exception as ex:
                print(ex)
                print(sql)
                print("=============================")
                continue
        text = tree.xpath(".//text()")
        text = [item.strip() for item in text]
        text = " ".join(text)
        text = re.sub("\s+","",text)
        text = text.replace("\\", "")
        item_dict['note'] = text.replace("'","")
        return "ok"

    except Exception as ex:
        print(product_id, "descContent_jiexi", "error:", ex)
        file_save = os.path.join("jiexi", product_id + "_" + "descContent" + ".html")
        f = codecs.open(file_save, "a+", encoding="utf-8")
        f.write(content)
        f.close()
        return False

    finally:
        x.EndSql()
