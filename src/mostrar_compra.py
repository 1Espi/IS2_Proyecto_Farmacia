import tkinter as tk
from tkinter import ttk
import utilities.connection as dbconn

class MostrarCompra(tk.Frame):  
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()
        container.geometry("1200x600")  

    def setup_ui(self):
        title = tk.Label(self, text="Mostrar registros de los articulos", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

       
        self.tree = ttk.Treeview(self, columns=("id_almacen", "id_articulo", "cantidad", "minimo", "maximo"), show="headings")
        self.tree.heading("id_almacen", text="ID almacen")
        self.tree.heading("id_articulo", text="ID Articulo")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("minimo", text="Mínimos")
        self.tree.heading("maximo", text="Máximos")
        
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=4, pady=20)

        self.btn_mostrar = tk.Button(button_frame, text="Mostrar Registros", command=self.mostrar_registros)  
        self.btn_mostrar.pack(side="left", padx=10)

    def mostrar_registros(self):
        con = dbconn.connection()
        connection = con.open()
        cursor = connection.cursor()

        query = "SELECT * FROM almacen"
        cursor.execute(query)

        for item in self.tree.get_children():
            self.tree.delete(item)

        resultados = cursor.fetchall()  

        for registro in resultados:
            if registro[2] <= registro[3]:
                self.tree.insert('', tk.END, values=registro)

        cursor.close()
        connection.close()

