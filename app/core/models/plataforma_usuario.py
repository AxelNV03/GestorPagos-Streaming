from app import db

class PlataformaUsuario(db.Model):
    __tablename__ = 'plataforma_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Llaves foráneas apuntando a los nombres de tabla en español
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    plataforma_id = db.Column(db.Integer, db.ForeignKey('plataformas.id', ondelete='CASCADE'), nullable=False)

    # El UNIQUE compuesto para evitar que un usuario se asigne dos veces a la misma plataforma
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'plataforma_id', name='unique_user_platform'),
    )

    def __repr__(self):
        return f'<PlataformaUsuario User_ID:{self.usuario_id} Plat_ID:{self.plataforma_id}>'