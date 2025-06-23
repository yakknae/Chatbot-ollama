-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.7.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para pp3_proyecto
CREATE DATABASE IF NOT EXISTS `pp3_proyecto` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `pp3_proyecto`;

-- Volcando estructura para tabla pp3_proyecto.categorias
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.categorias: ~50 rows (aproximadamente)
INSERT IGNORE INTO `categorias` (`id`, `nombre`, `descripcion`) VALUES
	(1, 'Lácteos', NULL),
	(2, 'Quesos', NULL),
	(3, 'Yogures', NULL),
	(4, 'Dulces y postres', NULL),
	(5, 'Galletitas', NULL),
	(6, 'Snacks', NULL),
	(7, 'Golocinas', NULL),
	(8, 'Cereales', NULL),
	(9, 'Conservas', NULL),
	(10, 'Jugos', NULL),
	(11, 'Bebidas sin alcohol', NULL),
	(12, 'Bebidas en polvo', NULL),
	(13, 'Carnes procesadas', NULL),
	(14, 'Embutidos', NULL),
	(15, 'Congelados', NULL),
	(16, 'Aceites y aderezos', NULL),
	(17, 'Mayonesas', NULL),
	(18, 'Salsas', NULL),
	(19, 'Pastas secas', NULL),
	(20, 'Arroz y legumbres', NULL),
	(21, 'Productos para desayuno', NULL),
	(22, 'Café y té', NULL),
	(23, 'Infusiones', NULL),
	(24, 'Electrodomésticos', NULL),
	(25, 'Pequeños electrodomésticos', NULL),
	(26, 'Tecnología', NULL),
	(27, 'Notebooks y PCs', NULL),
	(28, 'Componentes de PC', NULL),
	(29, 'TV y audio', NULL),
	(30, 'Colchones', NULL),
	(31, 'Sommier', NULL),
	(32, 'Muebles', NULL),
	(33, 'Decoración', NULL),
	(34, 'Pinturas', NULL),
	(35, 'Materiales para construcción', NULL),
	(36, 'Ferretería', NULL),
	(37, 'Hogar y jardín', NULL),
	(38, 'Juguetes', NULL),
	(39, 'Artículos escolares', NULL),
	(40, 'Ropa y calzado', NULL),
	(41, 'Calzado deportivo', NULL),
	(42, 'Supermercado', NULL),
	(43, 'Retail', NULL),
	(44, 'Perfumería y limpieza', NULL),
	(45, 'Productos de higiene personal', NULL),
	(46, 'Productos de limpieza', NULL),
	(47, 'Frutas y verduras', NULL),
	(48, 'Panadería', NULL),
	(49, 'Alimentos secos', NULL),
	(50, 'Alimentos enlatados', NULL);

-- Volcando estructura para tabla pp3_proyecto.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.clientes: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pp3_proyecto.compras
CREATE TABLE IF NOT EXISTS `compras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proveedor_id` int(11) NOT NULL,
  `fecha_compra` timestamp NULL DEFAULT current_timestamp(),
  `total_compra` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_compras_proveedores` (`proveedor_id`),
  CONSTRAINT `fk_compras_proveedores` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.compras: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pp3_proyecto.detallescompra
CREATE TABLE IF NOT EXISTS `detallescompra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `compra_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario_compra` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detallescompra_compra` (`compra_id`),
  KEY `fk_detallescompra_producto` (`producto_id`),
  CONSTRAINT `fk_detallescompra_compra` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`),
  CONSTRAINT `fk_detallescompra_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.detallescompra: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pp3_proyecto.detallesventa
CREATE TABLE IF NOT EXISTS `detallesventa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `venta_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario_venta` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detallesventa_venta` (`venta_id`),
  KEY `fk_detallesventa_producto` (`producto_id`),
  CONSTRAINT `fk_detallesventa_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  CONSTRAINT `fk_detallesventa_venta` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.detallesventa: ~0 rows (aproximadamente)

-- Volcando estructura para procedimiento pp3_proyecto.insertar_categorias
DELIMITER //
CREATE PROCEDURE `insertar_categorias`()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 10000 DO
    INSERT INTO Categorias (nombre, descripcion)
    VALUES (
      CONCAT('Categoria ', LPAD(i, 5, '0')),
      CONCAT('Descripción de la categoría ', i)
    );
    SET i = i + 1;
  END WHILE;
END//
DELIMITER ;

-- Volcando estructura para procedimiento pp3_proyecto.insertar_marcas
DELIMITER //
CREATE PROCEDURE `insertar_marcas`()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 10000 DO
    INSERT INTO Marcas (nombre)
    VALUES (CONCAT('Marca ', LPAD(i, 5, '0')));
    SET i = i + 1;
  END WHILE;
END//
DELIMITER ;

