from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError
from common.config.db import db
from models.usuarios import Usuarios
from common.utils.auth import role_required 

autenticacion = Blueprint('autenticacion', __name__)

@autenticacion.post("/api/auth/registro")
def registro_usuario():
    try:
        data = request.json
        nuevo_registro = Usuarios(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            email=data['email'],
            password=data['password'],
            rol=data['rol'],
            tipo_identificacion=data['tipo_identificacion'],
            identificacion=data['identificacion'],
            telefono=data['telefono'],
            direccion=data['direccion'],
            barrio=data['barrio'],
            ciudad=data['ciudad']
        )
        db.session.add(nuevo_registro)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error: El email ya está registrado'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error en el servidor'}), 500

    return jsonify({'message': 'Nuevo usuario creado correctamente'}), 201



@autenticacion.post('/api/auth/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Usuarios.query.filter_by(email=email).first()

    if user and user.check_password(password):

        access_token = create_access_token(identity={'id': user.id_usuarios, 'rol': user.rol.value})

        response = jsonify({"msg": "Login exitoso"})
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401


@autenticacion.post('/api/auth/logout')
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout exitoso"})
    unset_jwt_cookies(response) 
    return response, 200
