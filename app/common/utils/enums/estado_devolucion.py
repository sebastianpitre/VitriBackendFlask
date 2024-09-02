from enum import Enum as PyEnum

class EstadoDevolucion(PyEnum):
    SOLICITADA = "SOLICITADA" 
    EN_PROCESO = "EN_PROCESO" 
    APROBADA = "APROBADA" 
    RECHAZADA = "RECHAZADA" 
    COMPLETADA = "COMPLETADA"