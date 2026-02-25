SELECT 
    SUM(monto) as total_esperado,
    SUM(CASE WHEN estado = 'pagado' THEN monto ELSE 0 END) as recaudado,
    SUM(CASE WHEN estado = 'pendiente' THEN monto ELSE 0 END) as pendiente
FROM cobros
WHERE periodo_id = 1

SELECT * FROM periodos 
WHERE
    anio = YEAR(CURRENT_DATE) AND mes = MONTH(CURRENT_DATE);

            SELECT 
                p.nombre, p.precio_mensual, pr.mes, pr.anio, p.dia_cobro,
                (SELECT COUNT(*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users,
                (SELECT COUNT(*) FROM cobros c 
                    WHERE c.periodo_id = pr.id 
                    AND c.estado = 'pagado' 
                    AND c.user_plataforma_id IN (SELECT id FROM plataforma_user WHERE plataforma_id = p.id)
                ) AS pagaron
            FROM plataformas p
            CROSS JOIN periodos pr;
            WHERE pr.id=1;

INSERT INTO plataformas (nombre, precio_mensual, dia_cobro, url_logo, url_plataforma, correo_asociado) VALUES
('Netflix Premium (A)', 299.00, 5, 'https://cdn-icons-png.flaticon.com/512/732/732228.png', 'https://www.netflix.com/browse', 'admin.familiaA@gmail.com'),
('Netflix Premium (B)', 299.00, 15, 'https://cdn-icons-png.flaticon.com/512/732/732228.png', 'https://www.netflix.com/browse', 'cuentas.nava@outlook.com'),
('Spotify Familiar (G1)', 199.00, 1, 'https://cdn-icons-png.flaticon.com/512/174/174872.png', 'https://www.spotify.com/account', 'spotify.master1@gmail.com'),
('Spotify Familiar (G2)', 199.00, 1, 'https://cdn-icons-png.flaticon.com/512/174/174872.png', 'https://www.spotify.com/account', 'spotify.master2@gmail.com'),
('Spotify Familiar (G3)', 199.00, 10, 'https://cdn-icons-png.flaticon.com/512/174/174872.png', 'https://www.spotify.com/account', 'spotify.master1@gmail.com'),
('Disney+ Anual', 1599.00, 12, 'https://cdn-icons-png.flaticon.com/512/5977/5977583.png', 'https://www.disneyplus.com/account', 'disney.pro@gmail.com'),
('HBO Max (Legacy)', 149.00, 20, 'https://cdn-icons-png.flaticon.com/512/825/825590.png', 'https://auth.max.com/', 'max.movies@hotmail.com'),
('Amazon Prime', 99.00, 28, 'https://cdn-icons-png.flaticon.com/512/5968/5968202.png', 'https://www.amazon.com.mx/gp/video/settings', 'prime.mexico@gmail.com'),
('YouTube Premium', 119.00, 3, 'https://cdn-icons-png.flaticon.com/512/1384/1384060.png', 'https://www.youtube.com/paid_memberships', 'axel.yt@gmail.com'),
('Apple TV+', 129.00, 7, 'https://cdn-icons-png.flaticon.com/512/5968/5968535.png', 'https://tv.apple.com/settings', 'icloud.master@apple.com'),
('Crunchyroll Fan', 119.00, 14, 'https://cdn-icons-png.flaticon.com/512/5968/5968254.png', 'https://www.crunchyroll.com/acct', 'anime.nava@gmail.com'),
('Paramount+', 79.00, 18, 'https://cdn-icons-png.flaticon.com/512/825/825564.png', 'https://www.paramountplus.com/account', 'p.plus@gmail.com'),
('Star+ Solo', 199.00, 25, 'https://cdn-icons-png.flaticon.com/512/5977/5977590.png', 'https://www.starplus.com/account', 'disney.pro@gmail.com'),
('Mubi World', 149.00, 9, 'https://cdn-icons-png.flaticon.com/512/5971/5971609.png', 'https://mubi.com/settings', 'cinefilo.mx@gmail.com'),
('Canva Pro Team', 175.00, 2, 'https://cdn-icons-png.flaticon.com/512/5968/5968181.png', 'https://www.canva.com/settings/billing', 'design.team@canva.com'),
('ChatGPT Plus', 350.00, 22, 'https://cdn-icons-png.flaticon.com/512/11104/11104255.png', 'https://chat.openai.com/', 'openai.dev@gmail.com'),
('Midjourney Pro', 540.00, 30, 'https://cdn-icons-png.flaticon.com/512/2103/2103633.png', 'https://www.midjourney.com/account', 'ai.art@gmail.com'),
('Nintendo Online', 100.00, 15, 'https://cdn-icons-png.flaticon.com/512/889/889147.png', 'https://accounts.nintendo.com/', 'switch.games@gmail.com'),
('PlayStation Plus', 230.00, 12, 'https://cdn-icons-png.flaticon.com/512/5968/5968334.png', 'https://www.playstation.com/acct', 'psn.nava@hotmail.com'),
('Xbox Game Pass', 249.00, 1, 'https://cdn-icons-png.flaticon.com/512/5968/5968382.png', 'https://account.microsoft.com/services', 'xbox.master@outlook.com'),
-- Repeticiones para llegar a 50
('Spotify Familiar (G4)', 199.00, 5, 'https://cdn-icons-png.flaticon.com/512/174/174872.png', 'https://www.spotify.com/account', 'spotify.master4@gmail.com'),
('Netflix Standard (C)', 219.00, 10, 'https://cdn-icons-png.flaticon.com/512/732/732228.png', 'https://www.netflix.com/browse', 'cuentas.nava2@outlook.com'),
('Dropbox Plus', 190.00, 14, 'https://cdn-icons-png.flaticon.com/512/5968/5968224.png', 'https://www.dropbox.com/account', 'backup.cloud@gmail.com'),
('Google One 2TB', 169.00, 1, 'https://cdn-icons-png.flaticon.com/512/2991/2991148.png', 'https://one.google.com/settings', 'axel.nava@gmail.com'),
('Duolingo Super', 99.00, 20, 'https://cdn-icons-png.flaticon.com/512/5968/5968852.png', 'https://www.duolingo.com/settings/plus', 'languages@gmail.com'),
('Adobe Creative Cloud', 1100.00, 3, 'https://cdn-icons-png.flaticon.com/512/5968/5968397.png', 'https://account.adobe.com/', 'adobe.dev@gmail.com'),
('GitHub Pro', 75.00, 15, 'https://cdn-icons-png.flaticon.com/512/25/25231.png', 'https://github.com/settings/billing', 'git.dev@gmail.com'),
('DigitalOcean Droplet', 240.00, 1, 'https://cdn-icons-png.flaticon.com/512/5968/5968866.png', 'https://cloud.digitalocean.com/', 'droplets@gmail.com'),
('Vercel Pro', 380.00, 25, 'https://cdn-icons-png.flaticon.com/512/5968/5968391.png', 'https://vercel.com/dashboard', 'vercel.deploy@gmail.com'),
('Spotify Familiar (G5)', 199.00, 28, 'https://cdn-icons-png.flaticon.com/512/174/174872.png', 'https://www.spotify.com/account', 'spotify.master5@gmail.com'),
-- Más datos variados
('Notion Plus', 150.00, 5, 'https://cdn-icons-png.flaticon.com/512/5968/5968411.png', 'https://www.notion.so/settings', 'notes.nava@gmail.com'),
('Slack Pro', 140.00, 12, 'https://cdn-icons-png.flaticon.com/512/5968/5968434.png', 'https://slack.com/billing', 'slack.work@gmail.com'),
('Zoom Pro', 280.00, 10, 'https://cdn-icons-png.flaticon.com/512/3670/3670246.png', 'https://zoom.us/billing', 'calls.zoom@gmail.com'),
('Discord Nitro', 179.00, 18, 'https://cdn-icons-png.flaticon.com/512/5968/5968756.png', 'https://discord.com/settings/billing', 'discord.nava@gmail.com'),
('Twitch Turbo', 160.00, 20, 'https://cdn-icons-png.flaticon.com/512/5968/5968819.png', 'https://www.twitch.settings/subscriptions', 'stream.nava@gmail.com'),
('OnlyFans (Admin)', 200.00, 1, 'https://cdn-icons-png.flaticon.com/512/5968/5968500.png', 'https://onlyfans.com/settings', 'of.management@gmail.com'),
('Patreon Gold', 300.00, 1, 'https://cdn-icons-png.flaticon.com/512/5968/5968725.png', 'https://www.patreon.com/settings', 'patron.nava@gmail.com'),
('Figma Professional', 290.00, 15, 'https://cdn-icons-png.flaticon.com/512/5968/5968705.png', 'https://www.figma.com/settings', 'figma.dev@gmail.com'),
('Skillshare Premium', 250.00, 11, 'https://cdn-icons-png.flaticon.com/512/5968/5968940.png', 'https://www.skillshare.com/settings', 'study.nava@gmail.com'),
('MasterClass', 350.00, 5, 'https://cdn-icons-png.flaticon.com/512/5968/5968950.png', 'https://www.masterclass.com/settings', 'master.nava@gmail.com'),
('Vimeo Plus', 140.00, 9, 'https://cdn-icons-png.flaticon.com/512/5968/5968415.png', 'https://vimeo.com/settings', 'video.pro@gmail.com'),
('SoundCloud Go+', 115.00, 22, 'https://cdn-icons-png.flaticon.com/512/5968/5968420.png', 'https://soundcloud.com/settings', 'music.nava@gmail.com'),
('Tidal HiFi', 199.00, 30, 'https://cdn-icons-png.flaticon.com/512/5968/5968430.png', 'https://tidal.com/settings', 'audio.pro@gmail.com'),
('Deezer Premium', 119.00, 24, 'https://cdn-icons-png.flaticon.com/512/5968/5968435.png', 'https://www.deezer.com/settings', 'deezer.mx@gmail.com'),
('Telegram Premium', 89.00, 13, 'https://cdn-icons-png.flaticon.com/512/5968/5968441.png', 'https://web.telegram.org/', 'tel.nava@gmail.com'),
('Lingvist Pro', 180.00, 4, 'https://cdn-icons-png.flaticon.com/512/5968/5968450.png', 'https://lingvist.com/settings', 'ling.nava@gmail.com'),
('Babbel Plus', 160.00, 16, 'https://cdn-icons-png.flaticon.com/512/5968/5968460.png', 'https://babbel.com/settings', 'babbel.study@gmail.com'),
('Memrise Pro', 90.00, 21, 'https://cdn-icons-png.flaticon.com/512/5968/5968470.png', 'https://memrise.com/settings', 'mem.study@gmail.com'),
('Coursera Plus', 750.00, 1, 'https://cdn-icons-png.flaticon.com/512/5968/5968480.png', 'https://www.coursera.org/settings', 'coursera.nava@gmail.com'),
('Udemy Business', 450.00, 10, 'https://cdn-icons-png.flaticon.com/512/5968/5968490.png', 'https://www.udemy.com/settings', 'udemy.work@gmail.com');

DELETE FROM plataformas WHERE id >= 4;




SELECT 
    (SELECT COUNT(*) FROM cobros c WHERE c.periodo_id = pr.id AND c.estado = 'pagado' ) AS global_pagos,
    (SELECT COUNT(*) FROM cobros c WHERE c.periodo_id = pr.id ) AS global_users
FROM periodos pr
WHERE id = 1

SELECT 
                COUNT(*) as global_users,
                SUM(CASE WHEN estado = 'pagado' THEN 1 ELSE 0 END) as global_pagos
            FROM cobros 
            WHERE periodo_id = 1


SELECT *, p.nombre AS plataforma FROM users INNER JOIN plataforma_user pu ON id = ORDER BY id ASC;


SELECT u.*, p.nombre AS plataforma FROM plataforma_user pu 
INNER JOIN users u ON u.id = pu.user_id
INNER JOIN plataformas p ON p.id = pu.plataforma_id
WHERE p.id = 2;


UPDATE plataformas SET precio_mensual = 200 WHERE id = 1;

            UPDATE cobros c
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            SET c.monto = 40
            WHERE pu.plataforma_id = 1 
            AND c.estado = 'Pendiente';

                        SELECT * FROM vista_recaudacion_detallada WHERE mes = 2 AND anio = 2026;

SELECT SUM(monto) FROM cobros WHERE periodo_id = 2;


SELECT p.*, (SELECT COUNT (*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users FROM plataformas p;

SELECT p.*, (SELECT COUNT (*) FROM plataforma_user WHERE plataforma_id = p.id) AS total_users FROM plataformas p WHERE id=1;



SELECT
    c.*,
    CONCAT(u.nombres, ' ', u.apeP, ' ',u.apeM) AS usuario,
    per.mes, per.anio,
    com.id AS com_id, com.monto_abonado, com.ruta_archivo, com.nota, com.created_at AS fecha_comprobante,
    p.nombre AS plataforma
FROM cobros c
JOIN periodos per ON c.periodo_id = per.id
LEFT JOIN comprobantes com ON c.comprobante_id = com.id
JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
JOIN users u ON u.id = pu.user_id
JOIN plataformas p ON p.id = pu.plataforma_id


SELECT * FROM users



UPDATE cobros SET estado = 'pagado' WHERE id = 1

            SELECT
                c.*,
                CONCAT(u.nombres, ' ', u.apeP) AS usuario, u.nombres as nombre, u.id AS user_id,
                per.mes, per.anio, per.limite_pago,
                com.id AS com_id, com.monto_abonado, com.ruta_archivo, REPLACE(REPLACE(nota, '\n', ' '), '\r', '') as nota,
                com.created_at AS fecha_comprobante,
                p.id AS plat_id, p.nombre AS plataforma
            FROM cobros c
            JOIN periodos per ON c.periodo_id = per.id
            LEFT JOIN comprobantes com ON c.comprobante_id = com.id
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            JOIN users u ON u.id = pu.user_id
            JOIN plataformas p ON p.id = pu.plataforma_id
            WHERE 1=1

SELECT c.*, p.limite_pago
FROM cobros c
JOIN plataforma_user pu ON c.user_plataforma_id = pu.id 
JOIN periodos p ON c.periodo_id = p.id
WHERE pu.user_id = 9 AND estado = 'pendiente'
ORDER BY p.limite_pago DESC LIMIT 1


SELECT u.*, p.nombre AS plataforma FROM users u 
INNER JOIN plataforma_user pu ON pu.user_id = u.id
INNER JOIN plataformas p ON pu.plataforma_id = p.id
WHERE u.id = 2

SELECT u.*, p.nombre AS plataforma FROM users u 
LEFT JOIN plataforma_user pu ON pu.user_id = u.id
LEFT JOIN plataformas p ON pu.plataforma_id = p.id WHERE u.telefono = '7774399424'

SELECT c.* 
FROM cobros c
JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
JOIN periodos per ON c.periodo_id = per.id
LEFT JOIN comprobantes com ON com.id = c.comprobante_id
-- WHERE pu.plataforma_id = 1 AND per.id = 2
-- WHERE pu.user_id = 9

            SELECT 
                c.*, 
                per.mes, per.anio, 
                p.nombre as plataforma_nombre,
                com.ruta_archivo, com.estado as estado_comprobante, com.nota, com.created_at AS fecha_carga
            FROM cobros c
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            JOIN plataformas p ON pu.plataforma_id = p.id
            JOIN periodos per ON c.periodo_id = per.id
            LEFT JOIN comprobantes com ON com.id = c.comprobante_id 
            WHERE 1=1 AND pu.user_id=9


SELECT 
    c.*,
    com.created_at AS fecha_pago, com.nota
FROM cobros c
JOIN comprobantes com ON com.id = c.comprobante_id 
JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
WHERE 1=1 AND pu.user_id=9 

            SELECT 
                c.*,
                com.created_at AS fecha_pago, com.nota
            FROM cobros c
            JOIN comprobantes com ON com.id = c.comprobante_id 
            JOIN periodos per ON per.id = c.periodo_id
            JOIN plataforma_user pu ON c.user_plataforma_id = pu.id
            WHERE 1=1 AND pu.user_id=9
            ORDER BY per.anio DESC, per.mes DESC



    SELECT *, com.id AS com_id, com.*
    FROM cobros c 
    LEFT JOIN comprobantes com ON c.comprobante_id = com.id 
    WHERE c.id = 9
