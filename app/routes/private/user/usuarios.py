from flask import Blueprint, jsonify, request
from common.config.db import db
from models.usuarios import Usuarios

usuarios_user = Blueprint('usuarios_user', __name__)

@usuarios_user.get("/api/usuarios/<int:id>")
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
                      'tipo_identificacion': usuario.rol,
                      'identificacion': usuario.identificacion,
                      'telefono': usuario.telefono,
                      'direccion': usuario.direccion,
                      'barrio': usuario.barrio,
                      'ciudad': usuario.ciudad})

@usuarios_user.patch('/api/usuarios/<int:id>')
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
