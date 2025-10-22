-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: poker_academy
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class_views`
--

DROP TABLE IF EXISTS `class_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_views` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `class_id` int NOT NULL,
  `viewed_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `idx_user_class` (`user_id`,`class_id`),
  KEY `idx_class_views` (`class_id`),
  KEY `idx_viewed_at` (`viewed_at`),
  CONSTRAINT `class_views_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `class_views_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_views`
--

LOCK TABLES `class_views` WRITE;
/*!40000 ALTER TABLE `class_views` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `category` enum('iniciantes','preflop','postflop','mental','icm') DEFAULT 'preflop',
  `video_url` varchar(500) DEFAULT NULL,
  `instructor_id` int DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `views` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `video_path` varchar(255) DEFAULT NULL,
  `video_type` enum('youtube','local') DEFAULT 'local',
  `priority` int DEFAULT '5',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` (`id`, `name`, `description`, `category`, `video_url`, `instructor_id`, `date`, `views`, `created_at`, `updated_at`, `video_path`, `video_type`, `priority`) VALUES (8,'Equity Drop vs RPS Diferencas_Vanilla e PKO',NULL,'preflop',NULL,2,'2025-04-03 00:00:00',0,'2025-10-22 01:48:58','2025-10-22 01:48:57','20251022_014856_03.04.25-Cademito-PreFlop-Equity_Drop_vs_RPS_Diferencas_Vanilla_e_PKO.mp4','local',5),(9,'Cold Call deep em PKO',NULL,'preflop',NULL,3,'2025-02-04 00:00:00',0,'2025-10-22 01:49:18','2025-10-22 01:49:18','20251022_014917_04.02.25-Carlos.Rox-PreFlop-Cold_Call_deep_em_PKO.mp4','local',5),(10,'DKB Turn',NULL,'preflop',NULL,4,'2025-03-04 00:00:00',0,'2025-10-22 01:49:47','2025-10-22 01:49:47','20251022_014945_04.03.25-Eiji-PosFlop-DKB_Turn.mp4','local',5),(11,'Cbet IP-Simplificacao de sizes',NULL,'preflop',NULL,6,'2025-02-06 00:00:00',0,'2025-10-22 01:51:34','2025-10-22 01:51:33','20251022_015131_06.02.25-Harnefer-PosFlop-Cbet_IP-Simplificacao_de_sizes.mp4','local',5),(12,'Short',NULL,'preflop',NULL,7,'2025-03-06 00:00:00',0,'2025-10-22 01:51:39','2025-10-22 01:51:39','20251022_015138_06.03.25-_Pseudo_Fruto_-PreFlop-_Short.mp4','local',5),(13,'Limp PKO',NULL,'preflop',NULL,8,'2025-05-09 00:00:00',0,'2025-10-22 01:52:02','2025-10-22 01:52:01','20251022_015200_09.05.25-LeoFranco-PreFlop-Limp_PKO.mp4','local',5),(14,'4-bet',NULL,'preflop',NULL,10,'2025-08-09 00:00:00',0,'2025-10-22 01:53:00','2025-10-22 01:52:59','20251022_015251_09.08.25-Jose_Lucas-PreFlop-4-bet.mp4','local',5),(15,'Explicando os spots mais_dificeis do ko',NULL,'preflop',NULL,7,'2025-03-10 00:00:00',0,'2025-10-22 01:53:18','2025-10-22 01:53:18','20251022_015317_10.03.25-Pseudo_Fruto-PreFlop-Explicando_os_spots_mais_dificeis_do_ko.mp4','local',5),(16,'Como jogar apos XR',NULL,'preflop',NULL,17,'1925-03-18 00:00:00',0,'2025-10-22 01:56:24','2025-10-22 01:56:23','20251022_015623_18.03.25_-Ruan_Bispo-Check-Raise_Not_PFR-PosFlop_-_Como_jogar_apos_XR.mp4','local',5);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `user_id` int NOT NULL,
  `class_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`class_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_class_id` (`class_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `particoes`
--

DROP TABLE IF EXISTS `particoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `particoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ativa` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `particoes`
--

LOCK TABLES `particoes` WRITE;
/*!40000 ALTER TABLE `particoes` DISABLE KEYS */;
INSERT INTO `particoes` (`id`, `nome`, `descricao`, `ativa`, `created_at`, `updated_at`) VALUES (1,'Dojo','Partição principal do Dojo',1,'2025-10-16 06:40:54','2025-10-16 19:11:18'),(2,'Coco','Partição secundária Coco',1,'2025-10-16 06:40:54','2025-10-16 19:11:18');
/*!40000 ALTER TABLE `particoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist_classes`
--

DROP TABLE IF EXISTS `playlist_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist_classes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playlist_id` int DEFAULT NULL,
  `class_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `playlist_classes_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist_classes`
--

