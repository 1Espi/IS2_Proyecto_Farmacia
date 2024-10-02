import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class AlmacenFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Almacén", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por ID de Producto").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search_id = tk.Entry(self)
        self.entry_search_id.grid(row=1, column=1, pady=5, padx=10)

        self.search_button = tk.Button(self, text="Buscar")
        self.search_button.grid(row=1, column=2, padx=10)

        # ID(sera autoincremental,solo para lectura)
        tk.Label(self, text="ID del Producto").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_product_id = tk.Entry(self, state='readonly')  
        self.entry_product_id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre del Producto").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_product = tk.Entry(self)
        self.entry_product.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Cantidad").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Precio por Unidad").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_price_unit = tk.Entry(self)
        self.entry_price_unit.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Fecha de Entrada").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_date = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=6, column=1, pady=5, padx=10)

        tk.Label(self, text="Estado").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entry_status = ttk.Combobox(self, values=["Disponible", "Agotado"])
        self.entry_status.grid(row=7, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20)

        self.create_button = tk.Button(button_frame, text="Crear", width=10)
        self.create_button.grid(row=0, column=0, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10)
        self.update_button.grid(row=0, column=1, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", width=10)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10)
        self.cancel_button.grid(row=0, column=3, padx=10)
