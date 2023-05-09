from flask import Flask,session,redirect,url_for,flash,render_template,request,jsonify,json
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

@app.route("/tables")
def tables():
   return render_template("tables.html",tables=Models.get_tables())

@app.route('/table_orders/<int:id>')
def table_orders(id):
   return Models.OPM(id)

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