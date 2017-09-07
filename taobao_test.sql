-- MySQL dump 10.13  Distrib 5.7.18, for Win64 (x86_64)
--
-- Host: localhost    Database: taobao_test3
-- ------------------------------------------------------
-- Server version	5.7.18-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `color`
--

DROP TABLE IF EXISTS `color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `color` (
  `img_id` varchar(40) DEFAULT NULL,
  `color_id` varchar(40) NOT NULL DEFAULT '',
  `color` varchar(100) CHARACTER SET utf16 NOT NULL DEFAULT '',
  `update_time` date NOT NULL,
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=722202 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extend_information`
--

DROP TABLE IF EXISTS `extend_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extend_information` (
  `extend_product_id` varchar(32) NOT NULL DEFAULT '',
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `product_name` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `extend_type` char(2) DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11764542 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `img_src` varchar(200) NOT NULL DEFAULT '',
  `position` char(1) NOT NULL,
  `sequence` int(11) NOT NULL,
  `update_time` date NOT NULL,
  `from_who` char(1) NOT NULL,
  `review_id` varchar(40) DEFAULT NULL,
  `isSaved_Picture` varchar(3) NOT NULL DEFAULT '0',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pic_md5` char(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12745106 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `img_unique`
--

DROP TABLE IF EXISTS `img_unique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `img_unique` (
  `img_unique` char(32) NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`img_unique`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=112025 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_comment`
--

DROP TABLE IF EXISTS `product_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_comment` (
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `review_id` varchar(40) NOT NULL DEFAULT '',
  `customer_name` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `rate` varchar(10) DEFAULT NULL,
  `review_type` int(11) DEFAULT NULL,
  `content` text CHARACTER SET utf16,
  `review_date` date DEFAULT NULL,
  `review_time` time DEFAULT NULL,
  `Brief_information` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `back_comment` text CHARACTER SET utf16,
  `back_comment_day` varchar(10) DEFAULT NULL,
  `count_num` int(11) DEFAULT NULL,
  `refund_time` varchar(255) CHARACTER SET utf16 DEFAULT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1802650 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_detail_information`
--

DROP TABLE IF EXISTS `product_detail_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_detail_information` (
  `detail_id` varchar(40) NOT NULL DEFAULT '',
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `index_name` varchar(100) CHARACTER SET utf16 NOT NULL,
  `index_value` varchar(1000) CHARACTER SET utf16 NOT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3972265 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_impress`
--

DROP TABLE IF EXISTS `product_impress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_impress` (
  `impress_id` varchar(40) DEFAULT NULL,
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `impress_type` varchar(100) NOT NULL DEFAULT '',
  `impress_count` int(11) NOT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=231116 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_information`
--

DROP TABLE IF EXISTS `product_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_information` (
  `shop_id` varchar(32) CHARACTER SET gbk NOT NULL,
  `product_id` varchar(32) CHARACTER SET gbk NOT NULL DEFAULT '',
  `product_name` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `product_profile` varchar(200) CHARACTER SET utf16 DEFAULT NULL,
  `total_sales_volume` int(11) DEFAULT NULL,
  `transaction_volume` int(11) DEFAULT NULL,
  `cumulative_review` int(11) DEFAULT NULL,
  `price` varchar(20) CHARACTER SET utf16 DEFAULT NULL,
  `taobao_price` float DEFAULT NULL,
  `place_of_delivery` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `express_fee` float(100,0) DEFAULT NULL,
  `amount_of_inventory` int(11) DEFAULT NULL,
  `promise` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `payment_method` varchar(50) CHARACTER SET utf16 DEFAULT NULL,
  `collection_number` int(11) DEFAULT NULL,
  `note` text CHARACTER SET utf16,
  `comment_with_picture_num` int(11) DEFAULT NULL,
  `append_comment_num` int(11) DEFAULT NULL,
  `positive_comment_num` int(11) DEFAULT NULL,
  `moderate_comment_num` int(11) DEFAULT NULL,
  `negative_comment_num` int(11) DEFAULT NULL,
  `refund_comment_num` int(11) DEFAULT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=339295 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_list`
--

DROP TABLE IF EXISTS `product_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_list` (
  `shop_id` varchar(32) CHARACTER SET gbk DEFAULT NULL,
  `product_id` varchar(32) CHARACTER SET gbk NOT NULL DEFAULT '',
  `total_sales_volume` int(11) DEFAULT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_productid` (`product_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=417512 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seller_info`
--

DROP TABLE IF EXISTS `seller_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seller_info` (
  `shop_id` varchar(32) CHARACTER SET utf16 NOT NULL DEFAULT '',
  `alipay_Authentication` date DEFAULT NULL,
  `main_products` varchar(100) CHARACTER SET utf16 DEFAULT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `seller_credit` int(11) DEFAULT NULL,
  `buyer_credit` int(11) DEFAULT NULL,
  `seller_bond` float DEFAULT NULL,
  `commodity_score` float DEFAULT NULL,
  `seller_attitude_score` float DEFAULT NULL,
  `logistics_score` float DEFAULT NULL,
  `commodity_score_compare` float DEFAULT NULL,
  `seller_attitude_score_compare` float DEFAULT NULL,
  `logistics_score_compare` float DEFAULT NULL,
  `positive_comment_week` int(11) DEFAULT NULL,
  `moderate_comment_week` int(11) DEFAULT NULL,
  `negative_comment_week` int(11) DEFAULT NULL,
  `core_positive_comment_week` int(11) DEFAULT NULL,
  `core_moderate_comment_week` int(11) DEFAULT NULL,
  `core_negative_comment_week` int(11) DEFAULT NULL,
  `non_core_positive_comment_week` int(11) DEFAULT NULL,
  `non_core_moderate_comment_week` int(11) DEFAULT NULL,
  `non_core_negative_comment_week` int(11) DEFAULT NULL,
  `positive_comment_month` int(11) DEFAULT NULL,
  `moderate_comment_month` int(11) DEFAULT NULL,
  `negative_comment_month` int(11) DEFAULT NULL,
  `core_positive_comment_month` int(11) DEFAULT NULL,
  `core_moderate_comment_month` int(11) DEFAULT NULL,
  `core_negative_comment_month` int(11) DEFAULT NULL,
  `non_core_positive_comment_month` int(11) DEFAULT NULL,
  `non_core_moderate_comment_month` int(11) DEFAULT NULL,
  `non_core_negative_comment_month` int(11) DEFAULT NULL,
  `positive_comment_half_year` int(11) DEFAULT NULL,
  `moderate_comment_half_year` int(11) DEFAULT NULL,
  `negative_comment_half_year` int(11) DEFAULT NULL,
  `core_positive_comment_half_year` int(11) DEFAULT NULL,
  `core_moderate_comment_half_year` int(11) DEFAULT NULL,
  `core_negative_comment_half_year` int(11) DEFAULT NULL,
  `non_core_positive_comment_half_year` int(11) DEFAULT NULL,
  `non_core_moderate_comment_half_year` int(11) DEFAULT NULL,
  `non_core_negative_comment_half_year` int(11) DEFAULT NULL,
  `positive_comment_before_half_year` int(11) DEFAULT NULL,
  `moderate_comment_before_half_year` int(11) DEFAULT NULL,
  `negative_comment_before_half_year` int(11) DEFAULT NULL,
  `after_sales_speed_nearly_30` float DEFAULT NULL,
  `after_sales_speed_nearly_30_compare` float DEFAULT NULL,
  `refund_speed_nearly_30` float DEFAULT NULL,
  `full_refund_speed_nearly_30` float DEFAULT NULL,
  `after_sale_rate_nearly_30` float DEFAULT NULL,
  `after_sale_rate_nearly_30_compare` float DEFAULT NULL,
  `after_sales_count_nearly_30` int(11) DEFAULT NULL,
  `bad_goods_count_nearly_30` int(11) DEFAULT NULL,
  `buyer_dislike_count_nearly_30` int(11) DEFAULT NULL,
  `bad_seller_attitude_nearly_30` int(11) DEFAULT NULL,
  `dispute_rate_nearly_30` float DEFAULT NULL,
  `dispute_rate_nearly_30_compare` float DEFAULT NULL,
  `total_penalty` float DEFAULT NULL,
  `penalty_number_nearly_30` float DEFAULT NULL,
  `penalty_number_nearly_30_compare` float DEFAULT NULL,
  `aftersale_attitude_score_nearly_180` float DEFAULT NULL,
  `aftersale_attitude_score_nearly_180_compare` float DEFAULT NULL,
  `after_sale_rate_nearly_180` float DEFAULT NULL,
  `after_sale_rate_nearly_180_compare` float DEFAULT NULL,
  `penalty_number_fake_good` int(11) DEFAULT NULL,
  `penalty_number_false_transaction` int(11) DEFAULT NULL,
  `penalty_number_breach_promise` int(11) DEFAULT NULL,
  `penalty_number_bad_desc` int(11) DEFAULT NULL,
  `penalty_number_malicious_harassment` int(11) DEFAULT NULL,
  `average_score_for_commodity` float DEFAULT NULL,
  `count_of_judger_for_commodity` int(11) DEFAULT NULL,
  `five_score_rate_for_commodity` varchar(10) DEFAULT NULL,
  `four_score_rate_for_commodity` varchar(10) DEFAULT NULL,
  `three_score_rate_for_commodity` varchar(10) DEFAULT NULL,
  `two_score_rate_for_commodity` varchar(10) DEFAULT NULL,
  `one_score_rate_for_commodity` varchar(10) DEFAULT NULL,
  `average_score_for_seller` float DEFAULT NULL,
  `count_of_judger_for_seller` int(11) DEFAULT NULL,
  `five_score_rate_for_seller` varchar(10) DEFAULT NULL,
  `four_score_rate_for_seller` varchar(10) DEFAULT NULL,
  `three_score_rate_for_seller` varchar(10) DEFAULT NULL,
  `two_score_rate_for_seller` varchar(10) DEFAULT NULL,
  `one_score_rate_for_seller` varchar(10) DEFAULT NULL,
  `average_score_for_logistics` float DEFAULT NULL,
  `count_of_judger_for_logistics` int(11) DEFAULT NULL,
  `five_score_rate_for_logistics` varchar(10) DEFAULT NULL,
  `four_score_rate_for_logistics` varchar(10) DEFAULT NULL,
  `three_score_rate_for_logistics` varchar(10) DEFAULT NULL,
  `two_score_rate_for_logistics` varchar(10) DEFAULT NULL,
  `one_score_rate_for_logistics` varchar(10) DEFAULT NULL,
  `delivery_hour_after_payment` int(11) DEFAULT NULL,
  `refund_day_for_no_reason` int(11) DEFAULT NULL,
  `update_time` date NOT NULL DEFAULT '0000-00-00',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_shop_id` (`shop_id`,`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_homepage`
--

DROP TABLE IF EXISTS `shop_homepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_homepage` (
  `shop_id` varchar(32) NOT NULL DEFAULT '',
  `product_id` varchar(32) NOT NULL DEFAULT '',
  `product_name` varchar(100) CHARACTER SET utf16 NOT NULL,
  `sequence` int(11) NOT NULL,
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_product_id_updatetime` (`product_id`,`update_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=62807 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `size`
--

DROP TABLE IF EXISTS `size`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `size` (
  `product_id` varchar(32) CHARACTER SET gbk COLLATE gbk_bin NOT NULL DEFAULT '',
  `size_id` varchar(40) NOT NULL,
  `size` varchar(32) CHARACTER SET utf16 NOT NULL DEFAULT '',
  `update_time` date NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=922699 DEFAULT CHARSET=gbk;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-13 18:23:21
