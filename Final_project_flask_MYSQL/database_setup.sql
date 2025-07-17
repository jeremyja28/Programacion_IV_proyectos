-- Final_project_flask_mysql Database Setup Script (Simplified)
-- Para Laragon con MySQL en puerto 3307
-- Ejecuta este script en phpMyAdmin (http://localhost/phpmyadmin/) o línea de comandos

-- INSTRUCCIONES PARA LARAGON:
-- 1. Asegúrate de que Laragon esté ejecutándose
-- 2. Verifica que MySQL esté activo en Laragon
-- 3. Abre phpMyAdmin: http://localhost/phpmyadmin/
-- 4. Pega y ejecuta este script completo

-- Drop database if exists (BE CAREFUL!)
DROP DATABASE IF EXISTS Final_project_flask_mysql;

-- Create database
CREATE DATABASE Final_project_flask_mysql 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE Final_project_flask_mysql;

-- Create usuarios table (simplified)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE NOT NULL,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create notas table (simplified)
CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT NOT NULL,
    
    -- Foreign key
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Create provincias table (simplified)
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Create ciudades table (simplified)
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    es_costera BOOLEAN DEFAULT FALSE NOT NULL,
    provincia_id INT NOT NULL,
    
    -- Foreign key
    FOREIGN KEY (provincia_id) REFERENCES provincias(id) ON DELETE CASCADE,
    
    -- Unique constraint (ciudad must be unique within province)
    UNIQUE KEY unique_city_province (nombre, provincia_id)
);

-- Create rutas table (simplified - only distance/weight)
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    peso DECIMAL(10, 2) NOT NULL,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    
    -- Foreign keys
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_positive_weight CHECK (peso > 0),
    CONSTRAINT chk_different_cities CHECK (ciudad_origen_id != ciudad_destino_id),
    CONSTRAINT unique_route UNIQUE (ciudad_origen_id, ciudad_destino_id)
);

-- Insert default users (admin and regular user)
-- Password for both is 'admin123'
-- Using proper werkzeug password hashes
INSERT INTO usuarios (username, email, password_hash, nombre, apellido, es_admin, activo) VALUES
('admin', 'admin@admin.com', 'scrypt:32768:8:1$NkP6GnJeRyuGHKe3$e8a68007034cc2cd1d1b5a4466cb180aff89e086c1f2b7d1c52a37143d74794429d29dcfc7c8d255566625b1183d3a2288a17193b5b9723d90e2d91a88f319bd', 'Administrador', 'Sistema', TRUE, TRUE),
('usuario', 'usuario@usuario.com', 'scrypt:32768:8:1$OJikBuSMKTszB04E$3a37c9076b0732abcb8692f374c5d84d2a455bd919dcb313259605345c9bbf2c2ab6101c756770b02898e02e7bbcbe03dc31f0db7d6672985ce23e10ce85ac37', 'Usuario', 'Normal', FALSE, TRUE);

-- Insert sample provinces (Basic Ecuador provinces)
INSERT INTO provincias (nombre) VALUES
('Pichincha'),
('Guayas'),
('Azuay'),
('Manabí'),
('Loja');

-- Insert sample cities (Basic setup)
INSERT INTO ciudades (nombre, es_costera, provincia_id) VALUES
-- Pichincha (interior)
('Quito', FALSE, 1),
-- Guayas (costera)
('Guayaquil', TRUE, 2),
-- Azuay (interior)
('Cuenca', FALSE, 3),
-- Manabí (costera)
('Manta', TRUE, 4),
-- Loja (interior)
('Loja', FALSE, 5);

-- Insert basic routes (simple connected graph)
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso) VALUES
-- Quito connections
(1, 2, 450.0),  -- Quito -> Guayaquil
(1, 3, 440.0),  -- Quito -> Cuenca
(1, 4, 280.0),  -- Quito -> Manta
-- Guayaquil connections
(2, 3, 240.0),  -- Guayaquil -> Cuenca
(2, 5, 320.0),  -- Guayaquil -> Loja
-- Cuenca connections
(3, 5, 210.0),  -- Cuenca -> Loja
-- Manta connections
(4, 2, 300.0);  -- Manta -> Guayaquil

-- Insert sample notes
INSERT INTO notas (titulo, contenido, usuario_id) VALUES
('Bienvenido al Sistema', 'Sistema básico de gestión de rutas con algoritmo de Dijkstra.', 1),
('Funcionalidades', 'El sistema permite crear provincias, añadir ciudades (costeras/interiores) y registrar rutas con peso/distancia.', 1);

-- Show completion message
SELECT 'Database setup completed successfully!' as Status;
SELECT 'CREDENCIALES DE ACCESO:' as Info;
SELECT 'ADMIN - Usuario: admin / Contraseña: admin123' as AdminInfo;
SELECT 'USUARIO - Usuario: usuario / Contraseña: admin123' as UserInfo;
