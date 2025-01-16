-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-01-2025 a las 22:17:42
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
-- Estructura de tabla para la tabla `carga_academica_lectiva`
--

CREATE TABLE `carga_academica_lectiva` (
  `id_carga` int NOT NULL,
  `id_usuario` int NOT NULL,
  `periodo_academico` varchar(20) NOT NULL,
  `numero_memorandum` varchar(100) NOT NULL,
  `id_memorandum` int DEFAULT NULL,
  `horas_asignadas` int NOT NULL,
  `observaciones` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `carga_academica_lectiva`
--

INSERT INTO `carga_academica_lectiva` (`id_carga`, `id_usuario`, `periodo_academico`, `numero_memorandum`, `id_memorandum`, `horas_asignadas`, `observaciones`) VALUES
(4, 1, '2023-I', '2046', 134, 2, ''),
(5, 4, '2023-I', '2046', 135, 20, '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  ADD PRIMARY KEY (`id_carga`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_memorandum` (`id_memorandum`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  MODIFY `id_carga` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  ADD CONSTRAINT `carga_academica_lectiva_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `carga_academica_lectiva_ibfk_2` FOREIGN KEY (`id_memorandum`) REFERENCES `imagenesadjuntas` (`id_imagen`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
