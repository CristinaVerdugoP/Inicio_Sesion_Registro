from mi_app import app
from mi_app.controllers import usuario_controller


if __name__=="__main__":
    app.run(debug=True)

app.secret_key= 'keep in secret'