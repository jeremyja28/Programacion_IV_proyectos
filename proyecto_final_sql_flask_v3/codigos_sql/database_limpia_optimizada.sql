-- Base de datos limpia y optimizada para el proyecto
-- Sin tildes y con menos ciudades para mejor rendimiento

DROP DATABASE IF EXISTS proyecto_final_version2;
CREATE DATABASE proyecto_final_version2;
USE proyecto_final_version2;

-- Crear tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla provincias
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla ciudades
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INT NOT NULL,
    es_costera BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id)
);

-- Crear tabla rutas
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    peso DECIMAL(8,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id),
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id)
);

-- Insertar usuario administrador
INSERT INTO usuarios (username, email, password_hash, es_admin) VALUES
('admin', 'admin@sistema.com', '$2b$12$0zG8YsQPYKYf5NnQjKZb7u.8oLHH8JDlWm9MWEgQmJuSvLyqLZ5ay', TRUE);

-- Insertar provincias principales (sin tildes)
INSERT INTO provincias (nombre, codigo) VALUES
('Pichincha', 'PIC'),
('Guayas', 'GUA'),
('Azuay', 'AZU'),
('Manabi', 'MAN'),
('Tungurahua', 'TUN'),
('Imbabura', 'IMB'),
('Loja', 'LOJ'),
('El Oro', 'ORO'),
('Esmeraldas', 'ESM'),
('Chimborazo', 'CHI');

-- Insertar ciudades principales (sin tildes y reducidas)
INSERT INTO ciudades (nombre, provincia_id, es_costera) VALUES
-- Pichincha
('Quito', 1, FALSE),
-- Guayas
('Guayaquil', 2, TRUE),
('Duran', 2, FALSE),
-- Azuay
('Cuenca', 3, FALSE),
-- Manabi
('Manta', 4, TRUE),
('Portoviejo', 4, FALSE),
-- Tungurahua
('Ambato', 5, FALSE),
('Banos', 5, FALSE),
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
('Riobamba', 10, FALSE);

-- Insertar rutas bidireccionales entre ciudades principales
-- Quito como centro de conexiones
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, peso) VALUES
-- Quito <-> Otras ciudades
(1, 2, 420.00), (2, 1, 420.00), -- Quito <-> Guayaquil
(1, 4, 450.00), (4, 1, 450.00), -- Quito <-> Cuenca
(1, 7, 140.00), (7, 1, 140.00), -- Quito <-> Ambato
(1, 9, 115.00), (9, 1, 115.00), -- Quito <-> Ibarra
(1, 15, 220.00), (15, 1, 220.00), -- Quito <-> Riobamba

-- Guayaquil como centro costero
(2, 3, 25.00), (3, 2, 25.00), -- Guayaquil <-> Duran
(2, 5, 190.00), (5, 2, 190.00), -- Guayaquil <-> Manta
(2, 13, 180.00), (13, 2, 180.00), -- Guayaquil <-> Machala
(2, 4, 240.00), (4, 2, 240.00), -- Guayaquil <-> Cuenca

-- Conexiones regionales
(4, 11, 210.00), (11, 4, 210.00), -- Cuenca <-> Loja
(7, 8, 45.00), (8, 7, 45.00), -- Ambato <-> Banos
(9, 10, 25.00), (10, 9, 25.00), -- Ibarra <-> Otavalo
(5, 6, 35.00), (6, 5, 35.00), -- Manta <-> Portoviejo
(11, 12, 55.00), (12, 11, 55.00), -- Loja <-> Catamayo

-- Conexiones costeras
(5, 14, 290.00), (14, 5, 290.00), -- Manta <-> Esmeraldas
(13, 2, 180.00), (2, 13, 180.00), -- Machala <-> Guayaquil (ya existe)

-- Conexiones interiores adicionales
(7, 15, 85.00), (15, 7, 85.00), -- Ambato <-> Riobamba
(9, 1, 115.00), (1, 9, 115.00), -- Ibarra <-> Quito (ya existe)
(15, 4, 195.00), (4, 15, 195.00); -- Riobamba <-> Cuenca

-- Mostrar resumen de la base de datos
SELECT '✅ Base de datos creada exitosamente!' as resultado;
SELECT '📋 Credenciales: admin / admin123' as credenciales;
SELECT CONCAT('👥 Usuarios: ', COUNT(*)) as estadistica FROM usuarios;
SELECT CONCAT('🏛️ Provincias: ', COUNT(*)) as estadistica FROM provincias;
SELECT CONCAT('🏙️ Ciudades: ', COUNT(*)) as estadistica FROM ciudades;
SELECT CONCAT('🛣️ Rutas: ', COUNT(*)) as estadistica FROM rutas;
SELECT '✅ Todas las rutas son BIDIRECCIONALES' as info;
SELECT '🚀 Sistema listo para usar!' as final;
