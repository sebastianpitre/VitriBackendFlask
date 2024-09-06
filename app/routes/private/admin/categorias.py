from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from common.utils.auth import role_required
from common.utils.enums.roles import Roles
from common.config.db import db
from models.categorias import Categorias

categorias_admin = Blueprint('categorias_admin', __name__)

@categorias_admin.post("/api/admin/categorias")
@jwt_required() 
@role_required([Roles.ADMIN])
def guardar_categorias():
    data = request.json
    nueva_categoria = Categorias(nombre=data['nombre'],
                                 url_imagen=data['url_imagen'])
    db.session.add(nueva_categoria)
    db.session.commit()

    return jsonify({'message': 'Nueva categoria creada correctamente'}), 201

@categorias_admin.get("/api/admin/categorias")
@jwt_required() 
@role_required([Roles.ADMIN])
def obtener_categorias():
    categorias = Categorias.query.all()
    lista_categorias = [{'id_categorias': categoria.id_categorias, 
                        'nombre': categoria.nombre, 
                        'url_imagen': categoria.url_imagen,
                        'fecha_creacion' : categoria.fecha_creacion,
                        'fecha_actualizacion' : categoria.fecha_actualizacion} 
                        for categoria in categorias]
    return jsonify(lista_categorias)

@categorias_admin.get("/api/admin/categorias/<int:id>")
@jwt_required() 
@role_required([Roles.ADMIN])
def obtener_categoria_por_id(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    return jsonify({'id_categorias': categoria.id_categorias,
                    'nombre': categoria.nombre,
                    'url_imagen': categoria.url_imagen,
                    'fecha_creacion' : categoria.fecha_creacion,
                    'fecha_actualizacion' : categoria.fecha_actualizacion})

@categorias_admin.patch('/api/admin/categorias/<int:id>')
@jwt_required() 
@role_required([Roles.ADMIN])
def actualizar_categoria(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    data = request.json
    categoria.nombre = data['nombre']
    categoria.url_imagen = data['url_imagen']
    categoria.is_activo = data['is_activo']
    db.session.commit()
    return jsonify({'message': 'Categoria actualizada satisfactoriamente'}), 200

@categorias_admin.delete('/api/admin/categorias/<int:id>')
@jwt_required() 
@role_required([Roles.ADMIN])
def eliminar_categoria(id):
    categoria = Categorias.query.get(id)
    if not categoria:
        return jsonify({'message': 'Categoria no encontrada'}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'La categoria ha sido eliminada satisactoriamnete'}), 200