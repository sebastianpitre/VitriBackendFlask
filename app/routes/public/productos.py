from flask import Blueprint, jsonify, request
from common.config.db import db
from models.productos import Productos

productos = Blueprint('productos', __name__)

@productos.get("/api/publico/productos")
def obtener_productos():
    productos = Productos.query.all()
    lista_productos = [{'id_productos': producto.id_productos,
                        'nombre': producto.nombre,
                        'descripcion': producto.descripcion,
                        'url_imagen': producto.url_imagen,
                        'url_ficha_tecnica': producto.url_ficha_tecnica,
                        'unidad_producto': producto.unidad_producto,
                        'cantidad' : producto.cantidad,
                        'precio' : producto.precio,
                        'is_promocion' : producto.is_promocion,
                        'stock' : producto.stock,
                        'descuento' : producto.descuento,
                        'is_activo' : producto.is_activo,
                        'id_categorias' : producto.id_categorias,
                        'id_usuarios' : producto.id_usuarios} 
                        for producto in productos]
    return jsonify(lista_productos)

@productos.get("/api/publico/productos/<int:id>")
def obtener_producto_por_id(id):
    producto = Productos.query.get(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrada'}), 404
    return jsonify({'id_productos': producto.id_productos,
                        'nombre': producto.nombre,
                        'descripcion': producto.descripcion,
                        'url_imagen': producto.url_imagen,
                        'url_ficha_tecnica': producto.url_ficha_tecnica,
                        'unidad_producto': producto.unidad_producto,
                        'cantidad' : producto.cantidad,
                        'precio' : producto.precio,
                        'is_promocion' : producto.is_promocion,
                        'stock' : producto.stock,
                        'descuento' : producto.descuento,
                        'is_activo' : producto.is_activo,
                        'id_categorias' : producto.id_categorias,
                        'id_usuarios' : producto.id_usuarios})