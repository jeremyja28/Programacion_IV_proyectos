-- =========================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Gestión de Rutas con Grafos
-- =========================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS flask_practica_1 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE flask_practica_1;

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
    
    -- Índices para optimizar consultas
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
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
    
    -- Índices para optimizar consultas
    INDEX idx_nombre (nombre),
    INDEX idx_es_costera (es_costera),
    INDEX idx_coordenadas (latitud, longitud),
    INDEX idx_created_at (created_at)
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
    
    -- Claves foráneas
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Constraint para evitar rutas duplicadas
    UNIQUE KEY unique_ruta (ciudad_origen_id, ciudad_destino_id),
    
    -- Constraint para evitar rutas circulares (origen != destino)
    CHECK (ciudad_origen_id != ciudad_destino_id),
    
    -- Constraints para validar valores positivos
    CHECK (distancia > 0),
    CHECK (costo > 0),
    CHECK (tiempo_estimado IS NULL OR tiempo_estimado > 0),
    
    -- Constraint para validar estados
    CHECK (estado IN ('activa', 'inactiva', 'mantenimiento')),
    
    -- Índices para optimizar consultas
    INDEX idx_ciudad_origen (ciudad_origen_id),
    INDEX idx_ciudad_destino (ciudad_destino_id),
    INDEX idx_estado (estado),
    INDEX idx_costo (costo),
    INDEX idx_created_by (created_by),
    INDEX idx_created_at (created_at),
    INDEX idx_updated_at (updated_at),
    
    -- Índice compuesto para búsquedas de rutas
    INDEX idx_origen_destino_estado (ciudad_origen_id, ciudad_destino_id, estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================
-- INSERTAR DATOS INICIALES
-- =========================================

-- Insertar usuario administrador por defecto
INSERT INTO users (username, email, password_hash, role, created_at) VALUES 
(
    'admin', 
    'admin@rutas.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewBYHnACR8wQgKS6', -- Contraseña: admin123
    'admin', 
    NOW()
);

-- Insertar ciudades de Ecuador
INSERT INTO ciudades (nombre, es_costera, latitud, longitud, created_at) VALUES
('Ibarra', FALSE, 0.3516, -78.1312, NOW()),
('Quito', FALSE, -0.1807, -78.4678, NOW()),
('Santo Domingo', FALSE, -0.2532, -79.1745, NOW()),
('Manta', TRUE, -0.9517, -80.7217, NOW()),
('Portoviejo', TRUE, -1.0506, -80.4542, NOW()),
('Guayaquil', TRUE, -2.1962, -79.8862, NOW()),
('Cuenca', FALSE, -2.9001, -79.0059, NOW()),
('Loja', FALSE, -3.9928, -79.2042, NOW());

-- Insertar rutas entre ciudades
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, distancia, costo, tiempo_estimado, estado, created_by, created_at) VALUES
-- Desde Ibarra
(1, 2, 115.00, 10.00, 2.0, 'activa', 1, NOW()),

-- Desde Quito
(2, 3, 134.00, 15.00, 2.5, 'activa', 1, NOW()),
(2, 4, 269.00, 30.00, 5.0, 'activa', 1, NOW()),
(2, 7, 432.00, 35.00, 8.0, 'activa', 1, NOW()),

-- Desde Santo Domingo
(3, 4, 168.00, 12.00, 3.0, 'activa', 1, NOW()),
(3, 6, 290.00, 22.00, 5.5, 'activa', 1, NOW()),

-- Desde Manta
(4, 5, 35.00, 5.00, 0.7, 'activa', 1, NOW()),

-- Desde Portoviejo
(5, 6, 194.00, 20.00, 3.5, 'activa', 1, NOW()),

-- Desde Guayaquil
(6, 7, 193.00, 25.00, 3.8, 'activa', 1, NOW()),
(6, 8, 447.00, 40.00, 8.5, 'activa', 1, NOW()),

-- Desde Cuenca
(7, 8, 210.00, 18.00, 4.0, 'activa', 1, NOW());

-- =========================================
-- VISTAS ÚTILES PARA CONSULTAS
-- =========================================

-- Vista para obtener información completa de rutas
CREATE VIEW vista_rutas_completa AS
SELECT 
    r.id,
    co.nombre AS ciudad_origen,
    cd.nombre AS ciudad_destino,
    r.distancia,
    r.costo,
    r.tiempo_estimado,
    r.estado,
    u.username AS creado_por,
    r.created_at,
    r.updated_at,
    co.es_costera AS origen_es_costera,
    cd.es_costera AS destino_es_costera
FROM rutas r
INNER JOIN ciudades co ON r.ciudad_origen_id = co.id
INNER JOIN ciudades cd ON r.ciudad_destino_id = cd.id
INNER JOIN users u ON r.created_by = u.id;

-- Vista para estadísticas de ciudades
CREATE VIEW vista_estadisticas_ciudades AS
SELECT 
    c.id,
    c.nombre,
    c.es_costera,
    COUNT(DISTINCT ro.id) AS rutas_como_origen,
    COUNT(DISTINCT rd.id) AS rutas_como_destino,
    (COUNT(DISTINCT ro.id) + COUNT(DISTINCT rd.id)) AS total_conexiones,
    c.created_at
