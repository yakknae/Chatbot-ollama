-- SQLite no tiene CREATE DATABASE ni COLLATE complejos, se ignoran

-- Tabla categorias
CREATE TABLE IF NOT EXISTS categorias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT
);

INSERT OR IGNORE INTO categorias (id, nombre, descripcion) VALUES
  (1, 'Lacteos', NULL),
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

-- Tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  apellido TEXT,
  direccion TEXT,
  telefono TEXT,
  email TEXT UNIQUE,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla compras
CREATE TABLE IF NOT EXISTS compras (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proveedor_id INTEGER NOT NULL,
  fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_compra REAL NOT NULL,
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- Tabla detallescompra
CREATE TABLE IF NOT EXISTS detallescompra (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  compra_id INTEGER NOT NULL,
  producto_id INTEGER NOT NULL,
  cantidad INTEGER NOT NULL,
  precio_unitario_compra REAL NOT NULL,
  subtotal REAL NOT NULL,
  FOREIGN KEY (compra_id) REFERENCES compras(id),
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla detallesventa
CREATE TABLE IF NOT EXISTS detallesventa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  venta_id INTEGER NOT NULL,
  producto_id INTEGER NOT NULL,
  cantidad INTEGER NOT NULL,
  precio_unitario_venta REAL NOT NULL,
  subtotal REAL NOT NULL,
  FOREIGN KEY (venta_id) REFERENCES ventas(id),
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla marcas
CREATE TABLE IF NOT EXISTS marcas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE
);

INSERT OR IGNORE INTO marcas (id, nombre) VALUES
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
  (99, 'CBSé'),
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

-- Tabla productoproveedor
CREATE TABLE IF NOT EXISTS productoproveedor (
  proveedor_id INTEGER NOT NULL,
  producto_id INTEGER NOT NULL,
  precio_compra REAL,
  fecha_ultima_compra TIMESTAMP,
  PRIMARY KEY (proveedor_id, producto_id),
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla productos
CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  precio_costo REAL NOT NULL,
  precio_venta REAL NOT NULL,
  stock INTEGER NOT NULL DEFAULT 0,
  marca_id INTEGER,
  categoria_id INTEGER,
  codigo_barras TEXT UNIQUE,
  fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (marca_id) REFERENCES marcas(id),
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla proveedores
CREATE TABLE IF NOT EXISTS proveedores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  contacto TEXT,
  telefono TEXT,
  email TEXT,
  direccion TEXT
);

-- Tabla ventas
CREATE TABLE IF NOT EXISTS ventas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id INTEGER,
  fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_venta REAL NOT NULL,
  metodo_pago TEXT,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

INSERT INTO productos (
  id, nombre, descripcion, precio_costo, precio_venta,
  stock, marca_id, categoria_id, codigo_barras, fecha_alta
) VALUES
(1, 'Yerba Mate Marolio', 'Yerba mate elaborada tradicional', 80.0, 150.0, 100, 1, 1, '7790000000011', '2025-01-01'),
(2, 'Aceite de Girasol Natura', 'Aceite vegetal 1L', 200.0, 300.0, 50, 2, 2, '7790000000028', '2025-01-01'),
(3, 'Arroz Largo Fino Molto', 'Arroz blanco 1kg', 90.0, 170.0, 80, 3, 3, '7790000000035', '2025-01-01'),
(4, 'Fideos Tirabuzón Lucchetti', 'Fideos secos 500g', 70.0, 120.0, 60, 4, 4, '7790000000042', '2025-01-01'),
(5, 'Galletitas Criollitas Bagley', 'Galletitas saladas 3x100g', 100.0, 180.0, 30, 5, 5, '7790000000059', '2025-01-01'),
(6, 'Dulce de Leche La Serenísima', 'Clásico 400g', 150.0, 250.0, 40, 6, 6, '7790000000066', '2025-01-01'),
(7, 'Harina 0000 Pureza', 'Harina refinada 1kg', 85.0, 140.0, 90, 7, 7, '7790000000073', '2025-01-01'),
(8, 'Azúcar Ledesma', 'Azúcar común 1kg', 95.0, 160.0, 70, 8, 8, '7790000000080', '2025-01-01'),
(9, 'Sal Fina Dos Anclas', 'Sal refinada 500g', 40.0, 80.0, 100, 9, 9, '7790000000097', '2025-01-01'),
(10, 'Café Molido La Morenita', 'Café torrado 250g', 300.0, 420.0, 25, 10, 10, '7790000000103', '2025-01-01'),
(11, 'Leche Entera La Serenísima', 'Leche entera larga vida 1L', 120.0, 190.0, 60, 6, 11, '7790000000110', '2025-01-01'),
(12, 'Manteca Sancor', 'Manteca 200g', 250.0, 350.0, 40, 11, 12, '7790000000127', '2025-01-01'),
(13, 'Queso Cremoso Ilolay', 'Queso cremoso 1kg', 900.0, 1200.0, 15, 12, 13, '7790000000134', '2025-01-01'),
(14, 'Huevos Blancos x12', 'Maple de huevos', 600.0, 750.0, 20, 13, 14, '7790000000141', '2025-01-01'),
(15, 'Pan Lactal Fargo', 'Pan blanco 500g', 130.0, 220.0, 30, 14, 15, '7790000000158', '2025-01-01'),
(16, 'Jugo Baggio Multifruta', 'Jugo en caja 1L', 110.0, 180.0, 50, 15, 16, '7790000000165', '2025-01-01'),
(19, 'Agua Mineral Villavicencio 2L', 'Sin gas', 150.0, 220.0, 45, 17, 18, '7790000000196', '2025-01-01'),
(20, 'Cerveza Quilmes 1L', 'Rubia retornable', 300.0, 450.0, 60, 18, 19, '7790000000202', '2025-01-01'),
(21, 'Vino Toro Tinto 1L', 'Vino de mesa', 280.0, 400.0, 25, 19, 20, '7790000000219', '2025-01-01'),
(23, 'Aceitunas Nucete Verdes', 'Frasco 300g', 350.0, 520.0, 20, 21, 21, '7790000000233', '2025-01-01'),
(24, 'Atún en Lata La Campagnola', 'Al natural 170g', 270.0, 390.0, 35, 22, 22, '7790000000240', '2025-01-01'),
(25, 'Puré de Tomate Arcor', 'Caja 520g', 90.0, 160.0, 60, 23, 23, '7790000000257', '2025-01-01'),
(26, 'Salsa Fileto Knorr', 'Sachet 340g', 100.0, 180.0, 40, 24, 23, '7790000000264', '2025-01-01'),
(30, 'Galletitas Chocolinas Bagley', 'Chocolate 170g', 170.0, 280.0, 30, 5, 5, '7790000000301', '2025-01-01'),
(33, 'Caramelos Media Hora', 'Bolsa 100g', 90.0, 150.0, 50, 30, 25, '7790000000332', '2025-01-01'),
(34, 'Chicles Topline Menta', 'Pack x6', 120.0, 200.0, 40, 31, 25, '7790000000349', '2025-01-01'),
(35, 'Chocolate Águila Negro', 'Tableta 100g', 250.0, 370.0, 20, 32, 26, '7790000000356', '2025-01-01'),
(36, 'Turrón Arcor', 'Maní 25g', 50.0, 100.0, 60, 23, 25, '7790000000363', '2025-01-01'),
(37, 'Alfajor Jorgito', 'Doble chocolate', 90.0, 160.0, 35, 33, 27, '7790000000370', '2025-01-01'),
(39, 'Helado Grido Vainilla', 'Pote 1L', 500.0, 700.0, 10, 35, 28, '7790000000394', '2025-01-01'),
(40, 'Helado Frigor Bon o Bon', 'Pote 1L', 550.0, 750.0, 8, 36, 28, '7790000000400', '2025-01-01'),
(41, 'Papas Lays Clásicas', 'Paquete 80g', 250.0, 360.0, 30, 37, 29, '7790000000417', '2025-01-01'),
(42, 'Maní Salado Georgalos', 'Paquete 100g', 140.0, 220.0, 45, 38, 29, '7790000000424', '2025-01-01'),
(43, 'Galletitas de Arroz', 'Sin sal 100g', 100.0, 180.0, 50, 39, 5, '7790000000431', '2025-01-01'),
(44, 'Barra de Cereal Cerealitas', 'Avena y miel', 90.0, 160.0, 40, 40, 30, '7790000000448', '2025-01-01'),
(45, 'Yogur Yogurísimo Frutilla', 'Bebible 1L', 300.0, 450.0, 25, 6, 31, '7790000000455', '2025-01-01'),
(46, 'Postre Danette Chocolate', 'Vaso 100g', 100.0, 180.0, 30, 41, 31, '7790000000462', '2025-01-01'),
(47, 'Gelatina Ser Frutilla', 'Sobre 20g', 30.0, 80.0, 60, 42, 31, '7790000000479', '2025-01-01'),
(48, 'Cacao Nesquik', 'Polvo 400g', 250.0, 390.0, 35, 43, 32, '7790000000486', '2025-01-01'),
(49, 'Leche Chocolatada Cindor', 'Botella 1L', 270.0, 400.0, 20, 44, 32, '7790000000493', '2025-01-01');
