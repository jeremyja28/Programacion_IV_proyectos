-- =============================================
-- Base de datos para Sistema de Rutas Simplificado
-- Puerto: 3307 (Laragon)
-- Nombre de la base de datos: final_project_PrograIV
-- VERSIÓN SIN DUPLICADOS
-- =============================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS final_project_PrograIV;
USE final_project_PrograIV;

-- Crear las tablas (DROP y CREATE para limpiar)
DROP TABLE IF EXISTS rutas;
DROP TABLE IF EXISTS ciudades;
DROP TABLE IF EXISTS provincias;
DROP TABLE IF EXISTS users;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabla de provincias
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(10) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ciudades
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id),
    UNIQUE KEY unique_ciudad_provincia (nombre, provincia_id)
);

-- Tabla de rutas
CREATE TABLE rutas (
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

-- Insertar usuario administrador
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@sistema.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8U9GnGZrB.', 'admin');

-- Insertar provincias
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

-- Insertar ciudades
INSERT INTO ciudades (nombre, provincia_id, es_costera) VALUES 
('Quito', 1, FALSE),
('Sangolquí', 1, FALSE),
('Cayambe', 1, FALSE),
('Guayaquil', 2, TRUE),
('Durán', 2, TRUE),
('Milagro', 2, FALSE),
('Cuenca', 3, FALSE),
('Girón', 3, FALSE),
('Manta', 4, TRUE),
('Portoviejo', 4, FALSE),
('Bahía de Caráquez', 4, TRUE),
('Machala', 5, TRUE),
('Pasaje', 5, FALSE),
('Loja', 6, FALSE),
('Catamayo', 6, FALSE),
('Ibarra', 7, FALSE),
('Otavalo', 7, FALSE),
('Ambato', 8, FALSE),
('Baños', 8, FALSE),
('Azogues', 9, FALSE),
('Riobamba', 10, FALSE);

-- Insertar rutas únicas (sin duplicados)
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso) VALUES 
-- Desde Quito (1)
(1, 2, 25),
(1, 3, 90),
(1, 7, 460),
(1, 16, 115),
(1, 18, 180),

-- Desde Guayaquil (4)
(4, 5, 15),
(4, 6, 45),
(4, 7, 243),
(4, 9, 185),
(4, 12, 90),
(4, 16, 380),

-- Desde Cuenca (7)
(7, 14, 320),
(7, 18, 190),
(7, 20, 85),

-- Desde Manta (9)
(9, 10, 25),
(9, 11, 35),

-- Desde Machala (12)
(12, 4, 90),

-- Desde Loja (14)
(14, 15, 35),

-- Desde Ibarra (16)
(16, 17, 25),

-- Desde Ambato (18)
(18, 19, 45),
(18, 21, 120),

-- Rutas de regreso
(2, 1, 25),
(3, 1, 90),
(7, 1, 460),
(16, 1, 115),
(18, 1, 180),

(5, 4, 15),
(6, 4, 45),
(7, 4, 243),
(9, 4, 185),

(14, 7, 320),
(18, 7, 190),
(20, 7, 85),

(10, 9, 25),
(11, 9, 35),

(15, 14, 35),

(17, 16, 25),

(19, 18, 45),
(21, 18, 120),

-- Conexiones adicionales
(2, 18, 195),
(18, 2, 195);

-- Verificación final
SELECT 'Base de datos creada exitosamente' as estado;

SELECT 'Conteos:' as info;
SELECT 'provincias' as tabla, COUNT(*) as total FROM provincias
UNION ALL
SELECT 'ciudades' as tabla, COUNT(*) as total FROM ciudades
UNION ALL
SELECT 'rutas' as tabla, COUNT(*) as total FROM rutas
UNION ALL
SELECT 'users' as tabla, COUNT(*) as total FROM users;

SELECT 'Ciudades costeras:' as info, COUNT(*) as total FROM ciudades WHERE es_costera = TRUE;

SELECT 'Usuario admin:' as info, username, role FROM users WHERE username = 'admin';

SELECT 'Sistema listo para usar!' as resultado;
