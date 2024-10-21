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
