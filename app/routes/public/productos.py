from flask import Blueprint

productos = Blueprint('productos', __name__)

@productos.get("/productos")
def get_categorias():
    return "Hello World!"