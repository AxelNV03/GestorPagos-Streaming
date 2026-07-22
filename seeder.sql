use streaming;

INSERT INTO plataformas
(nombre, precio_total, cuota, dia_cobro, url_logo, correo_admin, max_cupos)
VALUES
('Netflix Premium', 329.00, 55.00, 5, 'netflix.png', 'admin@streaming.com', 5),
('Spotify Familiar', 179.00, 30.00, 10, 'spotify.png', 'admin@streaming.com', 5),
('Disney Plus', 249.00, 42.00, 8, 'disney.png', 'admin@streaming.com', 5),
('Max', 199.00, 35.00, 15, 'max.png', 'admin@streaming.com', 5),
('Prime Video', 99.00, 20.00, 12, 'primevideo.png', 'admin@streaming.com', 5),
('Crunchyroll Mega Fan', 149.00, 30.00, 18, 'crunchyroll.png', 'admin@streaming.com', 5),
('YouTube Premium', 159.00, 32.00, 20, 'youtubepremium.png', 'admin@streaming.com', 5),
('Paramount Plus', 179.00, 30.00, 7, 'paramount.png', 'admin@streaming.com', 5),
('Apple Music Familiar', 199.00, 35.00, 25, 'applemusic.png', 'admin@streaming.com', 6),
('Apple TV Plus', 129.00, 25.00, 4, 'appletv.png', 'admin@streaming.com', 5),
('Vix Premium', 119.00, 24.00, 11, 'vix.png', 'admin@streaming.com', 5),
('Canva Pro', 300.00, 50.00, 9, 'canva.png', 'admin@streaming.com', 5),
('Microsoft 365 Family', 1299.00, 217.00, 1, 'office365.png', 'admin@streaming.com', 5),
('ChatGPT Plus', 400.00, 80.00, 14, 'chatgpt.png', 'admin@streaming.com', 5),
('Deezer Family', 179.00, 30.00, 22, 'deezer.png', 'admin@streaming.com', 5);

delete from plataformas;
delete from cobros;
delete from comprobantes;
delete from plataforma_usuario;
delete from usuarios;