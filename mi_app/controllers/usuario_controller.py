from flask import render_template, request, redirect, session, flash
from mi_app import app
from mi_app.models.usuario_model import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#----------------------------------------------------------------------------
@app.route('/')
def formularios():
    return render_template("index.html")

#--------------------------------------------------------------------------
@app.route('/crear_usuario', methods = ['POST'])
def crear_usuario():
    if not Usuario.validaciones(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['contraseña'])
    data = {
        "nombre": request.form["nombre"],
        "apellido" : request.form["apellido"],
        "correo" : request.form["correo"],
        "contraseña" : pw_hash
    }
    user_id = Usuario.guardar(data)
    session['user_id'] = user_id
    return redirect(f'/mostrar_un_usuario/{session["user_id"]}')

#------------------------------------------------------------------------
@app.route('/mostrar_un_usuario/<int:id_usuario>')
def usuario(id_usuario):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id_usuario" : id_usuario
    }
    un_usuario = Usuario.mostrar_usuario(data)
    return render_template("show.html", un_usuario = un_usuario)

#-------------------------------------------------------------------------
@app.route('/iniciar_sesion', methods = ['POST'])
def login():
    data = {"correo" : request.form["correo"]}
    user = Usuario.iniciar_sesion(data)
    if not user:
        flash("Correo o contraseña incorrectos")
        return redirect("/")
    if not bcrypt.check_password_hash(user.contraseña, request.form['contraseña']):
        flash("Correo o contraseña incorrectos")
        return redirect('/')
    session['user_id'] = user.id
    return redirect(f'/mostrar_un_usuario/{session["user_id"]}')

#-----------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
