from flask import Blueprint

categorias = Blueprint('categorias', __name__)

@categorias.get("/")
def get_categorias():
    return "Hello World!"