-- Volcando estructura para procedimiento pp3_proyecto.insertar_productos
DELIMITER //
CREATE PROCEDURE `insertar_productos`()
BEGIN
  DECLARE i INT DEFAULT 1;
  WHILE i <= 10000 DO
    INSERT INTO Productos (
      nombre, descripcion, precio_costo, precio_venta,
      stock, marca_id, categoria_id, codigo_barras
    ) VALUES (
      CONCAT('Producto ', LPAD(i, 5, '0')),
      CONCAT('Descripción del producto ', i),
      ROUND(10 + (RAND() * 90), 2),
      ROUND(100 + (RAND() * 400), 2),
      FLOOR(1 + RAND() * 100),
      FLOOR(1 + RAND() * 10000),
      FLOOR(1 + RAND() * 10000),
      CONCAT('CB', LPAD(i, 10, '0'))
    );
    SET i = i + 1;
  END WHILE;
END//
DELIMITER ;

-- Volcando estructura para tabla pp3_proyecto.marcas
CREATE TABLE IF NOT EXISTS `marcas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.marcas: ~74 rows (aproximadamente)
INSERT IGNORE INTO `marcas` (`id`, `nombre`) VALUES
	(31, 'Acer Argentina'),
	(41, 'Aluar'),
	(2, 'Arcor'),
	(64, 'Atma'),
	(18, 'Baggio'),
	(4, 'Bagley'),
	(12, 'Bambi'),
	(29, 'Banghó'),
	(84, 'Braun'),
	(77, 'Cannon'),
	(32, 'Carrefour Argentina'),
	(21, 'Cetrogar'),
	(25, 'Colchones Cannon'),
	(26, 'Colchones Piero'),
	(34, 'Coto'),
	(86, 'CX'),
	(7, 'Danone Argentina'),
	(33, 'Disco'),
	(43, 'Dos Anclas'),
	(57, 'Drean'),
	(36, 'Easy'),
	(20, 'Electrodomésticos Liliana'),
	(59, 'Eskabe'),
	(55, 'Eurocase'),
	(53, 'Exo'),
	(61, 'Fortaleza Muebles'),
	(38, 'Fric-Rot'),
	(83, 'Gama'),
	(42, 'Georgalos'),
	(17, 'Grido'),
	(13, 'Havanna'),
	(50, 'Hellmann’s'),
	(48, 'Ilolay'),
	(35, 'Jumbo'),
	(54, 'Ken Brown'),
	(51, 'Knorr'),
	(76, 'Koil'),
	(49, 'La Campagnola'),
	(1, 'La Serenísima'),
	(45, 'La Virginia'),
	(14, 'Ledesma'),
	(52, 'Marolio'),
	(60, 'Mite'),
	(3, 'Molinos Río de la Plata'),
	(46, 'Molto'),
	(24, 'Muebles Nodari'),
	(23, 'Musimundo'),
	(44, 'Natura'),
	(19, 'Newsan'),
	(9, 'Noblex'),
	(85, 'Oral-B'),
	(58, 'Orbis'),
	(8, 'Paladini'),
	(56, 'Patrick'),
	(47, 'Paty'),
	(28, 'PCBox Argentina'),
	(81, 'Peabody'),
	(63, 'Peter Wells'),
	(11, 'Philco Argentina'),
	(80, 'Philips'),
	(79, 'Piero'),
	(30, 'Positivo BGH'),
	(40, 'Rasti'),
	(22, 'Roca'),
	(62, 'Safari'),
	(6, 'Sancor'),
	(82, 'Sanyo'),
	(10, 'Siam'),
	(39, 'Sinteplast'),
	(37, 'Sodimac'),
	(27, 'Sommier Center'),
	(78, 'Suavestar'),
	(5, 'Terrabusi'),
	(15, 'Tersuave'),
	(16, 'Topper');

-- Volcando estructura para tabla pp3_proyecto.productoproveedor
CREATE TABLE IF NOT EXISTS `productoproveedor` (
  `proveedor_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `fecha_ultima_compra` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`proveedor_id`,`producto_id`),
  KEY `fk_productoproveedor_producto` (`producto_id`),
  CONSTRAINT `fk_productoproveedor_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  CONSTRAINT `fk_productoproveedor_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.productoproveedor: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pp3_proyecto.productos
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio_costo` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `marca_id` int(11) DEFAULT NULL,
  `categoria_id` int(11) DEFAULT NULL,
  `codigo_barras` varchar(50) DEFAULT NULL,
  `fecha_alta` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_barras` (`codigo_barras`),
  KEY `fk_productos_marcas` (`marca_id`),
  KEY `fk_productos_categorias` (`categoria_id`),
  CONSTRAINT `fk_productos_categorias` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`),
  CONSTRAINT `fk_productos_marcas` FOREIGN KEY (`marca_id`) REFERENCES `marcas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.productos: ~44 rows (aproximadamente)
