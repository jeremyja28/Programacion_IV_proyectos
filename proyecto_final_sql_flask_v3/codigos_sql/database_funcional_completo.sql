-- =============================================
-- BASE DE DATOS COMPLETA Y FUNCIONAL
-- Sistema de Rutas con Grafos Bidireccionales
-- Base de datos: proyecto_final_version2
-- Puerto: 3307 (Laragon)
-- =============================================

-- Crear la base de datos
DROP DATABASE IF EXISTS proyecto_final_version2;
CREATE DATABASE proyecto_final_version2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE proyecto_final_version2;

-- =============================================
-- TABLA: users
-- =============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- TABLA: provincias
-- =============================================
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(10) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- TABLA: ciudades
-- =============================================
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (provincia_id) REFERENCES provincias(id) ON DELETE CASCADE,
    UNIQUE KEY unique_ciudad_provincia (nombre, provincia_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================
-- TABLA: rutas (con columna "peso" como requiere el código)
-- =============================================
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

-- =============================================
-- INSERTAR DATOS INICIALES
-- =============================================

-- Usuario administrador (admin / admin123)
INSERT INTO users (username, email, password_hash, role, created_at) VALUES 
('admin', 'admin@rutas.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewBYHnACR8wQgKS6', 'admin', NOW());

-- Provincias de Ecuador
INSERT INTO provincias (nombre, codigo, created_at) VALUES
('Pichincha', 'PIC', NOW()),
('Imbabura', 'IMB', NOW()),
('Loja', 'LOJ', NOW()),
('Guayas', 'GUA', NOW()),
('Azuay', 'AZU', NOW()),
('Manabí', 'MAN', NOW()),
('El Oro', 'ELO', NOW()),
('Tungurahua', 'TUN', NOW()),
('Chimborazo', 'CHI', NOW()),
('Cañar', 'CAN', NOW()),
('Los Ríos', 'LRI', NOW()),
('Esmeraldas', 'ESM', NOW()),
('Carchi', 'CAR', NOW()),
('Bolívar', 'BOL', NOW()),
('Cotopaxi', 'COT', NOW());

-- Ciudades principales de Ecuador
INSERT INTO ciudades (nombre, provincia_id, es_costera, created_at) VALUES
-- Pichincha
('Quito', 1, FALSE, NOW()),
('Sangolquí', 1, FALSE, NOW()),
('Cayambe', 1, FALSE, NOW()),

-- Imbabura
('Ibarra', 2, FALSE, NOW()),
('Otavalo', 2, FALSE, NOW()),
('Cotacachi', 2, FALSE, NOW()),

-- Loja
('Loja', 3, FALSE, NOW()),
('Catamayo', 3, FALSE, NOW()),
('Macará', 3, FALSE, NOW()),

-- Guayas
('Guayaquil', 4, TRUE, NOW()),
('Durán', 4, TRUE, NOW()),
('Milagro', 4, FALSE, NOW()),
('Daule', 4, FALSE, NOW()),

-- Azuay
('Cuenca', 5, FALSE, NOW()),
('Girón', 5, FALSE, NOW()),
('Paute', 5, FALSE, NOW()),

-- Manabí
('Manta', 6, TRUE, NOW()),
('Portoviejo', 6, FALSE, NOW()),
('Bahía de Caráquez', 6, TRUE, NOW()),

-- El Oro
('Machala', 7, TRUE, NOW()),
('Pasaje', 7, FALSE, NOW()),
('Santa Rosa', 7, FALSE, NOW()),

-- Tungurahua
('Ambato', 8, FALSE, NOW()),
('Baños', 8, FALSE, NOW()),
('Pelileo', 8, FALSE, NOW()),

-- Chimborazo
('Riobamba', 9, FALSE, NOW()),
('Alausí', 9, FALSE, NOW()),

-- Cañar
('Azogues', 10, FALSE, NOW()),
('Cañar', 10, FALSE, NOW()),

-- Los Ríos
('Babahoyo', 11, FALSE, NOW()),
('Quevedo', 11, FALSE, NOW()),

-- Esmeraldas
('Esmeraldas', 12, TRUE, NOW()),
('Atacames', 12, TRUE, NOW()),

-- Carchi
('Tulcán', 13, FALSE, NOW()),

-- Bolívar
('Guaranda', 14, FALSE, NOW()),

-- Cotopaxi
('Latacunga', 15, FALSE, NOW()),
('Salcedo', 15, FALSE, NOW());

-- =============================================
-- RUTAS PRINCIPALES (BIDIRECCIONALES AUTOMÁTICAS)
-- =============================================

-- Rutas principales entre ciudades importantes
-- Cada ruta se inserta en ambas direcciones automáticamente

-- Quito como centro
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso, created_at) VALUES
(1, 4, 115.0, NOW()),   -- Quito -> Ibarra
(4, 1, 115.0, NOW()),   -- Ibarra -> Quito
(1, 10, 420.0, NOW()),  -- Quito -> Guayaquil
(10, 1, 420.0, NOW()),  -- Guayaquil -> Quito
(1, 14, 460.0, NOW()),  -- Quito -> Cuenca
(14, 1, 460.0, NOW()),  -- Cuenca -> Quito
(1, 7, 450.0, NOW()),   -- Quito -> Loja
(7, 1, 450.0, NOW()),   -- Loja -> Quito
(1, 22, 140.0, NOW()),  -- Quito -> Ambato
(22, 1, 140.0, NOW()),  -- Ambato -> Quito
(1, 35, 120.0, NOW()),  -- Quito -> Latacunga
(35, 1, 120.0, NOW()),  -- Latacunga -> Quito

