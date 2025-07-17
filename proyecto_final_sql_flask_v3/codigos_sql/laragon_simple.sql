-- =========================================
-- BASE DE DATOS SIMPLE PARA LARAGON
-- Sistema de Gestión de Rutas con Grafos
-- Base de datos: proyecto_final_version2
-- =========================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS proyecto_final_version2 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE proyecto_final_version2;

-- =========================================
-- TABLA: users (Usuarios del sistema)
-- =========================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- TABLA: provincias (Provincias básicas)
-- =========================================
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(10) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- TABLA: ciudades (Ciudades del sistema)
-- =========================================
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (provincia_id) REFERENCES provincias(id) ON DELETE CASCADE,
    UNIQUE KEY unique_ciudad_provincia (nombre, provincia_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- TABLA: rutas (SIMPLE - solo origen, destino y peso)
-- =========================================
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    peso DECIMAL(8, 2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_ruta (ciudad_origen_id, ciudad_destino_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- INSERTAR DATOS INICIALES
-- =========================================

-- Usuario administrador (admin / admin123)
INSERT INTO users (username, email, password_hash, role, created_at) VALUES 
('admin', 'admin@rutas.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewBYHnACR8wQgKS6', 'admin', NOW());

-- 3 provincias básicas
INSERT INTO provincias (nombre, codigo, created_at) VALUES
('Pichincha', 'PIC', NOW()),
('Imbabura', 'IMB', NOW()),
('Loja', 'LOJ', NOW()),
('Guayas', 'GUA', NOW());

-- 4 ciudades predeterminadas como pediste
INSERT INTO ciudades (nombre, provincia_id, es_costera, created_at) VALUES
('Quito', 1, FALSE, NOW()),
('Ibarra', 2, FALSE, NOW()),
('Loja', 3, FALSE, NOW()),
('Guayaquil', 4, TRUE, NOW());

-- Rutas básicas entre las ciudades (SIMPLE - solo peso)
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso, created_at) VALUES
(2, 1, 115.00, NOW()), -- Ibarra -> Quito
(1, 4, 420.00, NOW()), -- Quito -> Guayaquil
(1, 3, 450.00, NOW()), -- Quito -> Loja
(4, 3, 650.00, NOW()); -- Guayaquil -> Loja

-- =========================================
-- VERIFICACION DE LA INSTALACION
-- =========================================
SELECT '✅ Base de datos "proyecto_final_version2" creada exitosamente!' AS resultado;
SELECT 'Credenciales: admin / admin123' AS credenciales;
SELECT CONCAT('Provincias: ', COUNT(*)) AS estadistica FROM provincias;
SELECT CONCAT('Ciudades: ', COUNT(*)) AS estadistica FROM ciudades;
SELECT CONCAT('Rutas: ', COUNT(*)) AS estadistica FROM rutas;
SELECT CONCAT('Usuarios: ', COUNT(*)) AS estadistica FROM users;
