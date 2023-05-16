from database import Database
from pprint import pprint
import datetime
from flask import jsonify
import json

class Table:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def get_table_by_id(cls, id):
        db = Database()
        return db.fetch_one("SELECT * FROM tables WHERE id=%s", (id,))
    
    @classmethod
    def get_date(cls):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def get_time(cls):
        return datetime.datetime.now().strftime("%H:%M:%S")

    @classmethod
    def get_table_orders(cls, id):
        db = Database()
        return db.fetch_all("SELECT o.id, m.name, m.description, o.quantity, m.price, o.status FROM orders AS o INNER JOIN menu AS m ON o.menu_id = m.id INNER JOIN tables AS t ON o.table_id = t.id INNER JOIN reservations AS r ON o.reservation_id = r.reservation_id AND t.id = r.table_id AND t.status = r.status WHERE t.id = %s ", (id,))

    @classmethod
    def open_table(cls, table_id, waiter, comment, status):
        db = Database()
        if status == "close":
            try:
                # Validar que la mesa no esté ya abierta
                table = cls.get_table_by_id(table_id)
                if table is None:
                    return "error: table not found"
                elif table[2] == "open":
                    return "error: table already open"

                db.execute("UPDATE tables SET status='open' WHERE id=%s", (table_id,))
                db.execute("INSERT INTO reservations (table_id, comment, reservation_date, start_time, status) VALUES (%s, %s, %s, %s, %s)", (table_id, comment, cls.get_date(), cls.get_time(), 'open',))
                if db.cursor.rowcount == 0:
                    print(f"[open_table] => None, time:{cls.get_time()}")
                    return None
                else:
                    print(f"[open_table] => success, time:{cls.get_time()}")
                    return "success"
            except Exception as err:
                print(err)
                return err

    @classmethod
    def close_table(cls,table_id):
        db = Database()
        try:
            db.execute("UPDATE tables SET status='close' WHERE id=%s",(table_id,))
            db.execute("UPDATE reservations SET status='close',end_time=%s WHERE table_id=%s AND status = 'open'",(cls.get_time(),table_id,))
            #return r1,r2
            if db.cursor.rowcount == 0:
                print(f"[close_table] => None, time:{cls.get_time()}")
                return None
            else:
                print(f"[close_table] => success, time:{cls.get_time()}")
                return "success"
        except Exception as err:
            print(err)
            return err

    @classmethod
    def get_open_table(cls, table_id):
        db = Database()
        result = db.fetch_one("SELECT r.reservation_id, r.comment, r.reservation_date, r.start_time FROM reservations AS r INNER JOIN tables AS t ON r.table_id = t.id WHERE t.id = %s AND r.status = t.status", (table_id,))
        if result is not None:
            return {
                "reservation_id": result[0],
                "comment": result[1],
                "reservation_date": result[2],
                "start_time": result[3]
            }
        else:
            return None

    @classmethod
    def get_all_tables(cls):
        data = []
        db = Database()
        results = db.fetch_all("SELECT * FROM tables")
        for i in results:
            open_table = cls.get_open_table(i[0])
            if i[2] == "open" and open_table is not None:
                data.append({
                    "tableId": i[0],
                    "name": i[1],
                    "reservation_id": open_table['reservation_id'],
                    "comment": open_table['comment'],
                    "reservation_date": open_table['reservation_date'],
                    "start_time": open_table['start_time'],
                    "end_time": "",
                    "status": i[2]
                })
            else:
                data.append({
                    "tableId": i[0],
                    "name": i[1],
                    "reservation_id": "0",
                    "comment": "N/A",
                    "reservation_date": "N/A",
                    "start_time": "N/A",
                    "end_time": "N/A",
                    "status": i[2]
                })
        return json.dumps(data,default=str)

    @classmethod
    def get_table_orders_data(cls, table_id):
        result = cls.get_table_by_id(table_id)
        data = {
            "tableId": result[0],
            "name": result[1],
            #"total": result[3],
            "orders": []
        }
        for i in cls.get_table_orders(table_id):
            data["orders"] += [{
                "id": i[0],
                "name": i[1],
                "description": i[2],
                "quantity": i[3],
                "price": i[4],
                "status": i[5]
            }]
        return json.dumps(data,default=str)
    
    @classmethod
    def search_menu(cls,search):
        db = Database()
        results = db.fetch_all(f"SELECT id, name, description, price FROM menu WHERE name LIKE '%{search}%' LIMIT 3")
        data = list()
        for i in results:
            data.append({
                "id":i[0],
                "name":i[1],
                "description":i[2],
                "cant":0,
                "price":i[3]
            })
        return data
    
    @classmethod
    def new_table_order(cls,tableId,menuId,cant):
        db = Database()
        result = db.fetch_one("SELECT t.id, r.reservation_id FROM tables AS t INNER JOIN reservations AS r ON t.id = r.table_id WHERE t.id = %s AND t.status = r.status",(tableId,))
        db.execute("INSERT INTO (table_id, reservation_id, menu_id, quantity,status)VALUES(%s,%s,%s,%s,%s)",(result[0],result[1],menuId,cant,'pending'))