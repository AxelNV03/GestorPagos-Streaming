DROP DATABASE IF EXISTS streaming;
CREATE DATABASE streaming;

USE streaming;
source /home/nv/KDE/www/pagos-project/app/core/tablas.sql

# Tabla: users, plataformas, plataforma_user, cobro, periodos
INSERT INTO users (nombres, apeP, apeM, telefono, rol) VALUES 
('AXEL', 'NAVA', 'SANCHEZ', '7774399424', 'admin'),
('JOSE ENRIQUE', 'LOPEZ', 'RIOS', '5525157398', 'no_admin'),
('JOSE ALEJANDRO', 'QUIROZ', 'BERNAL', '2461100897', 'no_admin'),
('EDUARDO', 'SANCHEZ', 'HERNANDEZ', '5534922003', 'no_admin'),
('DANIEL ISAID', 'ALTAMARINO', 'NUNEZ', '5528456695', 'no_admin'),
('MAURICIO', 'COLIN', 'RAMIREZ', '5619885934', 'no_admin'),
('DEBANNI ATXUL', 'MORALES', 'OSORIO', '7774580432', 'no_admin'),
('GERARDO', 'CHAPARRO', 'GUADARRAMA', '4423371515', 'no_admin'),
('EDGAR ALEJANDRO', 'MOLINA', 'CASTRO', '5560795878', 'no_admin'),
('MADRE', 'M', 'M', '5548577095', 'no_admin'),
('PADRE', 'P', 'P', '7774466339', 'no_admin'),
('ROBERTO CARLOS', 'CERVANTES', 'CERVANTES', '4171045858', 'no_admin'),
('ERASTO', 'LUIS', 'CRUZ', '5541775383', 'no_admin'),
('JOSE DAVID', 'JIMENEZ', 'LUNA', '5621852203', 'no_admin'),
('LUIS FERNANDO', 'ORTEGA', 'ARJONA', '5534908795', 'no_admin'),
('JOSE FEDERICO', 'PINEDA', 'CAMACHO', '4432454943', 'no_admin');


# Tabla: plataformas
INSERT INTO plataformas (nombre, precio_mensual, dia_cobro, url_logo, url_plataforma, correo_asociado) VALUES 
('Apple Music', 200.00, 5, '/static/img/logos/applemusic_logo.png', 'https://www.apple.com/apple-music/', 'apple@music.com'),
('Tidal', 180.00, 5, '/static/img/logos/tidal_logo.png', 'https://tidal.com/', 'tidal@tidal.com'),
('Qobuz', 250.00, 5, '/static/img/logos/qobuz_logo.png', 'https://www.qobuz.com/', 'qobuz@qobuz.com');


# Tabla: plataforma_user
/* Bloque 1: TIDAL (ID de plataforma: 2) para usuarios del 2 al 6 */
INSERT INTO plataforma_user (user_id, plataforma_id) VALUES 
(2, 2), (3, 2), (4, 2), (5, 2), (6, 2);

/* Bloque 2: APPLE MUSIC (ID de plataforma: 1) para usuarios del 7 al 11 */
INSERT INTO plataforma_user (user_id, plataforma_id) VALUES 
(7, 1), (8, 1), (9, 1), (10, 1), (11, 1);

/* Bloque 3: QOBUZ (ID de plataforma: 3) para usuarios del 12 al 16 */
INSERT INTO plataforma_user (user_id, plataforma_id) VALUES 
(12, 3), (13, 3), (14, 3), (15, 3), (16, 3);



# Periodos de cobro
DELIMITER //

CREATE PROCEDURE generar_periodos_hasta_2040()
BEGIN
    DECLARE fecha_actual DATE;
    DECLARE fecha_fin DATE;
    
    -- Empezamos en febrero 2026 (ajusta si ya insertaste febrero)
    SET fecha_actual = '2026-01-01';
    SET fecha_fin = '2040-12-01';

    WHILE fecha_actual <= fecha_fin DO
        INSERT INTO periodos (mes, anio, limite_pago)
        VALUES (
            MONTH(fecha_actual), 
            YEAR(fecha_actual), 
            DATE_ADD(fecha_actual, INTERVAL 4 DAY) -- Esto da el día 5
        );
        -- Avanzamos al siguiente mes
        SET fecha_actual = DATE_ADD(fecha_actual, INTERVAL 1 MONTH);
    END WHILE;
END //

DELIMITER ;

-- Ejecutamos el procedimiento
CALL generar_periodos_hasta_2040();

-- Borramos el procedimiento después de usarlo para limpiar
DROP PROCEDURE generar_periodos_hasta_2040;





# Cobros Enero 2026
INSERT INTO cobros (user_plataforma_id, periodo_id, monto, estado)
SELECT 
    up.id, 
    (SELECT id FROM periodos WHERE mes = 2 AND anio = 2026 LIMIT 1),
    (p.precio_mensual / (SELECT COUNT(*) FROM plataforma_user WHERE plataforma_id = p.id)),
    'pendiente'
FROM plataforma_user up
INNER JOIN plataformas p ON up.plataforma_id = p.id;

CREATE OR REPLACE VIEW vista_recaudacion_detallada AS
    SELECT 
        p.*, pr.mes, pr.anio,
        (SELECT COUNT(*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users,
        (SELECT COUNT(*) FROM cobros c 
            WHERE c.periodo_id = pr.id 
            AND c.estado = 'pagado' 
            AND c.user_plataforma_id IN (SELECT id FROM plataforma_user WHERE plataforma_id = p.id)
        ) AS pagaron
    FROM plataformas p
    CROSS JOIN periodos pr;
