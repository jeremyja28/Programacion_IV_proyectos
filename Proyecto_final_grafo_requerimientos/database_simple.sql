-- =========================================
-- SCRIPT SIMPLE - SOLO TABLAS BÁSICAS
-- Sistema de Gestión de Rutas con Grafos
-- =========================================

-- Crear y usar la base de datos
CREATE DATABASE IF NOT EXISTS flask_practica_1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE flask_practica_1;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- Tabla de ciudades
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    es_costera BOOLEAN NOT NULL DEFAULT FALSE,
    latitud DECIMAL(10, 8) NULL,
    longitud DECIMAL(11, 8) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabla de rutas
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    distancia DECIMAL(8, 2) NOT NULL,
    costo DECIMAL(8, 2) NOT NULL,
    tiempo_estimado DECIMAL(5, 2) NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activa',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NOT NULL,
    
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id),
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_ruta (ciudad_origen_id, ciudad_destino_id)
) ENGINE=InnoDB;

-- Datos iniciales básicos
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@rutas.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewBYHnACR8wQgKS6', 'admin');

INSERT INTO ciudades (nombre, es_costera, latitud, longitud) VALUES
('Ibarra', FALSE, 0.3516, -78.1312),
('Quito', FALSE, -0.1807, -78.4678),
('Santo Domingo', FALSE, -0.2532, -79.1745),
('Manta', TRUE, -0.9517, -80.7217),
('Portoviejo', TRUE, -1.0506, -80.4542),
('Guayaquil', TRUE, -2.1962, -79.8862),
('Cuenca', FALSE, -2.9001, -79.0059),
('Loja', FALSE, -3.9928, -79.2042);

INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, distancia, costo, tiempo_estimado, created_by) VALUES
(1, 2, 115.00, 10.00, 2.0, 1),
(2, 3, 134.00, 15.00, 2.5, 1),
(2, 4, 269.00, 30.00, 5.0, 1),
(3, 4, 168.00, 12.00, 3.0, 1),
(4, 5, 35.00, 5.00, 0.7, 1),
(5, 6, 194.00, 20.00, 3.5, 1),
(6, 7, 193.00, 25.00, 3.8, 1),
(7, 8, 210.00, 18.00, 4.0, 1),
(2, 7, 432.00, 35.00, 8.0, 1),
(3, 6, 290.00, 22.00, 5.5, 1),
(6, 8, 447.00, 40.00, 8.5, 1);
