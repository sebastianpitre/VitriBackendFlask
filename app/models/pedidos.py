from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Numeric, String, Boolean, Enum, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from common.config.db import Base 
from common.utils.enums.estado_pedido import EstadoPedido

class Pedidos(Base):
    __tablename__ = 'pedidos'

    id_pedidos: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    monto_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estado_pedido: Mapped[EstadoPedido] = mapped_column(Enum(EstadoPedido), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    #----------------------------------------------------------------------------------------------#
    # RELACIONES 
    # Reladcion uno a muchos entre usuarios y pedidos
    id_usuarios: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuarios"))
    usuarios: Mapped["Usuarios"] = relationship(back_populates="pedidos") # type: ignore
    # Reladcion uno a muchos entre pedidos y productos
    pedidos_productos: Mapped[list["PedidosProductos"]] = relationship(back_populates="pedidos") # type: ignore
    # Reladcion uno a muchos entre pagos y pedidos
    id_pagos: Mapped[int] = mapped_column(ForeignKey("pagos.id_pagos"))
    pagos: Mapped["Pagos"] = relationship(back_populates="pedidos") # type: ignore
    #----------------------------------------------------------------------------------------------#

    def __init__(self, email, monto_total, estado_pedido):
        self.email = email
        self.monto_total = monto_total
        self.estado_pedido = estado_pedido

    def __repr__(self):
        return f'<id {self.id!r}>, <email {self.email!r}, <monto_total {self.monto_total!r}, <estado_pedido {self.estado_pedido!r}>'