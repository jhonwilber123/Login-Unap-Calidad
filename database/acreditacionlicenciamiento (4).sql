-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-01-2025 a las 22:17:59
-- Versión del servidor: 8.0.39
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `unap_ccs_system`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `acreditacionlicenciamiento`
--

CREATE TABLE `acreditacionlicenciamiento` (
  `id_acreditacion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `id_imagen` int DEFAULT NULL,
  `id_imagen_evidencias` int DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `numero_resolucion` varchar(100) DEFAULT NULL,
  `fecha_resolucion` date DEFAULT NULL,
  `cargo_comite` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `acreditacionlicenciamiento`
--
ALTER TABLE `acreditacionlicenciamiento`
  ADD PRIMARY KEY (`id_acreditacion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_imagen` (`id_imagen`),
  ADD KEY `fk_imagenes_evidencias` (`id_imagen_evidencias`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `acreditacionlicenciamiento`
--
ALTER TABLE `acreditacionlicenciamiento`
  MODIFY `id_acreditacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `acreditacionlicenciamiento`
--
ALTER TABLE `acreditacionlicenciamiento`
  ADD CONSTRAINT `acreditacionlicenciamiento_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `acreditacionlicenciamiento_ibfk_2` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`),
  ADD CONSTRAINT `fk_imagenes_evidencias` FOREIGN KEY (`id_imagen_evidencias`) REFERENCES `imagenesadjuntas` (`id_imagen`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
