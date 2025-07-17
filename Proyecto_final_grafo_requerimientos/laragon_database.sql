-- =========================================
-- BASE DE DATOS PARA LARAGON - PUERTO 3307
-- Sistema de Gestión de Rutas con Grafos
-- 
-- CONFIGURACION LARAGON:
-- Apache: Puerto 80
-- MySQL: Puerto 3307
-- Usuario: root (sin contraseña)
-- phpMyAdmin: http://localhost/phpmyadmin
-- =========================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS flask_rutas_grafo 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE flask_rutas_grafo;

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
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- TABLA: ciudades (Ciudades del sistema)
-- =========================================
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    es_costera BOOLEAN NOT NULL DEFAULT FALSE,
    latitud DECIMAL(10, 8) NULL,
    longitud DECIMAL(11, 8) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_nombre (nombre),
    INDEX idx_es_costera (es_costera)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- TABLA: rutas (Conexiones entre ciudades)
-- =========================================
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    distancia DECIMAL(8, 2) NOT NULL,
    costo DECIMAL(8, 2) NOT NULL,
    tiempo_estimado DECIMAL(5, 2) NULL COMMENT 'Tiempo en horas',
    estado VARCHAR(20) NOT NULL DEFAULT 'activa',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NOT NULL,
    
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_ruta (ciudad_origen_id, ciudad_destino_id),
    
    INDEX idx_ciudad_origen (ciudad_origen_id),
    INDEX idx_ciudad_destino (ciudad_destino_id),
    INDEX idx_estado (estado),
    INDEX idx_costo (costo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- INSERTAR DATOS INICIALES
-- =========================================

-- Usuario administrador (admin / admin123)
INSERT INTO users (username, email, password_hash, role, created_at) VALUES 
('admin', 'admin@rutas.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewBYHnACR8wQgKS6', 'admin', NOW());

-- Ciudades de Ecuador con coordenadas reales
INSERT INTO ciudades (nombre, es_costera, latitud, longitud, created_at) VALUES
('Ibarra', FALSE, 0.3516, -78.1312, NOW()),
('Quito', FALSE, -0.1807, -78.4678, NOW()),
('Santo Domingo', FALSE, -0.2532, -79.1745, NOW()),
('Manta', TRUE, -0.9517, -80.7217, NOW()),
('Portoviejo', TRUE, -1.0506, -80.4542, NOW()),
('Guayaquil', TRUE, -2.1962, -79.8862, NOW()),
('Cuenca', FALSE, -2.9001, -79.0059, NOW()),
('Loja', FALSE, -3.9928, -79.2042, NOW());

-- Rutas entre ciudades (optimizadas para algoritmo de grafos)
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, distancia, costo, tiempo_estimado, estado, created_by, created_at) VALUES
-- Rutas principales del norte
(1, 2, 115.00, 10.00, 2.0, 'activa', 1, NOW()), -- Ibarra -> Quito

-- Rutas desde Quito (centro de conexión)
(2, 3, 134.00, 15.00, 2.5, 'activa', 1, NOW()), -- Quito -> Santo Domingo
(2, 4, 269.00, 30.00, 5.0, 'activa', 1, NOW()), -- Quito -> Manta
(2, 7, 432.00, 35.00, 8.0, 'activa', 1, NOW()), -- Quito -> Cuenca

-- Rutas costeras
(3, 4, 168.00, 12.00, 3.0, 'activa', 1, NOW()), -- Santo Domingo -> Manta
(4, 5, 35.00, 5.00, 0.7, 'activa', 1, NOW()),   -- Manta -> Portoviejo
(5, 6, 194.00, 20.00, 3.5, 'activa', 1, NOW()),  -- Portoviejo -> Guayaquil

-- Rutas hacia el sur
(3, 6, 290.00, 22.00, 5.5, 'activa', 1, NOW()),  -- Santo Domingo -> Guayaquil
(6, 7, 193.00, 25.00, 3.8, 'activa', 1, NOW()),  -- Guayaquil -> Cuenca
(7, 8, 210.00, 18.00, 4.0, 'activa', 1, NOW()),  -- Cuenca -> Loja

-- Ruta larga directa
(6, 8, 447.00, 40.00, 8.5, 'activa', 1, NOW());  -- Guayaquil -> Loja

-- =========================================
-- VERIFICACION DE LA INSTALACION
-- =========================================
SELECT '✅ Base de datos creada exitosamente para Laragon Puerto 3307!' AS resultado;
SELECT 'Credenciales Aplicación: admin / admin123' AS credenciales;
SELECT 'Configuración MySQL: localhost:3307 (root sin contraseña)' AS configuracion;
SELECT 'Apache: localhost:80' AS apache;
SELECT 'phpMyAdmin: http://localhost/phpmyadmin' AS phpmyadmin;
SELECT CONCAT('Total ciudades: ', COUNT(*)) AS estadistica FROM ciudades;
SELECT CONCAT('Total rutas: ', COUNT(*)) AS estadistica FROM rutas;
SELECT CONCAT('Total usuarios: ', COUNT(*)) AS estadistica FROM users;
