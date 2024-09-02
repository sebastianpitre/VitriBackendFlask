from enum import Enum as PyEnum

class EstadoPedido(PyEnum):

    APROBADO = "APROBADO"
    CANCELADO = "CANCELADO"
    PENDIENTE = "PENDIENTE"
    ENTREGADO = "ENTREGADO"
    DEVUELTO = "DEVUELTO"