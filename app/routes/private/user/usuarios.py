from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from common.utils.auth import role_required
from common.utils.enums.roles import Roles
from common.config.db import db
from models.usuarios import Usuarios

usuarios_user = Blueprint('usuarios_user', __name__)

@usuarios_user.get("/api/usuarios/<int:id>")
@jwt_required() 
@role_required([Roles.CLIENTE])
def obtener_usuario_por_id(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'message': 'usuario no encontrado'}), 404
    return jsonify({'id_usuarios': usuario.id_usuarios,
                      'nombres': usuario.nombres,
                      'apellidos': usuario.apellidos,
                      'email': usuario.email,
                      'password': usuario.password,
                      'rol': usuario.rol,
                      'tipo_identificacion': usuario.tipo_identificacion.value,
                      'identificacion': usuario.identificacion.value,
                      'telefono': usuario.telefono,
                      'direccion': usuario.direccion,
                      'barrio': usuario.barrio,
                      'ciudad': usuario.ciudad})

@usuarios_user.patch('/api/usuarios/<int:id>')
@jwt_required() 
@role_required([Roles.CLIENTE])
def actualizar_usuario(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrada'}), 404
    data = request.json
    usuario.nombres = data['nombres']
    usuario.apellidos = data['apellidos']
    usuario.email = data['email']
    usuario.password = data['password']
    usuario.telefono = data['telefono']
    usuario.direccion = data['direccion']
    usuario.barrio = data['barrio']
    usuario.ciudad = data['ciudad']    
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado satisfactoriamente'}), 200
