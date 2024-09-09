from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from common.utils.auth import role_required
from common.utils.enums.roles import Roles
from common.utils.enums.estado_pedido import EstadoPedido
from common.config.db import db
from models import Pedidos, PedidosProductos, Productos

pedidos_user = Blueprint('pedidos_user', __name__)

@pedidos_user.post('/api/usuarios/pedidos')
@jwt_required() 
@role_required([Roles.CLIENTE])
def crear_pedido():
    
    data = request.get_json()
    nuevo_pedido = Pedidos(
        monto_total=data['monto_total'],
        estado_pedido=data['estado_pedido'],
        id_usuarios=data['id_usuarios'],
        id_pagos=data['id_pagos']
    )
    db.session.add(nuevo_pedido)
    db.session.commit()

    # Agregar productos al pedido
    for producto in data['productos']:
        nuevo_producto_pedido = PedidosProductos(
            cantidad=producto['cantidad'],
            precio=producto['precio'],
            id_pedidos=nuevo_pedido.id_pedidos,
            id=producto['id']
        )
        db.session.add(nuevo_producto_pedido)
    
    db.session.commit()

    return jsonify({"mensaje": "Pedido creado", "id_pedido": nuevo_pedido.id_pedidos}), 201

# Obtener un pedido específico
@pedidos_user.get('/api/usuarios/pedidos/<int:pedido_id>')
@jwt_required() 
@role_required([Roles.CLIENTE])
def obtener_pedido(pedido_id):
    pedido = Pedidos.query.get(pedido_id)
    if not pedido:
        return jsonify({"mensaje": "Pedido no encontrado"}), 404
    
    productos = PedidosProductos.query.filter_by(id_pedidos=pedido_id).all()
    productos_data = [{"id": p.id, "cantidad": p.cantidad, "precio": p.precio} for p in productos]

    pedido_data = {
        "id_pedido": pedido.id_pedidos,
        "monto_total": pedido.monto_total,
        "estado_pedido": pedido.estado_pedido.value,
        "fecha_creacion": pedido.fecha_creacion,
        "productos": productos_data
    }

    return jsonify(pedido_data), 200

# Obtener todos los pedidos de un usuario
@pedidos_user.get('/api/usuarios/<int:usuario_id>/pedidos')
@jwt_required() 
@role_required([Roles.CLIENTE])
def obtener_pedidos_por_usuario(usuario_id):
    pedidos = Pedidos.query.filter_by(id_usuarios=usuario_id).all()
    pedidos_data = []
    
    for pedido in pedidos:
        productos = PedidosProductos.query.filter_by(id_pedidos=pedido.id_pedidos).all()
        productos_data = [{"id": p.id, "cantidad": p.cantidad, "precio": p.precio} for p in productos]

        pedidos_data.append({
            "id_pedido": pedido.id_pedidos,
            "monto_total": pedido.monto_total,
            "estado_pedido": pedido.estado_pedido.value,
            "fecha_creacion": pedido.fecha_creacion,
            "productos": productos_data
        })

    return jsonify(pedidos_data), 200

# Actualizar el estado de un pedido
@pedidos_user.patch('/api/usuarios/pedidos/<int:id>')
@jwt_required() 
@role_required([Roles.CLIENTE])
def actualizar_estado_pedido(id):
    pedido = Pedidos.query.get_or_404(id)
    data = request.json
    pedido.estado_pedido = EstadoPedido(data['estado_pedido'])
    db.session.commit()
    return jsonify(message="Estado del pedido actualizado exitosamente")

# Agregar productos a un pedido
@pedidos_user.post('/api/usuarios/pedidos/<int:id_pedido>/productos')
@jwt_required() 
@role_required([Roles.CLIENTE])
def agregar_producto_pedido(id_pedido):
    pedido = Pedidos.query.get_or_404(id_pedido)
    data = request.json
    producto = Productos.query.get_or_404(data['id'])
    nuevo_pedido_producto = PedidosProductos(
        cantidad=data['cantidad'],
        precio=producto.precio,
        id_pedidos=id_pedido,
        id=data['id']
    )
    db.session.add(nuevo_pedido_producto)
    pedido.monto_total += float(nuevo_pedido_producto.cantidad) * float(nuevo_pedido_producto.precio)
    db.session.commit()
    return jsonify(message="Producto agregado al pedido exitosamente"), 201

# Obtener productos de un pedido
@pedidos_user.get('/api/usuarios/pedidos/<int:pedido_id>/productos')
@jwt_required() 
@role_required([Roles.CLIENTE])
def obtener_productos_pedido(pedido_id):
    productos = PedidosProductos.query.filter_by(id_pedidos=pedido_id).all()
    productos_data = [{"id": p.id, 
                       "cantidad": p.cantidad, 
                       "precio": p.precio} for p in productos]

    return jsonify(productos_data), 200

# Eliminar un producto de un pedido
@pedidos_user.delete('/api/usuarios/pedidos/<int:id_pedido>/productos/<int:id_producto>')
@jwt_required() 
@role_required([Roles.CLIENTE])
def eliminar_producto_pedido(id_pedido, id_producto):
    pedido_producto = PedidosProductos.query.filter_by(id_pedidos=id_pedido, id=id_producto).first_or_404()
    pedido = Pedidos.query.get_or_404(id_pedido)
    pedido.monto_total -= float(pedido_producto.cantidad) * float(pedido_producto.precio)
    db.session.delete(pedido_producto)
    db.session.commit()
    return jsonify(message="Producto eliminado del pedido exitosamente")

# Actualizar un producto en un pedido
@pedidos_user.patch('/api/usuarios/pedidos/<int:id_pedido>/productos/<int:id_producto>')
@jwt_required() 
@role_required([Roles.CLIENTE])
def actualizar_cantidad_producto_pedido(id_pedido, id_producto):
    pedido_producto = PedidosProductos.query.filter_by(id_pedidos=id_pedido, id=id_producto).first_or_404()
    pedido = Pedidos.query.get_or_404(id_pedido)
    data = request.json
    nueva_cantidad = data['cantidad']
    
    # Actualizar el monto total del pedido
    diferencia_cantidad = float(nueva_cantidad) - float(pedido_producto.cantidad)
    pedido.monto_total += diferencia_cantidad * float(pedido_producto.precio)
    
    pedido_producto.cantidad = nueva_cantidad
    db.session.commit()
    return jsonify(message="Cantidad del producto actualizada exitosamente")