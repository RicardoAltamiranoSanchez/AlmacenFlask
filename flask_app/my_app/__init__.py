from flask import Flask
#utilizamos el blueprint 
#primero hacemos la configuracion de la base de datos para que no halla conflicto despues
#despues importamos la vista  y por el ultiom el blueprint para que no halla confilicto enla creacion 
#primero creamos la app flask 
app=Flask(__name__)

#ya cuando halla terminado de cargar todo lo mandamos a llamar la creacion de datos
#despues importamos la base de datos donde hicimos un modulo
from my_app.DB.database import db

#Importamos las vistas o donde estan las peticiones get put post etc
from my_app.productos.app import producto #importamos desde la ubicacion de la carpte y el nombre que de pusimos
#Importamos flask ya que despues de aqui lo vamos a importar a los demas archivo no olcidar
#utilizamos blueprint debemos registrar la vista de pasamos en nombre del archivo o vista

app.register_blueprint(producto)
#la ultimo mandamos a llamar y crear ala base de datos si no existe
db.create_all()

@app.template_filter('doble')
def doble_filter(n:int):
    return n*2
