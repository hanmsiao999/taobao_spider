import os
import codecs
from lxml import etree
import re
from connectMysql import Mymysql
import json
import uuid


def help(product_id, content, x, type_num, update_time):
    sequence = 0
    for item in content:
        try:
            product_name = item['itemName'] if 'itemName' in item else item['title'].replace("'","")
            if "'" in product_name:
                product_name = product_name.replace("'","")
            extend_product_id = item['itemId']
            sql = """
                              insert into extend_information(extend_product_id,\
                              product_id,product_name,extend_type,sequence,update_time)\
                                          values('%s','%s','%s','%s','%s','%s')
                              """ % (extend_product_id, product_id, product_name, type_num, sequence, update_time)
            sequence += 1
            x.ExecNonQuery(sql)
        except Exception as ex:
            print(product_id, "extend_information_jiexi", "error:", ex)
            print(sql)
            print("=============================")
            return False
    return "ok"

def return_to_json_text(html):
    begin_index = html.index("(")
    end_index = html.rindex(")")
    html = html[begin_index + 1:end_index]
    return html

def extend_information_jiexi(product_id, content_watch, content_buy, content_linija, update_time):
    try:
        x = Mymysql()
        x._GetConnect()
        content_watch = return_to_json_text(content_watch)
        content_watch = json.loads(content_watch, encoding='gbk')['result']

        content_buy = return_to_json_text(content_buy)
        content_buy = json.loads(content_buy, encoding='gbk')['result']

        content_linija = return_to_json_text(content_linija)
        if  content_linija:
            content_linija = json.loads(content_linija, encoding='gbk')['result']
        else:
            content_linija = None
        re_1 = help(product_id, content_watch, x, 1, update_time)
        re_2 = help(product_id, content_buy, x, 2, update_time)
        re_3 = help(product_id, content_linija, x, 3, update_time)
        if re_1 == re_2 == re_3 == 'ok':
            return "ok"
        else:
            raise Exception("help error")
    except Exception as ex:
        print(product_id, "extend_information_jiexi", "error:", ex)
        return False
    finally:
        x.EndSql()
