from sqlalchemy import Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from common.config.db import Base 

class PedidosProductos(Base):
    __tablename__ = 'pedidos_productos'

    id_pedidos_productos: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    id_pedidos: Mapped[int] = mapped_column(ForeignKey("pedidos.id_pedidos"))
    id_productos: Mapped[int] = mapped_column(ForeignKey("productos.id_productos"))

    @hybrid_property
    def total_producto(self):
        return self.precio * self.cantidad
    #----------------------------------------------------------------------------------------------#
    # RELACIONES 
    # Reladcion uno a muchos entre pedidos y pagos
    pedidos: Mapped["Pedidos"] = relationship(back_populates="pedidos_productos") #type: ignore
    # Reladcion uno a muchos entre pedidos_productos y productos
    productos: Mapped["Productos"] = relationship(back_populates="pedidos_productos") #type: ignore
    #----------------------------------------------------------------------------------------------#

    def __init__(self, cantidad, precio, id_pedidos, id_productos):
        self.cantidad = cantidad
        self.precio = precio
        self.id_pedidos = id_pedidos
        self.id_productos = id_productos

    def __repr__(self):
        return f'<id {self.id!r}>, <cantidad {self.cantidad!r}, <precio {self.precio!r}>'