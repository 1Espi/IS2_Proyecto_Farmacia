import tkinter as tk
from tkinter import ttk
import utilities.connection as dbconn

class Proveedores:
    def __init__(self):
        self.window_prov = tk.Tk()
        self.window_prov.geometry("900x500")
        self.window_prov.title("Información de proveedores")
        self.setup_ui()
        
        self.window_prov.mainloop()
        
    def setup_ui(self):
         # Labels y campos de entrada para proveedor
        tk.Label(self.window_prov, text="Compañía:").place(x=20, y=20)
        self.entry_compania = tk.Entry(self.window_prov)
        self.entry_compania.place(x=100, y=20)

        tk.Label(self.window_prov, text="Teléfono:").place(x=20, y=50)
        self.entry_telefono = tk.Entry(self.window_prov)
        self.entry_telefono.place(x=100, y=50)

        tk.Label(self.window_prov, text="Correo:").place(x=20, y=80)
        self.entry_correo = tk.Entry(self.window_prov)
        self.entry_correo.place(x=100, y=80)
        
        # Combobox de artículos
        tk.Label(self.window_prov, text="Artículo:").place(x=300, y=20)
        self.combobox_articulos = ttk.Combobox(self.window_prov, state='readonly')
        self.combobox_articulos.place(x=370, y=20)
        self.load_articulos()  # Cargar los artículos desde la base de datos

        # Campos de precio
        tk.Label(self.window_prov, text="Precio Individual:").place(x=300, y=50)
        self.entry_precio_individual = tk.Entry(self.window_prov)
        self.entry_precio_individual.place(x=400, y=50)

        tk.Label(self.window_prov, text="Precio Lote:").place(x=300, y=80)
        self.entry_precio_lote = tk.Entry(self.window_prov)
        self.entry_precio_lote.place(x=400, y=80)
        
        # Botones para guardar y buscar
        tk.Button(self.window_prov, text="Agregar Proveedor", command=self.agregar_proveedor).place(x=20, y=120)
        tk.Button(self.window_prov, text="Buscar", command=self.buscar_proveedor).place(x=180, y=120)
        
        # Campo de búsqueda
        tk.Label(self.window_prov, text="Buscar Proveedor:").place(x=300, y=120)
        self.entry_buscar = tk.Entry(self.window_prov)
        self.entry_buscar.place(x=420, y=120)
        
        # Treeview para mostrar los proveedores y artículos asociados
        self.treeview_articulos_del_proveedor = ttk.Treeview(self.window_prov, columns=("prodprov"), show='headings')
        self.treeview_articulos_del_proveedor.heading("prodprov", text="Productos del proveedor")
        self.treeview_articulos_del_proveedor.place(x=20, y=160, width=420, height=300)
        
        self.treeview_articulos_disponibles = ttk.Treeview(self.window_prov, columns=("proddis"), show='headings')
        self.treeview_articulos_disponibles.heading("proddis", text="Productos disponibles")
        self.treeview_articulos_disponibles.place(x=460, y=160, width=420, height=300)
        
        
    def load_articulos(self):
        pass
    
    def agregar_proveedor(self):
        pass
    
    def buscar_proveedor(self):
        pass