from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required
from flask import jsonify

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if 'rol' not in claims or claims['rol'] not in [role.value for role in allowed_roles]:
                return jsonify({"msg": "Acceso denegado, rol no autorizado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator