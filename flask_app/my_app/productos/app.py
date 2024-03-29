#from my_app import app
#importamos el app que esta en run.py desla carpteta inicial como si estuvieramos haciendo uncontrolador

#utilizamos el blueprint para registrar el modulo lo importamos el blueprint
from flask import Blueprint,render_template,request,redirect,url_for,flash,get_flashed_messages
from my_app.models.products import productos
from werkzeug.exceptions import abort
#importamos el modelos de la base de datos para usarla ne la visa
from my_app.models.modelProducto.productos import Productos
from my_app.DB.database import db
from sqlalchemy.sql.expression import not_,or_ #importamos elnot y el or
from my_app.models.modelProducto.productos import FormularioProducto
producto=Blueprint('producto',__name__)#pasamos el nombre de la aplicacion en el __name__ el primer parametro es como lo vamos a importar como asiganrla el nombre a un variable



@producto.route('/')
@producto.route('/Index')
@producto.route('/Index/<int:page>')
def Inicio(page=2):
     #productos=Productos.query.all()#obtemos todos los productos y query espara hacer consultas en la base de datos
     #Esto es para poder paginar la pagina mostar mas paginas y que no todo este desosrdenado con producto.query.paginate adentro de indicamos las paginas o valor de donde va empezar el paginado
     #el 5 es numero de elementos que se va mostrar en la parte de frente enviamos los items osea todo los elemnteos producto.items
    return  render_template('productos/index.html',productos=Productos.query.paginate(page,5))#lo mandamos ala plantilla html

@producto.route('/detalle-producto/<int:id>')#de ponemos el valor int  por que en defautl esta en string
def Detalle(id):
    producto=Productos.query.get_or_404(id)#con query.get(id )obtenmos el valor de un elemento con get_or_404 indica que si no existe el elemento que me muestre la pagina 404
   
    return render_template('productos/show.html',producto=producto)      

@producto.route('/filtro')
@producto.route('/filtro/<int:id>')
def Filtro(id):
    producto=productos.get(id)
    return render_template('productos/filtro.html',producto=producto)
#para el uso de los filtros documentacion  https://jinja.palletsprojects.com/en/2.10.x/templates/#list-of-builtin-filters
#ruta http://127.0.0.1:5000/filtro/4
#para crear nuestro propiso filtros
@producto.app_template_filter('iva')#indicamos la app  asi nombramos nuestra app con app=flask() y el app_template_filter es por defecto para creaer un nuevo filtro
def iva_filter(producto):#de pasamos en objeto odicionario pra hacer la validacion
    if(producto):
        return  producto['price']*0.20
    return 'Sin precio papu'

