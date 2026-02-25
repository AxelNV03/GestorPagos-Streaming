from app import db
from datetime import date

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apeP = db.Column(db.String(100), nullable=False)
    apeM = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    rol = db.Column(db.Enum('admin', 'no_admin', name='user_roles'), default='no_admin')
    created_at = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f'<User {self.nombres} ({self.rol})>'