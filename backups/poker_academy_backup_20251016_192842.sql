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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_views`
--

LOCK TABLES `class_views` WRITE;
/*!40000 ALTER TABLE `class_views` DISABLE KEYS */;
INSERT INTO `class_views` VALUES (1,26,1,'2025-10-16 20:08:47','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(2,26,1,'2025-10-16 20:09:07','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(3,26,1,'2025-10-16 20:19:39','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(4,26,1,'2025-10-16 20:20:01','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(5,26,1,'2025-10-16 20:29:56','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(6,26,1,'2025-10-16 20:36:38','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(7,26,1,'2025-10-16 20:37:10','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(8,26,1,'2025-10-16 20:37:31','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(9,26,1,'2025-10-16 20:37:58','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(10,26,1,'2025-10-16 20:38:12','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(11,26,1,'2025-10-16 20:43:45','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(12,26,1,'2025-10-16 20:44:29','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(13,26,1,'2025-10-16 20:45:01','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(14,26,1,'2025-10-16 20:56:47','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(15,26,1,'2025-10-16 20:57:08','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(16,26,1,'2025-10-16 21:02:40','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(17,26,1,'2025-10-16 21:03:00','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(18,26,1,'2025-10-16 21:08:24','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(19,26,1,'2025-10-16 21:08:46','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(20,26,1,'2025-10-16 21:09:07','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),(21,26,1,'2025-10-16 21:31:20','189.4.110.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'Teste de Upload',NULL,'preflop','https://www.youtube.com/watch?v=GAoR9ji8D6A',1,'2025-10-16 00:00:00',21,'2025-10-16 14:43:00','2025-10-16 21:31:20','20251016_182336_BW_SB_raised_40bb.mp4','local',5),(2,'Estratégias Pré-Flop',NULL,'preflop','https://www.youtube.com/watch?v=v3QzLjFLzd4',1,'2025-10-16 14:43:00',0,'2025-10-16 14:43:00','2025-10-16 16:11:56',NULL,'local',5),(3,'Estratégias Pós-Flop',NULL,'postflop','https://www.youtube.com/watch?v=v3QzLjFLzd4',1,'2025-10-16 14:43:00',0,'2025-10-16 14:43:00','2025-10-16 16:11:56',NULL,'local',5),(4,'Psicologia no Poker','Controle emocional e mentalidade','mental','https://www.youtube.com/watch?v=8wqw2H5U7Qs',1,'2025-10-16 14:43:00',0,'2025-10-16 14:43:00','2025-10-16 14:43:00',NULL,'local',5),(5,'ICM - Independent Chip Model',NULL,'icm','https://www.youtube.com/watch?v=ZJJ4PZ3eoNs',1,'2025-10-16 14:43:00',0,'2025-10-16 14:43:00','2025-10-16 16:11:56',NULL,'local',5);
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
INSERT INTO `favorites` VALUES (26,1);
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
INSERT INTO `particoes` VALUES (1,'Dojo','Partição principal do Dojo',1,'2025-10-16 06:40:54','2025-10-16 19:11:18'),(2,'Coco','Partição secundária Coco',1,'2025-10-16 06:40:54','2025-10-16 19:11:18');
/*!40000 ALTER TABLE `particoes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_graphs`
--

LOCK TABLES `student_graphs` WRITE;
/*!40000 ALTER TABLE `student_graphs` DISABLE KEYS */;
INSERT INTO `student_graphs` VALUES (1,26,'jan',2025,'/api/uploads/graphs/graph_26_jan_2025_d8837b3b.png','2025-10-16 21:47:55','2025-10-16 22:16:09');
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
INSERT INTO `user_progress` VALUES (26,1,47,0,'2025-10-16 21:31:24',2102.91,NULL,'2025-10-16 19:53:36','2025-10-16 21:31:24');
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
INSERT INTO `users` VALUES (1,'Administrador','admin','admin@pokeracademy.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 06:40:54','2025-10-16 21:59:27',1),(2,'Cademito','Cademito','Cademito@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(3,'Carlos.rox','Carlos.rox','Carlos.rox@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(4,'Eiji','Eiji','Eiji@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(5,'Jonas','Jonas','Jonas@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(6,'Harnefer','Harnefer','Harnefer@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(7,'Pseudo Fruto','Pseudo Fruto','Pseudo.Fruto@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(8,'LeoFranco','LeoFranco','LeoFranco@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(9,'Badinha','Badinha','Badinha@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(10,'Jose Lucas','Jose Lucas','Jose.Lucas@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(11,'Nanatopai','Nanatopai','Nanatopai@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(12,'Luandods','Luandods','Luandods@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(13,'Lenon318','Lenon318','Lenon318@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(14,'Danton','Danton','Danton@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(15,'Jwolter','Jwolter','Jwolter@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(16,'Gabriel','Gabriel','Gabriel@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(17,'Ruan Bispo','Ruan Bispo','Ruan.Bispo@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(18,'Morfeu90','Morfeu90','Morfeu90@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(19,'Biguethi','Biguethi','Biguethi@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(20,'Tgrinder','Tgrinder','Tgrinder@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(21,'Quadskilla','Quadskilla','Quadskilla@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(22,'Kapirov','Kapirov','Kapirov@gmail.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 14:42:03',NULL,1),(25,'Test User','testuser123','test@test.com','pbkdf2:sha256:260000$q4dWV5q3QhkFoGVQ$9018ffa684d8b2379e88932a2a16e1379fc5365d2deada52ed294a6b913256e8','admin',1,'2025-10-16 15:16:37',NULL,1),(26,'leandro','leandrokoles','Lekolesny@hotmail.com','pbkdf2:sha256:260000$cIa0e1tpsF65d1Uv$8366be3ff261803656ee5d64412bbd483e4e33c9d983846a1f9877d9ac29ccdc','student',1,'2025-10-16 18:25:40','2025-10-16 21:44:41',0),(27,'Teste Partição','teste_particao_1760639751','teste_1760639751@test.com','pbkdf2:sha256:260000$NSq4kRXSdbt7GO4p$4e2489184250eabe9c4a1b52b9178b76c33b0007679c5e7da930f2aa210b4c48','student',2,'2025-10-16 18:35:52',NULL,1);
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

-- Dump completed on 2025-10-16 22:28:43
