from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FolderViewArchivos(db.Model):
    __tablename__ = 'FolderView_Archivos'

    ArchivoID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(255))
    Tamano = db.Column(db.BigInteger)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    FechaModificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    Ruta = db.Column(db.String(500))
    Extension = db.Column(db.String(50))
    DirectorioID = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'ArchivoID': self.ArchivoID,
            'Nombre': self.Nombre,
            'Tamano': self.Tamano,
            'FechaCreacion': self.FechaCreacion,
            'FechaModificacion': self.FechaModificacion,
            'Ruta': self.Ruta,
            'Extension': self.Extension,
            'DirectorioID': self.DirectorioID,
        }

    def __repr__(self):
        return f"<Archivo {self.Nombre}>"
