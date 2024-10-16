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

        # Fila 1: Folio y Fecha
        tk.Label(self, text="Folio de Venta").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_folio = tk.Entry(self, state='readonly')  
        self.entry_folio.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(self, text="Fecha").grid(row=1, column=2, sticky='w', padx=10, pady=5)
        self.entry_date = DateEntry(self, state='readonly', width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=1, column=3, pady=5, padx=10)
        self.entry_date.set_date(datetime.now())

        # Fila 2: Combobox de Productos con búsqueda
        tk.Label(self, text="Producto").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.combo_product = ttk.Combobox(self, values=self.get_product_list(), width=50)
        self.combo_product.grid(row=2, column=1, pady=5, padx=10)
        self.combo_product['state'] = 'readonly'
        self.combo_product.bind('<KeyRelease>', self.filter_products)

        self.search_product_button = tk.Button(self, text="Buscar")
        self.search_product_button.grid(row=2, column=2, padx=5)

        # Fila 3: Entry de código del producto y Combobox de clientes con búsqueda
        tk.Label(self, text="Código Producto").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_code = tk.Entry(self)
        self.entry_code.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Cliente").grid(row=3, column=2, sticky='w', padx=10, pady=5)
        self.combo_client = ttk.Combobox(self, values=self.get_client_list(), width=30)
        self.combo_client.grid(row=3, column=3, pady=5, padx=10)
        self.combo_client['state'] = 'readonly'
        self.combo_client.bind('<KeyRelease>', self.filter_clients)

        # Fila 4: Entry de descripción del producto y teléfono del cliente
        tk.Label(self, text="Descripción").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_description = tk.Entry(self)
        self.entry_description.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Teléfono Cliente").grid(row=4, column=2, sticky='w', padx=10, pady=5)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=4, column=3, pady=5, padx=10)

        # Fila 5: Entry de precio del producto y email del cliente
        tk.Label(self, text="Precio").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_price = tk.Entry(self)
        self.entry_price.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Email Cliente").grid(row=5, column=2, sticky='w', padx=10, pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=5, column=3, pady=5, padx=10)

        # Fila 6: Entry de stock y puntos actuales del cliente
        tk.Label(self, text="Stock").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_stock = tk.Entry(self)
        self.entry_stock.grid(row=6, column=1, pady=5, padx=10)

        tk.Label(self, text="Puntos Cliente").grid(row=6, column=2, sticky='w', padx=10, pady=5)
        self.entry_points = tk.Entry(self)
        self.entry_points.grid(row=6, column=3, pady=5, padx=10)

        # Fila 7: Cantidad del producto seleccionado y botones agregar/quitar
        tk.Label(self, text="Cantidad").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=7, column=1, pady=5, padx=10)

        self.add_button = tk.Button(self, text="Agregar", command=self.add_product)
        self.add_button.grid(row=7, column=2, padx=5)

        self.remove_button = tk.Button(self, text="Quitar")
        self.remove_button.grid(row=7, column=3, padx=5)

        # Fila 8: Treeview de productos agregados
        self.treeview = ttk.Treeview(self, columns=("Código", "Descripción", "Precio", "Cantidad", "Importe"), show='headings')
        self.treeview.heading("Código", text="Código")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("Precio", text="Precio")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Importe", text="Importe")
        self.treeview.grid(row=8, column=0, columnspan=4, pady=10)

        # Fila 9: Subtotal, IVA y Total
        tk.Label(self, text="Subtotal").grid(row=9, column=0, sticky='w', padx=10, pady=5)
        self.entry_subtotal = tk.Entry(self)
        self.entry_subtotal.grid(row=9, column=1, pady=5, padx=10)

        tk.Label(self, text="IVA").grid(row=9, column=2, sticky='w', padx=10, pady=5)
        self.entry_iva = tk.Entry(self)
        self.entry_iva.grid(row=9, column=3, pady=5, padx=10)

        tk.Label(self, text="Total").grid(row=10, column=0, sticky='w', padx=10, pady=5)
        self.entry_total = tk.Entry(self)
        self.entry_total.grid(row=10, column=1, pady=5, padx=10)

        # Fila 10: Pago con y botón de pagar
        tk.Label(self, text="Pago con").grid(row=11, column=0, sticky='w', padx=10, pady=5)
        self.entry_payment = tk.Entry(self)
        self.entry_payment.grid(row=11, column=1, pady=5, padx=10)

        self.pay_button = tk.Button(self, text="Pagar", command=self.process_payment)
        self.pay_button.grid(row=11, column=2, padx=5)

    def get_product_list(self):
        return ["Coca Cola", "Pepsi", "Fanta", "Agua Mineral", "Jugo de Naranja"]

    def get_client_list(self):
        return ["Cliente 1", "Cliente 2", "Cliente 3", "Cliente 4"]

    def filter_products(self, event):
        value = event.widget.get().lower()
        filtered_products = [prod for prod in self.get_product_list() if value in prod.lower()]
        self.combo_product['values'] = filtered_products

    def filter_clients(self, event):
        value = event.widget.get().lower()
        filtered_clients = [client for client in self.get_client_list() if value in client.lower()]
        self.combo_client['values'] = filtered_clients

    def add_product(self):
        pass  # Aquí irá la lógica para agregar productos

    def process_payment(self):
        # Mostrar messagebox con puntos acumulados (simulado por ahora)
        messagebox.showinfo("Pago", "Puntos acumulados: 100\nCambio a regresar: $10.00")
