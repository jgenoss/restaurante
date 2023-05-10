from database import Database
from pprint import pprint
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
                "id":i[0],
                "name":i[1],
                "status":i[2],
                "persons":i[3]
            })
        return data
    
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

    