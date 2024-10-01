import tkinter as tk
from tkinter import messagebox
import utilities.connection as dbconn

class ComprasFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent 
        #PARA ACCEDER A LA INFO DE USUARIO USAR self.parent.user_info['AQUI VA EL CAMPO']
        self.setup_ui()

    def setup_ui(self):
        pass