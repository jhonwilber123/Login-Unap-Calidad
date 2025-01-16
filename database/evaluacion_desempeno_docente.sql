-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-01-2025 a las 22:18:19
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
-- Estructura de tabla para la tabla `evaluacion_desempeno_docente`
--

CREATE TABLE `evaluacion_desempeno_docente` (
  `id_evaluacion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `periodo_academico_evaluado` varchar(100) NOT NULL,
  `categoria_docente` varchar(100) NOT NULL,
  `promedio_evaluacion_general` decimal(5,2) NOT NULL,
  `promedio_evaluacion_autoridades` decimal(5,2) NOT NULL,
  `promedio_evaluacion_estudiantes` decimal(5,2) NOT NULL,
  `ruta_informes_evaluacion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  ADD PRIMARY KEY (`id_evaluacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  MODIFY `id_evaluacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  ADD CONSTRAINT `evaluacion_desempeno_docente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
