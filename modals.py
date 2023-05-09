from database import Database
from pprint import pprint
class Models:
    def __init__(self,id,name) -> None:
        self.id = id
        self.name = name
        
    @classmethod
    def get_id(self,id):
        db = Database()
        result = db.fetch_one("select * from tables where id='%s'",(id,))
        return {"id":result[0],"name":result[1]}
    
    @classmethod
    def get_tables(self):
        db = Database()
        results = db.fetch_all("select * from tables")
        data = list()
        for i in results:
            data.append({
                "id":i[0],
                "name":i[1]
            })
        return data
    
    @classmethod
    def OPM(self,id):
        db = Database()
        results = db.fetch_all("""
            SELECT
                o.id,
                m.name,
                m.description,
                o.quantity,
                m.price,
                o.status 
            FROM
                orders AS o
                INNER JOIN tables AS t ON o.table_id = t.id
                INNER JOIN menu AS m ON o.menu_id = m.id 
            WHERE
                t.id = %s """,(id,))
        data = list()
        for i in results:
            data.append({
                "id":i[0],
                "name":i[1],
                "description":i[2],
                "quantity":i[3],
                "price":i[4],
                "status":i[5]
            })
        return data
    
       

    