from mi_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from mi_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Usuario:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.contraseña = data['contraseña']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #METODO PARA GUARDAR USUARIO:
    @classmethod
    def guardar(cls, data ):
        query = "INSERT INTO usuarios (nombre, apellido ,correo ,contraseña, created_at, updated_at) VALUES ( %(nombre)s , %(apellido)s , %(correo)s, %(contraseña)s, NOW() , NOW() );"
        return connectToMySQL('schema_login').query_db( query, data )

    #METODO PARA VER UN USUARIO
    @classmethod
    def mostrar_usuario(cls,data):
        query  = "SELECT * FROM usuarios WHERE id = %(id_usuario)s";
        result = connectToMySQL('schema_login').query_db(query,data)
        return cls(result[0])
    
    #METODO PARA INICIAR SESION CON EL CORREO
    @classmethod
    def iniciar_sesion(cls,data):
        query = "SELECT * FROM usuarios WHERE correo = %(correo)s;"
        results = connectToMySQL('schema_login').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validaciones(data):
        is_valid= True
        if len(data['nombre']) <3:
            flash("El nombre debe tener al menos 3 letras",'registro')
            is_valid=False
        if len(data['apellido']) <3:
            flash("El apellido debe tener al menos 3 letras",'registro')
            is_valid=False
        if len(data['correo']) < 3:
            flash("El correo debe tener al menos 3 letras",'registro')
            is_valid = False
        if not EMAIL_REGEX.match(data['correo']): 
            flash("Correo invalido")
            is_valid = False
        if len(data['contraseña']) < 8:
            flash("la contraseña debe tener al menos 8 caracteres")
            is_valid = False
        return is_valid

