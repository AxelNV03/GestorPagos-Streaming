# app/core/models/usuario.py
# ===================================================================================================
from app import db
from datetime import date
# ===================================================================================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    # ===================================================================================================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apeP = db.Column(db.String(100), nullable=False)
    apeM = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    rol = db.Column(db.Enum('admin', 'no_admin', name='user_roles'), default='no_admin')
    created_at = db.Column(db.Date, default=date.today)
    # ===================================================================================================
    # Relación 1 a 1 (gracias a que manejas un usuario por plataforma)
    vinculo_plataforma = db.relationship('PlataformaUsuario', backref='usuario', uselist=False)
    # vinculos = db.relationship('PlataformaUsuario', backref='usuario')
    # ===================================================================================================
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apeP} {self.apeM}"
    # ===================================================================================================    
    @property
    def plataforma(self):
        """Retorna el objeto Plataforma vinculado o None."""
        if self.vinculo_plataforma and self.vinculo_plataforma.plataforma:
            return self.vinculo_plataforma.plataforma
        return None
    # ===================================================================================================
    @property
    def deuda_total(self):
        """Suma de cobros pendientes para el vínculo único."""
        total = 0
        # Quitamos el primer bucle 'for' porque es un objeto único, no una lista
        v = self.vinculo_plataforma
        if v:
            for cobro in v.historial_cobros:
                if cobro.estado == 'pendiente':
                    total += float(cobro.monto)
        return total
    # ===================================================================================================
    def __repr__(self):
        return f'<User {self.nombres} ({self.rol})>'
    # ===================================================================================================