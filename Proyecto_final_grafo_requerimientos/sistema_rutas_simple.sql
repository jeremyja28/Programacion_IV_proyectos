-- =============================================
-- Base de datos para Sistema de Rutas Simplificado
-- Puerto: 3307 (Laragon)
-- Nombre de la base de datos: final_project_PrograIV
-- =============================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS final_project_PrograIV;
USE final_project_PrograIV;

-- Tabla de usuarios (opcional pero útil para administración)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabla de provincias
CREATE TABLE IF NOT EXISTS provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(10) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ciudades
CREATE TABLE IF NOT EXISTS ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id),
    UNIQUE KEY unique_ciudad_provincia (nombre, provincia_id)
);

-- Tabla de rutas
CREATE TABLE IF NOT EXISTS rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    peso DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id),
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id),
    UNIQUE KEY unique_ruta (ciudad_origen_id, ciudad_destino_id)
);

-- Insertar usuario administrador por defecto
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@sistema.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8U9GnGZrB.', 'admin');

-- Insertar provincias de ejemplo (Ecuador)
INSERT INTO provincias (nombre, codigo) VALUES 
('Pichincha', 'PIC'),
('Guayas', 'GUA'),
('Azuay', 'AZU'),
('Manabí', 'MAN'),
('El Oro', 'ELO'),
('Loja', 'LOJ'),
('Imbabura', 'IMB'),
('Tungurahua', 'TUN'),
('Cañar', 'CAN'),
('Chimborazo', 'CHI');

-- Insertar ciudades de ejemplo
INSERT INTO ciudades (nombre, provincia_id, es_costera) VALUES 
-- Pichincha
('Quito', 1, FALSE),
('Sangolquí', 1, FALSE),
('Cayambe', 1, FALSE),

-- Guayas
('Guayaquil', 2, TRUE),
('Durán', 2, TRUE),
('Milagro', 2, FALSE),

-- Azuay
('Cuenca', 3, FALSE),
('Girón', 3, FALSE),

-- Manabí
('Manta', 4, TRUE),
('Portoviejo', 4, FALSE),
('Bahía de Caráquez', 4, TRUE),

-- El Oro
('Machala', 5, TRUE),
('Pasaje', 5, FALSE),

-- Loja
('Loja', 6, FALSE),
('Catamayo', 6, FALSE),

-- Imbabura
('Ibarra', 7, FALSE),
('Otavalo', 7, FALSE),

-- Tungurahua
('Ambato', 8, FALSE),
('Baños', 8, FALSE),

-- Cañar
('Azogues', 9, FALSE),

-- Chimborazo
('Riobamba', 10, FALSE);

-- Insertar rutas de ejemplo
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso) VALUES 
-- Rutas desde Quito (id=1)
(1, 2, 25),   -- Quito -> Sangolquí
(1, 3, 90),   -- Quito -> Cayambe
(1, 7, 460),  -- Quito -> Cuenca
(1, 16, 115), -- Quito -> Ibarra
(1, 18, 180), -- Quito -> Ambato

-- Rutas desde Guayaquil (id=4)
(4, 5, 15),   -- Guayaquil -> Durán
(4, 6, 45),   -- Guayaquil -> Milagro
(4, 12, 90),  -- Guayaquil -> Machala
(4, 7, 243),  -- Guayaquil -> Cuenca

-- Rutas entre ciudades costeras
(4, 9, 185),  -- Guayaquil -> Manta
(9, 11, 35),  -- Manta -> Bahía de Caráquez
(12, 4, 90),  -- Machala -> Guayaquil

-- Rutas Sierra
(7, 18, 190), -- Cuenca -> Ambato
(16, 17, 25), -- Ibarra -> Otavalo
(18, 19, 45), -- Ambato -> Baños
(18, 21, 120), -- Ambato -> Riobamba

-- Rutas adicionales
(14, 15, 35), -- Loja -> Catamayo
(20, 7, 85),  -- Azogues -> Cuenca
(10, 9, 25),  -- Portoviejo -> Manta
(2, 18, 195), -- Sangolquí -> Ambato

-- Rutas bidireccionales (rutas de regreso)
(2, 1, 25),   -- Sangolquí -> Quito
(3, 1, 90),   -- Cayambe -> Quito
(7, 1, 460),  -- Cuenca -> Quito
(16, 1, 115), -- Ibarra -> Quito
(18, 1, 180), -- Ambato -> Quito

(5, 4, 15),   -- Durán -> Guayaquil
(6, 4, 45),   -- Milagro -> Guayaquil
(12, 4, 90),  -- Machala -> Guayaquil
(7, 4, 243),  -- Cuenca -> Guayaquil

(9, 4, 185),  -- Manta -> Guayaquil
(11, 9, 35),  -- Bahía de Caráquez -> Manta
(4, 12, 90),  -- Guayaquil -> Machala

(18, 7, 190), -- Ambato -> Cuenca
(17, 16, 25), -- Otavalo -> Ibarra
(19, 18, 45), -- Baños -> Ambato
(21, 18, 120), -- Riobamba -> Ambato

(15, 14, 35), -- Catamayo -> Loja
(7, 20, 85),  -- Cuenca -> Azogues
(9, 10, 25),  -- Manta -> Portoviejo
(18, 2, 195); -- Ambato -> Sangolquí

-- Mostrar información de las tablas creadas
SELECT 'Provincias creadas:' as info;
SELECT id, nombre, codigo FROM provincias ORDER BY nombre;

SELECT 'Ciudades creadas:' as info;
SELECT c.id, c.nombre, p.nombre as provincia, c.es_costera 
FROM ciudades c 
JOIN provincias p ON c.provincia_id = p.id 
ORDER BY p.nombre, c.nombre;

SELECT 'Rutas creadas:' as info;
SELECT r.id, 
       co.nombre as ciudad_origen, 
       cd.nombre as ciudad_destino, 
       r.peso
FROM rutas r
JOIN ciudades co ON r.ciudad_origen_id = co.id
JOIN ciudades cd ON r.ciudad_destino_id = cd.id
ORDER BY co.nombre, cd.nombre;

SELECT 'Resumen:' as info;
SELECT 
    (SELECT COUNT(*) FROM provincias) as total_provincias,
    (SELECT COUNT(*) FROM ciudades) as total_ciudades,
    (SELECT COUNT(*) FROM rutas) as total_rutas,
    (SELECT COUNT(*) FROM ciudades WHERE es_costera = TRUE) as ciudades_costeras;
