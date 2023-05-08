import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='test'
        )
        self.cursor = self.conn.cursor(buffered=True)
    
    def execute(self, query, parameters=None):
        try:
            self.cursor.execute(query,parameters)
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as error:
            print("Error: {}".format(error))
    
    def fetch_all(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchone()
    
    def close(self):
        self.cursor.close()
        self.conn.close()
