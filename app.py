from flask import Flask,session,redirect,url_for,flash,render_template,request
from flask_socketio import SocketIO,emit
from modals import Models

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

@app.route("/plates")
def plates():
   return render_template("plates.html",tables=Models.get_mesas())

@app.route('/plastes_ordes/<int:id>')
def plate_orders(id):
   return "<h1>{0}</h1>".format(id)

@app.route("/orders")
def orders():
   return render_template("orders.html")

@socketio.on('message')
def handle_message(data):
   print('received message: ' + str(data))

#@socketio.on('connect')
#def handle_connect():
   #print('Cliente conectado')

#@socketio.on('disconnect')
#def handle_disconnect():
   #print('Cliente desconectado')

#run app
if __name__ == "__main__":
   socketio.run(
      app,
      port=app.config['PORT'],
      host=app.config['HOST']
   )