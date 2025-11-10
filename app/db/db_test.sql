CREATE DATABASE  IF NOT EXISTS `inventario_pastenplast` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `inventario_pastenplast`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: inventario_pastenplast
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area` (
  `cod_area` int NOT NULL AUTO_INCREMENT,
  `area` varchar(75) NOT NULL,
  PRIMARY KEY (`cod_area`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `autorizacion`
--

DROP TABLE IF EXISTS `autorizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autorizacion` (
  `cod_autori` int NOT NULL AUTO_INCREMENT,
  `Recurso_cod_recurso` int NOT NULL,
  `Rol_cod_rol` int NOT NULL,
  `Permiso_cod_permiso` int NOT NULL,
  `acceso` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_autori`),
  KEY `Autorizacion_Permiso` (`Permiso_cod_permiso`),
  KEY `Autorizacion_Recurso` (`Recurso_cod_recurso`),
  KEY `Autorizacion_Rol` (`Rol_cod_rol`),
  CONSTRAINT `Autorizacion_Permiso` FOREIGN KEY (`Permiso_cod_permiso`) REFERENCES `permiso` (`cod_permiso`),
  CONSTRAINT `Autorizacion_Recurso` FOREIGN KEY (`Recurso_cod_recurso`) REFERENCES `recurso` (`cod_recurso`),
  CONSTRAINT `Autorizacion_Rol` FOREIGN KEY (`Rol_cod_rol`) REFERENCES `rol` (`cod_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cargo`
--

DROP TABLE IF EXISTS `cargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargo` (
  `cod_cargo` int NOT NULL AUTO_INCREMENT,
  `cargo` varchar(45) NOT NULL,
  `detalle` varchar(100) DEFAULT NULL,
  `Area_cod_area` int NOT NULL,
  `dependencia` varchar(255) DEFAULT NULL,
  `puestos_cargo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cod_cargo`),
  KEY `Cargo_Area` (`Area_cod_area`),
  CONSTRAINT `Cargo_Area` FOREIGN KEY (`Area_cod_area`) REFERENCES `area` (`cod_area`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `cod_catg` int NOT NULL AUTO_INCREMENT,
  `categoria` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_catg`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciudad` (
  `cod_ciudad` int NOT NULL AUTO_INCREMENT,
  `ciudad` varchar(45) NOT NULL,
  `Pais_cod_pais` int NOT NULL,
  PRIMARY KEY (`cod_ciudad`),
  KEY `Ciudad_Pais` (`Pais_cod_pais`),
  CONSTRAINT `Ciudad_Pais` FOREIGN KEY (`Pais_cod_pais`) REFERENCES `pais` (`cod_pais`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `cod_cli` int NOT NULL AUTO_INCREMENT,
  `nit` varchar(20) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(25) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `fecha_nac` date DEFAULT NULL,
  `image` mediumblob,
  `Ciudad_cod_ciudad` int NOT NULL,
  `empresa` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_cli`),
  KEY `Cliente_Ciudad` (`Ciudad_cod_ciudad`),
  CONSTRAINT `Cliente_Ciudad` FOREIGN KEY (`Ciudad_cod_ciudad`) REFERENCES `ciudad` (`cod_ciudad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `compra_envase`
--

DROP TABLE IF EXISTS `compra_envase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra_envase` (
  `cod_comE` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `cantidad` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `OrdenCompra_cod_ordC` int NOT NULL,
  `Envase_cod_env` int NOT NULL,
  PRIMARY KEY (`cod_comE`),
  KEY `Compra_Envase_Envase` (`Envase_cod_env`),
  KEY `Compra_Envase_OrdenCompra` (`OrdenCompra_cod_ordC`),
  CONSTRAINT `Compra_Envase_Envase` FOREIGN KEY (`Envase_cod_env`) REFERENCES `envase` (`cod_env`),
  CONSTRAINT `Compra_Envase_OrdenCompra` FOREIGN KEY (`OrdenCompra_cod_ordC`) REFERENCES `ordencompra` (`cod_ordC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `compra_mp`
--

DROP TABLE IF EXISTS `compra_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra_mp` (
  `cod_comP` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `cantidad` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `OrdenCompra_cod_ordC` int NOT NULL,
  `MateriaP_cod_mp` int NOT NULL,
  PRIMARY KEY (`cod_comP`),
  KEY `Compra_MP_MateriaP` (`MateriaP_cod_mp`),
  KEY `Compra_MP_OrdenCompra` (`OrdenCompra_cod_ordC`),
  CONSTRAINT `Compra_MP_MateriaP` FOREIGN KEY (`MateriaP_cod_mp`) REFERENCES `materia_prima` (`cod_mp`),
  CONSTRAINT `Compra_MP_OrdenCompra` FOREIGN KEY (`OrdenCompra_cod_ordC`) REFERENCES `ordencompra` (`cod_ordC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuenta`
--

DROP TABLE IF EXISTS `cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuenta` (
  `cod_cu` int NOT NULL AUTO_INCREMENT,
  `username` varchar(75) NOT NULL,
  `password` mediumtext NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `Rol_cod_rol` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  PRIMARY KEY (`cod_cu`),
  KEY `Cuenta_Empleado` (`Empleado_cod_emp`),
  KEY `Cuenta_Rol` (`Rol_cod_rol`),
  CONSTRAINT `Cuenta_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Cuenta_Rol` FOREIGN KEY (`Rol_cod_rol`) REFERENCES `rol` (`cod_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuenta_por_cobrar`
--

DROP TABLE IF EXISTS `cuenta_por_cobrar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuenta_por_cobrar` (
  `cod_cobrar` int NOT NULL AUTO_INCREMENT,
  `saldo` decimal(15,2) NOT NULL,
  `Cliente_cod_cli` int NOT NULL,
  `Estado_Cuenta_Cobrar_cod_est_cc` int NOT NULL,
  PRIMARY KEY (`cod_cobrar`),
  KEY `CuentaPorCobrar_Cliente` (`Cliente_cod_cli`),
  KEY `Cuenta_Por_Cobrar_Estado_Cuenta_Cobrar` (`Estado_Cuenta_Cobrar_cod_est_cc`),
  CONSTRAINT `Cuenta_Por_Cobrar_Estado_Cuenta_Cobrar` FOREIGN KEY (`Estado_Cuenta_Cobrar_cod_est_cc`) REFERENCES `estado_cuenta_cobrar` (`cod_est_cc`),
  CONSTRAINT `CuentaPorCobrar_Cliente` FOREIGN KEY (`Cliente_cod_cli`) REFERENCES `cliente` (`cod_cli`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devolucion`
--

DROP TABLE IF EXISTS `devolucion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devolucion` (
  `cod_devolucion` int NOT NULL AUTO_INCREMENT,
  `Recibo_cod_vent` int NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`cod_devolucion`),
  KEY `Devolucion_Recibo` (`Recibo_cod_vent`),
  CONSTRAINT `Devolucion_Recibo` FOREIGN KEY (`Recibo_cod_vent`) REFERENCES `recibo` (`cod_vent`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `embolsado`
--

DROP TABLE IF EXISTS `embolsado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `embolsado` (
  `cod_emb` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `cantidad` int NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  PRIMARY KEY (`cod_emb`),
  KEY `Embolsado_Empleado` (`Empleado_cod_emp`),
  KEY `Embolsado_Producto` (`Producto_cod_prod`),
  CONSTRAINT `Embolsado_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Embolsado_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Productos que necesitan embolsado aparte de la producción (Cubiertos)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `cod_emp` int NOT NULL AUTO_INCREMENT,
  `ci` varchar(20) DEFAULT NULL,
  `nombre` varchar(50) NOT NULL,
  `a_paterno` varchar(45) NOT NULL,
  `a_materno` varchar(45) DEFAULT NULL,
  `telefono` varchar(25) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `fecha_nac` date DEFAULT NULL,
  `fecha_ini` date DEFAULT NULL,
  `image` mediumblob,
  `Ciudad_cod_ciudad` int NOT NULL,
  `Estado_Empleado_cod_estEmp` int NOT NULL,
  `Cargo_cod_cargo` int NOT NULL,
  PRIMARY KEY (`cod_emp`),
  KEY `Empleado_Cargo` (`Cargo_cod_cargo`),
  KEY `Empleado_Ciudad` (`Ciudad_cod_ciudad`),
  KEY `Empleado_Estado_Empleado` (`Estado_Empleado_cod_estEmp`),
  CONSTRAINT `Empleado_Cargo` FOREIGN KEY (`Cargo_cod_cargo`) REFERENCES `cargo` (`cod_cargo`),
  CONSTRAINT `Empleado_Ciudad` FOREIGN KEY (`Ciudad_cod_ciudad`) REFERENCES `ciudad` (`cod_ciudad`),
  CONSTRAINT `Empleado_Estado_Empleado` FOREIGN KEY (`Estado_Empleado_cod_estEmp`) REFERENCES `estado_empleado` (`cod_estEmp`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresa` (
  `cod_emp` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(150) NOT NULL,
  `Fecha` date NOT NULL,
  `Logo` tinyint(1) NOT NULL,
  `Direccion` varchar(60) NOT NULL,
  PRIMARY KEY (`cod_emp`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `envase`
--

DROP TABLE IF EXISTS `envase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `envase` (
  `cod_env` int NOT NULL AUTO_INCREMENT,
  `envase` varchar(45) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `image` blob NOT NULL,
  `precio` decimal(8,2) NOT NULL,
  `Unidad_cod_unidad` int NOT NULL,
  PRIMARY KEY (`cod_env`),
  KEY `Envase_Unidad` (`Unidad_cod_unidad`),
  CONSTRAINT `Envase_Unidad` FOREIGN KEY (`Unidad_cod_unidad`) REFERENCES `unidad` (`cod_unidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_cuenta_cobrar`
--

DROP TABLE IF EXISTS `estado_cuenta_cobrar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_cuenta_cobrar` (
  `cod_est_cc` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(55) NOT NULL,
  PRIMARY KEY (`cod_est_cc`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_empleado`
--

DROP TABLE IF EXISTS `estado_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_empleado` (
  `cod_estEmp` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_estEmp`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_maquina`
--

DROP TABLE IF EXISTS `estado_maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_maquina` (
  `cod_estMaq` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_estMaq`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_materia_prima`
--

DROP TABLE IF EXISTS `estado_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_materia_prima` (
  `cod_est_mp` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(55) NOT NULL,
  PRIMARY KEY (`cod_est_mp`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_producto`
--

DROP TABLE IF EXISTS `estado_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_producto` (
  `cod_estProd` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_estProd`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_recepcion`
--

DROP TABLE IF EXISTS `estado_recepcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_recepcion` (
  `cod_estRep` int NOT NULL AUTO_INCREMENT,
  `estado` int NOT NULL,
  PRIMARY KEY (`cod_estRep`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_recibo`
--

DROP TABLE IF EXISTS `estado_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_recibo` (
  `cod_estVen` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_estVen`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `falta_empleado`
--

DROP TABLE IF EXISTS `falta_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `falta_empleado` (
  `cod_falta` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`cod_falta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flujo_cuenta`
--

DROP TABLE IF EXISTS `flujo_cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flujo_cuenta` (
  `cod_fc` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `Recibo_Venta_cod_vent` int DEFAULT NULL,
  `Pagos_cod_pago` int DEFAULT NULL,
  `saldo` decimal(15,2) NOT NULL,
  `Cuenta_Por_Cobrar_cod_cobrar` int NOT NULL,
  PRIMARY KEY (`cod_fc`),
  KEY `Flujo_Cuentas_Cuenta_Por_Cobrar` (`Cuenta_Por_Cobrar_cod_cobrar`),
  KEY `Flujo_Cuentas_Pagos` (`Pagos_cod_pago`),
  KEY `Flujo_Cuentas_Recibo_Venta` (`Recibo_Venta_cod_vent`),
  CONSTRAINT `Flujo_Cuentas_Cuenta_Por_Cobrar` FOREIGN KEY (`Cuenta_Por_Cobrar_cod_cobrar`) REFERENCES `cuenta_por_cobrar` (`cod_cobrar`),
  CONSTRAINT `Flujo_Cuentas_Pagos` FOREIGN KEY (`Pagos_cod_pago`) REFERENCES `pagos` (`cod_pago`),
  CONSTRAINT `Flujo_Cuentas_Recibo_Venta` FOREIGN KEY (`Recibo_Venta_cod_vent`) REFERENCES `recibo_venta` (`cod_vent`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flujo_inventario_e`
--

DROP TABLE IF EXISTS `flujo_inventario_e`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flujo_inventario_e` (
  `cod_FI_e` int NOT NULL AUTO_INCREMENT,
  `movimiento` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` date NOT NULL,
  `detalle` varchar(255) NOT NULL,
  `Envase_cod_env` int NOT NULL,
  `ajuste` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_FI_e`),
  KEY `Flujo_Inventario_E_Envase` (`Envase_cod_env`),
  CONSTRAINT `Flujo_Inventario_E_Envase` FOREIGN KEY (`Envase_cod_env`) REFERENCES `envase` (`cod_env`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flujo_inventario_mp`
--

DROP TABLE IF EXISTS `flujo_inventario_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flujo_inventario_mp` (
  `cod_FI_mp` int NOT NULL AUTO_INCREMENT,
  `movimiento` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` int NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `Materia_Prima_cod_mp` int NOT NULL,
  `ajuste` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_FI_mp`),
  KEY `Flujo_Inventario_MP_Materia_Prima` (`Materia_Prima_cod_mp`),
  CONSTRAINT `Flujo_Inventario_MP_Materia_Prima` FOREIGN KEY (`Materia_Prima_cod_mp`) REFERENCES `materia_prima` (`cod_mp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flujo_inventario_productos`
--

DROP TABLE IF EXISTS `flujo_inventario_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flujo_inventario_productos` (
  `cod_FI_prod` int NOT NULL AUTO_INCREMENT,
  `Producto_cod_prod` int NOT NULL,
  `movimiento` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` date NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `ajuste` tinyint(1) NOT NULL,
  `Produccion_Planta_cod_prod_planta` int DEFAULT NULL,
  `Recibo_Venta_cod_vent` int DEFAULT NULL,
  `Embolsado_cod_emb` int DEFAULT NULL,
  `devolucion` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_FI_prod`),
  KEY `Flujo_Inventario_Producto` (`Producto_cod_prod`),
  KEY `Flujo_Inventario_Productos_Embolsado` (`Embolsado_cod_emb`),
  KEY `Flujo_Inventario_Productos_Produccion_Planta` (`Produccion_Planta_cod_prod_planta`),
  KEY `Flujo_Inventario_Productos_Recibo_Venta` (`Recibo_Venta_cod_vent`),
  CONSTRAINT `Flujo_Inventario_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`),
  CONSTRAINT `Flujo_Inventario_Productos_Embolsado` FOREIGN KEY (`Embolsado_cod_emb`) REFERENCES `embolsado` (`cod_emb`),
  CONSTRAINT `Flujo_Inventario_Productos_Produccion_Planta` FOREIGN KEY (`Produccion_Planta_cod_prod_planta`) REFERENCES `produccion_planta` (`cod_prod_planta`),
  CONSTRAINT `Flujo_Inventario_Productos_Recibo_Venta` FOREIGN KEY (`Recibo_Venta_cod_vent`) REFERENCES `recibo_venta` (`cod_vent`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forma_pago`
--

DROP TABLE IF EXISTS `forma_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forma_pago` (
  `cod_fp` int NOT NULL AUTO_INCREMENT,
  `forma_pago` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_fp`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_inventario_envase`
--

DROP TABLE IF EXISTS `h_inventario_envase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `h_inventario_envase` (
  `cod_invE` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `fecha` date NOT NULL,
  `Envase_cod_env` int NOT NULL,
  PRIMARY KEY (`cod_invE`),
  KEY `H_Inventario_Envase_Envase` (`Envase_cod_env`),
  CONSTRAINT `H_Inventario_Envase_Envase` FOREIGN KEY (`Envase_cod_env`) REFERENCES `envase` (`cod_env`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_inventario_mp`
--

DROP TABLE IF EXISTS `h_inventario_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `h_inventario_mp` (
  `cod_invMP` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `fecha` date NOT NULL,
  `Materia_Prima_cod_mp` int NOT NULL,
  PRIMARY KEY (`cod_invMP`),
  KEY `H_Inventario_MP_Materia_Prima` (`Materia_Prima_cod_mp`),
  CONSTRAINT `H_Inventario_MP_Materia_Prima` FOREIGN KEY (`Materia_Prima_cod_mp`) REFERENCES `materia_prima` (`cod_mp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_inventario_productos`
--

DROP TABLE IF EXISTS `h_inventario_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `h_inventario_productos` (
  `cod_invPH` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `fecha` date NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  PRIMARY KEY (`cod_invPH`),
  KEY `H_Inventario_Productos_Producto` (`Producto_cod_prod`),
  CONSTRAINT `H_Inventario_Productos_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventario_envase`
--

DROP TABLE IF EXISTS `inventario_envase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_envase` (
  `cod_invE` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `fecha` date NOT NULL,
  `Envase_cod_env` int NOT NULL,
  PRIMARY KEY (`cod_invE`),
  KEY `InventarioE_Envase` (`Envase_cod_env`),
  CONSTRAINT `InventarioE_Envase` FOREIGN KEY (`Envase_cod_env`) REFERENCES `envase` (`cod_env`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventario_mp`
--

DROP TABLE IF EXISTS `inventario_mp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_mp` (
  `cod_invMP` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `fecha` date NOT NULL,
  `MateriaP_cod_mp` int NOT NULL,
  PRIMARY KEY (`cod_invMP`),
  KEY `InventarioMP_MateriaP` (`MateriaP_cod_mp`),
  CONSTRAINT `InventarioMP_MateriaP` FOREIGN KEY (`MateriaP_cod_mp`) REFERENCES `materia_prima` (`cod_mp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventario_productos`
--

DROP TABLE IF EXISTS `inventario_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_productos` (
  `cod_invP` int NOT NULL AUTO_INCREMENT,
  `stock` int NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`cod_invP`),
  KEY `InventarioP_Producto` (`Producto_cod_prod`),
  CONSTRAINT `InventarioP_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mantenimiento`
--

DROP TABLE IF EXISTS `mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mantenimiento` (
  `cod_man` int NOT NULL AUTO_INCREMENT,
  `detalle` varchar(150) NOT NULL,
  `fecha_ini` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `Maquina_cod_maq` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  PRIMARY KEY (`cod_man`),
  KEY `Mantenimiento_Empleado` (`Empleado_cod_emp`),
  KEY `Mantenimiento_Maquina` (`Maquina_cod_maq`),
  CONSTRAINT `Mantenimiento_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Mantenimiento_Maquina` FOREIGN KEY (`Maquina_cod_maq`) REFERENCES `maquina` (`cod_maq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `maquina`
--

DROP TABLE IF EXISTS `maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maquina` (
  `cod_maq` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(30) NOT NULL,
  `maquina` varchar(45) NOT NULL,
  `fecha` date DEFAULT NULL,
  `Tipo_Maq_cod_tm` int NOT NULL,
  `image` mediumblob,
  `Estado_Maquina_cod_estMaq` int NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cod_maq`),
  KEY `Maquina_Estado_Maquina` (`Estado_Maquina_cod_estMaq`),
  KEY `Maquina_Tipo_Maq` (`Tipo_Maq_cod_tm`),
  CONSTRAINT `Maquina_Estado_Maquina` FOREIGN KEY (`Estado_Maquina_cod_estMaq`) REFERENCES `estado_maquina` (`cod_estMaq`),
  CONSTRAINT `Maquina_Tipo_Maq` FOREIGN KEY (`Tipo_Maq_cod_tm`) REFERENCES `tipo_maq` (`cod_tm`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `materia_prima`
--

DROP TABLE IF EXISTS `materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materia_prima` (
  `cod_mp` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(30) NOT NULL,
  `materiaP` varchar(45) DEFAULT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `precio` decimal(8,2) DEFAULT NULL,
  `image` mediumblob,
  `Estado_Materia_Prima_cod_est_mp` int NOT NULL,
  `Unidad_cod_unidad` int NOT NULL,
  PRIMARY KEY (`cod_mp`),
  KEY `Materia_Prima_Estado_Materia_Prima` (`Estado_Materia_Prima_cod_est_mp`),
  KEY `Materia_Prima_Unidad` (`Unidad_cod_unidad`),
  CONSTRAINT `Materia_Prima_Estado_Materia_Prima` FOREIGN KEY (`Estado_Materia_Prima_cod_est_mp`) REFERENCES `estado_materia_prima` (`cod_est_mp`),
  CONSTRAINT `Materia_Prima_Unidad` FOREIGN KEY (`Unidad_cod_unidad`) REFERENCES `unidad` (`cod_unidad`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ordencompra`
--

DROP TABLE IF EXISTS `ordencompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordencompra` (
  `cod_ordC` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `recepcion` tinyint(1) NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  `Tipo_Compra_cod_tc` int NOT NULL,
  `Proveedor_cod_prov` int NOT NULL,
  PRIMARY KEY (`cod_ordC`),
  KEY `OrdenCompra_Empleado` (`Empleado_cod_emp`),
  KEY `OrdenCompra_Proveedor` (`Proveedor_cod_prov`),
  KEY `OrdenCompra_Tipo_Compra` (`Tipo_Compra_cod_tc`),
  CONSTRAINT `OrdenCompra_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `OrdenCompra_Proveedor` FOREIGN KEY (`Proveedor_cod_prov`) REFERENCES `proveedor` (`cod_prov`),
  CONSTRAINT `OrdenCompra_Tipo_Compra` FOREIGN KEY (`Tipo_Compra_cod_tc`) REFERENCES `tipo_compra` (`cod_tc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `cod_pago` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `detalle` varchar(255) NOT NULL,
  `Cuenta_Por_Cobrar_cod_cobrar` int NOT NULL,
  `Forma_Pago_cod_fp` int NOT NULL,
  PRIMARY KEY (`cod_pago`),
  KEY `Pagos_Cuenta_Por_Cobrar` (`Cuenta_Por_Cobrar_cod_cobrar`),
  KEY `Pagos_Forma_Pago` (`Forma_Pago_cod_fp`),
  CONSTRAINT `Pagos_Cuenta_Por_Cobrar` FOREIGN KEY (`Cuenta_Por_Cobrar_cod_cobrar`) REFERENCES `cuenta_por_cobrar` (`cod_cobrar`),
  CONSTRAINT `Pagos_Forma_Pago` FOREIGN KEY (`Forma_Pago_cod_fp`) REFERENCES `forma_pago` (`cod_fp`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pais`
--

DROP TABLE IF EXISTS `pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pais` (
  `cod_pais` int NOT NULL AUTO_INCREMENT,
  `pais` varchar(50) NOT NULL,
  PRIMARY KEY (`cod_pais`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permiso`
--

DROP TABLE IF EXISTS `permiso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permiso` (
  `cod_permiso` int NOT NULL AUTO_INCREMENT,
  `permiso` varchar(65) NOT NULL,
  PRIMARY KEY (`cod_permiso`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permiso_empleado`
--

DROP TABLE IF EXISTS `permiso_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permiso_empleado` (
  `cod_permiso` int NOT NULL AUTO_INCREMENT,
  `motivo` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`cod_permiso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `precio_producto`
--

DROP TABLE IF EXISTS `precio_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `precio_producto` (
  `cod_precio_prod` int NOT NULL AUTO_INCREMENT,
  `Producto_cod_prod` int NOT NULL,
  `precio` decimal(7,2) NOT NULL,
  PRIMARY KEY (`cod_precio_prod`),
  KEY `Precio_Producto_Producto` (`Producto_cod_prod`),
  CONSTRAINT `Precio_Producto_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produccion_embolsado`
--

DROP TABLE IF EXISTS `produccion_embolsado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion_embolsado` (
  `cod_prod_embolsado` int NOT NULL AUTO_INCREMENT,
  `Turno_Produccion_cod_produccion` int NOT NULL,
  `Maquina_cod_maq` int NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  `Materia_Prima_cod_mp` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  `bolsas` int NOT NULL,
  `observacion` varchar(255) NOT NULL,
  `verificacion` tinyint(1) NOT NULL,
  `autorizacion` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_prod_embolsado`),
  KEY `Produccion_Embolsado_Empleado` (`Empleado_cod_emp`),
  KEY `Produccion_Embolsado_Maquina` (`Maquina_cod_maq`),
  KEY `Produccion_Embolsado_Materia_Prima` (`Materia_Prima_cod_mp`),
  KEY `Produccion_Embolsado_Producto` (`Producto_cod_prod`),
  KEY `Produccion_Embolsado_Turno_Produccion` (`Turno_Produccion_cod_produccion`),
  CONSTRAINT `Produccion_Embolsado_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Produccion_Embolsado_Maquina` FOREIGN KEY (`Maquina_cod_maq`) REFERENCES `maquina` (`cod_maq`),
  CONSTRAINT `Produccion_Embolsado_Materia_Prima` FOREIGN KEY (`Materia_Prima_cod_mp`) REFERENCES `materia_prima` (`cod_mp`),
  CONSTRAINT `Produccion_Embolsado_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`),
  CONSTRAINT `Produccion_Embolsado_Turno_Produccion` FOREIGN KEY (`Turno_Produccion_cod_produccion`) REFERENCES `turno_produccion` (`cod_produccion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produccion_planta`
--

DROP TABLE IF EXISTS `produccion_planta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion_planta` (
  `cod_prod_planta` int NOT NULL AUTO_INCREMENT,
  `Turno_Produccion_cod_produccion` int NOT NULL,
  `Maquina_cod_maq` int NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  `Materia_Prima_cod_mp` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  `malos` int NOT NULL,
  `buenos` int NOT NULL,
  `observacion` varchar(255) NOT NULL,
  `verificacion` tinyint(1) NOT NULL,
  `autorizacion` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_prod_planta`),
  KEY `Produccion_Empleado` (`Empleado_cod_emp`),
  KEY `Produccion_Maquina` (`Maquina_cod_maq`),
  KEY `Produccion_Materia_Prima` (`Materia_Prima_cod_mp`),
  KEY `Produccion_Producto` (`Producto_cod_prod`),
  KEY `Produccion_Turno_Produccion` (`Turno_Produccion_cod_produccion`),
  CONSTRAINT `Produccion_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Produccion_Maquina` FOREIGN KEY (`Maquina_cod_maq`) REFERENCES `maquina` (`cod_maq`),
  CONSTRAINT `Produccion_Materia_Prima` FOREIGN KEY (`Materia_Prima_cod_mp`) REFERENCES `materia_prima` (`cod_mp`),
  CONSTRAINT `Produccion_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`),
  CONSTRAINT `Produccion_Turno_Produccion` FOREIGN KEY (`Turno_Produccion_cod_produccion`) REFERENCES `turno_produccion` (`cod_produccion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `cod_prod` int NOT NULL AUTO_INCREMENT,
  `codigo` char(25) NOT NULL,
  `producto` varchar(45) NOT NULL,
  `descripcion` varchar(65) DEFAULT NULL,
  `paquete` int NOT NULL,
  `imagen` mediumblob,
  `Unidad_cod_unidad` int NOT NULL,
  `Categoria_cod_catg` int NOT NULL,
  `Estado_Producto_cod_estProd` int NOT NULL,
  `peso` decimal(7,2) NOT NULL,
  `stock_min` int NOT NULL,
  `embolsado` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_prod`),
  KEY `Producto_Categoria` (`Categoria_cod_catg`),
  KEY `Producto_Estado_Producto` (`Estado_Producto_cod_estProd`),
  KEY `Producto_Unidad` (`Unidad_cod_unidad`),
  CONSTRAINT `Producto_Categoria` FOREIGN KEY (`Categoria_cod_catg`) REFERENCES `categoria` (`cod_catg`),
  CONSTRAINT `Producto_Estado_Producto` FOREIGN KEY (`Estado_Producto_cod_estProd`) REFERENCES `estado_producto` (`cod_estProd`),
  CONSTRAINT `Producto_Unidad` FOREIGN KEY (`Unidad_cod_unidad`) REFERENCES `unidad` (`cod_unidad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `cod_prov` int NOT NULL AUTO_INCREMENT,
  `proveedor` varchar(60) NOT NULL,
  `empresa` varchar(60) NOT NULL,
  `telefono` char(15) NOT NULL,
  `correo` varchar(60) DEFAULT NULL,
  `image` mediumblob,
  `Tipo_Prov_cod_tp` int NOT NULL,
  `Ciudad_cod_ciudad` int NOT NULL,
  PRIMARY KEY (`cod_prov`),
  KEY `Proveedor_Ciudad` (`Ciudad_cod_ciudad`),
  KEY `Proveedor_Tipo_Prov` (`Tipo_Prov_cod_tp`),
  CONSTRAINT `Proveedor_Ciudad` FOREIGN KEY (`Ciudad_cod_ciudad`) REFERENCES `ciudad` (`cod_ciudad`),
  CONSTRAINT `Proveedor_Tipo_Prov` FOREIGN KEY (`Tipo_Prov_cod_tp`) REFERENCES `tipo_prov` (`cod_tp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recepcion`
--

DROP TABLE IF EXISTS `recepcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recepcion` (
  `cod_rep` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `detalle` varchar(100) NOT NULL,
  `OrdenCompra_cod_ordC` int NOT NULL,
  `Estado_Recepcion_cod_estRep` int NOT NULL,
  PRIMARY KEY (`cod_rep`),
  KEY `Recepcion_Estado_Recepcion` (`Estado_Recepcion_cod_estRep`),
  KEY `Recepcion_OrdenCompra` (`OrdenCompra_cod_ordC`),
  CONSTRAINT `Recepcion_Estado_Recepcion` FOREIGN KEY (`Estado_Recepcion_cod_estRep`) REFERENCES `estado_recepcion` (`cod_estRep`),
  CONSTRAINT `Recepcion_OrdenCompra` FOREIGN KEY (`OrdenCompra_cod_ordC`) REFERENCES `ordencompra` (`cod_ordC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recibo`
--

DROP TABLE IF EXISTS `recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recibo` (
  `cod_vent` int NOT NULL AUTO_INCREMENT,
  `nro_venta` int NOT NULL,
  `fecha` date NOT NULL,
  `detalle` varchar(255) DEFAULT NULL,
  `Cliente_cod_cli` int NOT NULL,
  `Estado_Recibo_cod_estVen` int NOT NULL,
  `Empleado_cod_emp` int NOT NULL,
  PRIMARY KEY (`cod_vent`),
  KEY `Recibo_Empleado` (`Empleado_cod_emp`),
  KEY `Recibo_Estado_Recibo` (`Estado_Recibo_cod_estVen`),
  KEY `Venta_Cliente` (`Cliente_cod_cli`),
  CONSTRAINT `Recibo_Empleado` FOREIGN KEY (`Empleado_cod_emp`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Recibo_Estado_Recibo` FOREIGN KEY (`Estado_Recibo_cod_estVen`) REFERENCES `estado_recibo` (`cod_estVen`),
  CONSTRAINT `Venta_Cliente` FOREIGN KEY (`Cliente_cod_cli`) REFERENCES `cliente` (`cod_cli`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recibo_venta`
--

DROP TABLE IF EXISTS `recibo_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recibo_venta` (
  `cod_vent` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `descuento` decimal(10,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `Recibo_cod_vent` int NOT NULL,
  `Producto_cod_prod` int NOT NULL,
  `importe` decimal(15,2) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `devuelto` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_vent`),
  KEY `ReciboVenta_Producto` (`Producto_cod_prod`),
  KEY `ReciboVenta_Recibo` (`Recibo_cod_vent`),
  CONSTRAINT `ReciboVenta_Producto` FOREIGN KEY (`Producto_cod_prod`) REFERENCES `producto` (`cod_prod`),
  CONSTRAINT `ReciboVenta_Recibo` FOREIGN KEY (`Recibo_cod_vent`) REFERENCES `recibo` (`cod_vent`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recurso`
--

DROP TABLE IF EXISTS `recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recurso` (
  `cod_recurso` int NOT NULL AUTO_INCREMENT,
  `recurso` varchar(100) NOT NULL,
  PRIMARY KEY (`cod_recurso`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `cod_rol` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(75) NOT NULL,
  PRIMARY KEY (`cod_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_compra`
--

DROP TABLE IF EXISTS `tipo_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_compra` (
  `cod_tc` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_tc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_maq`
--

DROP TABLE IF EXISTS `tipo_maq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_maq` (
  `cod_tm` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_tm`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_prov`
--

DROP TABLE IF EXISTS `tipo_prov`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_prov` (
  `cod_tp` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(60) NOT NULL,
  PRIMARY KEY (`cod_tp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turno`
--

DROP TABLE IF EXISTS `turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turno` (
  `cod_turno` int NOT NULL AUTO_INCREMENT,
  `turno` char(20) NOT NULL,
  `horario` varchar(45) NOT NULL,
  PRIMARY KEY (`cod_turno`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turno_produccion`
--

DROP TABLE IF EXISTS `turno_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turno_produccion` (
  `cod_produccion` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `auxiliares` varchar(200) DEFAULT NULL,
  `operador` int NOT NULL,
  `Turno_cod_turno` int NOT NULL,
  `embolsador` int NOT NULL,
  `verificacion` tinyint(1) NOT NULL,
  `autorizacion` tinyint(1) NOT NULL,
  PRIMARY KEY (`cod_produccion`),
  KEY `Produccion_Empleado2` (`embolsador`),
  KEY `Produccion_Empleado3` (`operador`),
  KEY `Produccion_Turno` (`Turno_cod_turno`),
  CONSTRAINT `Produccion_Empleado2` FOREIGN KEY (`embolsador`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Produccion_Empleado3` FOREIGN KEY (`operador`) REFERENCES `empleado` (`cod_emp`),
  CONSTRAINT `Produccion_Turno` FOREIGN KEY (`Turno_cod_turno`) REFERENCES `turno` (`cod_turno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unidad`
--

DROP TABLE IF EXISTS `unidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad` (
  `cod_unidad` int NOT NULL AUTO_INCREMENT,
  `unidad` varchar(55) NOT NULL,
  PRIMARY KEY (`cod_unidad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vacaciones_empleado`
--

DROP TABLE IF EXISTS `vacaciones_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vacaciones_empleado` (
  `cod_vacacion` int NOT NULL AUTO_INCREMENT,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  PRIMARY KEY (`cod_vacacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10  8:12:32
