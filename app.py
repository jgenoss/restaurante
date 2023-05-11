from flask import Flask,session,redirect,url_for,flash,render_template,request,jsonify,json
from flask_socketio import SocketIO
from modals import Models
from pprint import pprint

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

#vista de mesas
@app.route("/tables")
def tables():
   return render_template("tables.html")

#consultar mesas
@app.route("/tables/get_tables", methods=['GET','POST'])
def get_tables():
   if request.method == 'POST':
      return Models.get_tables()
   else:
      return redirect(url_for('tables'))

@app.route("/tables/getOrdersTableData", methods=['GET','POST'])
def getOrdersTableData():
   if request.method == 'POST':
      parseJson = request.json
      return Models.getOrdersTableData(parseJson['id'])
   else:
      return redirect(url_for('tables'))
   
#abrir mesa 
@app.route("/tables/open_table", methods=['GET','POST'])
def open_table():
   if request.method == 'POST':
      parseJson = request.json
      response = Models.open_table_id(parseJson['table_id'],parseJson['waiter'],parseJson['comment'],parseJson['status'])
      if response == None:
         return json.dumps({"message":"error"},default=str)
      else:
         socketio.emit("message",{"data":"update"})
         return json.dumps({"message":"success"},default=str)
   else:
      return redirect(url_for('tables'))


@app.route("/orders")
def orders():
   return render_template("orders.html")

@socketio.on('message')
def handle_message(data):
   print('received message: ' + str(data))
   
@socketio.on("open_table")
def handle_open_table(data):
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