LOCK TABLES `playlist_classes` WRITE;
/*!40000 ALTER TABLE `playlist_classes` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlist_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_database`
--

DROP TABLE IF EXISTS `student_database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_database` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `month` enum('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez') COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int NOT NULL,
  `file_url` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_size` int DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ativo',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_student_db_month_year` (`student_id`,`month`,`year`),
  CONSTRAINT `student_database_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_database`
--

LOCK TABLES `student_database` WRITE;
/*!40000 ALTER TABLE `student_database` DISABLE KEYS */;
INSERT INTO `student_database` (`id`, `student_id`, `month`, `year`, `file_url`, `file_size`, `status`, `created_at`, `updated_at`) VALUES (10,26,'jan',2025,'/api/uploads/databases/db_26_jan_2025_b64d6a85.zip',15478980,'deletado','2025-10-17 16:28:14','2025-10-18 00:26:26'),(11,26,'nov',2025,'/api/uploads/databases/db_26_nov_2025_c93675bd.zip',27,'deletado','2025-10-17 13:50:40','2025-10-17 16:56:40'),(12,26,'dez',2025,'/api/uploads/databases/db_26_dez_2025_f49db49f.zip',24,'deletado','2025-10-17 13:51:51','2025-10-17 16:57:52'),(13,26,'fev',2025,'/api/uploads/databases/db_26_fev_2025_2457b0b2.zip',15478980,'deletado','2025-10-18 00:25:57','2025-10-18 00:36:13'),(14,26,'abr',2025,'/api/uploads/databases/db_26_abr_2025_66d20f7f.zip',24,'deletado','2025-10-17 21:30:15','2025-10-18 00:36:17'),(15,26,'mar',2025,'/api/uploads/databases/db_26_mar_2025_833f9c65.zip',15478980,'deletado','2025-10-18 02:20:28','2025-10-18 02:57:24');
/*!40000 ALTER TABLE `student_database` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_graphs`
--

DROP TABLE IF EXISTS `student_graphs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_graphs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `month` enum('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez') NOT NULL,
  `year` int NOT NULL,
  `image_url` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_student_month_year` (`student_id`,`month`,`year`),
  CONSTRAINT `student_graphs_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_graphs`
--

LOCK TABLES `student_graphs` WRITE;
/*!40000 ALTER TABLE `student_graphs` DISABLE KEYS */;
INSERT INTO `student_graphs` (`id`, `student_id`, `month`, `year`, `image_url`, `created_at`, `updated_at`) VALUES (1,26,'jan',2025,'/api/uploads/graphs/graph_26_jan_2025_ac66cdf8.png','2025-10-16 21:47:55','2025-10-17 00:00:42'),(2,26,'fev',2025,'/api/uploads/graphs/graph_26_fev_2025_8894168d.png','2025-10-16 23:52:50','2025-10-16 23:52:50');
/*!40000 ALTER TABLE `student_graphs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_leaks`
--

DROP TABLE IF EXISTS `student_leaks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_leaks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `month` enum('jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez') NOT NULL,
  `year` int NOT NULL,
  `image_url` text NOT NULL,
  `improvements` text,
  `uploaded_by` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_student_leak_month_year` (`student_id`,`month`,`year`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `student_leaks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_leaks_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_leaks`
--

LOCK TABLES `student_leaks` WRITE;
/*!40000 ALTER TABLE `student_leaks` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_leaks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_progress`
--

DROP TABLE IF EXISTS `user_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_progress` (
  `user_id` int NOT NULL,
  `class_id` int NOT NULL,
  `progress` int NOT NULL DEFAULT '0',
  `watched` tinyint(1) NOT NULL DEFAULT '0',
  `last_watched` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `video_time` float NOT NULL DEFAULT '0',
  `completed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`class_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `user_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_progress_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_progress`
--

LOCK TABLES `user_progress` WRITE;
/*!40000 ALTER TABLE `user_progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(500) DEFAULT NULL,
  `type` enum('admin','student') NOT NULL DEFAULT 'student',
  `particao_id` int NOT NULL,
  `register_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `first_login` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `particao_id` (`particao_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`particao_id`) REFERENCES `particoes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `name`, `username`, `email`, `password_hash`, `type`, `particao_id`, `register_date`, `last_login`, `first_login`) VALUES (1,'Administrador','admin','admin@pokeracademy.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 06:40:54','2025-10-22 00:56:45',1),(2,'Cademito','Cademito','Cademito@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(3,'Carlos.rox','Carlos.rox','Carlos.rox@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(4,'Eiji','Eiji','Eiji@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(5,'Jonas','Jonas','Jonas@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(6,'Harnefer','Harnefer','Harnefer@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(7,'Pseudo Fruto','Pseudo Fruto','Pseudo.Fruto@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(8,'LeoFranco','LeoFranco','LeoFranco@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(9,'Badinha','Badinha','Badinha@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(10,'Jose Lucas','Jose Lucas','Jose.Lucas@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(11,'Nanatopai','Nanatopai','Nanatopai@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(12,'Luandods','Luandods','Luandods@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(13,'Lenon318','Lenon318','Lenon318@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(14,'Danton','Danton','Danton@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(15,'Jwolter','Jwolter','Jwolter@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(16,'Gabriel','Gabriel','Gabriel@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(17,'Ruan Bispo','Ruan Bispo','Ruan.Bispo@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(18,'Morfeu90','Morfeu90','Morfeu90@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(19,'Biguethi','Biguethi','Biguethi@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(20,'Tgrinder','Tgrinder','Tgrinder@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(21,'Quadskilla','Quadskilla','Quadskilla@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(22,'Kapirov','Kapirov','Kapirov@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(25,'Test User','testuser123','test@test.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 15:16:37',NULL,1),(26,'leandro','leandrokoles','Lekolesny@hotmail.com','pbkdf2:sha256:260000$cIa0e1tpsF65d1Uv$8366be3ff261803656ee5d64412bbd483e4e33c9d983846a1f9877d9ac29ccdc','student',1,'2025-10-16 18:25:40','2025-10-18 20:26:38',0),(27,'Teste Partição','teste_particao_1760639751','teste_1760639751@test.com','pbkdf2:sha256:260000$NSq4kRXSdbt7GO4p$4e2489184250eabe9c4a1b52b9178b76c33b0007679c5e7da930f2aa210b4c48','student',2,'2025-10-16 18:35:52',NULL,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-22  4:46:01
