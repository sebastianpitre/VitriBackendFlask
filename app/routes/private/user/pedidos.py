from flask import Blueprint, jsonify, request
from common.config.db import db
from models.pedidos import Pedidos

pedidos = Blueprint('pedidos', __name__)

@pedidos.post("/api/publico/pedidos")
def guardar_pedidos():
    data = request.json
    nueva_pedido = Pedidos(nombre=data['nombre'], 
                                 descripcion=data['descripcion'], 
                                 url_imagen=data['url_imagen'])
    db.session.add(nueva_pedido)
    db.session.commit()

    return jsonify({'message': 'Nuevo pedido creada correctamente'}), 201

@pedidos.get("/api/publico/pedidos")
def obtener_pedidos():
    pedidos = Pedidos.query.all()
    lista_pedidos = [{'id_pedidos': pedido.id_pedidos, 'nombre': pedido.nombre, 
                        'descripcion': pedido.descripcion,
                        'url_imagen': pedido.url_imagen} 
                        for pedido in pedidos]
    return jsonify(lista_pedidos)

@pedidos.get("/api/publico/pedidos/<int:id>")
def obtener_pedido_by_id(id):
    pedido = Pedidos.query.get(id)
    if not pedido:
        return jsonify({'message': 'Pedido no encontrada'}), 404
    return jsonify({'id_pedidos': pedido.id_pedidos,
                    'nombre': pedido.nombre,
                    'descripcion': pedido.descripcion,
                    'url_imagen': pedido.url_imagen})

@pedidos.patch('/api/publico/pedidos/<int:id>')
def actualizar_pedido(id):
    pedido = Pedidos.query.get(id)
    if not pedido:
        return jsonify({'message': 'Pedido no encontrada'}), 404
    data = request.json
    pedido.nombre = data['nombre']
    pedido.descripcion = data['descripcion']
    pedido.url_imagen = data['url_imagen']
    pedido.is_activo = data['is_activo']
    db.session.commit()
    return jsonify({'message': 'Pedido actualizado satisfactoriamente'}), 200

@pedidos.delete('/api/publico/pedidos/<int:id>')
def eliminar_pedido(id):
    pedido = Pedidos.query.get(id)
    if not pedido:
        return jsonify({'message': 'Pedidos no encontrada'}), 404
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': 'La pedido ha sido eliminada satisactoriamnete'}), 200