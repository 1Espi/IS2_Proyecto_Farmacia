import os
from dotenv import load_dotenv
import psycopg2

class connection:
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.environ['HOST']
        self.database = os.environ['DATABASE']
        self.user = os.environ['OSOARIO']
        self.password = os.environ['PASSWORD']
    
    def open(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        
        return self.conn
    
    def close(self):
        self.conn.close()
        
"""
    EJEMPLO DE USO
    
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username))
            user = cursor.fetchone() #DEVUELVE UNA LISTA CON LA INFO DE LAS TABLAS
"""