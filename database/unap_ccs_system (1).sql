-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-09-2024 a las 18:15:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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
-- Estructura de tabla para la tabla `actividadesproyeccionsocial`
--

CREATE TABLE `actividadesproyeccionsocial` (
  `id_actividad` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Organización','Expositor','Asistencia') DEFAULT NULL,
  `evento` enum('Congreso','Convención','Simposio','Foro','Seminario','Curso Taller','Charla') DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actualizacionescapacitaciones`
--

CREATE TABLE `actualizacionescapacitaciones` (
  `id_capacitacion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Curso Presencial','Curso Virtual','Diplomado Presencial','Diplomado Virtual','Especialización Médica','Segunda Especialidad','Maestría','Doctorado','Especialización en Docencia Universitaria') DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `horas` int(11) DEFAULT NULL,
  `creditos` int(11) DEFAULT NULL,
  `semestres_concluidos` int(11) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrativosinfoadicional`
--

CREATE TABLE `administrativosinfoadicional` (
  `id_administrativo_info` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `informacion_relevante` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivosevidencias`
--

CREATE TABLE `archivosevidencias` (
  `id_archivo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `ruta_archivo` varchar(255) DEFAULT NULL,
  `fecha_subida` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargalectiva`
--

CREATE TABLE `cargalectiva` (
  `id_carga` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `promedio_horas` decimal(5,2) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargosdirectivos`
--

CREATE TABLE `cargosdirectivos` (
  `id_cargo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `cargo` varchar(100) DEFAULT NULL,
  `anios` int(11) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datospersonales`
--

CREATE TABLE `datospersonales` (
  `id_datos` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `apellido_paterno` varchar(50) DEFAULT NULL,
  `apellido_materno` varchar(50) DEFAULT NULL,
  `nombres` varchar(100) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `lugar_nacimiento_departamento` varchar(50) DEFAULT NULL,
  `lugar_nacimiento_provincia` varchar(50) DEFAULT NULL,
  `lugar_nacimiento_distrito` varchar(50) DEFAULT NULL,
  `dni` varchar(15) DEFAULT NULL,
  `carne_extranjeria` varchar(20) DEFAULT NULL,
  `numero_colegiatura` varchar(20) DEFAULT NULL,
  `numero_ruc` varchar(20) DEFAULT NULL,
  `codigo` varchar(20) DEFAULT NULL,
  `condicion` varchar(20) DEFAULT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `dedicacion` varchar(50) DEFAULT NULL,
  `telefono_fijo` varchar(20) DEFAULT NULL,
  `movil` varchar(20) DEFAULT NULL,
  `correo_personal` varchar(100) DEFAULT NULL,
  `correo_institucional` varchar(100) DEFAULT NULL,
  `domicilio_actual` varchar(255) DEFAULT NULL,
  `referencia` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docentesinfoadicional`
--

CREATE TABLE `docentesinfoadicional` (
  `id_docente_info` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `sineace` varchar(50) DEFAULT NULL,
  `orcid` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluacionesdesempeno`
--

CREATE TABLE `evaluacionesdesempeno` (
  `id_evaluacion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `semestre` varchar(20) DEFAULT NULL,
  `evaluacion_autoridades` decimal(5,2) DEFAULT NULL,
  `evaluacion_estudiantes` decimal(5,2) DEFAULT NULL,
  `promedio` decimal(5,2) DEFAULT NULL,
  `nivel` enum('Excelente','Muy Bueno','Bueno','Regular','Deficiente') DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experienciadocente`
--

CREATE TABLE `experienciadocente` (
  `id_experiencia` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Movilidad Docente','Posgrado','Docencia en Categoría') DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `anios` int(11) DEFAULT NULL,
  `cursos` int(11) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gradostitulos`
--

CREATE TABLE `gradostitulos` (
  `id_grado` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `tipo` enum('Título Profesional','Título de Segunda Especialidad','Especialidad Médica','Maestría Profesional','Maestría en Ciencias','Doctorado','Ph.D.') DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `idiomas`
--

CREATE TABLE `idiomas` (
  `id_idioma` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `idioma` varchar(50) DEFAULT NULL,
  `nivel` enum('Básico','Intermedio','Avanzado') DEFAULT NULL,
  `certificado` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenesadjuntas`
--

CREATE TABLE `imagenesadjuntas` (
  `id_imagen` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `ruta_imagen` varchar(255) NOT NULL,
  `fecha_subida` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `investigaciones`
--

CREATE TABLE `investigaciones` (
  `id_investigacion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Artículo Científico','Artículo Aceptado','Artículo en Congreso','Registro de Patente','Informe de Investigación','Participación en Publicación Científica') DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `revista` varchar(255) DEFAULT NULL,
  `indice` enum('Thomson Reuters','Scopus','Web of Science','Scielo','Latin Index','Otro') DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `autor` tinyint(1) DEFAULT NULL,
  `coautor` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `participaciontesis`
--

CREATE TABLE `participaciontesis` (
  `id_participacion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Director','Asesor','Jurado') DEFAULT NULL,
  `nivel` enum('Pregrado','Posgrado') DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `universidad` varchar(255) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccionintelectual`
--

CREATE TABLE `produccionintelectual` (
  `id_produccion` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Texto Universitario','Traducción de Libro','Capítulo de Libro','Obra Literaria','Manual de Prácticas','Guía de Enseñanza','Monografía') DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `isbn` varchar(50) DEFAULT NULL,
  `deposito_legal` tinyint(1) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `autor` tinyint(1) DEFAULT NULL,
  `coautor` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ratificacionpuntos`
--

CREATE TABLE `ratificacionpuntos` (
  `id_puntaje` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `criterio` varchar(255) NOT NULL,
  `puntaje_obtenido` decimal(5,2) NOT NULL,
  `detalles` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reconocimientos`
--

CREATE TABLE `reconocimientos` (
  `id_reconocimiento` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('Docente Visitante','Premio Internacional','Premio Nacional','Miembro de Sociedad Científica Internacional','Miembro de Sociedad Científica Nacional','Distinción Académica','Resolución Rectoral','Resolución Decanal') DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `institucion` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `softwareespecializado`
--

CREATE TABLE `softwareespecializado` (
  `id_software` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `nombre_curso` varchar(255) DEFAULT NULL,
  `modalidad` enum('Presencial','Virtual') DEFAULT NULL,
  `horas` int(11) DEFAULT NULL,
  `institucion` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tutorias`
--

CREATE TABLE `tutorias` (
  `id_tutoria` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('Administrador','Docente','Administrativo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `contraseña`, `rol`) VALUES
(1, 'admin', '$2a$12$L3.lzToyQ0Ig8szPPwypseMkA.NvcWfI2vnQrx.KNxVwvAqf..UIe', 'Administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  ADD PRIMARY KEY (`id_actividad`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  ADD PRIMARY KEY (`id_capacitacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `administrativosinfoadicional`
--
ALTER TABLE `administrativosinfoadicional`
  ADD PRIMARY KEY (`id_administrativo_info`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `archivosevidencias`
--
ALTER TABLE `archivosevidencias`
  ADD PRIMARY KEY (`id_archivo`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `cargalectiva`
--
ALTER TABLE `cargalectiva`
  ADD PRIMARY KEY (`id_carga`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  ADD PRIMARY KEY (`id_cargo`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  ADD PRIMARY KEY (`id_datos`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `docentesinfoadicional`
--
ALTER TABLE `docentesinfoadicional`
  ADD PRIMARY KEY (`id_docente_info`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `evaluacionesdesempeno`
--
ALTER TABLE `evaluacionesdesempeno`
  ADD PRIMARY KEY (`id_evaluacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  ADD PRIMARY KEY (`id_experiencia`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  ADD PRIMARY KEY (`id_grado`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  ADD PRIMARY KEY (`id_idioma`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `imagenesadjuntas`
--
ALTER TABLE `imagenesadjuntas`
  ADD PRIMARY KEY (`id_imagen`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `investigaciones`
--
ALTER TABLE `investigaciones`
  ADD PRIMARY KEY (`id_investigacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  ADD PRIMARY KEY (`id_participacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  ADD PRIMARY KEY (`id_produccion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `ratificacionpuntos`
--
ALTER TABLE `ratificacionpuntos`
  ADD PRIMARY KEY (`id_puntaje`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `reconocimientos`
--
ALTER TABLE `reconocimientos`
  ADD PRIMARY KEY (`id_reconocimiento`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  ADD PRIMARY KEY (`id_software`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `tutorias`
--
ALTER TABLE `tutorias`
  ADD PRIMARY KEY (`id_tutoria`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  MODIFY `id_actividad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  MODIFY `id_capacitacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `administrativosinfoadicional`
--
ALTER TABLE `administrativosinfoadicional`
  MODIFY `id_administrativo_info` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `archivosevidencias`
--
ALTER TABLE `archivosevidencias`
  MODIFY `id_archivo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cargalectiva`
--
ALTER TABLE `cargalectiva`
  MODIFY `id_carga` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  MODIFY `id_cargo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  MODIFY `id_datos` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `docentesinfoadicional`
--
ALTER TABLE `docentesinfoadicional`
  MODIFY `id_docente_info` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `evaluacionesdesempeno`
--
ALTER TABLE `evaluacionesdesempeno`
  MODIFY `id_evaluacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  MODIFY `id_experiencia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  MODIFY `id_grado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  MODIFY `id_idioma` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `imagenesadjuntas`
--
ALTER TABLE `imagenesadjuntas`
  MODIFY `id_imagen` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `investigaciones`
--
ALTER TABLE `investigaciones`
  MODIFY `id_investigacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  MODIFY `id_participacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  MODIFY `id_produccion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ratificacionpuntos`
--
ALTER TABLE `ratificacionpuntos`
  MODIFY `id_puntaje` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reconocimientos`
--
ALTER TABLE `reconocimientos`
  MODIFY `id_reconocimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  MODIFY `id_software` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tutorias`
--
ALTER TABLE `tutorias`
  MODIFY `id_tutoria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  ADD CONSTRAINT `actividadesproyeccionsocial_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  ADD CONSTRAINT `actualizacionescapacitaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `administrativosinfoadicional`
--
ALTER TABLE `administrativosinfoadicional`
  ADD CONSTRAINT `administrativosinfoadicional_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `archivosevidencias`
--
ALTER TABLE `archivosevidencias`
  ADD CONSTRAINT `archivosevidencias_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `cargalectiva`
--
ALTER TABLE `cargalectiva`
  ADD CONSTRAINT `cargalectiva_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  ADD CONSTRAINT `cargosdirectivos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  ADD CONSTRAINT `datospersonales_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `docentesinfoadicional`
--
ALTER TABLE `docentesinfoadicional`
  ADD CONSTRAINT `docentesinfoadicional_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `evaluacionesdesempeno`
--
ALTER TABLE `evaluacionesdesempeno`
  ADD CONSTRAINT `evaluacionesdesempeno_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  ADD CONSTRAINT `experienciadocente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  ADD CONSTRAINT `gradostitulos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `idiomas`
--
ALTER TABLE `idiomas`
  ADD CONSTRAINT `idiomas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imagenesadjuntas`
--
ALTER TABLE `imagenesadjuntas`
  ADD CONSTRAINT `imagenesadjuntas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `investigaciones`
--
ALTER TABLE `investigaciones`
  ADD CONSTRAINT `investigaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  ADD CONSTRAINT `participaciontesis_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  ADD CONSTRAINT `produccionintelectual_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ratificacionpuntos`
--
ALTER TABLE `ratificacionpuntos`
  ADD CONSTRAINT `ratificacionpuntos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `reconocimientos`
--
ALTER TABLE `reconocimientos`
  ADD CONSTRAINT `reconocimientos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  ADD CONSTRAINT `softwareespecializado_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tutorias`
--
ALTER TABLE `tutorias`
  ADD CONSTRAINT `tutorias_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
