import os
from dotenv import load_dotenv
import psycopg2
from tkinter import messagebox

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

def connect_db():
    try:
        db_instance: connection = connection()
        conn = db_instance.open() 
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None
