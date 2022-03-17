##lo importamos de esta manera ya que db es una variable global

from my_app import db
#db.models es para crear un modelo de pasamos como parametro estos valores es por default
from flask_wtf import FlaskForm#Importaciones para crear el formulario de producto
from wtforms import StringField , DecimalField#Importaciones para crear el formulario de producto
from wtforms.validators import InputRequired , NumberRange
from decimal import Decimal
class Productos(db.Model):
    ___table___='productos'#Definimos elnombre de nuestra tabla con 3 guiones bajo
#db.Column es para definir si es una columna y adentro de poneoms los valores o el tipo de dato que van a tener    
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(255))
    precio=db.Column(db.Float)
    def __init__(self,nombre,precio):#Es solo el constructor
        self.nombre=nombre
        self.precio=precio
    def __repr__(self):#Es como lo vamos a mostra al momento de pedir el objeto en consola
        return '<Producto %r>' % (self.nombre)

#Creamos el formulario de producto
class FormularioProducto(FlaskForm):#de pasamoss la importacion  anuestra clase para crear el formulario
    nombre=StringField('nombre',validators=[InputRequired()])#de Indicamos que va ser de tipo string validator es para vadilar el campo loimportamos wtform
    precio=DecimalField('precio',validators=[InputRequired(),NumberRange(min=Decimal('0.0'))])
#Indicamos que va ser de tipo numerio NumberRange Es para medir el rango y decimal que tipo de datos igual lo importamos
#Documentacion de FlaskForm https://flask-wtf.readthedocs.io/en/stable/    
# https://wtforms.readthedocs.io/en/stable/fields/#basic-fields
#mas documentacion de validadciones https://wtforms.readthedocs.io/en/stable/validators/