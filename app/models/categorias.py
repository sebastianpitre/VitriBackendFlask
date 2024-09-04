from sqlalchemy import Integer, Numeric, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.config.db import Base 

class Categorias(Base):
    __tablename__ = 'categorias'

    id_categorias: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(1000))
    url_imagen: Mapped[str] = mapped_column(String(255))
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    #----------------------------------------------------------------------------------------------#
    # RELACIONES
    # Reladcion uno a muchos entre categorias y productos
    productos: Mapped[list["Productos"]] = relationship( back_populates="categorias", cascade="all, delete-orphan") # type: ignore
    #----------------------------------------------------------------------------------------------#

    def __init__(self, nombre, descripcion, url_imagen):
        self.nombre = nombre
        self.descripcion = descripcion
        self.url_imagen = url_imagen

    def __repr__(self):
        return f'<Nombre {self.nombre!r}, <Descripcion {self.descripcion!r}, <URLImagen {self.url_imagen!r}, <IsActivo {self.is_activo!r}>'
