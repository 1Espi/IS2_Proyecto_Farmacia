import tkinter as tk
from tkinter import ttk
import utilities.connection as dbconn

class MostrarCompra(tk.Frame):  # Hereda de tk.Frame
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()
        container.geometry("1200x600")  # Ajustar el tamaño de la ventana

    def setup_ui(self):
        # Título
        title = tk.Label(self, text="Mostrar registros de compras", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        # Treeview como atributo de la clase (self.tree)
        self.tree = ttk.Treeview(self, columns=("id", "nombre", "cantidad", "minimo", "maximo", "disponible"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("minimo", text="Mínimos")
        self.tree.heading("maximo", text="Máximos")
        self.tree.heading("disponible", text="Disponible")

        # Expansión del Treeview en el grid
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # Configurar expansión del grid para que los widgets se ajusten al redimensionar la ventana
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame para los botones
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=4, pady=20)

        # Botón para mostrar registros
        self.btn_mostrar = tk.Button(button_frame, text="Mostrar Registros", command=self.mostrar_registros)  
        self.btn_mostrar.pack(side="left", padx=10)

    def mostrar_registros(self):
        con = dbconn.connection()
        connection = con.open()
        cursor = connection.cursor()

        query = "SELECT * FROM almacen"
        cursor.execute(query)

        
        # Limpiar el Treeview antes de insertar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        resultados = cursor.fetchall()  # Obtiene todos los registros

        # Inserta cada registro en el Treeview
        for registro in resultados:
            disponible = registro[5]
            if disponible[0] == 'Agotado':
                self.tree.insert('', tk.END, values=registro)

        cursor.close()
        connection.close()