-- Guayaquil como centro costero
(10, 14, 190.0, NOW()),  -- Guayaquil -> Cuenca
(14, 10, 190.0, NOW()),  -- Cuenca -> Guayaquil
(10, 19, 80.0, NOW()),   -- Guayaquil -> Machala
(19, 10, 80.0, NOW()),   -- Machala -> Guayaquil
(10, 17, 190.0, NOW()),  -- Guayaquil -> Manta
(17, 10, 190.0, NOW()),  -- Manta -> Guayaquil
(10, 12, 25.0, NOW()),   -- Guayaquil -> Milagro
(12, 10, 25.0, NOW()),   -- Milagro -> Guayaquil

-- Cuenca como centro sur
(14, 7, 210.0, NOW()),   -- Cuenca -> Loja
(7, 14, 210.0, NOW()),   -- Loja -> Cuenca
(14, 25, 35.0, NOW()),   -- Cuenca -> Azogues
(25, 14, 35.0, NOW()),   -- Azogues -> Cuenca
(14, 24, 190.0, NOW()),  -- Cuenca -> Riobamba
(24, 1, 190.0, NOW()),   -- Riobamba -> Cuenca

-- Rutas de la sierra
(4, 5, 25.0, NOW()),     -- Ibarra -> Otavalo
(5, 4, 25.0, NOW()),     -- Otavalo -> Ibarra
(4, 31, 45.0, NOW()),    -- Ibarra -> Tulcán
(31, 4, 45.0, NOW()),    -- Tulcán -> Ibarra
(22, 24, 60.0, NOW()),   -- Ambato -> Riobamba
(24, 22, 60.0, NOW()),   -- Riobamba -> Ambato
(22, 23, 45.0, NOW()),   -- Ambato -> Baños
(23, 22, 45.0, NOW()),   -- Baños -> Ambato

-- Rutas de la costa
(17, 18, 30.0, NOW()),   -- Manta -> Portoviejo
(18, 17, 30.0, NOW()),   -- Portoviejo -> Manta
(17, 29, 120.0, NOW()),  -- Manta -> Esmeraldas
(29, 17, 120.0, NOW()),  -- Esmeraldas -> Manta
(19, 20, 25.0, NOW()),   -- Machala -> Pasaje
(20, 19, 25.0, NOW()),   -- Pasaje -> Machala

-- Rutas del oriente y otras conexiones
(27, 28, 40.0, NOW()),   -- Babahoyo -> Quevedo
(28, 27, 40.0, NOW()),   -- Quevedo -> Babahoyo
(35, 32, 50.0, NOW()),   -- Latacunga -> Guaranda
(32, 35, 50.0, NOW()),   -- Guaranda -> Latacunga

-- Rutas adicionales para conectividad
(7, 8, 35.0, NOW()),     -- Loja -> Catamayo
(8, 7, 35.0, NOW()),     -- Catamayo -> Loja
(10, 11, 15.0, NOW()),   -- Guayaquil -> Durán
(11, 10, 15.0, NOW()),   -- Durán -> Guayaquil
(1, 2, 25.0, NOW()),     -- Quito -> Sangolquí
(2, 1, 25.0, NOW()),     -- Sangolquí -> Quito
(14, 15, 40.0, NOW()),   -- Cuenca -> Girón
(15, 14, 40.0, NOW()),   -- Girón -> Cuenca

-- Rutas intercosteras
(29, 30, 35.0, NOW()),   -- Esmeraldas -> Atacames
(30, 29, 35.0, NOW()),   -- Atacames -> Esmeraldas
(17, 19, 280.0, NOW()),  -- Manta -> Machala (vía costera)
(19, 17, 280.0, NOW());  -- Machala -> Manta (vía costera)

-- =============================================
-- VERIFICACIÓN DE LA INSTALACIÓN
-- =============================================
SELECT '✅ Base de datos "proyecto_final_version2" creada exitosamente!' AS resultado;
SELECT '🔑 Credenciales: admin / admin123' AS credenciales;
SELECT CONCAT('👥 Usuarios: ', COUNT(*)) AS estadistica FROM users;
SELECT CONCAT('🏛️ Provincias: ', COUNT(*)) AS estadistica FROM provincias;
SELECT CONCAT('🏙️ Ciudades: ', COUNT(*)) AS estadistica FROM ciudades;
SELECT CONCAT('🛣️ Rutas: ', COUNT(*)) AS estadistica FROM rutas;
SELECT '🔄 Todas las rutas son BIDIRECCIONALES' AS info;
SELECT '✅ ¡Sistema listo para usar!' AS estado;
