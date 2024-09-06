from flask import Blueprint, jsonify, request
from common.config.db import db
from models.productos import Productos

productos_admin = Blueprint('productos_admin', __name__)

@productos_admin.post("/api/admin/productos")
def guardar_productos():
    data = request.json
    nuevo_producto = Productos(sku=data['sku'], 
                                nombre=data['nombre'], 
                                descripcion=data['descripcion'], 
                                url_imagen=data['url_imagen'],
                                url_ficha_tecnica=data['url_ficha_tecnica'], 
                                unidad_producto=data['unidad_producto'],
                                cantidad=data['cantidad'], 
                                precio=data['precio'], 
                                is_promocion=data['is_promocion'], 
                                stock=data['stock'], 
                                descuento=data['descuento'],
                                id_categorias=data['id_categorias'], 
                                id_usuarios=data['id_usuarios'], )
    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({'message': 'Nueva producto creada correctamente'}), 201

@productos_admin.get("/api/admin/productos")
def obtener_productos():
    productos = Productos.query.all()
    lista_productos = [{'id_productos': producto.id_productos,
                        'sku': producto.sku,
                        'nombre': producto.nombre,
                        'descripcion': producto.descripcion,
                        'url_imagen': producto.url_imagen,
                        'url_ficha_tecnica': producto.url_ficha_tecnica,
                        'unidad_producto': producto.unidad_producto.value,
                        'cantidad': producto.cantidad,
                        'precio': producto.precio,
                        'is_promocion': producto.is_promocion,
                        'stock': producto.stock,
                        'descuento': producto.descuento,
                        'is_activo': producto.is_activo,
                        'id_categorias': producto.id_categorias,
                        'id_usuarios': producto.id_usuarios,
                        'fecha_creacion': producto.fecha_creacion,
                        'fecha_actualizacion': producto.fecha_actualizacion,
                        'fecha_inicio_descuento': producto.fecha_inicio_descuento,
                        'fecha_fin_descuento': producto.fecha_fin_descuento}
                        for producto in productos]
    return jsonify(lista_productos)

@productos_admin.get("/api/admin/productos/<int:id>")
def obtener_producto_por_id(id):
    producto = Productos.query.get(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrada'}), 404
    return jsonify({'id_productos': producto.id_productos,
                        'nombre': producto.nombre,
                        'descripcion': producto.descripcion,
                        'url_imagen': producto.url_imagen,
                        'url_ficha_tecnica': producto.url_ficha_tecnica,
                        'unidad_producto': producto.unidad_producto.value,
                        'cantidad' : producto.cantidad,
                        'precio' : producto.precio,
                        'is_promocion' : producto.is_promocion,
                        'stock' : producto.stock,
                        'descuento' : producto.descuento,
                        'is_activo' : producto.is_activo,
                        'id_categorias' : producto.id_categorias,
                        'id_usuarios' : producto.id_usuarios,
                        'fecha_inicio_descuento' : producto.fecha_inicio_descuento,
                        'fecha_fin_descuento' : producto.fecha_fin_descuento,
                        'fecha_creacion' : producto.fecha_creacion,
                        'fecha_actualizacion' : producto.fecha_actualizacion})

@productos_admin.patch('/api/admin/productos/<int:id>')
def actualizar_producto(id):
    producto = Productos.query.get(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrada'}), 404
    data = request.json
    producto.nombre = data['nombre']
    producto.descripcion = data['descripcion']
    producto.url_imagen = data['url_imagen']
    producto.url_ficha_tecnica = data['url_ficha_tecnica']
    producto.unidad_producto = data['unidad_producto']
    producto.cantidad = data['cantidad']
    producto.precio = data['precio']
    producto.is_promocion = data['is_promocion']
    producto.stock = data['stock']
    producto.descuento = data['descuento']
    producto.is_activo = data['is_activo']
    producto.id_categorias = data['id_categorias']
    producto.id_usuarios = data['id_usuarios']
    db.session.commit()
    return jsonify({'message': 'Producto actualizada satisfactoriamente'}), 200

@productos_admin.delete('/api/admin/productos/<int:id>')
def eliminar_producto(id):
    producto = Productos.query.get(id)
    if not producto:
        return jsonify({'message': 'Producto no encontrada'}), 404
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'message': 'La producto ha sido eliminada satisactoriamnete'}), 200