INSERT IGNORE INTO `productos` (`id`, `nombre`, `descripcion`, `precio_costo`, `precio_venta`, `stock`, `marca_id`, `categoria_id`, `codigo_barras`, `fecha_alta`) VALUES
	(2, 'Yerba Mate Marolio', 'Yerba mate elaborada tradicional', 80.00, 120.00, 200, 52, 1, '779123456002', '2025-05-25 21:13:28'),
	(3, 'Salame Paladini', 'Salame tipo milán de Paladini', 150.00, 200.00, 50, 8, 14, '779123456003', '2025-05-25 21:13:28'),
	(4, 'Dulce de Leche La Serenísima', 'Dulce de leche clásico', 100.00, 150.00, 80, 1, 4, '779123456004', '2025-05-25 21:13:28'),
	(5, 'Aceite de Girasol Natura', 'Aceite de girasol 1L', 90.00, 130.00, 120, 42, 16, '779123456005', '2025-05-25 21:13:28'),
	(6, 'Notebook Banghó Max', 'Notebook Banghó con procesador Intel i5', 50000.00, 65000.00, 30, 29, 26, '779123456006', '2025-05-25 21:13:28'),
	(7, 'PC de Escritorio EXO', 'Computadora de escritorio EXO básica', 40000.00, 55000.00, 25, 53, 26, '779123456007', '2025-05-25 21:13:28'),
	(8, 'All in One Ken Brown', 'Computadora All in One Ken Brown 21"', 45000.00, 60000.00, 20, 54, 26, '779123456008', '2025-05-25 21:13:28'),
	(9, 'Tablet CX', 'Tablet CX de 10 pulgadas', 30000.00, 40000.00, 40, 86, 26, '779123456009', '2025-05-25 21:13:28'),
	(10, 'Monitor Eurocase 24"', 'Monitor LED Eurocase de 24 pulgadas', 20000.00, 27000.00, 35, 55, 26, '779123456010', '2025-05-25 21:13:28'),
	(11, 'Heladera Patrick 320L', 'Heladera Patrick con freezer superior', 60000.00, 75000.00, 15, 56, 3, '779123456011', '2025-05-25 21:13:28'),
	(12, 'Lavarropas Drean Next 6.06', 'Lavarropas automático Drean 6kg', 55000.00, 70000.00, 10, 57, 3, '779123456012', '2025-05-25 21:13:28'),
	(13, 'Cocina Orbis 4 Hornallas', 'Cocina a gas Orbis con horno', 50000.00, 65000.00, 12, 58, 3, '779123456013', '2025-05-25 21:13:28'),
	(14, 'Estufa Eskabe TB 5000', 'Estufa a gas Eskabe tiro balanceado 5000 kcal', 25000.00, 32000.00, 18, 59, 3, '779123456014', '2025-05-25 21:13:28'),
	(15, 'Aire Acondicionado BGH 3000W', 'Aire acondicionado BGH frío/calor 3000W', 45000.00, 60000.00, 8, 30, 3, '779123456015', '2025-05-25 21:13:28'),
	(16, 'Silla de Oficina Mite', 'Silla ergonómica para oficina marca Mite', 8000.00, 12000.00, 20, 60, 28, '779123456016', '2025-05-25 21:13:28'),
	(17, 'Escritorio Genoud', 'Escritorio de madera para computadora', 10000.00, 15000.00, 10, 61, 28, '779123456017', '2025-05-25 21:13:28'),
	(18, 'Mesa de Comedor Peter Wells', 'Mesa de comedor para 6 personas', 15000.00, 20000.00, 5, 63, 28, '779123456018', '2025-05-25 21:13:28'),
	(19, 'Sillón Safari', 'Sillón de 2 cuerpos tapizado', 12000.00, 18000.00, 7, 62, 28, '779123456019', '2025-05-25 21:13:28'),
	(20, 'Biblioteca Seis Mobiliario', 'Biblioteca de madera con 5 estantes', 9000.00, 13000.00, 9, 61, 28, '779123456020', '2025-05-25 21:13:28'),
	(21, 'Colchón King Koil 2 Plazas', 'Colchón de resortes 2 plazas', 20000.00, 25000.00, 6, 76, 29, '779123456021', '2025-05-25 21:13:28'),
	(22, 'Somier Piero 1 Plaza', 'Somier de 1 plaza con colchón', 15000.00, 20000.00, 8, 23, 29, '779123456022', '2025-05-25 21:13:28'),
	(23, 'Colchón Cannon 2 Plazas', 'Colchón espuma alta densidad', 18000.00, 23000.00, 5, 24, 29, '779123456023', '2025-05-25 21:13:28'),
	(24, 'Somier Suavestar Queen', 'Somier Queen con base y colchón', 22000.00, 28000.00, 4, 78, 29, '779123456024', '2025-05-25 21:13:28'),
	(25, 'Colchón La Cardeuse 1 Plaza', 'Colchón de espuma 1 plaza', 12000.00, 16000.00, 10, 79, 29, '779123456025', '2025-05-25 21:13:28'),
	(26, 'Licuadora Atma 600W', 'Licuadora de 600W con vaso de vidrio', 5000.00, 7000.00, 15, 64, 23, '779123456026', '2025-05-25 21:13:28'),
	(27, 'Tostadora Liliana 2 Rebanadas', 'Tostadora eléctrica para 2 rebanadas', 3000.00, 4500.00, 20, 20, 23, '779123456027', '2025-05-25 21:13:28'),
	(28, 'Cafetera Philips 1L', 'Cafetera eléctrica de 1 litro', 4000.00, 6000.00, 12, 80, 23, '779123456028', '2025-05-25 21:13:28'),
	(29, 'Batidora Peabody 300W', 'Batidora de mano 300W', 3500.00, 5000.00, 18, 81, 23, '779123456029', '2025-05-25 21:13:28'),
	(30, 'Microondas Sanyo 20L', 'Microondas digital de 20 litros', 8000.00, 10000.00, 10, 82, 23, '779123456030', '2025-05-25 21:13:28'),
	(31, 'Secador de Pelo Gama 2000W', 'Secador de pelo profesional 2000W', 4000.00, 5500.00, 25, 83, 42, '779123456031', '2025-05-25 21:13:28'),
	(32, 'Plancha de Pelo Philips', 'Plancha alisadora de cerámica', 3500.00, 5000.00, 20, 80, 42, '779123456032', '2025-05-25 21:13:28'),
	(33, 'Afeitadora Eléctrica Braun', 'Afeitadora recargable', 6000.00, 8000.00, 15, 84, 42, '779123456033', '2025-05-25 21:13:28'),
	(34, 'Depiladora Philips Satinelle', 'Depiladora eléctrica compacta', 4500.00, 6000.00, 18, 80, 42, '779123456034', '2025-05-25 21:13:28'),
	(35, 'Cepillo Eléctrico Oral-B', 'Cepillo dental eléctrico recargable', 3000.00, 4500.00, 22, 85, 42, '779123456035', '2025-05-25 21:13:28'),
	(46, 'Galletitas Chocolinas Bagley', 'Galletitas de chocolate clásicas de Bagley', 120.00, 160.00, 50, 3, 5, '779500002001', '2025-05-25 21:28:55'),
	(47, 'Galletitas Opera Bagley', 'Galletitas rellenas sabor vainilla', 135.00, 180.00, 60, 3, 5, '779500002002', '2025-05-25 21:28:55'),
	(48, 'Galletitas Rex Bagley', 'Galletitas crocantes ideales para el desayuno', 110.00, 150.00, 80, 3, 5, '779500002003', '2025-05-25 21:28:55'),
	(49, 'Galletitas Diversión Bagley', 'Con formas divertidas y sabor a vainilla', 140.00, 185.00, 40, 3, 5, '779500002004', '2025-05-25 21:28:55'),
	(50, 'Galletitas Manón Bagley', 'Clásicas galletitas dulces sabor vainilla', 125.00, 170.00, 70, 3, 5, '779500002005', '2025-05-25 21:28:55'),
	(51, 'Galletitas Mini Diversión Bagley', 'Mini galletitas dulces para llevar', 100.00, 135.00, 90, 3, 5, '779500002006', '2025-05-25 21:28:55'),
	(52, 'Galletitas Tentación Bagley', 'Rellenas con crema de chocolate', 145.00, 190.00, 35, 3, 5, '779500002007', '2025-05-25 21:28:55'),
	(53, 'Galletitas Mellizas Bagley', 'Rellenas con dulce de leche', 130.00, 175.00, 45, 3, 5, '779500002008', '2025-05-25 21:28:55'),
	(54, 'Galletitas Variedad Familiar Bagley', 'Mix de galletitas dulces y saladas', 180.00, 240.00, 30, 3, 5, '779500002009', '2025-05-25 21:28:55'),
	(55, 'Galletitas Arroz Bagley', 'Galletitas livianas a base de arroz', 115.00, 155.00, 65, 3, 5, '779500002010', '2025-05-25 21:28:55');

-- Volcando estructura para tabla pp3_proyecto.proveedores
CREATE TABLE IF NOT EXISTS `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `contacto` varchar(255) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.proveedores: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pp3_proyecto.ventas
CREATE TABLE IF NOT EXISTS `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) DEFAULT NULL,
  `fecha_venta` timestamp NULL DEFAULT current_timestamp(),
  `total_venta` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ventas_clientes` (`cliente_id`),
  CONSTRAINT `fk_ventas_clientes` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Volcando datos para la tabla pp3_proyecto.ventas: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
