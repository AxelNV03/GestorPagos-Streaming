CREATE TABLE plataformas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio_mensual DECIMAL(10, 2) NOT NULL,
    dia_cobro INT DEFAULT 1,
    url_logo VARCHAR(255) DEFAULT 'https://via.placeholder.com/50',
    url_plataforma VARCHAR(255),
    correo_asociado VARCHAR(255)
);
CREATE TABLE periodos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mes INT CHECK (mes BETWEEN 1 AND 12),
    anio INT NOT NULL,
    limite_pago DATE NOT NULL,
    UNIQUE(mes, anio)
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apeP VARCHAR(100) NOT NULL,
    apeM VARCHAR(100),
    telefono VARCHAR(20) UNIQUE NOT NULL,
    rol ENUM('admin', 'no_admin') DEFAULT 'no_admin',
    created_at DATE DEFAULT (CURRENT_DATE)
);
CREATE TABLE plataforma_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    plataforma_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (plataforma_id) REFERENCES plataformas(id) ON DELETE CASCADE,
    UNIQUE(user_id, plataforma_id)
);
CREATE TABLE comprobantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    monto_abonado DECIMAL(10, 2) NOT NULL,
    estado ENUM('revision', 'aprobado', 'rechazado') DEFAULT 'revision',
    ruta_archivo VARCHAR(255) NOT NULL,
    nota TEXT,
    created_at DATE DEFAULT (CURRENT_DATE)
);
CREATE TABLE cobros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_plataforma_id INT NOT NULL,
    periodo_id INT NOT NULL,
    comprobante_id INT NULL,
    estado ENUM('pendiente', 'pagado', 'rechazado') DEFAULT 'pendiente',
    monto DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_plataforma_id) REFERENCES plataforma_user(id) ON DELETE CASCADE,
    FOREIGN KEY (periodo_id) REFERENCES periodos(id) ON DELETE CASCADE,
    FOREIGN KEY (comprobante_id) REFERENCES comprobantes(id) ON DELETE SET NULL
);