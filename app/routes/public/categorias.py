from flask import Blueprint, jsonify, request
from common.config.db import db
from models.categorias import Categorias

categorias = Blueprint('categorias', __name__)

@categorias.get("/api/publico/categorias")
def obtener_categorias():
    categorias = Categorias.query.all()
    lista_categorias = [{'id_categorias': categoria.id_categorias, 'nombre': categoria.nombre, 
                        'descripcion': categoria.descripcion,
                        'url_imagen': categoria.url_imagen} 
                        for categoria in categorias]
    return jsonify(lista_categorias)

@categorias.get("/api/publico/categorias/<int:id>")
def obtener_categoria_por_id(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    return jsonify({'id_categorias': categoria.id_categorias,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'url_imagen': categoria.url_imagen})