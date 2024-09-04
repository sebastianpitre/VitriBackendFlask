from flask import Blueprint, jsonify, request
from common.config.db import db
from models.categorias import Categorias

categorias = Blueprint('categorias', __name__)

@categorias.post("/api/admin/categorias")
def guardar_categorias():
    data = request.json
    nueva_categoria = Categorias(nombre=data['nombre'], 
                                 descripcion=data['descripcion'], 
                                 url_imagen=data['url_imagen'])
    db.session.add(nueva_categoria)
    db.session.commit()

    return jsonify({'message': 'Nueva categoria creada correctamente'}), 201

@categorias.get("/api/admin/categorias")
def obtener_categorias():
    categorias = Categorias.query.all()
    lista_categorias = [{'id_categorias': categoria.id_categorias, 'nombre': categoria.nombre, 
                        'descripcion': categoria.descripcion,
                        'url_imagen': categoria.url_imagen} 
                        for categoria in categorias]
    return jsonify(lista_categorias)

@categorias.get("/api/admin/categorias/<int:id>")
def obtener_categoria_por_id(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    return jsonify({'id_categorias': categoria.id_categorias,
                    'nombre': categoria.nombre,
                    'descripcion': categoria.descripcion,
                    'url_imagen': categoria.url_imagen})

@categorias.patch('/api/admin/categorias/<int:id>')
def actualizar_categoria(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    data = request.json
    categoria.nombre = data['nombre']
    categoria.descripcion = data['descripcion']
    categoria.url_imagen = data['url_imagen']
    categoria.is_activo = data['is_activo']
    db.session.commit()
    return jsonify({'message': 'Categoria actualizada satisfactoriamente'}), 200

@categorias.delete('/api/admin/categorias/<int:id>')
def eliminar_categoria(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'La categoria ha sido eliminada satisactoriamnete'}), 200