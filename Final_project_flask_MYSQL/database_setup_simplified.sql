-- Database Setup for Sistema de Grafos (Simplified)
-- This script creates a clean database focused only on graph management

-- Create database
CREATE DATABASE IF NOT EXISTS sistema_grafos;
USE sistema_grafos;

-- Table for users
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for provinces
CREATE TABLE IF NOT EXISTS provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for cities
CREATE TABLE IF NOT EXISTS ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT,
    es_costera BOOLEAN DEFAULT FALSE,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id) ON DELETE CASCADE,
    UNIQUE KEY unique_city_province (nombre, provincia_id)
);

-- Table for routes
CREATE TABLE IF NOT EXISTS rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT,
    ciudad_destino_id INT,
    peso DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    UNIQUE KEY unique_route (ciudad_origen_id, ciudad_destino_id)
);

-- Insert default admin user
INSERT INTO usuarios (nombre, apellido, username, email, password_hash, es_admin) 
VALUES ('Admin', 'Sistema', 'admin', 'admin@grafos.com', 'scrypt:32768:8:1$wXg8rNh9WjFtaOaZ$8e6a6e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0b6f8c8e0', TRUE)
ON DUPLICATE KEY UPDATE es_admin = TRUE;

-- Insert sample provinces
INSERT INTO provincias (nombre, descripcion) VALUES
('Buenos Aires', 'Provincia de Buenos Aires'),
('Córdoba', 'Provincia de Córdoba'),
('Santa Fe', 'Provincia de Santa Fe'),
('Mendoza', 'Provincia de Mendoza')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- Insert sample cities
INSERT INTO ciudades (nombre, provincia_id, es_costera) VALUES
('La Plata', 1, TRUE),
('Mar del Plata', 1, TRUE),
('Bahía Blanca', 1, TRUE),
('Córdoba', 2, FALSE),
('Villa Carlos Paz', 2, FALSE),
('Rosario', 3, TRUE),
('Santa Fe', 3, TRUE),
('Mendoza', 4, FALSE),
('San Rafael', 4, FALSE)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- Insert sample routes
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso, descripcion) VALUES
(1, 2, 56.0, 'Ruta 2 - La Plata a Mar del Plata'),
(1, 4, 695.0, 'Ruta 9 - La Plata a Córdoba'),
(2, 3, 300.0, 'Ruta 3 - Mar del Plata a Bahía Blanca'),
(4, 5, 36.0, 'Ruta E55 - Córdoba a Villa Carlos Paz'),
(4, 6, 400.0, 'Ruta 9 - Córdoba a Rosario'),
(6, 7, 175.0, 'Ruta 11 - Rosario a Santa Fe'),
(4, 8, 600.0, 'Ruta 7 - Córdoba a Mendoza'),
(8, 9, 230.0, 'Ruta 144 - Mendoza a San Rafael')
ON DUPLICATE KEY UPDATE peso = VALUES(peso);

-- Create indexes for better performance
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_ciudades_provincia ON ciudades(provincia_id);
CREATE INDEX idx_rutas_origen ON rutas(ciudad_origen_id);
CREATE INDEX idx_rutas_destino ON rutas(ciudad_destino_id);

-- Show table structure
SHOW TABLES;

-- Show sample data
SELECT 'Usuarios' as tabla, COUNT(*) as total FROM usuarios
UNION ALL
SELECT 'Provincias' as tabla, COUNT(*) as total FROM provincias  
UNION ALL
SELECT 'Ciudades' as tabla, COUNT(*) as total FROM ciudades
UNION ALL
SELECT 'Rutas' as tabla, COUNT(*) as total FROM rutas;
