from flask import Blueprint, jsonify, request
from common.config.db import db
from models.usuarios import Usuarios

usuarios_admin = Blueprint('usuarios_admin', __name__)

@usuarios_admin.post("/api/admin/usarios/registro")
def guardar_usuarios():
    data = request.json
    nuevo_registro = Usuarios(nombres=data['nombres'], 
                                apellidos=data['apellidos'], 
                                email=data['email'],
                                password=data['password'],
                                rol=data['rol'],
                                tipo_identificacion=data['tipo_identificacion'],
                                identificacion=data['identificacion'],
                                telefono=data['telefono'],
                                direccion=data['direccion'],
                                barrio=data['barrio'],
                                ciudad=data['ciudad'],
                                is_activo=data['is_activo'])
    db.session.add(nuevo_registro)
    db.session.commit()

    return jsonify({'message': 'Nuevo usuario creado correctamente'}), 201

@usuarios_admin.get("/api/admin/usuarios")
def obtener_usuarios():
    usuarios = Usuarios.query.all()
    lista_usuarios = [{'id_usuarios': usuario.id_usuarios,
                      'nombres': usuario.nombres,
                      'apellidos': usuario.apellidos,
                      'email': usuario.email,
                      'password': usuario.password,
                      'rol': usuario.rol.value,
                      'tipo_identificacion': usuario.tipo_identificacion.value,
                      'identificacion': usuario.identificacion,
                      'telefono': usuario.telefono,
                      'direccion': usuario.direccion,
                      'barrio': usuario.barrio,
                      'ciudad': usuario.ciudad,
                      'is_activo': usuario.is_activo,
                      'fecha_creacion': usuario.fecha_creacion,
                    'fecha_actualizacion': usuario.fecha_actualizacion} 
                    for usuario in usuarios]
    return jsonify(lista_usuarios)

@usuarios_admin.get("/api/admin/usuarios/<int:id>")
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
                    'ciudad': usuario.ciudad,
                    'is_activo': usuario.is_activo,
                    'fecha_creacion': usuario.fecha_creacion,
                    'fecha_actualizacion': usuario.fecha_actualizacion})

@usuarios_admin.patch('/api/admin/usuarios/<int:id>')
def actualizar_usuario(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrada'}), 404
    data = request.json
    usuario.nombres = data['nombres']
    usuario.apellidos = data['apellidos']
    usuario.email = data['email']
    usuario.password = data['password']
    usuario.rol = data['rol']
    usuario.identificacion = data['identificacion']
    usuario.identificacion = data['identificacion']
    usuario.telefono = data['telefono']
    usuario.direccion = data['direccion']
    usuario.barrio = data['barrio']
    usuario.ciudad = data['ciudad']
    usuario.is_activo = data['is_activo']
        
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado satisfactoriamente'}), 200

@usuarios_admin.delete('/api/admin/usuarios/<int:id>')
def eliminar_usuario(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrada'}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'El usuario ha sido eliminado satisactoriamnete'}), 200