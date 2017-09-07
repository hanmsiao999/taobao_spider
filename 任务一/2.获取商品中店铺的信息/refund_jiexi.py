# coding:utf-8
import os
import codecs
from lxml import etree
import re
from connectMysql import Mymysql


def refund_jiexi(shop_id, content, update_time):
    try:
        x = Mymysql()
        x._GetConnect()
        tree = etree.HTML(content)
        kuang = tree.xpath(".//div[@class='tb-r-box kg-rate-wd-refund']")
        trs = tree.xpath(".//tr[@class='J_KgRate_RefundSummary_TR']")

        tmp_tr = trs[0]
        tds = tmp_tr.xpath(".//td/text()")
        # 近30天售后速度
        after_sales_speed_nearly_30 = re.findall("\d+.?\d+", tds[1])
        after_sales_speed_nearly_30 = -1 if len(after_sales_speed_nearly_30) == 0 else after_sales_speed_nearly_30[0]
        # print "after_sales_speed_nearly_30",after_sales_speed_nearly_30
        # 近30天售后速度 比行业值
        if u"持平" in tds[2]:
            after_sales_speed_nearly_30_compare = 0
        else:
            after_sales_speed_nearly_30_compare = re.findall("\d+.?\d+", tds[2])
            after_sales_speed_nearly_30_compare = -1 if len(after_sales_speed_nearly_30_compare) == 0 else \
            after_sales_speed_nearly_30_compare[0]
            if u"快" not in tds[2] and after_sales_speed_nearly_30_compare != -1:
                after_sales_speed_nearly_30_compare = "-" + after_sales_speed_nearly_30_compare
                after_sales_speed_nearly_30_compare = float(after_sales_speed_nearly_30_compare) * 0.01
        # print "after_sales_speed_nearly_30_compare",after_sales_speed_nearly_30_compare


        tmp = tree.xpath(".//div[@data-kg-rate-gl-hover='refundfeedback.3.6']/ul/li/text()")
        # print "tmp:",tmp
        if len(tmp) != 0:
            # 仅退款速度
            refund_speed_nearly_30 = re.findall(u"仅退款速度 (\d+.?\d+)", tmp[0])
            # print "refund_speed_nearly_30:",refund_speed_nearly_30
            refund_speed_nearly_30 = -1 if len(refund_speed_nearly_30) == 0 else refund_speed_nearly_30[0]
            # print "refund_speed_nearly_30",refund_speed_nearly_30
            # 退货退款速度
            full_refund_speed_nearly_30 = re.findall(u"退货退款速度 (\d+.?\d+)", tmp[-1])
            # print "full_refund_speed_nearly_30:",full_refund_speed_nearly_30
            full_refund_speed_nearly_30 = -1 if len(full_refund_speed_nearly_30) == 0 else full_refund_speed_nearly_30[
                0]
            # print "full_refund_speed_nearly_30",full_refund_speed_nearly_30
        else:
            refund_speed_nearly_30 = -1
            full_refund_speed_nearly_30 = -1

        tmp_tr = trs[1]
        tds = tmp_tr.xpath(".//td/text()")
        # 近30天纠纷率
        dispute_rate_nearly_30 = re.findall("\d+.?\d+", tds[1])

        if len(dispute_rate_nearly_30) > 0:
            dispute_rate_nearly_30 = float(dispute_rate_nearly_30[0]) * 0.01
        else:
            dispute_rate_nearly_30 = -1
        # print "dispute_rate_nearly_30",dispute_rate_nearly_30
        #  近30天纠纷率 比行业值
        if u"持平" in tds[2]:
            dispute_rate_nearly_30_compare = 0
        else:
            dispute_rate_nearly_30_compare = re.findall("\d+.?\d+", tds[2])
            dispute_rate_nearly_30_compare = -1 if len(dispute_rate_nearly_30_compare) == 0 else \
            dispute_rate_nearly_30_compare[0]
            if u"低" in tds[2] and dispute_rate_nearly_30_compare != -1:
                dispute_rate_nearly_30_compare = "-" + dispute_rate_nearly_30_compare
                dispute_rate_nearly_30_compare = float(dispute_rate_nearly_30_compare) * 0.01
        # print "dispute_rate_nearly_30_compare",dispute_rate_nearly_30_compare

        tmp_tr = trs[2]
        tds = tmp_tr.xpath(".//td/text()")
        # 近30天售后率
        after_sale_rate_nearly_30 = re.findall("\d+.?\d+", tds[1])
        after_sale_rate_nearly_30 = -1 if len(after_sale_rate_nearly_30) == 0 else after_sale_rate_nearly_30[0]
        after_sale_rate_nearly_30 = float(after_sale_rate_nearly_30) * 0.01
        # print "after_sale_rate_nearly_30",after_sale_rate_nearly_30

        if u"持平" in tds[2]:
            after_sale_rate_nearly_30_compare = 0
        else:
            after_sale_rate_nearly_30_compare = re.findall("\d+.?\d+", tds[2])
            after_sale_rate_nearly_30_compare = -1 if len(after_sale_rate_nearly_30_compare) == 0 else \
            after_sale_rate_nearly_30_compare[0]

            if u"低" in tds[2] and after_sale_rate_nearly_30_compare != -1:
                after_sale_rate_nearly_30_compare = "-" + after_sale_rate_nearly_30_compare
                after_sale_rate_nearly_30_compare = float(after_sale_rate_nearly_30_compare) * 0.01
        # print "after_sale_rate_nearly_30_compare",after_sale_rate_nearly_30_compare

        # hover frame
        hover_frame_for_rate = tree.xpath(".//div[@data-kg-rate-gl-hover='refundfeedback.3.8']//text()")
        hover_frame_for_rate = list(filter(lambda x: len(x.strip()) > 0, hover_frame_for_rate))
        after_sales_count_nearly_30 = re.findall("\d+", hover_frame_for_rate[0])[1]
        # print "after_sales_count_nearly_30",after_sales_count_nearly_30
        bad_goods_count_nearly_30 = re.findall("\d+", hover_frame_for_rate[1])[0]
        # print "bad_goods_count_nearly_30",bad_goods_count_nearly_30
        buyer_dislike_count_nearly_30 = re.findall("\d+", hover_frame_for_rate[2])[0]
        # print "buyer_dislike_count_nearly_30",buyer_dislike_count_nearly_30
        bad_seller_attitude_nearly_30 = re.findall("\d+", hover_frame_for_rate[3])[0]
        # print "bad_seller_attitude_nearly_30",bad_seller_attitude_nearly_30


        tmp_tr = trs[3]
        tds = tmp_tr.xpath(".//td/text()")
        # 近180天售后态度评分
        aftersale_attitude_score_nearly_180 = re.findall("\d+.?\d+", tds[1])
        aftersale_attitude_score_nearly_180 = -1 if len(aftersale_attitude_score_nearly_180) == 0 else \
        aftersale_attitude_score_nearly_180[0]
        # print "aftersale_attitude_score_nearly_180",aftersale_attitude_score_nearly_180

        if u"持平" in tds[2]:
            aftersale_attitude_score_nearly_180_compare = 0
        else:
            aftersale_attitude_score_nearly_180_compare = re.findall("\d+.?\d+", tds[2])
            aftersale_attitude_score_nearly_180_compare = -1 if len(
                aftersale_attitude_score_nearly_180_compare) == 0 else aftersale_attitude_score_nearly_180_compare[0]
            if u"低" in tds[2] and aftersale_attitude_score_nearly_180_compare != -1:
                aftersale_attitude_score_nearly_180_compare = "-" + aftersale_attitude_score_nearly_180_compare
                aftersale_attitude_score_nearly_180_compare = float(aftersale_attitude_score_nearly_180_compare) * 0.01
        # print "aftersale_attitude_score_nearly_180_compare",aftersale_attitude_score_nearly_180_compare


        tmp_tr = trs[4]
        tds = tmp_tr.xpath(".//td/text()")
        # 近180天售后速度评分
        after_sale_rate_nearly_180 = re.findall("\d+.?\d+", tds[1])
        after_sale_rate_nearly_180 = -1 if len(after_sale_rate_nearly_180) == 0 else after_sale_rate_nearly_180[0]
        # print "after_sale_rate_nearly_180",after_sale_rate_nearly_180
        if u"持平" in tds[2]:
            after_sale_rate_nearly_180_compare = 0
        else:
            after_sale_rate_nearly_180_compare = re.findall("\d+.?\d+", tds[2])
            after_sale_rate_nearly_180_compare = -1 if len(after_sale_rate_nearly_180_compare) == 0 else \
            after_sale_rate_nearly_180_compare[0]
            if u"低" in tds[2] and after_sale_rate_nearly_180_compare != -1:
                after_sale_rate_nearly_180_compare = "-" + after_sale_rate_nearly_180_compare
                after_sale_rate_nearly_180_compare = float(after_sale_rate_nearly_180_compare) * 0.01
        # print "after_sale_rate_nearly_180_compare",after_sale_rate_nearly_180_compare
        sql = """
              update seller_info set after_sales_speed_nearly_30='%s',
                                     after_sales_speed_nearly_30_compare='%s',
                                     refund_speed_nearly_30='%s',
                                     full_refund_speed_nearly_30='%s',
                                     dispute_rate_nearly_30='%s',
                                     dispute_rate_nearly_30_compare='%s',
                                     after_sale_rate_nearly_30='%s',
                                     after_sale_rate_nearly_30_compare='%s',
                                     after_sales_count_nearly_30='%s',
                                     bad_goods_count_nearly_30='%s',
                                     buyer_dislike_count_nearly_30='%s',
                                     bad_seller_attitude_nearly_30='%s',
                                     aftersale_attitude_score_nearly_180='%s',
                                     aftersale_attitude_score_nearly_180_compare='%s',
                                     after_sale_rate_nearly_180='%s',
                                     after_sale_rate_nearly_180_compare='%s'           
              where shop_id = '%s' and update_time='%s'   
              """ % (after_sales_speed_nearly_30,
                     after_sales_speed_nearly_30_compare,
                     refund_speed_nearly_30,
                     full_refund_speed_nearly_30,
                     dispute_rate_nearly_30,
                     dispute_rate_nearly_30_compare,
                     after_sale_rate_nearly_30,
                     after_sale_rate_nearly_30_compare,
                     after_sales_count_nearly_30,
                     bad_goods_count_nearly_30,
                     buyer_dislike_count_nearly_30,
                     bad_seller_attitude_nearly_30,
                     aftersale_attitude_score_nearly_180,
                     aftersale_attitude_score_nearly_180_compare,
                     after_sale_rate_nearly_180,
                     after_sale_rate_nearly_180_compare, shop_id, update_time)
        x.ExecNonQuery(sql)
    except Exception as ex:
        print(shop_id, "refund_jiexi", "error:", ex)
        log_path = os.path.join("jiexi", shop_id + "_" + "refund_jiexi.txt")
        f = codecs.open(log_path, "w+",encoding="utf-8")
        f.write(content)
        f.close()
        return False
    finally:
        x.EndSql()
