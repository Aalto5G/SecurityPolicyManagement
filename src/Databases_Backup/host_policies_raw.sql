-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: host_policies
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

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
-- Table structure for table `ces_policies`
--

DROP TABLE IF EXISTS `ces_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ces_policies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(32) DEFAULT NULL,
  `types` varchar(16) DEFAULT NULL,
  `policy_element` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`,`types`,`policy_element`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ces_policies`
--

LOCK TABLES `ces_policies` WRITE;
/*!40000 ALTER TABLE `ces_policies` DISABLE KEYS */;
/*!40000 ALTER TABLE `ces_policies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ces_policy_identity`
--

DROP TABLE IF EXISTS `ces_policy_identity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ces_policy_identity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_ces_id` varchar(256) DEFAULT NULL,
  `protocol` varchar(64) DEFAULT NULL,
  `uuid` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `protocol` (`protocol`,`host_ces_id`,`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ces_policy_identity`
--

LOCK TABLES `ces_policy_identity` WRITE;
/*!40000 ALTER TABLE `ces_policy_identity` DISABLE KEYS */;
/*!40000 ALTER TABLE `ces_policy_identity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firewall_policies`
--

DROP TABLE IF EXISTS `firewall_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firewall_policies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(32) NOT NULL,
  `types` varchar(32) NOT NULL,
  `sub_type` varchar(32) NOT NULL,
  `policy_element` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`uuid`,`types`,`sub_type`,`policy_element`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firewall_policies`
--

LOCK TABLES `firewall_policies` WRITE;
/*!40000 ALTER TABLE `firewall_policies` DISABLE KEYS */;
/*!40000 ALTER TABLE `firewall_policies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_ids`
--

DROP TABLE IF EXISTS `host_ids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_ids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(32) NOT NULL,
  `fqdn` varchar(256) NOT NULL,
  `msisdn` varchar(16) DEFAULT NULL,
  `ipv4` varchar(16) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`fqdn`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `ipv4` (`ipv4`),
  UNIQUE KEY `msisdn` (`msisdn`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_ids`
--

LOCK TABLES `host_ids` WRITE;
/*!40000 ALTER TABLE `host_ids` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_ids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_policies`
--

DROP TABLE IF EXISTS `host_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_policies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(32) DEFAULT NULL,
  `types` varchar(16) DEFAULT NULL,
  `policy_element` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`,`types`,`policy_element`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_policies`
--

LOCK TABLES `host_policies` WRITE;
/*!40000 ALTER TABLE `host_policies` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_policies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_policy_identity`
--

DROP TABLE IF EXISTS `host_policy_identity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_policy_identity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `local_fqdn` varchar(256) DEFAULT NULL,
  `remote_fqdn` varchar(256) DEFAULT NULL,
  `reputation` varchar(48) DEFAULT NULL,
  `direction` varchar(16) DEFAULT NULL,
  `uuid` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `local_fqdn` (`local_fqdn`,`remote_fqdn`,`reputation`,`direction`,`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_policy_identity`
--

LOCK TABLES `host_policy_identity` WRITE;
/*!40000 ALTER TABLE `host_policy_identity` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_policy_identity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_policy_ts`
--

DROP TABLE IF EXISTS `host_policy_ts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_policy_ts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(64) NOT NULL,
  `policy` varchar(128) NOT NULL,
  `time_stamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`,`policy`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_policy_ts`
--

LOCK TABLES `host_policy_ts` WRITE;
/*!40000 ALTER TABLE `host_policy_ts` DISABLE KEYS */;
/*!40000 ALTER TABLE `host_policy_ts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-30 16:33:18
