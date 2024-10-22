create table usuarios ( --Angel
    ID SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    perfil VARCHAR(15) NOT NULL
);


CREATE TABLE cliente ( --Angel
    id_cliente bigserial PRIMARY KEY,
    nombre varchar(50),
    telefono varchar(10), 
    email varchar(100),
    puntos bigint
);

CREATE TABLE proveedores ( --Balam
    id_proveedor bigserial PRIMARY KEY,
    compania varchar(100),
    telefono varchar(11),
    correo varchar(70)
);

CREATE TABLE articulos_proveedores ( --Balam
    id_proveedor bigint,
    id_articulo bigint,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_articulo) REFERENCES articulos(id_articulo)
);

CREATE TABLE reabastecimientos ( --Zuzuky
    id_reabastecimiento bigserial PRIMARY KEY,
    id_proveedor bigint,
    id_usuario bigint,
    fecha date,
    monto float,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(ID)
);

CREATE TABLE articulos ( --Zuzuky
    id_articulo bigserial PRIMARY KEY,
    nombre varchar(100),
    precio float,
    cantidad bigint,
    maximos bigint,
    minimos bigint
);

CREATE TABLE articulos_reabastecimientos ( --Zuzuky
    id_reabastecimiento bigint,
    id_articulo bigint,
    cantidad bigint,
    precio_unitario float,
    subtotal float,
    FOREIGN KEY (id_articulo) REFERENCES articulos(id_articulo),
    FOREIGN KEY (id_reabastecimiento) REFERENCES reabastecimientos(id_reabastecimiento)
);

CREATE TABLE compras ( --Angel
    id_compra bigserial PRIMARY KEY,
    id_usuario bigint,
    id_cliente bigint,
    fecha date,
    subtotal float,
    descuento float,
    total float,
    puntos_acumulados float,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(ID),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE articulos_compras ( --Balam
    id_compra bigint,
    id_articulo bigint,
    cantidad bigint,
    subtotal float,
    FOREIGN KEY (id_articulo) REFERENCES articulos(id_articulo),
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra)
);


-- INSERT VALUES PARA PRUEBAS 
INSERT INTO usuarios (username, password, nombre, perfil) VALUES 
('angel123', 'angel', 'Angel Parada', 'Admin'),
('balam2023', 'balam', 'Balam Perez', 'Farmacéutico'),
('zuzuky99', 'zuzuky', 'Zuzuky Lopez', 'Cajera');

INSERT INTO cliente (nombre, telefono, email, puntos) VALUES 
('Carlos Gonzalez', '5551234567', 'carlos.gonzalez@example.com', 0),
('Ana Martinez', '5557654321', 'ana.martinez@example.com', 0),
('Pedro Ramirez', '5559876543', 'pedro.ramirez@example.com', 0);

INSERT INTO proveedores (compania, telefono, correo) VALUES 
('Medicamentos Global', '55511223344', 'ventas@medicamentosglobal.com'),
('Salud Farma', '55522334455', 'contacto@saludfarma.com'),
('Distribuidora Pharma', '55533445566', 'atencion@distribuidorapharma.com');

INSERT INTO reabastecimientos (id_proveedor, id_usuario, fecha, monto) VALUES 
(1, 1, '2024-10-21', 5000.00),
(2, 2, '2024-09-15', 1500.50),
(3, 3, '2024-08-10', 800.75);

INSERT INTO articulos_reabastecimientos (id_reabastecimiento, id_articulo, cantidad, precio_unitario, subtotal) VALUES 
(1, 1, 300, 25.00, 7500.00),
(2, 2, 150, 35.50, 5325.00),
(3, 3, 50, 70.00, 3500.00);

INSERT INTO articulos (nombre, precio, cantidad, maximos, minimos) VALUES 
('Amoxicilina 500mg', 60.00, 150, 300, 50),
('Omeprazol 20mg', 45.00, 200, 400, 60),
('Aspirina 100mg', 25.00, 500, 1000, 100),
('Vitamina C 500mg', 30.00, 250, 600, 80),
('Gel antibacterial 500ml', 75.00, 100, 300, 30),
('Alcohol etílico 70% 1L', 50.00, 200, 400, 50),
('Tiras reactivas para glucosa (50 uds)', 200.00, 50, 150, 10),
('Termómetro digital', 120.00, 30, 100, 10),
('Nebulizador portátil', 850.00, 20, 50, 5),
('Venda elástica 10cm', 35.00, 100, 200, 20),
('Esparadrapo 5cm', 20.00, 150, 300, 30),
('Solución salina 1L', 40.00, 50, 150, 10),
('Cintas adhesivas para curación', 15.00, 200, 500, 50),
('Jarabe para la gripe 100ml', 80.00, 70, 200, 10),
('Crema antibiótica 30g', 90.00, 40, 100, 10),
('Pastillas antialérgicas 10mg', 55.00, 300, 600, 50);

INSERT INTO articulos_proveedores (id_proveedor, id_articulo) VALUES 
(1, 1), -- Medicamentos Global provee Amoxicilina
(1, 2), -- Medicamentos Global provee Omeprazol
(1, 3), -- Medicamentos Global provee Aspirina
(2, 4), -- Salud Farma provee Vitamina C
(2, 5), -- Salud Farma provee Gel antibacterial
(2, 6), -- Salud Farma provee Alcohol etílico
(3, 7), -- Distribuidora Pharma provee Tiras reactivas para glucosa
(3, 8), -- Distribuidora Pharma provee Termómetro digital
(3, 9), -- Distribuidora Pharma provee Nebulizador portátil
(1, 10), -- Medicamentos Global provee Venda elástica
(2, 11), -- Salud Farma provee Esparadrapo
(2, 12), -- Salud Farma provee Solución salina
(3, 13), -- Distribuidora Pharma provee Cintas adhesivas para curación
(1, 14), -- Medicamentos Global provee Jarabe para la gripe
(2, 15), -- Salud Farma provee Crema antibiótica
(3, 16); -- Distribuidora Pharma provee Pastillas antialérgicas


