from flask import Flask,session,redirect,url_for,flash,render_template,request
from flask_socketio import SocketIO,emit

app = Flask(__name__)
socketio = SocketIO(app)

app.config['DEBUG'] = True
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/menu")
def menu():
   return render_template("menu.html")

@app.route("/mesas")
def mesas():
   return render_template("mesas.html")

@app.route("/pedidos")
def pedidos():
   return render_template("pedidos.html")

@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))


#run app
if __name__ == "__main__":
   socketio.run(
      app,
      port=app.config['PORT'],
      host=app.config['HOST']
   )