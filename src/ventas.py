import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class VentasFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Ventas", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar Folio de Venta").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search_folio = tk.Entry(self)
        self.entry_search_folio.grid(row=1, column=1, pady=5, padx=10)
        self.search_folio_button = tk.Button(self, text="Buscar")
        self.search_folio_button.grid(row=1, column=2, padx=5)

        # Campo para folio de venta (bloqueado, será autoincremental o lo generaremos)
        tk.Label(self, text="Folio de Venta").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_folio = tk.Entry(self, state='readonly')  
        self.entry_folio.grid(row=2, column=1, pady=5, padx=10)

        # Campo para la fecha (bloqueado debido a que tomará la fecha del día, solo lectura)
        tk.Label(self, text="Fecha").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_date = DateEntry(self, state='readonly', width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=3, column=1, pady=5, padx=10)
        self.entry_date.set_date(datetime.now())  

        tk.Label(self, text="Usuario").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Cliente").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_client = tk.Entry(self)
        self.entry_client.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Productos").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.listbox_products = tk.Listbox(self, height=5)
        self.listbox_products.grid(row=6, column=1, pady=5, padx=10)

        # Simulando una lista de productos disponibles
        self.products = [("Producto A - $100", 100), ("Producto B - $200", 200), ("Producto C - $300", 300)]
        for product in self.products:
            self.listbox_products.insert(tk.END, product[0])  

        tk.Label(self, text="Cantidad").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=7, column=1, pady=5, padx=10)

        self.add_product_button = tk.Button(self, text="Agregar Producto", command=self.add_product)
        self.add_product_button.grid(row=8, column=1, pady=10)

        # Tabla para mostrar productos seleccionados y su cantidad, ademas de precio unitario y total
        self.treeview = ttk.Treeview(self, columns=("Producto", "Cantidad", "Precio Unitario", "Precio Total"), show='headings')
        self.treeview.heading("Producto", text="Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Precio Unitario", text="Precio Unitario")
        self.treeview.heading("Precio Total", text="Precio Total")
        self.treeview.grid(row=9, column=0, columnspan=2, pady=10)

        self.total_label = tk.Label(self, text="Total a Pagar: $0.00", font=("Helvetica", 12, "bold"))
        self.total_label.grid(row=10, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=11, column=0, columnspan=4, pady=20)

        self.create_button = tk.Button(button_frame, text="Crear Venta", width=10)
        self.create_button.grid(row=0, column=0, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar Venta", width=10)
        self.update_button.grid(row=0, column=1, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar Venta", width=10)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10)
        self.cancel_button.grid(row=0, column=3, padx=10)

    def add_product(self):
        selected_product_index = self.listbox_products.curselection()
        if selected_product_index:
            product_info = self.listbox_products.get(selected_product_index)
            product_name = product_info.split(" - ")[0]  
            price = float(product_info.split("$")[1])  
            quantity = self.entry_quantity.get()

            if quantity.isdigit() and int(quantity) > 0:
                quantity = int(quantity)
                total_price = price * quantity  

                self.treeview.insert("", "end", values=(product_name, quantity, f"${price:.2f}", f"${total_price:.2f}"))
                self.entry_quantity.delete(0, tk.END)  
                
                self.update_total()  
            else:
                messagebox.showerror("Error", "Cantidad inválida.")  

    def update_total(self):
        total = 0.0
        for item in self.treeview.get_children():
            # Sumar todos los precios totales
            total += float(self.treeview.item(item)["values"][3].replace('$', '').replace(',', ''))
        self.total_label.config(text=f"Total a Pagar: ${total:.2f}")  # Actualizar etiqueta de total