#Formulario
@producto.route('/crear-producto',methods=['GET','POST'])
def Crear():
    formulario=FormularioProducto(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
        p=Productos(request.form['nombre'],request.form['precio'])
        db.session.add(p)
        db.session.commit()
        flash('Producto creado con exito!!')
        return redirect(url_for('producto.Crear'))
    if formulario.errors:
          flash(formulario.errors,'danger')#de pasamos los errores si hay alguno dange es para decir que es un error lo muestra asi 
       
    #print(get_flashed_messages())#Obtemos todos los mensajes hechos con el metodo flash
    return render_template('productos/crear.html',formulario=formulario)



##con request obtemos los valor que estan en el formulario igual que node solo ponermos el id que queremos
#lo pusimos en comentarios este es solo la misma funcon de Crear pero lo metimos juntos para ahorrar codigo
##@producto.route('/crear-producto',methods=['POST'])
#def CrearProducto():
#    p=Productos(request.form['nombre'],request.form['precio'])
#    db.session.add(p)
#    db.session.commit()
#    flash('Producto creado con exito!!')#flash es para crear un mensaje con si fuera un alert
#    return redirect(url_for('producto.Crear'))#lo redirigimos al al funcion de get ponemos le modulo y la funcion en donde queremos redigir des pues de termianr la ejecucion

#funcion de editar
#@producto.route('/editar-producto/<int:id>')
#def Editar(id):
#    producto=Productos.query.get_or_404(id)
#    return render_template('productos/editar.html',producto=producto)
#Creamos una nueva ruta no importa la ruta pero si el id y el methos ya que la utilizamos
#en el html en action para referenciar al modulo y la funcions solo nos interesa el proceso de la funcion
@producto.route('/actualizar-producto/<int:id>',methods=['GET','POST'])
def Actualizar(id):
    producto=Productos.query.get_or_404(id)
    formulario=FormularioProducto(meta={ 'csrf':False})#quitamos el token para poder hacer la peticion sin problema mas adelan lo pondremos el token sirve para protegernos de los ataques del exterior
    if request.method == 'GET': #para cada vez que entre el usuario pueda tomar el valor en los inputs del proudco y los muestre
        formulario.nombre.data=producto.nombre#ponemos el valor del producto del id en el input
        formulario.precio.data=producto.precio
    
    if formulario.validate_on_submit():#Es par verficar si dio submit al boton o si es una peticion post
         producto.nombre=formulario.nombre.data#se puede obteneer el valor directamente ya que usarmo el wtform 
         producto.precio=formulario.precio.data
         db.session.add(producto)
         db.session.commit()
         flash("Registro Actualizado con Exito")
         return redirect(url_for('producto.Inicio'))#con  redirect se usa el modulo y la funcion para redirigir a otra pagina
    if formulario.errors:
        flash("No se puede Actualizar el Prodcuto",'danger')
    return render_template('productos/editar.html',formulario=formulario,producto=producto)        


@producto.route('/eliminar-producto/<int:id>')
def Eliminar(id):
    producto=Productos.query.get_or_404(id)
    
    db.session.delete(producto)
    db.session.commit()
    flash('Producto Elimnado con exito!!')
    return redirect(url_for('producto.Inicio'))
    
          
@producto.route('/test')
def test():
    #p=Productos.query.limit(2).all() Obtenemos todos los elementos pero  con el limit lo limitamos a dos
    #p=Productos.query.limit(2).first() nos da el primer valor con first
    #p=Productos.query.order_by(Productos.id:desc()).all() nos devuelve los valor pero los ordenamos enforma descendente 
    #p=Producto.query.get({"id":"1"}) obtenemos el valor con el id solo se pude con get usar el id 
    #p=Producto.query.filter_by(name="producto 1").all() nos devuelve el valor del nombre producto 1 con filter_by para buscar el valor a travez d eotro parametro que n sea el id
    #p=Producto.query.filter(Producto.id > 1).all() para indicar operaciones debemo poner filter operacones de menor o mayor
    #p=Producto.query.filter_by(nombre="Producto 1",id=1).first() de pones dos condiciones para que nos traiga el valor de especificamos la coma seria como un and
    #p=Producto.query.filter_by(Producto.nombre.like('P%')).all() buscamos por el nombre que empieze por la letra P y que nos traiga todos los elementos
    #p=Producto.query.filter(not_(Producto.id > 1)).all()lo usamos para negar las cosas hacer a inversa 
    #p=Producto.query.filter(or_(Producto.id > 1,Producto.name=="Producto 1"))all() si una de las dos condiciones se cumple se ejecuta
    #para crear un registro en la base de datos
    #Crear nuevo registro
    #p=Productos("producto 5",80.49)
    #db.session.add(p)#Creamos un nuevos registro con session.add debemos importar el db
    #db.session.commit()#Guaradamos el nuevo registro en la vase de datos despues de agregado
    #
    ##Actualizamos el nuevo registro
    #p=Productos.query.filter_by(nombre="Producto 1")#primero buscamos el registro que vamos a actualizar 
    #p.nombre="ProductoActualizado"#Despues lo actualziamos en la base de datos
    #db.session.add(p)
    #db.session.commit()
    ##Eliminamos un registro con delete
    #p=Productos.query.filter_by(id=1)#Buscamos el registro 
    #db.session.delete(p)#Eliminaos el registro 
    #db.session.commit()#guardamos los cambios en la base de datos
    return 'Pruebas con consultas query'

