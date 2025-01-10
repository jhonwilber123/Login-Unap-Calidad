-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 12-12-2024 a las 21:17:06
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
  `cargo` varchar(255) NOT NULL,
  `nombre_comite` varchar(255) NOT NULL,
  `tipo_participacion` varchar(100) NOT NULL,
  `numero_resolucion` varchar(50) NOT NULL,
  `fecha_resolucion` date NOT NULL,
  `ruta_resolucion_nombramiento` varchar(255) DEFAULT NULL,
  `ruta_evidencias` varchar(255) DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `logros` text,
  `id_imagen` int DEFAULT NULL,
  `id_imagen_evidencias` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `acreditacionlicenciamiento`
--

INSERT INTO `acreditacionlicenciamiento` (`id_acreditacion`, `id_usuario`, `cargo`, `nombre_comite`, `tipo_participacion`, `numero_resolucion`, `fecha_resolucion`, `ruta_resolucion_nombramiento`, `ruta_evidencias`, `fecha_inicio`, `fecha_fin`, `logros`, `id_imagen`, `id_imagen_evidencias`) VALUES
(3, 1, 'jefe de TI', 'Holamundo', 'Acreditación', '02011', '2024-04-09', '1734027622_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '1734021726_Informe_de_incidencias.pdf', '2024-03-06', '2024-03-06', '', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividadesproyeccionsocial`
--

CREATE TABLE `actividadesproyeccionsocial` (
  `id_actividad` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Organización','Expositor','Asistencia') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nivel` enum('Pregrado','Posgrado') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `evento` enum('Congreso','Convención','Simposio','Foro','Seminario','Curso Taller','Charla') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `Emitido_por` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividadesproyeccionsocial`
--

INSERT INTO `actividadesproyeccionsocial` (`id_actividad`, `id_usuario`, `tipo`, `nivel`, `evento`, `descripcion`, `fecha`, `puntaje`, `id_imagen`, `Emitido_por`) VALUES
(3, 1, 'Organización', 'Pregrado', 'Convención', 'ssss', '2024-03-06', NULL, 73, NULL),
(5, 1, 'Organización', NULL, 'Congreso', 'ssss', '2024-05-06', NULL, 121, NULL),
(6, 1, 'Organización', NULL, 'Congreso', 'dsdsdsa', '2022-03-06', NULL, 122, 'San lorenzo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actualizacionescapacitaciones`
--

CREATE TABLE `actualizacionescapacitaciones` (
  `id_capacitacion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Curso Presencial','Curso Virtual','Diplomado Presencial','Diplomado Virtual','Especialización Médica','Segunda Especialidad','Maestría','Doctorado','Especialización en Docencia Universitaria') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `creditos` int DEFAULT NULL,
  `semestres_concluidos` int DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `institucion_otorga` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actualizacionescapacitaciones`
--

INSERT INTO `actualizacionescapacitaciones` (`id_capacitacion`, `id_usuario`, `tipo`, `descripcion`, `horas`, `creditos`, `semestres_concluidos`, `puntaje`, `id_imagen`, `institucion_otorga`) VALUES
(1, 1, 'Diplomado Presencial', 'hola', 20, NULL, NULL, 20.00, 22, NULL),
(5, 1, 'Curso Presencial', 'dsdsds', 20, NULL, NULL, NULL, 78, NULL),
(6, 1, 'Maestría', 'ssss', NULL, NULL, 2, NULL, 79, NULL),
(7, 1, 'Maestría', 'ssss', NULL, NULL, 6, NULL, 81, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrativosinfoadicional`
--

CREATE TABLE `administrativosinfoadicional` (
  `id_administrativo_info` int NOT NULL,
  `id_usuario` int NOT NULL,
  `informacion_relevante` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivosevidencias`
--

CREATE TABLE `archivosevidencias` (
  `id_archivo` int NOT NULL,
  `id_usuario` int NOT NULL,
  `categoria` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ruta_archivo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_subida` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargalectiva`
--

CREATE TABLE `cargalectiva` (
  `id_carga` int NOT NULL,
  `id_usuario` int NOT NULL,
  `promedio_horas` decimal(5,2) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `categoria_docente` varchar(20) NOT NULL,
  `horas_asignadas` int NOT NULL,
  `observaciones` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `carga_academica_lectiva`
--

INSERT INTO `carga_academica_lectiva` (`id_carga`, `id_usuario`, `periodo_academico`, `numero_memorandum`, `id_memorandum`, `categoria_docente`, `horas_asignadas`, `observaciones`) VALUES
(4, 1, '2023-I', '2046', 134, 'Auxiliar', 2, ''),
(5, 4, '2023-I', '2046', 135, 'Auxiliar', 20, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargosdirectivos`
--

CREATE TABLE `cargosdirectivos` (
  `id_cargo` int NOT NULL,
  `id_usuario` int NOT NULL,
  `cargo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `anios` int DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datospersonales`
--

CREATE TABLE `datospersonales` (
  `id_datos` int NOT NULL,
  `id_usuario` int NOT NULL,
  `apellido_paterno` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `apellido_materno` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nombres` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `lugar_nacimiento_departamento` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lugar_nacimiento_provincia` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lugar_nacimiento_distrito` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dni` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `carne_extranjeria` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_colegiatura` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_ruc` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `codigo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `condicion` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dedicacion` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telefono_fijo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `movil` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `correo_personal` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `correo_institucional` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `domicilio_actual` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `referencia` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_foto_docente` int DEFAULT NULL,
  `id_constancia_habilitacion` int DEFAULT NULL,
  `ID_CTI` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ID_Scopus` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ID_ORCID` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `datospersonales`
--

INSERT INTO `datospersonales` (`id_datos`, `id_usuario`, `apellido_paterno`, `apellido_materno`, `nombres`, `fecha_nacimiento`, `lugar_nacimiento_departamento`, `lugar_nacimiento_provincia`, `lugar_nacimiento_distrito`, `dni`, `carne_extranjeria`, `numero_colegiatura`, `numero_ruc`, `codigo`, `condicion`, `categoria`, `dedicacion`, `telefono_fijo`, `movil`, `correo_personal`, `correo_institucional`, `domicilio_actual`, `referencia`, `id_foto_docente`, `id_constancia_habilitacion`, `ID_CTI`, `ID_Scopus`, `ID_ORCID`) VALUES
(1, 4, 'AJATA', 'ASCARRUNZ', 'JHON WILBER ', '2002-03-06', 'PUNO', 'PUNO', 'PUNO', '77799463', 'no', '112263', '000000', '191962', 'Nombrado', 'Si', 'Total', '191962', '900235387', 'jhonwaa123@gmail.com', 'jajataa@est.unap.edu.pe', 'salcedo tepro', 'a una cuadra del peda', NULL, NULL, NULL, NULL, NULL),
(2, 1, 'Ajata', 'Ascarrunz', 'Jhon Wilber', '2020-03-06', 'PUNO', 'PUNO', 'PUNO', '77799463', 'na', 'na', 'na', '191962', 'Nombrado', 'Asociado', 'Exclusiva', '900235387', '900235387', 'jhonwaa123@gmail.com', 'jajataa@est.unap.edu.pe', 'salcedo tepro', 'a una cuadra del pedagogico', 120, 125, 'NA', 'NA', 'NA'),
(3, 9, 'AJATA', 'ASCARRUNZ', 'JHON WILBER ', '2024-03-06', 'PUNO', 'PUNO', 'PUNO', '77799463', NULL, 'na', NULL, '191962', 'Contratado', 'A1', 'Tiempo completo', '191962', '900235387', 'jhonwaa123@gmail.com', 'jajataa@est.unap.edu.pe', 'salcedo tepro', 'a una cuadra del pedagogico', 136, 137, 'NA', 'NA', 'NA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docentesinfoadicional`
--

CREATE TABLE `docentesinfoadicional` (
  `id_docente_info` int NOT NULL,
  `id_usuario` int NOT NULL,
  `sineace` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `orcid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluacionesdesempeno`
--

CREATE TABLE `evaluacionesdesempeno` (
  `id_evaluacion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `semestre` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `evaluacion_autoridades` decimal(5,2) DEFAULT NULL,
  `evaluacion_estudiantes` decimal(5,2) DEFAULT NULL,
  `promedio` decimal(5,2) DEFAULT NULL,
  `nivel` enum('Excelente','Muy Bueno','Bueno','Regular','Deficiente') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `evaluacion_desempeno_docente`
--

INSERT INTO `evaluacion_desempeno_docente` (`id_evaluacion`, `id_usuario`, `periodo_academico_evaluado`, `categoria_docente`, `promedio_evaluacion_general`, `promedio_evaluacion_autoridades`, `promedio_evaluacion_estudiantes`, `ruta_informes_evaluacion`) VALUES
(2, 1, '2024-I', 'Contratado', 2.00, 2.00, 2.00, '1733336961_Chi_cuadrado.pdf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experienciadocente`
--

CREATE TABLE `experienciadocente` (
  `id_experiencia` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Movilidad Docente','Posgrado','Docencia en Categoría') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `anios` int DEFAULT NULL,
  `cursos` int DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `experienciadocente`
--

INSERT INTO `experienciadocente` (`id_experiencia`, `id_usuario`, `tipo`, `descripcion`, `anios`, `cursos`, `puntaje`, `id_imagen`) VALUES
(1, 1, 'Docencia en Categoría', 'Categorizado gaaa', 2, 4, 16.00, 26),
(2, 1, 'Posgrado', 'dssdds', 5, 4, NULL, 84);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gradostitulos`
--

CREATE TABLE `gradostitulos` (
  `id_grado` int NOT NULL,
  `id_usuario` int NOT NULL,
  `titulo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo` enum('Título Profesional','Título de Segunda Especialidad Profesional','Especialidad Médica','Maestría (un año de duración)','Maestría (dos años de duración)','Doctorado o Ph.D.','Grado de Bachiller') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `universidad` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pais` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_expedicion` date DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `id_imagen_sunedu` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gradostitulos`
--

INSERT INTO `gradostitulos` (`id_grado`, `id_usuario`, `titulo`, `tipo`, `puntaje`, `universidad`, `pais`, `fecha_expedicion`, `id_imagen`, `id_imagen_sunedu`) VALUES
(15, 4, 'Ingeniería Estadística e informática ', 'Título Profesional', NULL, 'Universidad Nacional Del Altiplano', 'Peru', '2020-03-06', NULL, NULL),
(40, 1, 'Ingeniería Estadística e informática ', 'Título Profesional', NULL, 'Universidad Nacional Del Altiplano', 'Perú', '2021-03-07', 111, 112),
(42, 1, 'Ingeniería Estadística e informática ', 'Título Profesional', NULL, 'Universidad Nacional Del Altiplano', 'Perú', '2021-03-07', 115, 116),
(46, 1, 'Ingeniería Estadística e informática ', 'Grado de Bachiller', NULL, 'Universidad Nacional Del Altiplano', 'Perú', '1999-06-06', 123, 124),
(48, 1, 'Ingeniería Estadística e informática ', 'Grado de Bachiller', NULL, 'Universidad Nacional Del Altiplano', 'Bahamas', '2023-04-06', 128, 129),
(49, 9, 'Ingeniería Estadística e informática ', 'Grado de Bachiller', NULL, 'Universidad Nacional Del Altiplano', 'Perú', '2023-03-06', 138, 139),
(50, 1, 'Ingeniería Informática ', 'Grado de Bachiller', NULL, 'UNA PUNO', 'Perú', '2024-03-06', 141, 142);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `idiomas`
--

CREATE TABLE `idiomas` (
  `id_idioma` int NOT NULL,
  `id_usuario` int NOT NULL,
  `idioma` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nivel` enum('Básico','Intermedio','Avanzado') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `certificado` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `idiomas`
--

INSERT INTO `idiomas` (`id_idioma`, `id_usuario`, `idioma`, `nivel`, `certificado`, `puntaje`, `id_imagen`) VALUES
(1, 1, 'hnnhnh', 'Básico', 1, NULL, 66),
(2, 1, 'Inglés', 'Intermedio', 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenesadjuntas`
--

CREATE TABLE `imagenesadjuntas` (
  `id_imagen` int NOT NULL,
  `id_usuario` int NOT NULL,
  `categoria` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ruta_imagen` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_subida` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imagenesadjuntas`
--

INSERT INTO `imagenesadjuntas` (`id_imagen`, `id_usuario`, `categoria`, `descripcion`, `ruta_imagen`, `fecha_subida`) VALUES
(1, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-23 12:24:42'),
(2, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-25 09:40:38'),
(3, 1, 'Título Profesional', 'Jhon Wilber', 'uploads/Captura.PNG', '2024-09-25 09:41:17'),
(4, 4, 'Título Profesional', 'Ingeniería Estadística', 'uploads/Prueba.PNG', '2024-09-25 09:42:16'),
(5, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-25 09:57:00'),
(6, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Captura.PNG', '2024-09-25 09:57:21'),
(7, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-25 10:15:03'),
(8, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-25 10:29:02'),
(9, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', 'uploads/Prueba.PNG', '2024-09-25 10:34:26'),
(10, 4, 'Título Profesional', 'Ingeniería Estadística e informática ', '4_1727297988_Prueba.PNG', '2024-09-25 10:59:49'),
(11, 1, 'Título Profesional', 'Ingeniería Estadística', 'Prueba_1727280240.PNG', '2024-09-25 11:04:00'),
(12, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', '1727289505_Prueba.PNG', '2024-09-25 13:38:25'),
(13, 1, 'Título Profesional', 'Ingeniería Informática ', 'Prueba_1727361490.PNG', '2024-09-26 09:38:10'),
(14, 1, 'Título Profesional', 'Ingeniería en ciencias de la computación', '1727711140_logo.png', '2024-09-30 10:45:40'),
(15, 1, 'Título Profesional', 'Ingeniería Informática ', '1727710311_Captura.PNG', '2024-09-30 10:31:51'),
(16, 1, 'Título de Segunda Especialidad', 'Ingeniería Estadística e informática ', '1727711029_Captura.PNG', '2024-09-30 10:43:49'),
(17, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', '1727912142_logo.png', '2024-10-02 18:35:42'),
(18, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', '1727914734_logo.png', '2024-10-02 19:18:54'),
(19, 1, 'Título Profesional', 'Ingeniería Estadística e informática ', '1727914806_frame.png', '2024-10-02 19:20:06'),
(20, 1, 'imagen', 'Ingeniería informática ', '1727916543_frame.png', '2024-10-02 19:49:03'),
(21, 1, 'imagen', 'Ingeniería Estadística e informática ', '1728054406_ac2cfaf9-049a-4b50-9bfb-4b05eda7a75f.jpeg', '2024-10-04 10:06:46'),
(22, 1, 'pdf', 'hola', '1727978310_LETRERO_EL_RAPIDO_TURBO_-JULIACA.pdf', '2024-10-03 12:58:30'),
(26, 1, 'pdf', 'Categorizado gaaa', '1727985890_manual_de_identidad_CCS_2024.pdf', '2024-10-03 15:04:50'),
(32, 1, 'imagen', 'Ingeniería Estadística', '1729266030_Estadistica_Informatica_High_Quality.png', '2024-10-18 10:40:30'),
(56, 1, 'pdf', 'ssss', '1729630355_5.10_Alineamiento_Perfil-de-egreso-y-propositos-Vers-3-_curriculo_flexible_2021-2026_1.pdf', '2024-10-22 15:52:35'),
(59, 1, 'pdf', 'Hola mundo 2', '1729631685_5.10_Alineamiento_Perfil-de-egreso-y-propositos-Vers-3-_curriculo_flexible_2021-2026_1.pdf', '2024-10-22 16:14:45'),
(62, 1, 'imagen', 'ssss', '1729633314_Prueba.PNG', '2024-10-22 16:41:54'),
(64, 1, 'imagen', 'dfsdf', '1729639737_Prueba.PNG', '2024-10-22 18:28:57'),
(65, 1, 'imagen', 'Jhon Wilber', '1729640184_Captura.PNG', '2024-10-22 18:36:24'),
(66, 1, 'imagen', 'Certificado de hnnhnh', '1729641191_Captura.PNG', '2024-10-22 18:53:12'),
(68, 1, 'pdf', 'Ingeniería Estadística e informática ', '1729646128_EstaNoParame-ARDILA-OK.pdf', '2024-10-22 20:15:28'),
(73, 1, 'pdf', 'ssss', '1729699093_report23354411.pdf', '2024-10-23 10:58:13'),
(78, 1, 'pdf', 'dsdsds', '1729713616_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '2024-10-23 15:00:16'),
(79, 1, 'pdf', 'ssss', '1729717335_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '2024-10-23 16:02:15'),
(81, 1, 'pdf', 'ssss', '1729717660_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '2024-10-23 16:07:40'),
(84, 1, 'pdf', 'dssdds', '1729724796_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '2024-10-23 18:06:36'),
(85, 1, 'imagen', 'Foto de Docente', '1732291095_Prueba.PNG', '2024-11-22 10:58:15'),
(86, 1, 'documento', 'Constancia de Habilitación', '1732291095_EstaNoParame-ARDILA-OK.pdf', '2024-11-22 10:58:15'),
(89, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732554201_LE_WAGON__El_contrato_llego_Vamos_a_firm.pdf', '2024-11-25 12:03:21'),
(90, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732554292_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 12:04:52'),
(91, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732554514_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 12:08:34'),
(92, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732554549_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 12:09:09'),
(94, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732555562_EstaNoParame-ARDILA-OK.pdf', '2024-11-25 12:26:02'),
(96, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562066_Estad-Inferenc-Juarez2002.pdf', '2024-11-25 14:14:26'),
(97, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562182_Estad-Inferenc-Juarez2002.pdf', '2024-11-25 14:16:22'),
(98, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562185_Estad-Inferenc-Juarez2002.pdf', '2024-11-25 14:16:25'),
(99, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562879_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 14:27:59'),
(100, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562925_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 14:28:45'),
(101, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732562948_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 14:29:08'),
(102, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732563012_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 14:30:12'),
(103, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732563023_EstaNoParame-ARDILA-OK_1.pdf', '2024-11-25 14:30:23'),
(104, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732563046_EstaNoParame-ARDILA-OK.pdf', '2024-11-25 14:30:46'),
(107, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732634403_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:20:03'),
(108, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732634403_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:20:03'),
(110, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732634470_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:21:10'),
(111, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732634863_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:27:43'),
(112, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732634863_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:27:43'),
(115, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732636408_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:53:28'),
(116, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732636408_EstaNoParame-ARDILA-OK.pdf', '2024-11-26 10:53:29'),
(120, 1, 'imagen', 'Foto de Docente', '1732816988_427385269_414394368295075_3155024189884265456_n.jpg', '2024-11-28 13:03:08'),
(121, 1, 'pdf', 'ssss', '1732829006_Spearman.pdf', '2024-11-28 16:23:26'),
(122, 1, 'pdf', 'dsdsdsa', '1732829857_RR-2641-2024-R-UNA-con-REGLAMENTO_1.pdf', '2024-11-28 16:37:37'),
(123, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732896774_RR-2641-2024-R-UNA-con-REGLAMENTO_1.pdf', '2024-11-29 11:12:54'),
(124, 1, 'pdf', 'Ingeniería Estadística e informática ', '1732896775_Spearman.pdf', '2024-11-29 11:12:55'),
(125, 1, 'documento', 'Constancia de Habilitación', '1732904599_Spearman.pdf', '2024-11-29 13:23:19'),
(128, 1, 'pdf', 'Ingeniería Estadística e informática ', '1733158602_CamScanner_02-12-2024_10.11.pdf', '2024-12-02 11:56:42'),
(129, 1, 'pdf', 'Ingeniería Estadística e informática ', '1733158602_RR-2641-2024-R-UNA-con-REGLAMENTO_1.pdf', '2024-12-02 11:56:42'),
(134, 1, 'pdf', 'Memorándum de Asignación de Carga', '1733344868_Chi_cuadrado.pdf', '2024-12-04 15:41:08'),
(135, 4, 'pdf', 'Memorándum de Asignación de Carga', '1733854287_Chi_cuadrado.pdf', '2024-12-10 13:11:27'),
(136, 9, 'imagen', 'Foto de Docente', '1733930185_427385269_414394368295075_3155024189884265456_n.jpg', '2024-12-11 10:16:25'),
(137, 9, 'documento', 'Constancia de Habilitación', '1733930186_Formato_de_proyecto_de_tesis_-b_Finesi_1.pdf', '2024-12-11 10:16:26'),
(138, 9, 'imagen', 'Ingeniería Estadística e informática ', '1733936544_Enei.jpg', '2024-12-11 12:02:24'),
(139, 9, 'pdf', 'Ingeniería Estadística e informática ', '1733936544_Formato_de_proyecto_de_tesis_-b_Finesi_1.pdf', '2024-12-11 12:02:24'),
(141, 1, 'imagen', 'Ingeniería Informática ', '1734035993_Enei.jpg', '2024-12-12 15:39:53'),
(142, 1, 'pdf', 'Ingeniería Informática ', '1734035994_Informe_de_incidencias.pdf', '2024-12-12 15:39:54');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `investigaciones`
--

CREATE TABLE `investigaciones` (
  `id_investigacion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Artículo Científico','Artículo Aceptado','Artículo en Congreso','Registro de Patente','Informe de Investigación','Participación en Publicación Científica') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `titulo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `revista` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `indice` enum('Thomson Reuters','Scopus','Web of Science','Scielo','Latin Index','Otro') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `autor` tinyint(1) DEFAULT NULL,
  `coautor` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `investigaciones`
--

INSERT INTO `investigaciones` (`id_investigacion`, `id_usuario`, `tipo`, `titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `revista`, `indice`, `fecha_publicacion`, `autor`, `coautor`, `puntaje`, `id_imagen`) VALUES
(3, 1, 'Artículo Aceptado', 'dfd', 'dfsdf', '2020-03-06', '2022-03-06', 'science', 'Scopus', '2023-03-06', 1, 0, NULL, 64);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `participaciontesis`
--

CREATE TABLE `participaciontesis` (
  `id_participaciontesis` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Director','Asesor','Jurado') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nivel` enum('Pregrado','Posgrado') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `universidad` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `participaciontesis`
--

INSERT INTO `participaciontesis` (`id_participaciontesis`, `id_usuario`, `tipo`, `nivel`, `descripcion`, `fecha`, `universidad`, `puntaje`, `id_imagen`) VALUES
(2, 1, 'Asesor', 'Pregrado', 'ssss', '2023-03-06', 'Universidad Nacional Del Altiplano', NULL, 56);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `produccionintelectual`
--

CREATE TABLE `produccionintelectual` (
  `id_produccion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Texto Universitario','Traducción de Libro','Capítulo de Libro','Obra Literaria','Manual de Prácticas','Guía de Enseñanza','Monografía') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `titulo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `isbn` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `deposito_legal` tinyint(1) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `autor` tinyint(1) DEFAULT NULL,
  `coautor` tinyint(1) DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `editorial_prestigiosa` enum('No','Scopus','Web of Science','SciELO') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'No'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `produccionintelectual`
--

INSERT INTO `produccionintelectual` (`id_produccion`, `id_usuario`, `tipo`, `titulo`, `isbn`, `deposito_legal`, `fecha_publicacion`, `autor`, `coautor`, `puntaje`, `id_imagen`, `editorial_prestigiosa`) VALUES
(4, 1, 'Texto Universitario', 'Jhon Wilber', 'dssds', 1, '2024-03-06', 1, 0, NULL, 65, 'Scopus');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ratificacionpuntos`
--

CREATE TABLE `ratificacionpuntos` (
  `id_puntaje` int NOT NULL,
  `id_usuario` int NOT NULL,
  `criterio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `puntaje_obtenido` decimal(5,2) NOT NULL,
  `detalles` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reconocimientos`
--

CREATE TABLE `reconocimientos` (
  `id_reconocimiento` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tipo` enum('Docente Visitante','Premio Internacional','Premio Nacional','Miembro de Sociedad Científica Internacional','Miembro de Sociedad Científica Nacional','Distinción Académica','Resolución Rectoral','Resolución Decanal') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `institucion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `tipo_institucion` enum('Universidad','Sociedad Científica','Organización Internacional','Organización Nacional','Gobierno','Empresa Privada','Otra') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reconocimientos`
--

INSERT INTO `reconocimientos` (`id_reconocimiento`, `id_usuario`, `tipo`, `descripcion`, `institucion`, `fecha`, `puntaje`, `id_imagen`, `tipo_institucion`) VALUES
(5, 1, 'Premio Nacional', 'ssss', 'MA', '2023-03-06', NULL, 62, 'Universidad');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `softwareespecializado`
--

CREATE TABLE `softwareespecializado` (
  `id_software` int NOT NULL,
  `id_usuario` int NOT NULL,
  `nombre_curso` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modalidad` enum('Presencial','Virtual') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `institucion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL,
  `top_1000` tinyint(1) DEFAULT '0',
  `nombre_institucion` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `softwareespecializado`
--

INSERT INTO `softwareespecializado` (`id_software`, `id_usuario`, `nombre_curso`, `modalidad`, `horas`, `institucion`, `fecha`, `puntaje`, `id_imagen`, `top_1000`, `nombre_institucion`) VALUES
(11, 1, 'Hola mundo 2', 'Presencial', 20, 'Universidad', '2024-03-06', NULL, 59, 1, 'Las americas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tutorias`
--

CREATE TABLE `tutorias` (
  `id_tutoria` int NOT NULL,
  `id_usuario` int NOT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `anio` int DEFAULT NULL,
  `puntaje` decimal(5,2) DEFAULT NULL,
  `id_imagen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL,
  `usuario` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `contraseña` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rol` enum('Administrador','Docente','Administrativo') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `contraseña`, `rol`) VALUES
(1, 'admin', '$2b$12$NUnPsZ5KK12e2PgpAxoh8u2/z6ZmNZdaqwd5tlNW8.CkBnr8YvNN6', 'Administrador'),
(4, 'Prueba', '$2a$12$L3.lzToyQ0Ig8szPPwypseMkA.NvcWfI2vnQrx.KNxVwvAqf..UIe', 'Docente'),
(6, 'admin12', '$2b$12$d7sTiFuOg0LEP8lXY7ylEOI78ygLvPWdxo7sKIpuDvmtWkpuA7Im.', 'Docente'),
(7, 'OGARCIA', '$2b$12$mkCxfYAgu/h29NCu6G4vTuK2NG0V589f7eUF00QNVZrZBHy3RLbU6', 'Administrador'),
(8, 'japazaq@unap.edu.pe', '$2b$12$6IZdOliWzALWd2BhBe7.uutMUXHmRFwhx88mla9E4T3e9mRkKovsa', 'Administrador'),
(9, 'jajataa@est.unap.edu.pe', '$2b$12$cB8wY91/2AQ4bT/lA2Q.I.rdnmGl31ZyxEbjMa04o8sd.fEoDCqT2', 'Administrador');

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
-- Indices de la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  ADD PRIMARY KEY (`id_actividad`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_actividades_imagenes` (`id_imagen`);

--
-- Indices de la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  ADD PRIMARY KEY (`id_capacitacion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_actualizaciones_imagenes` (`id_imagen`);

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
-- Indices de la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  ADD PRIMARY KEY (`id_carga`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_memorandum` (`id_memorandum`);

--
-- Indices de la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  ADD PRIMARY KEY (`id_cargo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_cargos_imagenes` (`id_imagen`);

--
-- Indices de la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  ADD PRIMARY KEY (`id_datos`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_foto_docente` (`id_foto_docente`),
  ADD KEY `fk_constancia_habilitacion` (`id_constancia_habilitacion`);

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
-- Indices de la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  ADD PRIMARY KEY (`id_evaluacion`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  ADD PRIMARY KEY (`id_experiencia`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_experienciadocente_imagenes` (`id_imagen`);

--
-- Indices de la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  ADD PRIMARY KEY (`id_grado`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_gradostitulos_imagenesadjuntas` (`id_imagen`),
  ADD KEY `fk_gradostitulos_imagen_sunedu` (`id_imagen_sunedu`);

--
-- Indices de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  ADD PRIMARY KEY (`id_idioma`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_idiomas_imagenes` (`id_imagen`);

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
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_investigaciones_imagenes` (`id_imagen`);

--
-- Indices de la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  ADD PRIMARY KEY (`id_participaciontesis`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_participaciontesis_imagenes` (`id_imagen`);

--
-- Indices de la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  ADD PRIMARY KEY (`id_produccion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_produccionintelectual_imagenes` (`id_imagen`);

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
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_reconocimientos_imagenes` (`id_imagen`);

--
-- Indices de la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  ADD PRIMARY KEY (`id_software`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_softwareespecializado_imagenes` (`id_imagen`);

--
-- Indices de la tabla `tutorias`
--
ALTER TABLE `tutorias`
  ADD PRIMARY KEY (`id_tutoria`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `fk_tutorias_imagenes` (`id_imagen`);

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
-- AUTO_INCREMENT de la tabla `acreditacionlicenciamiento`
--
ALTER TABLE `acreditacionlicenciamiento`
  MODIFY `id_acreditacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  MODIFY `id_actividad` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  MODIFY `id_capacitacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `administrativosinfoadicional`
--
ALTER TABLE `administrativosinfoadicional`
  MODIFY `id_administrativo_info` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `archivosevidencias`
--
ALTER TABLE `archivosevidencias`
  MODIFY `id_archivo` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cargalectiva`
--
ALTER TABLE `cargalectiva`
  MODIFY `id_carga` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  MODIFY `id_carga` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  MODIFY `id_cargo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  MODIFY `id_datos` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `docentesinfoadicional`
--
ALTER TABLE `docentesinfoadicional`
  MODIFY `id_docente_info` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `evaluacionesdesempeno`
--
ALTER TABLE `evaluacionesdesempeno`
  MODIFY `id_evaluacion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  MODIFY `id_evaluacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  MODIFY `id_experiencia` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  MODIFY `id_grado` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  MODIFY `id_idioma` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `imagenesadjuntas`
--
ALTER TABLE `imagenesadjuntas`
  MODIFY `id_imagen` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143;

--
-- AUTO_INCREMENT de la tabla `investigaciones`
--
ALTER TABLE `investigaciones`
  MODIFY `id_investigacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  MODIFY `id_participaciontesis` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  MODIFY `id_produccion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `ratificacionpuntos`
--
ALTER TABLE `ratificacionpuntos`
  MODIFY `id_puntaje` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reconocimientos`
--
ALTER TABLE `reconocimientos`
  MODIFY `id_reconocimiento` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  MODIFY `id_software` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `tutorias`
--
ALTER TABLE `tutorias`
  MODIFY `id_tutoria` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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

--
-- Filtros para la tabla `actividadesproyeccionsocial`
--
ALTER TABLE `actividadesproyeccionsocial`
  ADD CONSTRAINT `actividadesproyeccionsocial_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_actividades_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL;

--
-- Filtros para la tabla `actualizacionescapacitaciones`
--
ALTER TABLE `actualizacionescapacitaciones`
  ADD CONSTRAINT `actualizacionescapacitaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_actualizaciones_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL;

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
-- Filtros para la tabla `carga_academica_lectiva`
--
ALTER TABLE `carga_academica_lectiva`
  ADD CONSTRAINT `carga_academica_lectiva_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `carga_academica_lectiva_ibfk_2` FOREIGN KEY (`id_memorandum`) REFERENCES `imagenesadjuntas` (`id_imagen`);

--
-- Filtros para la tabla `cargosdirectivos`
--
ALTER TABLE `cargosdirectivos`
  ADD CONSTRAINT `cargosdirectivos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_cargos_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL;

--
-- Filtros para la tabla `datospersonales`
--
ALTER TABLE `datospersonales`
  ADD CONSTRAINT `datospersonales_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_constancia_habilitacion` FOREIGN KEY (`id_constancia_habilitacion`) REFERENCES `imagenesadjuntas` (`id_imagen`),
  ADD CONSTRAINT `fk_foto_docente` FOREIGN KEY (`id_foto_docente`) REFERENCES `imagenesadjuntas` (`id_imagen`);

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
-- Filtros para la tabla `evaluacion_desempeno_docente`
--
ALTER TABLE `evaluacion_desempeno_docente`
  ADD CONSTRAINT `evaluacion_desempeno_docente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `experienciadocente`
--
ALTER TABLE `experienciadocente`
  ADD CONSTRAINT `experienciadocente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_experienciadocente_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL;

--
-- Filtros para la tabla `gradostitulos`
--
ALTER TABLE `gradostitulos`
  ADD CONSTRAINT `fk_gradostitulos_imagen_sunedu` FOREIGN KEY (`id_imagen_sunedu`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_gradostitulos_imagenesadjuntas` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `gradostitulos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `idiomas`
--
ALTER TABLE `idiomas`
  ADD CONSTRAINT `fk_idiomas_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
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
  ADD CONSTRAINT `fk_investigaciones_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `investigaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `participaciontesis`
--
ALTER TABLE `participaciontesis`
  ADD CONSTRAINT `fk_participaciontesis_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `participaciontesis_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `produccionintelectual`
--
ALTER TABLE `produccionintelectual`
  ADD CONSTRAINT `fk_produccionintelectual_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
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
  ADD CONSTRAINT `fk_reconocimientos_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `reconocimientos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `softwareespecializado`
--
ALTER TABLE `softwareespecializado`
  ADD CONSTRAINT `fk_softwareespecializado_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `softwareespecializado_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tutorias`
--
ALTER TABLE `tutorias`
  ADD CONSTRAINT `fk_tutorias_imagenes` FOREIGN KEY (`id_imagen`) REFERENCES `imagenesadjuntas` (`id_imagen`) ON DELETE SET NULL,
  ADD CONSTRAINT `tutorias_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
