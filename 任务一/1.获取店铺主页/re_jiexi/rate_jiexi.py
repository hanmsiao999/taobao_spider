#coding:utf-8
import os
import codecs
from lxml import etree
import re
import datetime
def exist_or_0(item):
    if len(item)==0:
        return -1
    else:
        return item[0]

def rating_jiexi(shop_ID,html):
    values = []
    tree  = etree.HTML(html)
    # 1 店铺ID shop_id %s
    shop_id = re.findall("\"shopID\":(.*?),",html)[0].strip()[1:-1]
    #print shopID
    values.append(shop_id)
    
    # 2 .支付宝认证时间: alipay_Authentication
    alipay_Authentication = tree.xpath(".//span[@class='id-time']/text()")
    if len(alipay_Authentication)==0:
        alipay_Authentication = '0000-00-00'
    else:
        alipay_Authentication = alipay_Authentication[0]
    values.append(alipay_Authentication)

    # 3. 主营: main_products
    main_products = tree.xpath(".//*[@id='chart-name']/text()")[0].strip()
    print main_products
    values.append(main_products)

    # 4. 所在地区 Location
    location_text =  "".join(tree.xpath(".//div[@class='info-block info-block-first']//ul/li[2]/text()"))
    print location_text
    Location = location_text.split("：")[1].strip()
    values.append(Location)

    # 5. 卖家信用 seller_credit
    seller_credit = tree.xpath(".//ul[@class='sep']/li[1]/text()")[0].split("：")[1].strip()
    values.append(seller_credit)
    
    # 6. 买家信用 buyer_credit
    buyer_credit = tree.xpath(".//ul[@class='sep']/li[2]/text()")[0].split("：")[1].strip()
    values.append(buyer_credit)

    # 7.保证金余额: seller_bond
    seller_bond = tree.xpath(".//div[@class='charge']/span/text()")
    if len(seller_bond) == 0:
        seller_bond = 0
    else:
        seller_bond = seller_bond[0][1:].split(".")[0].replace(",","")
    values.append(seller_bond)

    # 8-10 评分
    rating =  tree.xpath(".//div[@class='item-scrib']")
    rating_baby = 0 ; rating_baby_industry_score = 0
    rating_seller = 0 ;rating_seller_industry_score = 0
    rating_logistics = 0 ; rating_logistics_industry_score = 0
    if len(rating) == 3:
       # 8.宝贝与描述相符分数 commodity_score
       commodity_score =  rating[0].xpath(".//em[@class='count']/text()")[0]
       values.append(commodity_score)
    
       # 9.卖家的服务态度 seller_attitude_score
       seller_attitude_score = rating[1].xpath(".//em[@class='count']/text()")[0]
       values.append(seller_attitude_score)

       # 10.物流服务质量 logistics_score
       logistics_score = rating[2].xpath(".//em[@class='count']/text()")[0]
       values.append(logistics_score)

       # 11-13 同行业
       # 11 宝贝与描述相符分数比同行业平均水平 commodity _score_compare
       rating_baby_Same_industry = rating[0].xpath(".//strong")[0]
       strong_class = rating_baby_Same_industry.get("class")
       rating_baby_industry_score = rating_baby_Same_industry.xpath(".//text()")[0]
       if "--" in rating_baby_industry_score:
          commodity_score_compare= 0
       else:
          commodity_score_compare = float(rating_baby_Same_industry.xpath(".//text()")[0][:-1])*1.0/100
          if "over" not in strong_class:
             commodity_score_compare*=-1
       #print rating_baby_industry_score
       values.append(commodity_score_compare)

       # 12 卖家的服务态度分数比同行业平均水平 seller_attitude_score_compare
       rating_seller_Same_industry = rating[1].xpath(".//strong")[0]
       strong_class = rating_seller_Same_industry.get("class")
       rating_seller_industry_score = rating_seller_Same_industry.xpath(".//text()")[0]
       if "--" in rating_seller_industry_score:
          seller_attitude_score_compare = 0
       else:
          seller_attitude_score_compare = float(rating_seller_Same_industry.xpath(".//text()")[0][:-1])*1.0/100
          if "over" not in strong_class:
            seller_attitude_score_compare*=-1
       values.append(seller_attitude_score_compare)
    
       # 13 物流服务的质量分数比同行业平均水平 logistics_score_compare
       rating_logistics_Same_industry = rating[2].xpath(".//strong")[0]
       strong_class = rating_logistics_Same_industry.get("class")
       rating_logistics_industry_score = rating_logistics_Same_industry.xpath(".//text()")[0]
       if "--" in rating_logistics_industry_score:
          logistics_score_compare = 0
       else:
          logistics_score_compare = float(rating_logistics_Same_industry.xpath(".//text()")[0][:-1])*1.0/100
          if "over" not in strong_class:
              logistics_score_compare*=-1
       values.append(logistics_score_compare)

    
    # 14最近一周
    week = tree.xpath(".//div[@id='J_show_list']//li[1]//text()")
    week = filter(lambda x: len(re.findall("\d+",x))>=1,week)
    week = [re.findall("\d+",item)[0] for item in week]
    # 最近一周好评总数
    positive_comment_week = week[0]
    values.append(positive_comment_week)
    # 最近一周中评总数
    moderate_comment_week= week[1]
    values.append(moderate_comment_week)
    # 最近一周差评总数
    negative_comment_week= week[2]
    values.append(negative_comment_week)
    # 最近一周所属类别好评总数
    core_positive_comment_week= week[3]
    values.append(core_positive_comment_week)
    # 最近一周所属类别中评总数
    core_moderate_comment_week= week[4]
    values.append(core_moderate_comment_week)
    # 最近一周所属类别差评总数
    core_negative_comment_week= week[5]
    values.append(core_negative_comment_week)
    # 最近一周非主营行业好评总数
    non_core_positive_comment_week= week[6]
    values.append(non_core_positive_comment_week)
    # 最近一周非主营行业中评总数
    non_core_moderate_comment_week= week[7]
    values.append(non_core_moderate_comment_week)
    # 最近一周非主营行业差评总数
    non_core_negative_comment_week= week[8]
    values.append(non_core_negative_comment_week)

    # 15 最近一月
    month = tree.xpath(".//div[@id='J_show_list']//li[2]//text()")
    month = filter(lambda x: len(re.findall("\d+",x))>=1,month)
    month = [re.findall("\d+",item)[0] for item in month]
    # 最近一月好评总数
    positive_comment_month = month[0]
    values.append(positive_comment_month)
    # 最近一月中评总数
    moderate_comment_month= month[1]
    values.append(moderate_comment_month)
    # 最近一月差评总数
    negative_comment_month= month[2]
    values.append(negative_comment_month)
    # 最近一月所属类别好评总数
    core_positive_comment_month= month[3]
    values.append(core_positive_comment_month)
    # 最近一月所属类别中评总数
    core_moderate_comment_month= month[4]
    values.append(core_moderate_comment_month)
    # 最近一月所属类别差评总数
    core_negative_comment_month= month[5]
    values.append(core_negative_comment_month)
    # 最近一月非主营行业好评总数
    non_core_positive_comment_month= month[6]
    values.append(non_core_positive_comment_month)
    # 最近一月非主营行业中评总数
    non_core_moderate_comment_month= month[7]
    values.append(non_core_moderate_comment_month)
    # 最近一月非主营行业差评总数
    non_core_negative_comment_month= month[8]
    values.append(non_core_negative_comment_month)
    

    # 16 最近半年
    half_year = tree.xpath(".//div[@id='J_show_list']//li[3]//text()")
    half_year = filter(lambda x: len(re.findall("\d+",x))>=1,half_year)
    half_year = [re.findall("\d+",item)[0] for item in half_year]
    # 最近半年好评总数
    positive_comment_half_year = half_year[0]
    values.append(positive_comment_half_year)
    # 最近半年中评总数
    moderate_comment_half_year= half_year[1]
    values.append(moderate_comment_half_year)
    # 最近半年差评总数
    negative_comment_half_year= half_year[2]
    values.append(negative_comment_half_year)
    # 最近半年所属类别好评总数
    core_positive_comment_half_year= half_year[3]
    values.append(core_positive_comment_half_year)
    # 最近半年所属类别中评总数
    core_moderate_comment_half_year= half_year[4]
    values.append(core_moderate_comment_half_year)
    # 最近半年所属类别差评总数
    core_negative_comment_half_year= half_year[5]
    values.append(core_negative_comment_half_year)
    # 最近半年非主营行业好评总数
    non_core_positive_comment_half_year= half_year[6]
    values.append(non_core_positive_comment_half_year)
    # 最近半年非主营行业中评总数
    non_core_moderate_comment_half_year= half_year[7]
    values.append(non_core_moderate_comment_half_year)
    # 最近半年非主营行业差评总数
    non_core_negative_comment_half_year= half_year[8]
    values.append(non_core_negative_comment_half_year)
    

    # 17 半年以前
    before_half = tree.xpath(".//div[@id='J_show_list']//li[4]//text()")
    before_half = filter(lambda x: len(re.findall("\d+",x))>=1,before_half)
    before_half = [re.findall("\d+",item)[0] for item in before_half]
    #print before_half
    #半年以前好评总数
    positive_comment_before_half_year=before_half[0]
    values.append(positive_comment_before_half_year)
    #半年以前中评总数
    moderate_comment_before_half_year=before_half[1]
    values.append(moderate_comment_before_half_year)
    #半年以前差评总数
    negative_comment_before_half_year=before_half[2]
    values.append(negative_comment_before_half_year)
    
    # 18-25 30天服务情况
    table = tree.xpath(".//table[@class='tb-rate-table']/tbody/tr")
    total_penalty = -1
    after_sales_speed_nearly_30= -1
    after_sales_speed_nearly_30_compare = -1
    after_sale_rate_nearly_30 = -1
    after_sale_rate_nearly_30_compare= -1
    dispute_rate_nearly_30=-1
    dispute_rate_nearly_30_compare=-1
    penalty_number_nearly_30=-1
    penalty_number_nearly_30_compare=-1
    penalty_number_fake_good=-1
    penalty_number_false_transaction=-1
    penalty_number_breach_promise=-1
    penalty_number_bad_desc=-1
    penalty_number_malicious_harassment=-1
    
    if len(table)!=0:
       # 18 售后速度
       # 19 售后速度行业值
       tds = table[0].xpath(".//td/text()")[1:]
       aftermarket_Speed = float(tds[0][:-1])
       aftermarket_Industry_Speed = float(tds[2][:-1])
       if tds[1]=="小于":
          aftermarket_Industry_Speed*=-1
       #本店近30天售后速度
       after_sales_speed_nearly_30 =aftermarket_Speed
       
       #本店近30天售后速度比行业均值
       after_sales_speed_nearly_30_compare = aftermarket_Industry_Speed
       
    
       # 20 售后率
       # 21 售后率行业值
       tds = table[1].xpath(".//td/text()")[1:]
       after_sale_rate = float(tds[0][:-1])*0.01
       after_sale_Industry_rate = float(tds[2][:-1])*0.01
       if tds[1]=="小于":
          after_sale_Industry_rate*=-1
       # 本店近30天售后率
       after_sale_rate_nearly_30 = after_sale_rate
       
       # 本店近30天售后率比行业均值
       after_sale_rate_nearly_30_compare = after_sale_Industry_rate
       

       # 22 纠纷率
       # 23 纠纷率行业值
       tds = table[2].xpath(".//td/text()")[1:]
       dispute_rate = float(tds[0][:-1])*0.01
       dispute_Industry_rate = float(tds[2][:-1])*0.01
       if tds[1]=="小于":
          dispute_Industry_rate*=-1
       # 本店近30天纠纷率
       dispute_rate_nearly_30 = dispute_rate
       
       # 本店近30天纠纷率比行业均值
       dispute_rate_nearly_30_compare = dispute_Industry_rate
       

       # 24 处罚数
       # 25 处罚数行业值
       tds = table[3].xpath(".//td/text()")[1:]
       penalty_number = float(tds[0][:-1])
       penalty_Industry_number = float(tds[2][:-1])
       if tds[1]=="小于":
          penalty_Industry_number*=-1
       # 本店近30天处罚数
       penalty_number_nearly_30 = penalty_number
       
       # 本店近30天处罚数比行业均值
       penalty_number_nearly_30_compare = penalty_Industry_number
       
    
       # 26-31 虚假信息
       tds = tree.xpath(".//div[@class='J_TBR_MonthInfo_Detail detail']/div[4]")[0]
       info = tds.xpath("string(.)")
       content=info.replace('\n','').replace(' ','')
       print content
       fake_info = re.findall("\d+",content)
       fake_info = [int(item) for item in fake_info]
       #print fake_info
       #26 本店近30天被处罚总次数
       total_penalty = fake_info[1]
    
       #print total_penalty
       #27 因出售假冒商品，被处罚次数
       penalty_number_fake_good = fake_info[2]
       
    
       #28 因虚假交易，被处罚次数
       penalty_number_false_transaction = fake_info[3]
       
       #29 因违背承诺，被处罚次数
       penalty_number_breach_promise = fake_info[4]
       
       #30 因描述不符，被处罚次数
       penalty_number_bad_desc = fake_info[5]
       
       #31 因恶意骚扰，被处罚次数
       penalty_number_malicious_harassment = fake_info[6]
    
    """
    after_sales_speed_nearly_30,
    after_sales_speed_nearly_30_compare,
    after_sale_rate_nearly_30,
    after_sale_rate_nearly_30_compare,
    dispute_rate_nearly_30,
    dispute_rate_nearly_30_compare,
    penalty_number_nearly_30,
    penalty_number_nearly_30_compare,
    penalty_number_fake_good,
    penalty_number_false_transaction,
    penalty_number_breach_promise,
    penalty_number_bad_desc,
    penalty_number_malicious_harassment,
    """
    
    
    
    
    values.append(total_penalty)
    values.append(after_sales_speed_nearly_30)
    values.append(after_sales_speed_nearly_30_compare)
    values.append(after_sale_rate_nearly_30) 
    values.append(after_sale_rate_nearly_30_compare)
    values.append(dispute_rate_nearly_30)
    values.append(dispute_rate_nearly_30_compare)
    values.append(penalty_number_nearly_30)
    values.append(penalty_number_nearly_30_compare)
    values.append(penalty_number_fake_good)
    values.append(penalty_number_false_transaction)
    values.append(penalty_number_breach_promise)
    values.append(penalty_number_bad_desc)
    values.append(penalty_number_malicious_harassment)
      
      
    #32-38 评分
    tbs = tree.xpath(".//div[@class='box-wrap']")
    if len(tbs)==3:
       # 宝贝评分打星
       baby = tbs[0]
       # 宝贝评分均分
       average_score_for_commodity = exist_or_0(baby.xpath(".//div[@class='total']/em[@class='h']/text()"))
       values.append(average_score_for_commodity)
       # 评价总人数
       count_of_judger_for_commodity = exist_or_0(baby.xpath(".//div[@class='total']/span/text()"))
       values.append(count_of_judger_for_commodity)
       # 五分好评人数占比
       five_score_rate_for_commodity = exist_or_0(baby.xpath(".//div[@class='count count5']/em/text()"))
       values.append(five_score_rate_for_commodity)
       # 四分好评人数占比
       four_score_rate_for_commodity = exist_or_0(baby.xpath(".//div[@class='count count4']/em/text()"))
       values.append(four_score_rate_for_commodity)
       # 三分好评人数占比
       three_score_rate_for_commodity = exist_or_0(baby.xpath(".//div[@class='count count3']/em/text()"))
       values.append(three_score_rate_for_commodity)
       # 二分好评人数占比
       two_score_rate_for_commodity = exist_or_0(baby.xpath(".//div[@class='count count2']/em/text()"))
       values.append(two_score_rate_for_commodity)
       # 一分好评人数占比
       one_score_rate_for_commodity = exist_or_0(baby.xpath(".//div[@class='count count1']/em/text()"))
       values.append(one_score_rate_for_commodity)

       # 服务态度评分打星
       attitude = tbs[1]
       # 服务态度均分
       average_score_for_seller = exist_or_0(attitude.xpath(".//div[@class='total']/em[@class='h']/text()"))
       values.append(average_score_for_seller)
       # 评价总人数
       count_of_judger_for_seller = exist_or_0(attitude.xpath(".//div[@class='total']/span/text()"))
       values.append(count_of_judger_for_seller)
       # 五分好评人数占比
       five_score_rate_for_seller = exist_or_0(attitude.xpath(".//div[@class='count count5']/em/text()"))
       values.append(five_score_rate_for_seller)
       # 四分好评人数占比
       four_score_rate_for_seller = exist_or_0(attitude.xpath(".//div[@class='count count4']/em/text()"))
       values.append(four_score_rate_for_seller)
       # 三分好评人数占比
       three_score_rate_for_seller = exist_or_0(attitude.xpath(".//div[@class='count count3']/em/text()"))
       values.append(three_score_rate_for_seller)
       # 二分好评人数占比
       two_score_rate_for_seller = exist_or_0(attitude.xpath(".//div[@class='count count2']/em/text()"))
       values.append(two_score_rate_for_seller)
       # 一分好评人数占比
       one_score_rate_for_seller = exist_or_0(attitude.xpath(".//div[@class='count count1']/em/text()"))
       values.append(one_score_rate_for_seller)
    
    
       # 物流评分打星
       logistic = tbs[2]
       # 物流评分均分
       average_score_for_logistics = exist_or_0(logistic.xpath(".//div[@class='total']/em[@class='h']/text()"))
       values.append(average_score_for_logistics)
       # 评价总人数
       count_of_judger_for_logistics = exist_or_0(logistic.xpath(".//div[@class='total']/span/text()"))
       values.append(count_of_judger_for_logistics)
       # 五分好评人数占比
       five_score_rate_for_logistics = exist_or_0(logistic.xpath(".//div[@class='count count5']/em/text()"))
       values.append(five_score_rate_for_logistics)
       # 四分好评人数占比
       four_score_rate_for_logistics = exist_or_0(logistic.xpath(".//div[@class='count count4']/em/text()"))
       values.append(four_score_rate_for_logistics)
       # 三分好评人数占比
       three_score_rate_for_logistics = exist_or_0(logistic.xpath(".//div[@class='count count3']/em/text()"))
       values.append(three_score_rate_for_logistics)
       # 二分好评人数占比
       two_score_rate_for_logistics = exist_or_0(logistic.xpath(".//div[@class='count count2']/em/text()"))
       values.append(two_score_rate_for_logistics)
       # 一分好评人数占比
       one_score_rate_for_logistics = exist_or_0(logistic.xpath(".//div[@class='count count1']/em/text()"))
       values.append(one_score_rate_for_logistics)
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d")
    values.append(otherStyleTime)


f = codecs.open("68770487_rating","r+", encoding="utf-8")
html = f.read()
f.close()
rating_jiexi(1000, html)
    
    


