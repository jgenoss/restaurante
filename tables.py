from flask import Blueprint, request, redirect, url_for, jsonify, render_template
from app import RestaurantApp
from models.tables import ClassTables

tables_bp = Blueprint('tables', __name__)


@tables_bp.route("/tables")
def tables():
   return render_template("tables.html")

@tables_bp.route("/tables/get_tables", methods=['GET','POST'])
def get_tables():
   if request.method == 'POST':
      return ClassTables.getTables()
   else:
      return redirect(url_for('tables'))

@tables_bp.route("/tables/getOrdersTableData", methods=['GET','POST'])
def getOrdersTableData():
   if request.method == 'POST':
      parseJson = request.json
      return ClassTables.getOrdersTableData(parseJson['id'])
   else:
      return redirect(url_for('tables'))

@tables_bp.route("/tables/open_table", methods=['GET','POST'])
def open_table():
   if request.method == 'POST':
      parseJson = request.json
      response = ClassTables.openTableId(parseJson['table_id'],parseJson['waiter'],parseJson['comment'],parseJson['status'])
      if response == None:
         return jsonify({"message":"error"})
      else:
        socketio = RestaurantApp().socketio
        socketio.emit("message", {"data": "update"})
        return jsonify({"message":"success"})
   else:
      return redirect(url_for('tables'))