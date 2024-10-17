import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class ComprasFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Compras", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Folio").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search_folio = tk.Entry(self)
        self.entry_search_folio.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar")
        self.search_button.grid(row=1, column=2, padx=10)

        # Folio de compra (Sera el id unico, podemos hacerlo autoincremental o que se genere uno automatico y distinto con el datetime)
        tk.Label(self, text="Folio de Compra").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_folio = tk.Entry(self, state='readonly') 
        self.entry_folio.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Proveedor").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_supplier = tk.Entry(self)
        self.entry_supplier.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Producto").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_product = tk.Entry(self)
        self.entry_product.grid(row=4, column=1, pady=5, padx=10)

        # Al salir de ingresar la cantidad o precio por unidad podemos agregar un tipo onblur para que justo lo coloquemos se calcule el total de compra
        tk.Label(self, text="Cantidad").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Precio por Unidad").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_price_unit = tk.Entry(self)
        self.entry_price_unit.grid(row=6, column=1, pady=5, padx=10)

        #El campo podriamos bloquearlo para que solo tome la fecha actual.
        tk.Label(self, text="Fecha de Compra").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entry_date = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=7, column=1, pady=5, padx=10)

        #El campo sera solo de lectura
        tk.Label(self, text="Total de Compra").grid(row=8, column=0, sticky='w', padx=10, pady=5)
        self.entry_total = tk.Entry(self, state='readonly') 
        self.entry_total.grid(row=8, column=1, pady=5, padx=10)

        tk.Label(self, text="Estado").grid(row=9, column=0, sticky='w', padx=10, pady=5)
        self.entry_status = ttk.Combobox(self, values=["Pendiente", "Completada"])
        self.entry_status.grid(row=9, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=10, column=0, columnspan=4, pady=20)

        self.create_button = tk.Button(button_frame, text="Crear", width=10, command=self.calculate_total)
        self.create_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(button_frame, text="Guardar", width=10)
        self.save_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10)
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", width=10)
        self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10)
        self.cancel_button.grid(row=0, column=4, padx=10)

    def calculate_total(self):
        try:
            quantity = int(self.entry_quantity.get())
            price_per_unit = float(self.entry_price_unit.get())
            total = quantity * price_per_unit
            self.entry_total.config(state='normal')
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
            self.entry_total.config(state='readonly')
        except ValueError:
            pass  