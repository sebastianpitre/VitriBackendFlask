from sqlalchemy import Integer, String, Boolean, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.utils.enums.roles import Roles
from common.config.db import Base 
from common.utils.enums.tipo_identificacion import TipoIdentificacion

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id_usuarios: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombres: Mapped[str] = mapped_column(String(255), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False)
    tipo_identificacion: Mapped[TipoIdentificacion] = mapped_column(Enum(TipoIdentificacion), nullable=False)
    identificacion: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str] = mapped_column(String(255), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    barrio: Mapped[str] = mapped_column(String(255), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(255), nullable=False)
    is_activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    #----------------------------------------------------------------------------------------------#
    # RELACIONES
    # Reladcion uno a muchos entre usuarios y productos
    productos: Mapped[list["Productos"]] = relationship(back_populates="usuarios", cascade="all, delete-orphan") # type: ignore
    # Reladcion uno a muchos entre usuarios y pedidos
    pedidos: Mapped[list["Pedidos"]] = relationship(back_populates="usuarios", cascade="all, delete-orphan") # type: ignore
    #----------------------------------------------------------------------------------------------#

    def set_initial_values(self):
        self.is_activo = True


    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "rol": self.rol.name,
            "tipo_identificacion": self.tipo_identificacion.name,
            "identificacion": self.identificacion,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "barrio": self.barrio,
            "ciudad": self.ciudad,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }

    def __repr__(self):
        return f'<Nombres {self.nombres!r}>, <Apellidos {self.apellidos!r}, <Password {self.password!r}, <TipoIdentificacion {self.tipo_identificacion!r}, <Identificacion {self.identificacion!r}, <Telefono {self.telefono!r}, <Direccion {self.direccion!r},<Barrio {self.barrio!r},<Ciudad {self.ciudad!r},<IsActivo {self.is_activo!r},<IsStock {self.stock!r},<IsActivo {self.isActivo!r}>'