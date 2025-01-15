-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-01-2025 a las 22:18:39
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
-- Estructura de tabla para la tabla `participaciongestionuniversitaria`
--

CREATE TABLE `participaciongestionuniversitaria` (
  `id` int NOT NULL,
  `area_gestion` enum('Administración Académica','Administración Financiera','Desarrollo de Infraestructura','Innovación y Tecnología','Otro') NOT NULL,
  `otro_area_gestion` varchar(255) DEFAULT NULL,
  `rol_gestion` enum('Coordinador','Secretario','Miembro del Comité','Otro') NOT NULL,
  `otro_rol_gestion` varchar(255) DEFAULT NULL,
  `descripcion_responsabilidades` text NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `logros_contribuciones` text,
  `adjuntar_documentacion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `participaciongestionuniversitaria`
--

INSERT INTO `participaciongestionuniversitaria` (`id`, `area_gestion`, `otro_area_gestion`, `rol_gestion`, `otro_rol_gestion`, `descripcion_responsabilidades`, `fecha_inicio`, `fecha_fin`, `logros_contribuciones`, `adjuntar_documentacion`) VALUES
(1, 'Administración Académica', NULL, 'Coordinador', NULL, 'volar en el cielo', '2024-03-06', '2024-07-06', 'muchos', '148');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `participaciongestionuniversitaria`
--
ALTER TABLE `participaciongestionuniversitaria`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `participaciongestionuniversitaria`
--
ALTER TABLE `participaciongestionuniversitaria`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
