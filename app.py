from flask import Flask, session, redirect, url_for, flash, render_template, request, jsonify
from flask_socketio import SocketIO
from models.tables import Table
from pprint import pprint

class RestaurantApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = True
        self.app.config['HOST'] = '0.0.0.0'
        self.app.config['PORT'] = 8000
        self.socketio = SocketIO(self.app)
        self.socketio.init_app(self.app)
        
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/menu", view_func=self.menu)
        self.app.add_url_rule("/tables", view_func=self.tables)
        self.app.add_url_rule("/tables/get_tables", view_func=self.get_tables, methods=['POST'])
        self.app.add_url_rule("/tables/get_orders_table_data", view_func=self.get_orders_table_data, methods=['POST'])
        self.app.add_url_rule("/tables/open_table", view_func=self.open_table, methods=['POST'])
        self.app.add_url_rule("/tables/close_table", view_func=self.close_table, methods=['POST'])
        self.app.add_url_rule("/orders", view_func=self.orders)
        
        self.socketio.on_event('message', self.handle_message)
        self.socketio.on_event('open_table', self.handle_open_table)
        
    def home(self):
        return render_template("index.html")
    
    def menu(self):
        return render_template("menu.html")
    
    def tables(self):
        return render_template("tables.html")
    
    def get_tables(self):
        if request.method == 'POST':
            return Table.get_all_tables()
    
    def get_orders_table_data(self):
        if request.method == 'POST':
            parse_json = request.json
            return Table.get_table_orders_data(parse_json['id'])
    
    def open_table(self):
        if request.method == 'POST':
            parse_json = request.json
            response = Table.open_table(parse_json['tableId'], parse_json['waiter'], parse_json['comment'], parse_json['status'])
            if response is None:
                return jsonify(message="error")
            else:
                self.socketio.emit("message", {"data": "update"})
                return jsonify(message="success")
    
    def close_table(self, table_id):
        # Obtener la información de la mesa desde la base de datos
        table = Table.get_table_by_id(table_id)
        if table is None:
            return jsonify(message="error: table not found")
        
        # Emitir un mensaje a través de Socket.IO para notificar a los clientes que la mesa se ha cerrado
        self.socketio.emit("message", {"data": "update"})
        return jsonify(message="success")
    
    def orders(self):
        return render_template("orders.html")
    
    def handle_message(self, data):
        print('received message: ' + str(data))
    
    def handle_open_table(self, data):
        print('received message: ' + str(data))
    
    def run(self):
        self.socketio.run(
            self.app,
            port=self.app.config['PORT'],
            host=self.app.config['HOST']
        )

if __name__ == '__main__':
    app = RestaurantApp()
    app.run()