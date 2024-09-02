from enum import Enum as PyEnum

class TipoIdentificacion(PyEnum):

    CEDULA = "CC"
    TARJETA_IDENTIDAD = "TI"
    CARNET_EXTRANJERIA = "CE"
    NIT = "NIT"
    PERMISO_PERMANECIA_TRANSITORIA = "PPT"