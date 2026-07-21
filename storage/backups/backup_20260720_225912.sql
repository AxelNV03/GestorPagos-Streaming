/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: db    Database: streaming
-- ------------------------------------------------------
-- Server version	12.2.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `cobros`
--

DROP TABLE IF EXISTS `cobros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cobros` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_plataforma_id` int(11) NOT NULL,
  `comprobante_id` int(11) DEFAULT NULL,
  `mes_anio` date NOT NULL,
  `monto_deuda` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','pagado') DEFAULT 'pendiente',
  `motivo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_plataforma_id` (`usuario_plataforma_id`),
  KEY `comprobante_id` (`comprobante_id`),
  CONSTRAINT `1` FOREIGN KEY (`usuario_plataforma_id`) REFERENCES `plataforma_usuario` (`id`) ON DELETE CASCADE,
  CONSTRAINT `2` FOREIGN KEY (`comprobante_id`) REFERENCES `comprobantes` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobros`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `cobros` WRITE;
/*!40000 ALTER TABLE `cobros` DISABLE KEYS */;
INSERT INTO `cobros` VALUES
(48,20,14,'2026-07-01',55.00,'pagado','Mensualidad - Netflix Premium (Julio 2026)'),
(49,21,15,'2026-07-01',30.00,'pagado','Mensualidad - Spotify Familiar (Julio 2026)'),
(50,20,NULL,'2026-08-01',55.00,'pendiente','Mensualidad - Netflix Premium (August 2026)'),
(52,22,16,'2026-07-01',217.00,'pagado','Mensualidad - Microsoft 365 Family (Julio 2026)'),
(53,22,16,'2026-08-01',217.00,'pagado','Mensualidad - Microsoft 365 Family (August 2026)'),
(55,23,18,'2026-07-01',24.00,'pagado','Mensualidad - Vix Premium (Julio 2026)'),
(56,24,18,'2026-07-01',30.00,'pagado','Mensualidad - Deezer Family (Julio 2026)'),
(58,23,NULL,'2026-08-01',24.00,'pendiente','Mensualidad - Vix Premium (Agosto 2026)'),
(59,25,19,'2026-07-01',32.00,'pagado','Mensualidad - YouTube Premium (Julio 2026)'),
(60,25,NULL,'2026-08-01',32.00,'pendiente','Mensualidad - YouTube Premium (Agosto 2026)'),
(62,26,21,'2026-07-01',50.00,'pagado','Mensualidad - Canva Pro (Julio 2026)'),
(63,27,NULL,'2026-07-01',55.00,'pendiente','Mensualidad - Netflix Premium (Julio 2026)'),
(64,26,21,'2026-08-01',50.00,'pagado','Mensualidad - Canva Pro (Agosto 2026)'),
(65,26,21,'2026-09-01',50.00,'pagado','Mensualidad - Canva Pro (Septiembre 2026)'),
(66,26,21,'2026-10-01',50.00,'pagado','Mensualidad - Canva Pro (Octubre 2026)'),
(67,26,NULL,'2026-11-01',50.00,'pendiente','Mensualidad - Canva Pro (Noviembre 2026)'),
(68,28,NULL,'2026-07-01',25.00,'pendiente','Mensualidad - Apple TV Plus (Julio 2026)');
/*!40000 ALTER TABLE `cobros` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `comprobantes`
--

DROP TABLE IF EXISTS `comprobantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comprobantes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `ruta_archivo` varchar(255) NOT NULL,
  `nota_usuario` text DEFAULT NULL,
  `motivo_rechazo` text DEFAULT NULL,
  `comentario` text DEFAULT NULL,
  `estado` enum('revision','aprobado','rechazado') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comprobantes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `comprobantes` WRITE;
/*!40000 ALTER TABLE `comprobantes` DISABLE KEYS */;
INSERT INTO `comprobantes` VALUES
(14,8,'8/adan_ortiz_20260720_033650_aprobado.jpg','CHILL',NULL,NULL,'aprobado','2026-07-20 03:36:50'),
(15,8,'8/adan_ortiz_20260720_034651_aprobado.png','SEIO',NULL,NULL,'aprobado','2026-07-20 03:46:51'),
(16,8,'8/adan_ortiz_20260720_042811_aprobado.png','TIDAL',NULL,NULL,'aprobado','2026-07-20 04:28:11'),
(18,8,'8/adan_ortiz_20260720_180632_aprobado.png','Siu',NULL,NULL,'aprobado','2026-07-20 18:06:32'),
(19,8,'8/adan_ortiz_20260720_181319_aprobado.png','spo',NULL,NULL,'aprobado','2026-07-20 18:13:19'),
(21,8,'8/adan_ortiz_20260720_195526_aprobado.png','PRobando',NULL,'El pago coincide perfectamente con el cargo del periodo.','aprobado','2026-07-20 19:55:26'),
(25,8,'8/adan_ortiz_20260720_215031_rechazado.png','Prisiclla','PRisicla probando\r\n',NULL,'rechazado','2026-07-20 21:50:31'),
(26,8,'8/adan_ortiz_20260720_215119_rechazado.jpeg','hhdhss','Nomas por que si ',NULL,'rechazado','2026-07-20 21:51:19');
/*!40000 ALTER TABLE `comprobantes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `plataforma_usuario`
--

DROP TABLE IF EXISTS `plataforma_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `plataforma_usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `plataforma_id` int(11) NOT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `correo_plataforma` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_usuario_plataforma` (`usuario_id`,`plataforma_id`),
  KEY `plataforma_id` (`plataforma_id`),
  CONSTRAINT `1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `2` FOREIGN KEY (`plataforma_id`) REFERENCES `plataformas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plataforma_usuario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `plataforma_usuario` WRITE;
/*!40000 ALTER TABLE `plataforma_usuario` DISABLE KEYS */;
INSERT INTO `plataforma_usuario` VALUES
(20,8,31,'2026-07-19',1,'netflixprueba@gmail.com'),
(21,8,32,'2026-07-19',0,NULL),
(22,8,43,'2026-07-20',1,''),
(23,8,41,'2026-07-19',1,''),
(24,8,45,'2026-07-20',1,''),
(25,8,37,'2026-07-20',1,'ytpremiun@s.com'),
(26,8,42,'2026-07-20',1,''),
(27,9,31,'2026-07-20',1,''),
(28,8,40,'2026-07-20',1,'appel.tv@tv.com');
/*!40000 ALTER TABLE `plataforma_usuario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `plataformas`
--

DROP TABLE IF EXISTS `plataformas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `plataformas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio_total` decimal(10,2) NOT NULL,
  `cuota` decimal(10,2) DEFAULT NULL,
  `dia_cobro` int(11) DEFAULT NULL,
  `url_logo` varchar(255) DEFAULT NULL,
  `correo_admin` varchar(255) NOT NULL,
  `max_cupos` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plataformas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `plataformas` WRITE;
/*!40000 ALTER TABLE `plataformas` DISABLE KEYS */;
INSERT INTO `plataformas` VALUES
(31,'Netflix Premium',329.00,55.00,5,'netflix.png','admin@streaming.com',5),
(32,'Spotify Familiar',179.00,30.00,10,'spotify.png','admin@streaming.com',5),
(33,'Disney Plus',249.00,42.00,8,'disney.png','admin@streaming.com',5),
(34,'Max',199.00,35.00,15,'max.png','admin@streaming.com',5),
(35,'Prime Video',99.00,20.00,12,'primevideo.png','admin@streaming.com',5),
(36,'Crunchyroll Mega Fan',149.00,30.00,18,'crunchyroll.png','admin@streaming.com',5),
(37,'YouTube Premium',159.00,32.00,20,'youtubepremium.png','admin@streaming.com',5),
(38,'Paramount Plus',179.00,30.00,7,'paramount.png','admin@streaming.com',5),
(39,'Apple Music Familiar',199.00,35.00,25,'applemusic.png','admin@streaming.com',6),
(40,'Apple TV Plus',129.00,25.00,4,'appletv.png','admin@streaming.com',5),
(41,'Vix Premium',119.00,24.00,11,'vix.png','admin@streaming.com',5),
(42,'Canva Pro',300.00,50.00,9,'canva.png','admin@streaming.com',5),
(43,'Microsoft 365 Family',1299.00,217.00,1,'office365.png','admin@streaming.com',5),
(44,'ChatGPT Plus',400.00,80.00,14,'chatgpt.png','admin@streaming.com',5),
(45,'Deezer Family',179.00,30.00,22,'deezer.png','admin@streaming.com',5);
/*!40000 ALTER TABLE `plataformas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) NOT NULL,
  `apeP` varchar(100) NOT NULL,
  `apeM` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `rol` enum('admin','no_admin') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES
(8,'ADAN','ORTIZ','MARTINEZ','1234567890','a@a.com','no_admin','2026-07-20 03:36:33'),
(9,'DEBHANNI ATXUL','MORALES','OSORIO','0987654321','a@a.com1','no_admin','2026-07-20 18:49:48');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-07-20 22:59:12
