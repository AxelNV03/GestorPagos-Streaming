-- 1. Catálogo de Plataformas (Añadimos capacidad y gestión de costos)
CREATE TABLE plataformas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio_total DECIMAL(10, 2) NOT NULL, -- Lo que paga el admin
    cuota_sugerida DECIMAL(10, 2) GENERATED ALWAYS AS (precio_total / 5) STORED, -- MariaDB calcula esto solo
    dia_cobro INT DEFAULT 1 CHECK (dia_cobro BETWEEN 1 AND 31),
    url_logo VARCHAR(255) DEFAULT 'default_logo.png',
    correo_admin VARCHAR(255) NOT NULL,
    max_cupos INT DEFAULT 5
);

-- 2. Usuarios (Ajustamos a tu estructura de nombres)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apeP VARCHAR(100) NOT NULL,
    apeM VARCHAR(100),
    telefono VARCHAR(20) UNIQUE NOT NULL, -- Identificador único
    rol ENUM('admin', 'no_admin') DEFAULT 'no_admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Relación Usuario-Plataforma (Aquí manejamos el cupo)
CREATE TABLE plataforma_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    plataforma_id INT NOT NULL,
    fecha_ingreso DATE DEFAULT (CURRENT_DATE),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (plataforma_id) REFERENCES plataformas(id) ON DELETE CASCADE,
    UNIQUE(usuario_id, plataforma_id)
);

-- 4. Comprobantes (El "contenedor" de la foto)
CREATE TABLE comprobantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    ruta_archivo VARCHAR(255) NOT NULL,
    nota_usuario TEXT,
    motivo_rechazo TEXT,
    estado ENUM('revision', 'aprobado', 'rechazado') DEFAULT 'revision',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 5. Cobros Mensuales (El corazón de la deuda)
CREATE TABLE cobros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_plataforma_id INT NOT NULL,
    comprobante_id INT NULL,
    mes_anio DATE NOT NULL, -- Siempre el día 1 del mes
    monto_deuda DECIMAL(10, 2) NOT NULL, -- Aquí guardaremos el prorrateo si aplica
    estado ENUM('pendiente', 'en_revision', 'pagado') DEFAULT 'pendiente',
    FOREIGN KEY (usuario_plataforma_id) REFERENCES plataforma_usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (comprobante_id) REFERENCES comprobantes(id) ON DELETE SET NULL
);