-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2024 a las 13:57:49
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
-- Base de datos: `inscripcion_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grados`
--

CREATE TABLE `grados` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `ciclo` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grados`
--

INSERT INTO `grados` (`id`, `nombre`, `ciclo`) VALUES
(1, 'Primero', 'Primaria'),
(2, 'Segundo', 'Primaria'),
(3, 'Tercero', 'Primaria'),
(4, 'Cuarto', 'Primaria'),
(5, 'Quinto', 'Primaria'),
(6, 'Sexto', 'Primaria'),
(7, 'Primero', 'Secundaria'),
(8, 'Segundo', 'Secundaria'),
(9, 'Tercero', 'Secundaria'),
(10, 'Cuarto', 'Secundaria'),
(11, 'Quinto', 'Secundaria'),
(12, 'Sexto', 'Secundaria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscriptions`
--

CREATE TABLE `inscriptions` (
  `id` int(11) NOT NULL,
  `id_student` int(11) NOT NULL,
  `id_grado` int(11) NOT NULL,
  `id_section` int(11) NOT NULL,
  `nombre_tutor` varchar(100) NOT NULL,
  `celular_tutor` varchar(15) NOT NULL,
  `direccion_estudiante` varchar(255) NOT NULL,
  `estado` enum('activo','expulsado','retirado','abandonado','inactivo') DEFAULT 'activo',
  `año_escolar` int(4) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inscriptions`
--

INSERT INTO `inscriptions` (`id`, `id_student`, `id_grado`, `id_section`, `nombre_tutor`, `celular_tutor`, `direccion_estudiante`, `estado`, `año_escolar`, `created_at`, `updated_at`) VALUES
(1, 2, 1, 2, 'brayan', '7272631', 'av. viva', 'activo', 2024, '2024-12-08 17:21:28', '2024-12-08 17:21:28'),
(2, 6, 2, 4, 'daniel', '213213', 'av. fortaleza', 'activo', 2024, '2024-12-08 18:45:00', '2024-12-08 18:45:00'),
(3, 9, 1, 2, 'brayan', '21321', 'av .lslsksksjk', 'activo', 2024, '2024-12-08 18:48:29', '2024-12-08 18:48:29'),
(4, 8, 2, 4, 'ndksandksla', '321321', 'ndksandal', 'activo', 2024, '2024-12-08 18:51:01', '2024-12-08 18:51:01'),
(5, 5, 2, 4, 'SBJAKD', '12312', 'ndskaldsa', 'activo', 2024, '2024-12-08 18:53:08', '2024-12-08 18:53:08'),
(6, 10, 1, 2, 'dbnsajdkb', '21321', 'ndksaln', 'activo', 2024, '2024-12-08 18:58:07', '2024-12-08 18:58:07'),
(7, 13, 1, 2, 'dnskal', '3213', 'dnsakldn', 'activo', 2024, '2024-12-08 19:05:20', '2024-12-08 19:05:20'),
(8, 12, 2, 5, 'dnsakld', '2321', 'ndksaln', 'activo', 2024, '2024-12-08 19:09:08', '2024-12-08 19:09:08'),
(9, 14, 6, 13, 'd nsak', '21321', 'ndksladnl', 'activo', 2024, '2024-12-08 19:11:34', '2024-12-08 19:11:34'),
(10, 15, 4, 9, 'dbjsakd', '21321', 'ndskandkla', 'activo', 2024, '2024-12-09 02:01:03', '2024-12-09 02:01:03'),
(11, 16, 4, 9, 'prueba', '21312', 'ndksadnsa', 'activo', 2024, '2024-12-09 14:23:30', '2024-12-09 14:23:30'),
(12, 17, 4, 9, 'Daniel', '73636212', 'Av. Los andes', 'activo', 2024, '2024-12-09 20:45:27', '2024-12-09 20:45:27'),
(13, 18, 4, 9, 'Juan', '7363221', 'Av. Los Andes', 'activo', 2024, '2024-12-09 21:15:13', '2024-12-09 21:15:13'),
(14, 19, 2, 4, 'Angel Ramiro', '73636212', 'Av. Los pinos', 'activo', 2024, '2024-12-10 00:13:46', '2024-12-10 00:13:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sections`
--

CREATE TABLE `sections` (
  `id` int(11) NOT NULL,
  `nombre` char(1) NOT NULL,
  `id_grado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sections`
--

INSERT INTO `sections` (`id`, `nombre`, `id_grado`) VALUES
(1, 'W', 7),
(2, 'B', 1),
(3, 'C', 1),
(4, 'A', 2),
(5, 'B', 2),
(6, 'A', 3),
(7, 'B', 3),
(8, 'C', 3),
(9, 'A', 4),
(10, 'B', 4),
(11, 'A', 5),
(12, 'B', 5),
(13, 'A', 6),
(14, 'B', 6),
(15, 'F', 5),
(20, 'S', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `nombres` varchar(45) NOT NULL,
  `apellidos` varchar(45) NOT NULL,
  `ci` varchar(20) NOT NULL,
  `genero` char(1) NOT NULL,
  `num_celular` varchar(15) DEFAULT NULL,
  `fecha_nacimiento` date NOT NULL,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `fecha_ingreso` date NOT NULL,
  `id_user` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `students`
--

INSERT INTO `students` (`id`, `nombres`, `apellidos`, `ci`, `genero`, `num_celular`, `fecha_nacimiento`, `estado`, `fecha_ingreso`, `id_user`) VALUES
(1, 'Juan peres editado', 'Pérez', '12345678', 'F', '789456123', '2008-05-08', 'inactivo', '2023-02-15', 5),
(2, 'Ana', 'Gómez', '87654321', 'F', '789654321', '2009-09-22', 'activo', '2023-02-15', 1),
(3, 'Luis', 'Rodríguez', '11223344', 'M', '741852963', '2007-01-18', 'inactivo', '2023-03-10', 1),
(4, 'María', 'Fernández', '22334455', 'F', '963852741', '2010-11-05', 'inactivo', '2022-05-20', 1),
(5, 'Pedro', 'López', '33445566', 'M', '951753852', '2006-04-14', 'activo', '2023-01-01', 1),
(6, 'Laura', 'Torres', '44556677', 'F', '789456321', '2009-12-25', 'activo', '2023-02-15', 1),
(7, 'Carlos', 'Vargas', '55667788', 'M', '852963147', '2007-07-08', 'inactivo', '2021-09-10', 1),
(8, 'Isabel', 'Morales', '66778899', 'F', '753951852', '2008-02-28', 'activo', '2023-01-25', 1),
(9, 'Diego editado', 'Hernández', '77889900', 'M', '789321654', '2009-06-16', 'activo', '0000-00-00', 5),
(10, 'Lucía', 'Ramírez', '88990011', 'F', '654987321', '2010-03-30', 'activo', '2023-02-15', 1),
(12, 'nuevo', 'nuevo', '9900', 'M', '321321', '2024-11-27', 'activo', '2024-12-08', 5),
(13, 'dmslamd', 'mldsaml', '321', 'M', '21321', '2024-12-07', 'activo', '2024-12-08', 5),
(14, 'prueba', 'apelidos de prueba', '12345', 'M', '321321', '2024-12-06', 'activo', '2024-12-07', 5),
(15, 'prueba2', 'prueba', '2321', 'M', '33213', '2024-12-05', 'activo', '2024-12-05', 5),
(16, 'prueba2', 'apellido', '444', 'F', '123', '2024-12-04', 'activo', '2024-12-09', 5),
(17, 'Juanito', 'Mamani', '222', 'M', '76353623', '2016-06-21', 'activo', '2024-12-09', 8),
(18, 'Antonio', 'Mamani', '656565', 'M', '76353623', '2019-02-14', 'activo', '2024-12-06', 8),
(19, 'Martha', 'Morales ', '321321', 'F', '7635251', '2020-06-08', 'activo', '2024-12-09', 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stundent_notes`
--

CREATE TABLE `stundent_notes` (
  `id` int(11) NOT NULL,
  `id_inscription` int(11) NOT NULL,
  `id_subject` int(11) NOT NULL,
  `nota1` decimal(5,2) DEFAULT 0.00,
  `nota2` decimal(5,2) DEFAULT 0.00,
  `nota3` decimal(5,2) DEFAULT 0.00,
  `nota4` decimal(5,2) DEFAULT 0.00,
  `promedio` decimal(5,2) GENERATED ALWAYS AS ((`nota1` + `nota2` + `nota3` + `nota4`) / 4) STORED,
  `observaciones` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `stundent_notes`
--

INSERT INTO `stundent_notes` (`id`, `id_inscription`, `id_subject`, `nota1`, `nota2`, `nota3`, `nota4`, `observaciones`, `created_at`, `updated_at`) VALUES
(13, 7, 1, 20.00, 22.00, 0.00, 0.00, 'observacio edito', '2024-12-08 19:05:20', '2024-12-08 21:16:03'),
(14, 7, 2, 19.99, 30.00, 40.00, 50.00, 'nada', '2024-12-08 19:05:20', '2024-12-08 21:11:34'),
(15, 7, 3, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:05:20', '2024-12-08 19:05:20'),
(16, 7, 4, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:05:20', '2024-12-08 19:05:20'),
(17, 8, 5, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:09:08', '2024-12-08 19:09:08'),
(18, 8, 6, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:09:08', '2024-12-08 19:09:08'),
(19, 8, 7, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:09:08', '2024-12-08 19:09:08'),
(20, 8, 8, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:09:08', '2024-12-08 19:09:08'),
(21, 9, 21, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:11:34', '2024-12-08 19:11:34'),
(22, 9, 22, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:11:34', '2024-12-08 19:11:34'),
(23, 9, 23, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:11:34', '2024-12-08 19:11:34'),
(24, 9, 24, 0.00, 0.00, 0.00, 0.00, '', '2024-12-08 19:11:34', '2024-12-08 19:11:34'),
(25, 10, 13, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 02:01:03', '2024-12-09 02:01:03'),
(26, 10, 14, 100.00, 100.00, 100.00, 100.00, '', '2024-12-09 02:01:03', '2024-12-09 02:36:31'),
(27, 10, 15, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 02:01:03', '2024-12-09 02:01:03'),
(28, 10, 16, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 02:01:03', '2024-12-09 02:01:03'),
(29, 11, 13, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 14:23:30', '2024-12-09 14:23:30'),
(30, 11, 14, 50.00, 0.00, 0.00, 0.00, '', '2024-12-09 14:23:30', '2024-12-09 14:56:12'),
(31, 11, 15, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 14:23:30', '2024-12-09 14:23:30'),
(32, 11, 16, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 14:23:30', '2024-12-09 14:23:30'),
(33, 12, 13, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 20:45:27', '2024-12-09 20:45:27'),
(34, 12, 14, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 20:45:27', '2024-12-09 20:45:27'),
(35, 12, 15, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 20:45:27', '2024-12-09 20:45:27'),
(36, 12, 16, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 20:45:27', '2024-12-09 20:45:27'),
(37, 13, 13, 80.00, 90.00, 70.00, 80.00, '', '2024-12-09 21:15:13', '2024-12-09 21:29:07'),
(38, 13, 14, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 21:15:13', '2024-12-09 21:15:13'),
(39, 13, 15, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 21:15:13', '2024-12-09 21:15:13'),
(40, 13, 16, 0.00, 0.00, 0.00, 0.00, '', '2024-12-09 21:15:13', '2024-12-09 21:15:13'),
(41, 14, 5, 100.00, 90.00, 80.00, 45.00, '', '2024-12-10 00:13:46', '2024-12-10 00:17:01'),
(42, 14, 6, 0.00, 0.00, 0.00, 0.00, '', '2024-12-10 00:13:46', '2024-12-10 00:13:46'),
(43, 14, 7, 90.00, 0.00, 0.00, 0.00, '', '2024-12-10 00:13:46', '2024-12-10 00:17:35'),
(44, 14, 8, 0.00, 0.00, 0.00, 0.00, '', '2024-12-10 00:13:46', '2024-12-10 00:13:46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `id_grado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `subjects`
--

INSERT INTO `subjects` (`id`, `nombre`, `id_grado`) VALUES
(1, 'Matemáticas', 1),
(2, 'Ciencias Naturales', 1),
(3, 'Lenguaje', 1),
(4, 'Arte y Cultura', 1),
(5, 'Matemáticas', 2),
(6, 'Ciencias Sociales', 2),
(7, 'Lenguaje y Comunicación', 2),
(8, 'Educación Física', 2),
(9, 'Matemáticas', 3),
(10, 'Historia', 3),
(11, 'Lenguaje y Literatura', 3),
(12, 'Música', 3),
(13, 'Matemáticas Avanzadas', 4),
(14, 'Ciencias Naturales y Biología', 4),
(15, 'Redacción y Ortografía', 4),
(16, 'Computación Básica', 4),
(17, 'Álgebra Básica', 5),
(18, 'Geografía', 5),
(19, 'Expresión Oral y Escrita', 5),
(20, 'Ciencias Ambientales', 5),
(21, 'Geometría', 6),
(22, 'Historia del Perú', 6),
(23, 'Lenguaje y Literatura Avanzada', 6),
(24, 'Proyectos de Ciencia', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `subject_teacher`
--

CREATE TABLE `subject_teacher` (
  `id` int(11) NOT NULL,
  `id_teacher` int(11) NOT NULL,
  `id_subject` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `subject_teacher`
--

INSERT INTO `subject_teacher` (`id`, `id_teacher`, `id_subject`) VALUES
(1, 33, 9),
(6, 43, 9),
(7, 43, 10),
(15, 42, 5),
(16, 42, 6),
(17, 35, 1),
(18, 35, 2),
(19, 51, 17),
(20, 51, 18),
(21, 54, 14),
(22, 54, 15),
(23, 55, 13),
(24, 55, 15),
(25, 55, 16),
(29, 56, 13),
(30, 56, 14),
(31, 56, 15),
(32, 56, 16),
(35, 57, 5),
(36, 57, 6),
(37, 57, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `sexo` enum('masculino','femenino') NOT NULL,
  `ci` varchar(20) NOT NULL,
  `num_celular` varchar(15) DEFAULT NULL,
  `fecha_ingreso` date NOT NULL,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `id_user` int(11) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `teachers`
--

INSERT INTO `teachers` (`id`, `nombres`, `apellidos`, `sexo`, `ci`, `num_celular`, `fecha_ingreso`, `estado`, `id_user`, `create_at`, `update_at`) VALUES
(2, 'teacher', 'apellidos', 'femenino', '123131', '82312381', '2024-11-14', 'activo', 1, '2024-11-29 16:25:41', '2024-11-29 16:45:05'),
(3, 'brayan', 'sonco machaca', 'femenino', '12450302', '75888457', '2024-11-29', 'activo', 1, '2024-11-29 16:40:47', '2024-11-29 16:44:55'),
(4, 'ediado', 'nkdlsa', 'femenino', 'ndksla', '12132', '2024-11-11', 'activo', 1, '2024-11-29 16:51:29', '2024-12-02 13:43:14'),
(5, 'editado', 'dsadsa', 'masculino', 'dsadsa', '123', '2024-11-15', 'inactivo', 1, '2024-11-29 16:58:15', '2024-11-29 17:08:17'),
(6, 'editado', 'sadsad', 'masculino', 'dasdsa', 'dasdsa', '2024-11-15', 'inactivo', 1, '2024-11-29 17:15:32', '2024-12-05 15:25:47'),
(7, 'dasdda', 'sdasaddsadsa', 'femenino', 'dasda', 'dsadsa', '2024-11-22', 'activo', 1, '2024-11-29 17:15:48', '2024-11-29 17:15:48'),
(8, 'editado', 'nkdasnl', 'femenino', 'nkdlals', 'ndksal', '2024-11-23', 'inactivo', 5, '2024-11-29 17:16:48', '2024-11-29 17:19:00'),
(10, 'dsadsa', 'dsadsa', 'masculino', '12312313', '321321313', '2024-12-03', 'inactivo', 5, '2024-12-04 23:09:58', '2024-12-05 20:12:46'),
(11, 'dsadsad', 'dsdsad', 'femenino', '2331321', '123213', '2024-12-03', 'activo', 5, '2024-12-04 23:29:09', '2024-12-04 23:29:09'),
(12, 'dsadsadsa', 'dsadadsa', 'masculino', '12323213', '23123232', '2024-12-03', 'activo', 5, '2024-12-04 23:40:44', '2024-12-04 23:40:44'),
(14, 'dsadsadsa', 'dsadsadsa', 'masculino', '12321', '21332', '2024-12-04', 'activo', 5, '2024-12-04 23:50:14', '2024-12-04 23:50:14'),
(15, 'dsads', 'dsadsa', 'femenino', '1231', '32231', '2024-12-02', 'activo', 5, '2024-12-04 23:53:02', '2024-12-04 23:53:02'),
(18, 'dsadsad', 'dsadsad', 'femenino', '123123', '321332', '2024-12-03', 'activo', 5, '2024-12-05 00:02:28', '2024-12-05 00:02:28'),
(19, 'ddsadas', 'dsadsa', 'femenino', '1221', '3231', '2024-12-03', 'activo', 5, '2024-12-05 00:07:21', '2024-12-05 00:07:21'),
(20, 'dsadsa', 'dsadsa', 'masculino', '21321', '213', '2024-12-03', 'activo', 5, '2024-12-05 00:08:04', '2024-12-05 00:08:04'),
(22, 'dsadsa', 'dsadsa', 'femenino', '2131', '3213', '2024-12-03', 'activo', 5, '2024-12-05 00:09:29', '2024-12-05 00:09:29'),
(26, 'dsadsa', 'dsadsa', 'femenino', '1232', '21323', '2024-12-03', 'activo', 5, '2024-12-05 00:17:07', '2024-12-05 00:17:07'),
(27, 'dasdasdsa', 'dasdsa', 'femenino', '3213', '3213', '2024-12-02', 'activo', 5, '2024-12-05 00:19:35', '2024-12-05 00:19:35'),
(28, 'dsadsad', 'dsadsa', 'femenino', '3232', '3123', '2024-11-25', 'activo', 5, '2024-12-05 00:24:17', '2024-12-05 00:24:17'),
(29, 'dassda', 'dsdsa', 'femenino', '3321321', '12332', '2024-12-03', 'activo', 5, '2024-12-05 00:32:17', '2024-12-05 00:32:17'),
(30, 'dsadsa', 'dsads', 'femenino', '32321', '321321', '2024-12-03', 'activo', 5, '2024-12-05 00:38:01', '2024-12-05 00:38:01'),
(31, 'dasdsadsa', 'dsadsadsa', 'femenino', '211', '222', '2024-12-03', 'activo', 5, '2024-12-05 00:41:42', '2024-12-05 00:41:42'),
(32, 'dasdsa', 'dssda', 'masculino', '3231', '12321', '2024-12-03', 'activo', 5, '2024-12-05 00:44:57', '2024-12-05 00:44:57'),
(33, 'dadsdas', 'dsad', 'masculino', '31232', '2332', '2024-12-03', 'activo', 5, '2024-12-05 00:47:33', '2024-12-05 00:47:33'),
(35, 'editado 22', 'dsad', 'femenino', '32121', '231321', '2024-12-03', 'activo', 5, '2024-12-05 00:48:26', '2024-12-05 15:25:33'),
(36, 'dsadsa', 'dsadsad', 'femenino', '3223132', '231231', '2024-12-03', 'activo', 5, '2024-12-05 00:54:01', '2024-12-05 00:54:01'),
(37, 'ddas', 'dsdadas', 'masculino', '23321', '23123', '2024-12-10', 'activo', 5, '2024-12-05 00:58:20', '2024-12-05 00:58:20'),
(38, 'dsadsa', 'dsasda', 'femenino', '123321', '3223', '2024-11-30', 'activo', 5, '2024-12-05 14:40:11', '2024-12-05 14:40:11'),
(39, 'dsadas', 'dsadsa', 'femenino', '213', '32132', '2024-12-04', 'activo', 5, '2024-12-05 14:41:06', '2024-12-05 14:41:06'),
(42, 'dasdsa', 'dsadsa', 'femenino', '123', '321', '2024-12-03', 'activo', 5, '2024-12-05 14:46:01', '2024-12-05 14:46:01'),
(43, 'profesor 1', 'apeliodo', 'femenino', '123213', '312231', '2024-12-04', 'activo', 5, '2024-12-05 14:54:51', '2024-12-05 14:54:51'),
(51, 'editado', 'sdadsa', 'femenino', '999', '231231', '2024-12-03', 'activo', 5, '2024-12-05 15:22:45', '2024-12-05 20:12:23'),
(53, 'angel', 'dsadsa', 'masculino', '998', '123', '2024-12-04', 'inactivo', 5, '2024-12-05 18:51:56', '2024-12-05 20:09:50'),
(54, 'brayan', 'sonco', 'masculino', '124503021', '32718937912', '2024-12-06', 'activo', 5, '2024-12-09 01:36:45', '2024-12-09 01:36:45'),
(55, 'Alberto', 'Quispe', 'masculino', '333', '76532312', '2024-12-06', 'activo', 8, '2024-12-09 20:43:16', '2024-12-09 20:43:16'),
(56, 'pablo', 'Quispe', 'masculino', '321321', '76353623', '2024-12-09', 'activo', 8, '2024-12-09 21:13:42', '2024-12-09 21:13:42'),
(57, 'jaime', 'Serrano', 'masculino', '66666', '75888457', '2024-12-09', 'activo', 8, '2024-12-10 00:11:41', '2024-12-10 00:11:41');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `usuario` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `nombre_completo` varchar(255) DEFAULT NULL,
  `rol` enum('administrador','docente','estudiante') NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `usuario`, `contrasena`, `nombre_completo`, `rol`, `estado`, `created_at`, `updated_at`) VALUES
(1, 'brayan', 'scrypt:32768:8:1$glVZMIjpDl46RExW$fb3b39879300f8597c4121f909cea72d0945b6c7901d357509257c3292b51250ad4a4a15019a048f366f613a5743e1d8576a563805f9c59df1f2d2bb16dcd224', 'brayan sonco machaca', 'docente', 'activo', '2024-11-29 15:11:34', '2024-11-29 15:14:39'),
(2, 'estudiante', 'scrypt:32768:8:1$BPqf2axbKRYOFXc1$876fd66b212756e7a40028e2488cc6b6fd3e7f70785da8f93af25fa0770c9a17d642f7295c109dcf00cf5b950c4fee562e9a4d6ab3bd016e1c4ca8fa05d5fecd', 'Persona estudiante', 'estudiante', 'inactivo', '2024-11-29 15:11:59', '2024-11-29 15:28:30'),
(4, 'usuario2', 'scrypt:32768:8:1$DH78YGulMIEAgbJY$98ec22b733fe217a3b7786a9eebd2d390dc6f3026a80a0b3d6239249e6d5c2f7aec940efb332a4e9aacf11bd429f8baf267b5b47bed8ab48481cf0d93beccadc', 'nombre completo', 'docente', 'activo', '2024-11-29 16:48:49', '2024-11-29 16:48:49'),
(5, 'admin', 'scrypt:32768:8:1$O4SjOyF9m5Zutl6X$5aae6ec365ac3b087c1339a3f43345a5aaadea41df2290ea69a41e38996be4399a59fe6fb86ad460417fcf6ca426c3c66905144f2dbed52c3ba4e2a0c3253ae5', 'administrador GAA', 'administrador', 'activo', '2024-11-29 17:16:16', '2024-11-29 17:16:16'),
(6, 'neko', 'scrypt:32768:8:1$8KDf4UcxWo0xTI1s$1000eb859a4e863c1042bebed9546fe39d0464e378cae9262cfa8316d1f27371bc18fe74f47d92d8c71e0ffdc424cb37a7ab964fcf0e1c3e62a409245895679d', 'neko dark', 'docente', 'activo', '2024-12-09 00:48:33', '2024-12-09 00:48:33'),
(7, '124503021', 'scrypt:32768:8:1$OBm5ViencnZSlMsS$7e69fca02f2a4f1e7c24bf36fac60d4bf7c846a07df821aa7e276fc7463daf755c765c924fa00febf92ab805887ca79a7d3b2a60ef6901a0b66ee034fa12046b', 'brayan sonco', 'docente', 'activo', '2024-12-09 01:36:45', '2024-12-09 01:36:45'),
(8, 'administrador', 'scrypt:32768:8:1$jbyy7e5ve2WpszVj$ec73b8ac8be7147f1553d59cf9e091391b108d87bdddf9d49abffd7b2ae3a627b5eef81a7303c5fcc40bdbe1b827c94ef9e4c685619ae147b5fb64ec862cbd1e', 'Brayan Sonco Machcaca', 'administrador', 'activo', '2024-12-09 19:52:14', '2024-12-09 19:52:14'),
(9, '333', 'scrypt:32768:8:1$W34KUdNjpNIamAGX$264fe5aeba4067e90564eb2dbc0d84bb605301ad3bed7d4f0742d0cfc5c27819cb338763ea955c3b216c71ff3bbedd86a5fcab475b8f467bba90dea84abb7ff3', 'Alberto Quispe', 'docente', 'inactivo', '2024-12-09 20:43:16', '2024-12-09 21:09:22'),
(10, '321321', 'scrypt:32768:8:1$EwxQTQyBcc5izX8C$b343078dfedf9560b4aa39b92bf2e5b8af6a880e37a0aa7db96b367991b5987ad37fda9a18af10a38cb3ba1e45f7682ad836b6806fc2ff84904b5d673ab423ff', 'pablo Quispe', 'docente', 'activo', '2024-12-09 21:13:42', '2024-12-09 21:13:42'),
(11, '66666', 'scrypt:32768:8:1$ZXrW3ZnOslGUCkLP$edc441fa574924f11858fec95e31e228f71d486f88e40979035fda1e73d7f5cb7fa8ea7bb92c0deabfcf4afcc330ea8ce9d3960b14eb52b30efc814b5a260ac7', 'jaime Serrano', 'docente', 'activo', '2024-12-10 00:11:41', '2024-12-10 00:11:41');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `grados`
--
ALTER TABLE `grados`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inscriptions`
--
ALTER TABLE `inscriptions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_student` (`id_student`),
  ADD KEY `id_grado` (`id_grado`),
  ADD KEY `id_section` (`id_section`);

--
-- Indices de la tabla `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_grado` (`id_grado`);

--
-- Indices de la tabla `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `stundent_notes`
--
ALTER TABLE `stundent_notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_inscription` (`id_inscription`),
  ADD KEY `id_subject` (`id_subject`);

--
-- Indices de la tabla `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_grado` (`id_grado`);

--
-- Indices de la tabla `subject_teacher`
--
ALTER TABLE `subject_teacher`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_teacher` (`id_teacher`),
  ADD KEY `id_subject` (`id_subject`);

--
-- Indices de la tabla `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ci` (`ci`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `grados`
--
ALTER TABLE `grados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `inscriptions`
--
ALTER TABLE `inscriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `sections`
--
ALTER TABLE `sections`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `stundent_notes`
--
ALTER TABLE `stundent_notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `subject_teacher`
--
ALTER TABLE `subject_teacher`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT de la tabla `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inscriptions`
--
ALTER TABLE `inscriptions`
  ADD CONSTRAINT `inscriptions_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `inscriptions_ibfk_2` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id`),
  ADD CONSTRAINT `inscriptions_ibfk_3` FOREIGN KEY (`id_section`) REFERENCES `sections` (`id`);

--
-- Filtros para la tabla `sections`
--
ALTER TABLE `sections`
  ADD CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id`);

--
-- Filtros para la tabla `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `stundent_notes`
--
ALTER TABLE `stundent_notes`
  ADD CONSTRAINT `stundent_notes_ibfk_1` FOREIGN KEY (`id_inscription`) REFERENCES `inscriptions` (`id`),
  ADD CONSTRAINT `stundent_notes_ibfk_2` FOREIGN KEY (`id_subject`) REFERENCES `subjects` (`id`);

--
-- Filtros para la tabla `subjects`
--
ALTER TABLE `subjects`
  ADD CONSTRAINT `subjects_ibfk_1` FOREIGN KEY (`id_grado`) REFERENCES `grados` (`id`);

--
-- Filtros para la tabla `subject_teacher`
--
ALTER TABLE `subject_teacher`
  ADD CONSTRAINT `subject_teacher_ibfk_1` FOREIGN KEY (`id_teacher`) REFERENCES `teachers` (`id`),
  ADD CONSTRAINT `subject_teacher_ibfk_2` FOREIGN KEY (`id_subject`) REFERENCES `subjects` (`id`);

--
-- Filtros para la tabla `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