FROM ciudades c
LEFT JOIN rutas ro ON c.id = ro.ciudad_origen_id AND ro.estado = 'activa'
LEFT JOIN rutas rd ON c.id = rd.ciudad_destino_id AND rd.estado = 'activa'
GROUP BY c.id, c.nombre, c.es_costera, c.created_at;

-- =========================================
-- PROCEDIMIENTOS ALMACENADOS ÚTILES
-- =========================================

-- Procedimiento para buscar ruta más económica
DELIMITER //
CREATE PROCEDURE BuscarRutaEconomica(
    IN origen_id INT,
    IN destino_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    SELECT 
        'Búsqueda de ruta más económica' AS consulta,
        co.nombre AS origen,
        cd.nombre AS destino
    FROM ciudades co, ciudades cd 
    WHERE co.id = origen_id AND cd.id = destino_id;
    
    -- Mostrar rutas directas disponibles
    SELECT 
        r.id,
        co.nombre AS ciudad_origen,
        cd.nombre AS ciudad_destino,
        r.distancia,
        r.costo,
        r.tiempo_estimado,
        CASE 
            WHEN co.es_costera OR cd.es_costera THEN 'SÍ'
            ELSE 'NO'
        END AS incluye_ciudad_costera
    FROM rutas r
    INNER JOIN ciudades co ON r.ciudad_origen_id = co.id
    INNER JOIN ciudades cd ON r.ciudad_destino_id = cd.id
    WHERE r.ciudad_origen_id = origen_id 
      AND r.ciudad_destino_id = destino_id 
      AND r.estado = 'activa';
END //
DELIMITER ;

-- Procedimiento para obtener estadísticas del sistema
DELIMITER //
CREATE PROCEDURE EstadisticasSistema()
BEGIN
    SELECT 
        'Estadísticas Generales del Sistema' AS seccion;
    
    SELECT 
        (SELECT COUNT(*) FROM users) AS total_usuarios,
        (SELECT COUNT(*) FROM users WHERE role = 'admin') AS administradores,
        (SELECT COUNT(*) FROM users WHERE role = 'user') AS usuarios_regulares,
        (SELECT COUNT(*) FROM ciudades) AS total_ciudades,
        (SELECT COUNT(*) FROM ciudades WHERE es_costera = TRUE) AS ciudades_costeras,
        (SELECT COUNT(*) FROM rutas) AS total_rutas,
        (SELECT COUNT(*) FROM rutas WHERE estado = 'activa') AS rutas_activas,
        (SELECT COUNT(*) FROM rutas WHERE estado = 'inactiva') AS rutas_inactivas;
END //
DELIMITER ;

-- =========================================
-- TRIGGERS PARA AUDITORÍA
-- =========================================

-- Trigger para actualizar fecha de modificación en rutas
DELIMITER //
CREATE TRIGGER tr_rutas_update_timestamp
    BEFORE UPDATE ON rutas
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END //
DELIMITER ;

-- =========================================
-- FUNCIONES ÚTILES
-- =========================================

-- Función para verificar si una ciudad es costera
DELIMITER //
CREATE FUNCTION EsCiudadCostera(ciudad_id INT)
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE costera BOOLEAN DEFAULT FALSE;
    
    SELECT es_costera INTO costera
    FROM ciudades 
    WHERE id = ciudad_id;
    
    RETURN costera;
END //
DELIMITER ;

-- =========================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- =========================================

-- Índices compuestos para consultas comunes
CREATE INDEX idx_rutas_activas_costo ON rutas (estado, costo) WHERE estado = 'activa';
CREATE INDEX idx_ciudades_costeras ON ciudades (es_costera, nombre) WHERE es_costera = TRUE;

-- =========================================
-- GRANTS Y PERMISOS (Opcional)
-- =========================================

-- Crear usuario específico para la aplicación (opcional)
-- CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON flask_practica_1.* TO 'flask_user'@'localhost';
-- FLUSH PRIVILEGES;

-- =========================================
-- VERIFICACIÓN DE LA INSTALACIÓN
-- =========================================

-- Verificar que todas las tablas se crearon correctamente
SELECT 
    TABLE_NAME as 'Tabla',
    TABLE_ROWS as 'Filas',
    CREATE_TIME as 'Fecha_Creacion'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'flask_practica_1'
ORDER BY TABLE_NAME;

-- Verificar datos iniciales
SELECT 'Verificación de datos iniciales' AS seccion;
SELECT COUNT(*) as usuarios FROM users;
SELECT COUNT(*) as ciudades FROM ciudades;
SELECT COUNT(*) as rutas FROM rutas;

-- Mostrar algunas rutas de ejemplo
SELECT 
    co.nombre AS origen,
    cd.nombre AS destino,
    r.costo,
    r.distancia
FROM rutas r
JOIN ciudades co ON r.ciudad_origen_id = co.id
JOIN ciudades cd ON r.ciudad_destino_id = cd.id
LIMIT 5;

-- =========================================
-- SCRIPT COMPLETADO EXITOSAMENTE
-- =========================================
SELECT '✅ Base de datos creada exitosamente!' AS resultado;
