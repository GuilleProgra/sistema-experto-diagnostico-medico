-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: sistema_experto
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Current Database: `sistema_experto`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `sistema_experto` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `sistema_experto`;

--
-- Table structure for table `cuadro_patologico`
--

DROP TABLE IF EXISTS `cuadro_patologico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuadro_patologico` (
  `id_relacion` int NOT NULL AUTO_INCREMENT,
  `id_enfermedad` int NOT NULL,
  `id_sintoma` int NOT NULL,
  `peso` int NOT NULL,
  `SUMA_TOTAL` int NOT NULL,
  `bandera` int DEFAULT '0',
  PRIMARY KEY (`id_relacion`),
  KEY `id_enfermedad` (`id_enfermedad`),
  KEY `id_sintoma` (`id_sintoma`),
  CONSTRAINT `cuadro_patologico_ibfk_1` FOREIGN KEY (`id_enfermedad`) REFERENCES `enfermedad` (`id_enfermedad`) ON DELETE CASCADE,
  CONSTRAINT `cuadro_patologico_ibfk_2` FOREIGN KEY (`id_sintoma`) REFERENCES `sintoma` (`id_sintoma`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuadro_patologico`
--

LOCK TABLES `cuadro_patologico` WRITE;
/*!40000 ALTER TABLE `cuadro_patologico` DISABLE KEYS */;
INSERT INTO `cuadro_patologico` VALUES (1,1,2,25,100,1),(2,1,3,30,100,0),(3,1,4,25,100,0),(4,1,5,20,100,0),(5,2,1,25,150,1),(6,2,8,25,150,0),(7,2,9,40,150,0),(8,2,10,60,150,0),(9,2,11,0,150,0),(10,3,1,25,120,1),(11,3,6,25,120,1),(12,3,12,40,120,0),(13,3,13,30,120,0),(14,4,13,30,100,0),(15,4,15,30,100,0),(16,4,16,20,100,0),(17,4,17,20,100,0),(18,5,18,30,100,0),(19,5,19,30,100,0),(20,5,20,20,100,0),(21,5,21,20,100,0),(22,6,23,25,100,0),(23,6,24,25,100,0),(24,6,25,20,100,0),(25,6,26,30,100,0),(26,7,27,40,100,0),(27,7,28,20,100,0),(28,7,29,20,100,0),(29,7,30,20,100,0),(30,8,14,30,100,0),(31,8,31,30,100,0),(32,8,32,20,100,0),(33,8,33,20,100,0),(34,9,34,35,100,0),(35,9,35,25,100,0),(36,9,36,20,100,0),(37,9,37,20,100,0),(38,10,2,20,100,1),(39,10,7,35,100,0),(40,10,14,20,100,0),(41,10,38,25,100,0),(42,11,1,25,100,1),(43,11,39,35,100,0),(44,11,40,25,100,0),(45,11,41,15,100,0),(46,12,28,15,100,0),(47,12,42,30,100,0),(48,12,43,25,100,0),(49,12,44,30,100,0),(50,13,8,25,100,0),(51,13,14,15,100,0),(52,13,45,30,100,0),(53,13,46,30,100,0),(54,14,2,20,120,1),(55,14,19,25,120,0),(56,14,47,30,120,0),(57,14,48,25,120,0),(58,15,14,25,100,0),(59,15,33,20,100,0),(60,15,49,25,100,0),(61,15,50,30,100,0),(64,14,49,20,120,0);
/*!40000 ALTER TABLE `cuadro_patologico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enfermedad`
--

DROP TABLE IF EXISTS `enfermedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enfermedad` (
  `id_enfermedad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_enfermedad`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enfermedad`
--

LOCK TABLES `enfermedad` WRITE;
/*!40000 ALTER TABLE `enfermedad` DISABLE KEYS */;
INSERT INTO `enfermedad` VALUES (1,'Gripe Com├║n','Infecci├│n viral que ataca el sistema respiratorio.','gripe.jpg'),(2,'Dengue','Enfermedad viral transmitida por mosquitos que provoca fiebre alta y dolor muscular.','dengue.jpg'),(3,'COVID-19','Enfermedad respiratoria aguda altamente contagiosa causada por el coronavirus SARS-CoV-2.','covid19.jpg'),(4,'Asma','Trastorno cr├│nico de las v├¡as respiratorias que causa dificultad para respirar.','asma.jpg'),(5,'Diabetes Tipo 2','Afecci├│n cr├│nica que afecta la forma en que el cuerpo procesa el az├║car en sangre.','diabetes.jpg'),(6,'Hipertensi├│n','Presi├│n arterial alta constante que puede derivar en problemas cardiovasculares.','hipertension.jpg'),(7,'Migra├▒a','Dolor de cabeza intenso y puls├ítil, a menudo acompa├▒ado de n├íuseas y sensibilidad a la luz.','migrana.jpg'),(8,'Anemia','Afecci├│n caracterizada por la falta de suficientes gl├│bulos rojos sanos.','anemia.jpg'),(9,'Gastritis','Inflamaci├│n del revestimiento del est├│mago, frecuentemente acompa├▒ada de ardor.','gastritis.jpg'),(10,'Bronquitis','Inflamaci├│n de los conductos bronquiales que transportan aire a los pulmones.','bronquitis.jpg'),(11,'Varicela','Infecci├│n viral muy contagiosa que provoca fiebre y una erupci├│n con peque├▒as ampollas con picaz├│n.','varicela.jpg'),(12,'Conjuntivitis','Inflamaci├│n o infecci├│n de la membrana transparente que recubre el p├írpado y el globo ocular.','conjuntivitis.jpg'),(13,'Artritis Reumatoide','Trastorno inflamatorio cr├│nico que afecta las articulaciones, causando dolor e hinchaz├│n.','artritis.jpg'),(14,'Infecci├│n Urinaria','Infecci├│n en cualquier parte del sistema urinario, frecuentemente en la vejiga o la uretra.','urinaria.jpg'),(15,'Hipotiroidismo','Afecci├│n en la que la gl├índula tiroides no produce suficientes hormonas tiroideas.','hipotiroidismo.jpg'),(16,'Gastroenteritis','Inflamaci├│n del revestimiento del est├│mago y los intestinos, causada por virus, bacterias o par├ísitos.',NULL);
/*!40000 ALTER TABLE `enfermedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sintoma`
--

DROP TABLE IF EXISTS `sintoma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sintoma` (
  `id_sintoma` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `imagen` varchar(255) DEFAULT 'default.png',
  PRIMARY KEY (`id_sintoma`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sintoma`
--

LOCK TABLES `sintoma` WRITE;
/*!40000 ALTER TABLE `sintoma` DISABLE KEYS */;
INSERT INTO `sintoma` VALUES (1,'Fiebre alta mayor a 38.5┬░C','fiebre_alta.jpg'),(2,'Fiebre moderada o febr├¡cula','default.png'),(3,'Congesti├│n o escurrimiento nasal','default.png'),(4,'Estornudos frecuentes','default.png'),(5,'Dolor e irritaci├│n de garganta','default.png'),(6,'Tos seca persistente','default.png'),(7,'Tos con flemas (productiva)','default.png'),(8,'Dolor muscular y de articulaciones severo (rompehuesos)','default.png'),(9,'Dolor detr├ís de los ojos (retroocular)','default.png'),(10,'Conteo bajo de plaquetas','default.png'),(11,'Escalofr├¡os constantes','default.png'),(12,'P├®rdida del olfato y del gusto (anosmia/ageusia)','default.png'),(13,'Dificultad para respirar o falta de aire (disnea)','default.png'),(14,'Fatiga o cansancio extremo','default.png'),(15,'Sibilancias (silbidos en el pecho al respirar)','default.png'),(16,'Opresi├│n en el pecho','default.png'),(17,'Tos que empeora por la noche o con el ejercicio','default.png'),(18,'Sed excesiva (polidipsia)','default.png'),(19,'Necesidad frecuente de orinar (poliuria)','default.png'),(20,'Hambre constante (polifagia)','default.png'),(21,'Visi├│n borrosa','default.png'),(22,'P├®rdida de peso inexplicable','default.png'),(23,'Zumbido en los o├¡dos (tinnitus)','default.png'),(24,'Mareos o v├®rtigo frecuente','default.png'),(25,'Sangrado nasal ocasional','default.png'),(26,'Dolor de cabeza en la nuca por las ma├▒anas','default.png'),(27,'Dolor de cabeza intenso y puls├ítil en un solo lado','default.png'),(28,'Sensibilidad extrema a la luz (fotofobia)','default.png'),(29,'Sensibilidad extrema al ruido (fonofobia)','default.png'),(30,'N├íuseas y v├│mitos','default.png'),(31,'Palidez en la piel y mucosas','default.png'),(32,'Manos y pies fr├¡os','default.png'),(33,'U├▒as quebradizas o d├®biles','default.png'),(34,'Ardor o dolor en la boca del est├│mago','default.png'),(35,'Acidez estomacal o reflujo','default.png'),(36,'Sensaci├│n de inflamaci├│n o llenura abdominal','default.png'),(37,'Eructos frecuentes e indigesti├│n','default.png'),(38,'Molestia en el pecho al toser','default.png'),(39,'Erupci├│n en la piel con peque├▒as ampollas y picaz├│n','default.png'),(40,'Costras en la piel tras romperse las ampollas','default.png'),(41,'P├®rdida de apetito','default.png'),(42,'Enrojecimiento en la parte blanca del ojo','default.png'),(43,'Lagrimeo constante y picaz├│n ocular','default.png'),(44,'Secreci├│n ocular (laga├▒as) que pega las pesta├▒as','default.png'),(45,'Hinchaz├│n y calor en las articulaciones','default.png'),(46,'Rigidez articular matutina','default.png'),(47,'Ardor o dolor al orinar (disuria)','default.png'),(48,'Orina turbia o con olor fuerte','default.png'),(49,'Intolerancia al fr├¡o','default.png'),(50,'Aumento de peso inexplicable y piel seca','default.png'),(51,'Diarrea l├¡quida frecuente','default.png'),(52,'C├│licos y retortijones intensos','default.png');
/*!40000 ALTER TABLE `sintoma` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-19 18:12:35
