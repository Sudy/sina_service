-- MySQL dump 10.13  Distrib 5.5.32, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: weibo_service
-- ------------------------------------------------------
-- Server version	5.5.32-0ubuntu0.12.04.1

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
-- Table structure for table `report_info`
--

DROP TABLE IF EXISTS `report_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_info` (
  `rid` varchar(20) COLLATE utf8_bin NOT NULL,
  `report_count` int(11) DEFAULT '0',
  `reporter` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `bereporteder` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `first_report_time` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `report_type` tinyint(4) DEFAULT '5',
  `report_origin_text` text COLLATE utf8_bin,
  `weibo_repost_count` int(11) DEFAULT '0',
  `weibo_like_count` int(11) DEFAULT '0',
  `weibo_comment_count` int(11) DEFAULT '0',
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_info`
--

LOCK TABLES `report_info` WRITE;
/*!40000 ALTER TABLE `report_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `report_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `udomain` varchar(45) COLLATE utf8_bin NOT NULL,
  `idstr` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `location` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `description` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `gender` char(2) COLLATE utf8_bin DEFAULT 'm',
  `followers_count` tinyint(4) DEFAULT '0',
  `friends_count` tinyint(4) DEFAULT '0',
  `statuses_count` tinyint(4) DEFAULT '0',
  `favourites_count` tinyint(4) DEFAULT '0',
  `created_at` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `verified` varchar(8) COLLATE utf8_bin DEFAULT 'False',
  `verified_type` tinyint(4) DEFAULT NULL,
  `verified_reason` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `bi_followers_count` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`udomain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-29 15:03:57
