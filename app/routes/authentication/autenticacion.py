from flask import Blueprint, jsonify, request
from common.config.db import db
from models.usuarios import Usuarios

usuarios = Blueprint('autenticacion', __name__)

@usuarios.post("/api/auth/registro")
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
                                ciudad=data['ciudad'])
    db.session.add(nuevo_registro)
    db.session.commit()

    return jsonify({'message': 'Nuevo usuario creado correctamente'}), 201

@usuarios.post("/api/auth/login")
def login():
    return jsonify({'message': 'Login exitoso'}), 200

@usuarios.post("/api/auth/logout")
def logout():
    return jsonify({'message': 'Logout exitoso'}), 200

