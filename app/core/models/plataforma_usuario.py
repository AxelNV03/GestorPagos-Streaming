from app import db

class PlataformaUsuario(db.Model):
    __tablename__ = 'plataforma_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    plataforma_id = db.Column(db.Integer, db.ForeignKey('plataformas.id', ondelete='CASCADE'), nullable=False)

    # Un vínculo puede tener muchos cobros (mes tras mes)
    # historial_cobros = db.relationship('Cobro', backref='registro_vinculo')

    # El UNIQUE compuesto para evitar que un usuario se asigne dos veces a la misma plataforma
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'plataforma_id', name='unique_user_platform'),
    )

    @property
    def ultimo_cobro(self):
        """Retorna el cobro más reciente de este vínculo."""
        if not self.historial_cobros:
            return None
        # Ordenamos por el ID del periodo más alto (asumiendo que los periodos son secuenciales)
        return sorted(self.historial_cobros, key=lambda x: x.periodo_id, reverse=True)[0]

    @property
    def esta_al_dia(self):
        """Verifica si el último cobro ya está pagado."""
        ultimo = self.ultimo_cobro
        if not ultimo:
            return False
        return ultimo.estado == 'pagado'

    def __repr__(self):
        return f'<PlataformaUsuario User_ID:{self.usuario_id} Plat_ID:{self.plataforma_id}>'