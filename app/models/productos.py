from sqlalchemy import Integer, Numeric, String, Boolean, Enum, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.config.db import Base 
from common.utils.enums.unidad_producto import UnidadProducto

class Productos(Base):
    __tablename__ = 'productos'

    id_productos: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(1000))
    url_imagen: Mapped[str] = mapped_column(String(255))
    url_ficha_tecnica: Mapped[str] = mapped_column(String(255))
    unidad_producto: Mapped[UnidadProducto] = mapped_column(Enum(UnidadProducto), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    is_promocion: Mapped[bool] = mapped_column(Boolean, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_activo: Mapped[bool] = mapped_column(Boolean, nullable=True)
    descuento: Mapped[float] = mapped_column(Numeric(10, 2))
    fecha_inicio_descuento: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_fin_descuento: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    id_categorias: Mapped[int] = mapped_column(ForeignKey("categorias.id_categorias"))
    id_usuarios: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuarios"))
    #----------------------------------------------------------------------------------------------#
    # RELACIONES 
    # Reladcion uno a muchos entre categorias y productos
    categorias: Mapped["Categorias"] = relationship( back_populates="productos") # type: ignore
    # Reladcion uno a muchos entre usuarios y productos
    usuarios: Mapped["Usuarios"] = relationship(back_populates="productos") # type: ignore
    # Reladcion uno a muchos entre pedidos_productos y productos
    pedidos_productos: Mapped[list["PedidosProductos"]] = relationship(back_populates="productos") # type: ignore # type: ignore
    #----------------------------------------------------------------------------------------------#

    def set_initial_values(self):
        self.is_activo = True

    def __init__(self, sku, nombre, descripcion, url_imagen, url_ficha_tecnica, unidad_producto, cantidad, precio, is_promocion, stock, descuento, id_categorias, id_usuarios):
        self.sku = sku
        self.nombre = nombre
        self.descripcion = descripcion
        self.url_imagen = url_imagen
        self.url_ficha_tecnica = url_ficha_tecnica
        self.unidad_producto = unidad_producto
        self.cantidad = cantidad
        self.precio = precio
        self.is_promocion = is_promocion
        self.stock = stock
        self.descuento = descuento
        self.id_categorias = id_categorias
        self.id_usuarios = id_usuarios

    def __repr__(self):
        return f'<SKU {self.sku!r}>, <Nombre {self.nombre!r}, <URLImagen {self.url_imagen!r}, <URLFichaTecnica {self.url_ficha_tecnica!r}, <UnidadProducto {self.unidad_producto!r}, <Cantidad {self.cantidad!r}, <Precio {self.precio!r},<IsPromocion {self.is_promocion!r},<IsStock {self.stock!r},<IsActivo {self.is_activo!r}, <Descuento {self.descuento!r}, <FechaInicioDescuento {self.fecha_inicio_descuento!r}, <FechaFinDescuento {self.fecha_fin_descuento!r}>'
