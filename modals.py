from database import Database
from pprint import pprint
import datetime
import json
class Models:
    def __init__(self,id,name) -> None:
        self.id = id
        self.name = name
        
    @classmethod
    def get_table_id(self,id):
        db = Database()
        return db.fetch_one("select * from tables where id='%s'",(id,))
    
    @classmethod
    def get_tables(self):
        data = list()
        db = Database()
        results = db.fetch_all("select * from tables")
        
        for i in results:
            data.append({
                "table_id":i[0],
                "name":i[1],
                "status":i[2]
            })
        return json.dumps(data,default=str)
    
    @classmethod
    def get_table_open_id(self,table_id):
        db = Database()
        result = db.fetch_one("SELECT r.reservation_id,r.comment,r.reservation_date,r.start_time FROM reservations AS r INNER JOIN tables AS t ON r.table_id = t.id WHERE t.id = %s AND r.status = t.status",(table_id,))
        if result != None:
            return {
                "reservation_id":result[0],
                "comment":result[1],
                "reservation_date":result[2],
                "start_time":result[3]
            }
        else:
            return None

            
    @classmethod
    def open_table_id(self,table_id,waiter,comment,status):
        db = Database()
        if status == "close":
            try:
                db.execute("update tables set status='open' where id=%s",(table_id,))
                db.execute("insert into reservations (table_id,comment,reservation_date,start_time,status)values(%s,%s,%s,%s,%s)",(table_id,comment,self.get_date(),self.get_time(),'open',))
                if db.cursor.rowcount == 0:
                    print(f"[open_table_id] => None, time:{self.get_time()}")
                    return None
                else:
                    print(f"[open_table_id] => success, time:{self.get_time()}")
                    return "success"
            except Exception as err:
                print(err)
                return(err)
    
    @classmethod
    def get_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    @classmethod
    def get_time(self): 
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    @classmethod
    def get_tables_id(self,id):
        db = Database()
        return db.fetch_all("SELECT o.id,m.name,m.description,o.quantity,m.price,o.status from orders AS o INNER JOIN tables AS t ON o.table_id = t.id INNER JOIN menu AS m ON o.menu_id = m.id WHERE t.id = %s ",(id,))
    
    @classmethod
    def get_table_orders_id(self,id):
        data = list()
        result = self.get_table_id(id)
        data.append({
            "id":result[0],
            "name":result[1],
            "orders":[]
        })
        for i in self.get_tables_id(id):
            data[0]["orders"] += [{
                "id":i[0],
                "name":i[1],
                "description":i[2],
                "quantity":i[3],
                "price":i[4],
                "status":i[5]
            }]
        return data
    
pprint(Models.get_date())


    