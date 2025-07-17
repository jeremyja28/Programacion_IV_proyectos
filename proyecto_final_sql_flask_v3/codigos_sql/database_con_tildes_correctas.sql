-- Base de datos con tildes y ñ correctas
-- Configuración UTF-8 para caracteres especiales

DROP DATABASE IF EXISTS proyecto_final_version2;
CREATE DATABASE proyecto_final_version2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE proyecto_final_version2;

-- Configurar la sesión para UTF-8
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear tabla provincias
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear tabla ciudades
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear tabla rutas
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    peso DECIMAL(8,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id),
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Insertar usuario administrador
INSERT INTO usuarios (username, email, password_hash, es_admin) VALUES
('admin', 'admin@sistema.com', '$2b$12$0zG8YsQPYKYf5NnQjKZb7u.8oLHH8JDlWm9MWEgQmJuSvLyqLZ5ay', TRUE);

-- Insertar provincias con tildes correctas
INSERT INTO provincias (nombre, codigo) VALUES
('Pichincha', 'PIC'),
('Guayas', 'GUA'),
('Azuay', 'AZU'),
('Manabí', 'MAN'),
('Tungurahua', 'TUN'),
('Imbabura', 'IMB'),
('Loja', 'LOJ'),
('El Oro', 'ORO'),
('Esmeraldas', 'ESM'),
('Chimborazo', 'CHI'),
('Cotopaxi', 'COT'),
('Los Ríos', 'LRI'),
('Cañar', 'CAN'),
('Bolívar', 'BOL'),
('Carchi', 'CAR');

-- Insertar ciudades con tildes y ñ correctas
INSERT INTO ciudades (nombre, provincia_id, es_costera) VALUES
-- Pichincha
('Quito', 1, FALSE),
('Sangolquí', 1, FALSE),

-- Guayas
('Guayaquil', 2, TRUE),
('Durán', 2, FALSE),
('Milagro', 2, FALSE),

-- Azuay
('Cuenca', 3, FALSE),
('Gualaceo', 3, FALSE),

-- Manabí
('Manta', 4, TRUE),
('Portoviejo', 4, FALSE),
('Bahía de Caráquez', 4, TRUE),

-- Tungurahua
('Ambato', 5, FALSE),
('Baños', 5, FALSE),

-- Imbabura
('Ibarra', 6, FALSE),
('Otavalo', 6, FALSE),

-- Loja
('Loja', 7, FALSE),
('Catamayo', 7, FALSE),

-- El Oro
('Machala', 8, TRUE),

-- Esmeraldas
('Esmeraldas', 9, TRUE),

-- Chimborazo
('Riobamba', 10, FALSE),

-- Cotopaxi
('Latacunga', 11, FALSE),

-- Los Ríos
('Babahoyo', 12, FALSE),

-- Cañar
('Azogues', 13, FALSE),

-- Bolívar
('Guaranda', 14, FALSE),

-- Carchi
('Tulcán', 15, FALSE);

-- Insertar rutas bidireccionales entre ciudades principales
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso) VALUES
-- Quito como centro de conexiones
(1, 3, 420.00), (3, 1, 420.00), -- Quito <-> Guayaquil
(1, 6, 450.00), (6, 1, 450.00), -- Quito <-> Cuenca
(1, 11, 140.00), (11, 1, 140.00), -- Quito <-> Ambato
(1, 13, 115.00), (13, 1, 115.00), -- Quito <-> Ibarra
(1, 18, 220.00), (18, 1, 220.00), -- Quito <-> Riobamba
(1, 2, 45.00), (2, 1, 45.00), -- Quito <-> Sangolquí
(1, 19, 90.00), (19, 1, 90.00), -- Quito <-> Latacunga

-- Guayaquil como centro costero
(3, 4, 25.00), (4, 3, 25.00), -- Guayaquil <-> Durán
(3, 8, 190.00), (8, 3, 190.00), -- Guayaquil <-> Manta
(3, 17, 180.00), (17, 3, 180.00), -- Guayaquil <-> Machala
(3, 6, 240.00), (6, 3, 240.00), -- Guayaquil <-> Cuenca
(3, 5, 85.00), (5, 3, 85.00), -- Guayaquil <-> Milagro
(3, 20, 120.00), (20, 3, 120.00), -- Guayaquil <-> Babahoyo

-- Conexiones regionales
(6, 15, 210.00), (15, 6, 210.00), -- Cuenca <-> Loja
(6, 7, 35.00), (7, 6, 35.00), -- Cuenca <-> Gualaceo
(6, 21, 65.00), (21, 6, 65.00), -- Cuenca <-> Azogues
(11, 12, 45.00), (12, 11, 45.00), -- Ambato <-> Baños
(11, 18, 85.00), (18, 11, 85.00), -- Ambato <-> Riobamba
(13, 14, 25.00), (14, 13, 25.00), -- Ibarra <-> Otavalo
(13, 23, 45.00), (23, 13, 45.00), -- Ibarra <-> Tulcán
(8, 9, 35.00), (9, 8, 35.00), -- Manta <-> Portoviejo
(8, 10, 85.00), (10, 8, 85.00), -- Manta <-> Bahía de Caráquez
(15, 16, 55.00), (16, 15, 55.00), -- Loja <-> Catamayo

-- Conexiones costeras
(8, 18, 290.00), (18, 8, 290.00), -- Manta <-> Esmeraldas
(17, 3, 180.00), (3, 17, 180.00), -- Machala <-> Guayaquil

-- Conexiones interiores adicionales
(18, 22, 120.00), (22, 18, 120.00), -- Riobamba <-> Guaranda
(19, 11, 65.00), (11, 19, 65.00), -- Latacunga <-> Ambato
(19, 1, 90.00), (1, 19, 90.00); -- Latacunga <-> Quito

-- Mostrar resumen de la base de datos
SELECT '✅ Base de datos creada exitosamente con UTF-8!' as resultado;
SELECT '📋 Credenciales: admin / admin123' as credenciales;
SELECT CONCAT('👥 Usuarios: ', COUNT(*)) as estadistica FROM usuarios;
SELECT CONCAT('🏛️ Provincias: ', COUNT(*)) as estadistica FROM provincias;
SELECT CONCAT('🏙️ Ciudades: ', COUNT(*)) as estadistica FROM ciudades;
SELECT CONCAT('🛣️ Rutas: ', COUNT(*)) as estadistica FROM rutas;
SELECT '✅ Todas las rutas son BIDIRECCIONALES' as info;
SELECT '✅ Caracteres especiales (tildes y ñ) configurados correctamente' as encoding;
SELECT '🚀 Sistema listo para usar!' as final;
