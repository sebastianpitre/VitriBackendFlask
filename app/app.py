from flask import Flask
from common.config.db import db
from models import Productos, Categorias, Pedidos, PedidosProductos, Pagos, Usuarios  # Importación de los modelos
from routes.public import productos, categorias  # Importación de los Blueprints

# Creación de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión de SQLAlchemy a la Base de Datos
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/vitridb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True  # Habilitar el echo para ver las sentencias SQL

# Inicialización de SQLAlchemy con la aplicación
db.init_app(app)

# Creación de las tablas en la base de datos a través de los modelos con SQLAlchemy
with app.app_context():
    db.create_all()

# Registro de Blueprints
app.register_blueprint(productos)
app.register_blueprint(categorias)

# Inicializador de la aplicación
if __name__ == '__main__':
    app.run(debug=True)


