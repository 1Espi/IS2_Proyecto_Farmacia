import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import utilities.connection as dbconn

class VentasFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.connection = self.connect_db() 
        self.setup_ui()
        self.subtotal = 0.0
        self.iva_rate = 0.16  # 16% IVA
        self.total = 0.0
        self.puntos_acumulados = 0
        self.cliente_id = None  
        self.puntos_cliente = 0

        
    def connect_db(self):
        try:
            con = dbconn.connection()
            connection = con.open()  
            return connection
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Ventas", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=5, pady=10)

        # Barra de búsqueda de folio
        tk.Label(self, text="Buscar por Folio:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.search_folio_entry = tk.Entry(self)
        self.search_folio_entry.grid(row=1, column=1, padx=10, pady=5)
        self.search_button = tk.Button(self, text="Buscar", command=self.search_sale)
        self.search_button.grid(row=1, column=2, padx=5)

        # Botones de Crear, Modificar y Eliminar Venta
        self.create_button = tk.Button(self, text="Crear Venta", command=self.create_sale)
        self.create_button.grid(row=1, column=3, padx=5, pady=5)
        self.modify_button = tk.Button(self, text="Modificar Venta", command=self.modify_sale)
        self.modify_button.grid(row=1, column=4, padx=5, pady=5)
        self.delete_button = tk.Button(self, text="Eliminar Venta", command=self.delete_sale)
        self.delete_button.grid(row=1, column=5, padx=5, pady=5)

        # Fila 2: Folio y Fecha
        tk.Label(self, text="Folio de Venta").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_folio = tk.Entry(self, state='readonly')  
        self.entry_folio.grid(row=2, column=1, pady=5, padx=10)
        tk.Label(self, text="Fecha").grid(row=2, column=2, sticky='w', padx=10, pady=5)
        self.entry_date = DateEntry(self, state='readonly', width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_date.grid(row=2, column=3, pady=5, padx=10)
        self.entry_date.set_date(datetime.now())
        tk.Label(self, text="Usuario que atendio").grid(row=2, column=4, sticky='w', padx=10, pady=5)
        self.entry_usuario = tk.Entry(self, state='normal')  
        self.entry_usuario.grid(row=2, column=5, pady=5, padx=10)
        self.entry_usuario.insert(0, self.parent.user_info['USERNAME'])
        self.entry_usuario.config(state="readonly")
        self.user_id = self.parent.user_info['ID']  # ID Almacenado para futuro

        # Fila 3: Combobox de Cliente
        tk.Label(self, text="Cliente").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.combo_client = ttk.Combobox(self, values=self.get_client_list(), width=50)
        self.combo_client.grid(row=3, column=1, pady=5, padx=10)
        self.combo_client['state'] = 'readonly'
        self.combo_client.bind('<<ComboboxSelected>>', self.load_client_details)

        # Fila 4: Información del Cliente
        tk.Label(self, text="Teléfono").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=4, column=1, pady=5, padx=10)
        tk.Label(self, text="Correo").grid(row=4, column=2, sticky='w', padx=10, pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=4, column=3, pady=5, padx=10)
        tk.Label(self, text="Puntos").grid(row=4, column=4, sticky='w', padx=10, pady=5)
        self.entry_puntos = tk.Entry(self)
        self.entry_puntos.grid(row=4, column=5, pady=5, padx=10)

        # Fila 5: Combobox de Productos
        tk.Label(self, text="Producto").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.combo_product = ttk.Combobox(self, values=self.get_product_list(), width=50)
        self.combo_product.grid(row=5, column=1, pady=5, padx=10)
        self.combo_product['state'] = 'readonly'
        self.combo_product.bind('<<ComboboxSelected>>', self.load_product_details)
        

        # Fila 7: Precio y stock
        tk.Label(self, text="Precio").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_price = tk.Entry(self)
        self.entry_price.grid(row=6, column=1, pady=5, padx=10)
        tk.Label(self, text="Stock").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.entry_stock = tk.Entry(self)
        self.entry_stock.grid(row=7, column=1, pady=5, padx=10)
        
        # Fila 9: Cantidad y agregar/quitar
        tk.Label(self, text="Cantidad").grid(row=8, column=0, sticky='w', padx=10, pady=5)
        self.entry_quantity = tk.Entry(self)
        self.entry_quantity.grid(row=8, column=1, pady=5, padx=10)
        self.add_button = tk.Button(self, text="Agregar", command=self.add_product)
        self.add_button.grid(row=8, column=2, padx=5)
        self.remove_button = tk.Button(self, text="Quitar", command=self.remove_product)
        self.remove_button.grid(row=8, column=3, padx=5)


        # Fila 10: Treeview de productos
        self.treeview = ttk.Treeview(self, columns=("Código", "Descripción", "Precio", "Cantidad", "Importe"), show='headings')
        self.treeview.heading("Código", text="Código")
        self.treeview.heading("Descripción", text="Descripción")
        self.treeview.heading("Precio", text="Precio")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Importe", text="Importe")
        self.treeview.grid(row=10, column=0, columnspan=4, pady=10)
        
        # Fila 11: Subtotal, IVA y Total
        tk.Label(self, text="Subtotal").grid(row=11, column=0, sticky='w', padx=10, pady=5)
        self.entry_subtotal = tk.Entry(self)
        self.entry_subtotal.grid(row=11, column=1, pady=5, padx=10)
        tk.Label(self, text="IVA").grid(row=11, column=2, sticky='w', padx=10, pady=5)
        self.entry_iva = tk.Entry(self)
        self.entry_iva.grid(row=11, column=3, pady=5, padx=10)
        tk.Label(self, text="Total").grid(row=12, column=0, sticky='w', padx=10, pady=5)
        self.entry_total = tk.Entry(self)
        self.entry_total.grid(row=12, column=1, pady=5, padx=10)
        tk.Label(self, text="Puntos acumulados").grid(row=12, column=2, sticky='w', padx=10, pady=5)
        self.entry_puntosAcumulados = tk.Entry(self)
        self.entry_puntosAcumulados.grid(row=12, column=3, pady=5, padx=10)

        # Fila 13: Pago y botón de pagar
        tk.Label(self, text="Pago con").grid(row=13, column=0, sticky='w', padx=10, pady=5)
        self.entry_payment = tk.Entry(self)
        self.entry_payment.grid(row=13, column=1, pady=5, padx=10)
        self.pay_button = tk.Button(self, text="Pagar", command=self.process_payment)
        self.pay_button.grid(row=13, column=2, padx=5)
        self.cancel_button = tk.Button(self, text="Cancelar compra", command=self.cancel_sale)
        self.cancel_button.grid(row=13, column=3, padx=5)

    def create_sale(self):
        pass

    def modify_sale(self):
        pass

    def delete_sale(self):
        pass

    def cancel_sale(self):
        # Obtener la lista de productos en el Treeview
        items = self.treeview.get_children()
        
        if not items:
            messagebox.showinfo("Información", "No hay ventas que cancelar.")
            return
        
        # Conectar a la base de datos
        cursor = self.connection.cursor()
        
        for item in items:
            item_values = self.treeview.item(item, 'values')
            product_id = int(item_values[0])  # ID del producto
            quantity = int(item_values[3])  # Cantidad de producto en la venta

            # Actualizar el stock en la base de datos
            cursor.execute(
                "UPDATE almacen SET cantidad = cantidad + %s WHERE id_articulo = %s",
                (quantity, product_id)
            )
        
        # Confirmar los cambios en la base de datos
        self.connection.commit()
        
        # Limpiar los campos (excepto el nombre de usuario)
        self.entry_folio.config(state='normal')
        self.entry_folio.delete(0, tk.END)
        self.entry_date.set_date(datetime.now())
        self.combo_client.set('')
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_puntos.delete(0, tk.END)
        self.combo_product.set('')
        self.entry_price.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

        # Limpiar el Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Reiniciar el subtotal, IVA y total
        self.entry_subtotal.delete(0, tk.END)
        self.entry_iva.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
        self.entry_puntosAcumulados.delete(0, tk.END)
        self.entry_payment.delete(0, tk.END)
        
        messagebox.showinfo("Información", "La venta ha sido cancelada")

        
    def get_client_list(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_cliente, nombre FROM cliente")
        clients = cursor.fetchall()
        self.clients_dict = {name: id_cliente for id_cliente, name in clients}
        return list(self.clients_dict.keys())

    def load_client_details(self, event):
        client_name = self.combo_client.get()
        client_id = self.clients_dict.get(client_name)
        cursor = self.connection.cursor()
        cursor.execute("SELECT telefono, email, puntos FROM cliente WHERE id_cliente = %s", (client_id,))
        self.cliente_id = client_id
        client_data = cursor.fetchone()
        if client_data:
            telefono, correo, puntos = client_data
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, telefono)
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, correo)
            self.entry_puntos.delete(0, tk.END)
            self.entry_puntos.insert(0, puntos)
            
            self.puntos_cliente = puntos
            if self.puntos_cliente >= 20:
                messagebox.showinfo("Descuento Disponible", "Tendrás un 50% de descuento en tu compra.")
            

    def get_product_list(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT almacen.id_articulo, nombre FROM articulos LEFT JOIN almacen ON articulos.id_articulo=almacen.id_articulo WHERE almacen.cantidad > 0")
        products = cursor.fetchall()
        self.products_dict = {name: id_art for id_art, name in products}
        return list(self.products_dict.keys())

    def load_product_details(self, event):
        product_name = self.combo_product.get()
        product_id = self.products_dict.get(product_name)
        cursor = self.connection.cursor()
        cursor.execute("SELECT precio, almacen.cantidad FROM articulos LEFT JOIN almacen ON articulos.id_articulo = almacen.id_articulo WHERE articulos.id_articulo = %s", (product_id,))
        product_data = cursor.fetchone()
        if product_data:
            precio, stock = product_data
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, precio)
            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, stock)
            
    def add_product(self):
        product_name = self.combo_product.get()

        try:
            quantity = int(self.entry_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una cantidad válida.")
            return

        if not product_name:
            messagebox.showerror("Error", "Por favor, selecciona un producto.")
            return

        product_id = self.products_dict.get(product_name)

        cursor = self.connection.cursor()
        cursor.execute("SELECT cantidad FROM almacen WHERE id_articulo = %s", (product_id,))
        stock_data = cursor.fetchone()

        if stock_data:
            stock_available = stock_data[0]
            if quantity > stock_available:
                messagebox.showerror("Error", "La cantidad excede el stock disponible.")
                return
        else:
            messagebox.showerror("Error", "No se encontró el stock del producto.")
            return

        # Verificar si el producto ya está en el Treeview
        for item in self.treeview.get_children():
            item_values = self.treeview.item(item, 'values')
            if item_values[0] == str(product_id):  # Comparar con el ID del producto como cadena
                current_quantity = int(item_values[3])
                new_quantity = current_quantity + quantity
                new_importe = new_quantity * float(item_values[2])
                self.treeview.item(item, values=(item_values[0], product_name, item_values[2], new_quantity, new_importe))
                break
        else:
            try:
                price = float(self.entry_price.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa un precio válido.")
                return

            # Aplicar el descuento del 50% si el cliente tiene 20 puntos
            if self.puntos_cliente >= 20:
                price *= 0.5

            importe = quantity * price
            self.treeview.insert('', 'end', values=(str(product_id), product_name, price, quantity, importe))

        new_stock = stock_available - quantity
        cursor.execute("UPDATE almacen SET cantidad = %s WHERE id_articulo = %s", (new_stock, product_id))
        self.connection.commit()

        self.update_totals()

        self.clear_fields()

    def remove_product(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un producto para eliminar.")
            return

        item_values = self.treeview.item(selected_item, 'values')
        product_id = item_values[0]
        quantity_to_return = int(item_values[3])  # Obtener la cantidad del artículo a eliminar

        # Eliminar el producto del Treeview
        self.treeview.delete(selected_item)

        # Devolver el stock al almacén
        cursor = self.connection.cursor()
        cursor.execute("SELECT cantidad FROM almacen WHERE id_articulo = %s", (product_id,))
        stock_data = cursor.fetchone()
        if stock_data:
            current_stock = stock_data[0]
            new_stock = current_stock + quantity_to_return
            cursor.execute("UPDATE almacen SET cantidad = %s WHERE id_articulo = %s", (new_stock, product_id))
            self.connection.commit()
        else:
            messagebox.showerror("Error", "No se encontró el stock del producto.")

        self.update_totals()

        messagebox.showinfo("Información", "Producto eliminado y stock actualizado.")

    def update_totals(self):
        self.subtotal = sum(float(self.treeview.item(item, 'values')[4]) for item in self.treeview.get_children())
        self.entry_subtotal.delete(0, tk.END)
        self.entry_subtotal.insert(0, f"{self.subtotal:.2f}")

        iva = self.subtotal * self.iva_rate
        self.entry_iva.delete(0, tk.END)
        self.entry_iva.insert(0, f"{iva:.2f}")

        self.total = self.subtotal + iva
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, f"{self.total:.2f}")

        self.puntos = int(self.total // 100)  
        self.entry_puntosAcumulados.delete(0, tk.END)
        self.entry_puntosAcumulados.insert(0, self.puntos)

    def clear_fields(self):
        """Limpia los campos de entrada."""
        self.combo_product.set('')
        self.entry_stock.delete(0,tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
    

    def process_payment(self):
        # Verificar si se ha seleccionado un cliente
        if self.cliente_id is None:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente antes de proceder al pago.")
            return

        payment = self.entry_payment.get()
        if not payment:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el monto del pago.")
            return

        try:
            payment = float(payment)
            if payment < self.total:
                messagebox.showwarning("Advertencia", "El pago es insuficiente.")
                return

            change = payment - self.total
            cursor = self.connection.cursor()

            # Obtener información de la compra
            subtotal = float(self.entry_subtotal.get())
            if self.puntos_cliente >= 20:
                descuento = 50  
                self.puntos_cliente -= 20  
                self.update_cliente_puntos(aplicar_descuento=True)  
            else:
                descuento = 0
                self.puntos_acumulados += self.puntos
                self.update_cliente_puntos(aplicar_descuento=False)  


            total = float(self.entry_total.get())
            fecha = self.entry_date.get_date()
            cliente_id = self.cliente_id
            usuario_id = self.user_id

            cursor.execute(
                "INSERT INTO compras (id_usuario, id_cliente, fecha, subtotal, descuento, total) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_compra",
                (usuario_id, cliente_id, fecha, subtotal, descuento, total)
            )
            id_compra = cursor.fetchone()[0]

            # Insertar cada artículo en la tabla 'articulos_compras'
            for item in self.treeview.get_children():
                item_data = self.treeview.item(item, 'values')
                id_articulo = self.products_dict[item_data[1]]
                cantidad = int(item_data[3])
                subtotal_item = float(item_data[4])

                cursor.execute(
                    "INSERT INTO articulos_compras (id_compra, id_articulo, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                    (id_compra, id_articulo, cantidad, subtotal_item)
                )

            self.connection.commit()

            if descuento == 0:
                self.puntos_acumulados += self.puntos
                self.update_cliente_puntos()  # Actualizamos los puntos del cliente en la BD si no se aplicó descuento

            # Preguntar al usuario si quiere ver el ticket
            response = messagebox.askyesno("Transacción Completa", f"Pago recibido. Cambio: {change:.2f}.\n\n¿Desea ver el ticket de compra?")
            if response:
                self.show_ticket(descuento)  

            messagebox.showinfo("Éxito", f"La venta ha sido registrada con el folio: {id_compra}")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un monto de pago válido.")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo completar la venta: {e}")




    def search_sale(self):
        folio = self.search_folio_entry.get()

        if not folio:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un folio para buscar.")
            return
        try:
            cursor = self.connection.cursor()

            # Consulta principal para la tabla compras
            cursor.execute("""
                SELECT c.id_compra, c.fecha, c.subtotal, c.descuento, c.total, c.id_cliente, u.nombre 
                FROM compras c 
                JOIN usuarios u ON c.id_usuario = u.id
                WHERE c.id_compra = %s
            """, (folio,))
            sale_data = cursor.fetchone()

            if sale_data:
                id_compra, fecha, subtotal, descuento, total, id_cliente, usuario_nombre = sale_data

                self.entry_folio.config(state='normal')
                self.entry_folio.delete(0, tk.END)
                self.entry_folio.insert(0, id_compra)
                self.entry_folio.config(state='readonly')

                self.entry_date.set_date(fecha)
                self.entry_usuario.config(state='normal')
                self.entry_usuario.delete(0, tk.END)
                self.entry_usuario.insert(0, usuario_nombre)
                self.entry_usuario.config(state='readonly')
                
                cursor.execute("SELECT nombre, telefono, email, puntos FROM cliente WHERE id_cliente = %s", (id_cliente,))
                client_data = cursor.fetchone()
                if client_data:
                    nombre_cliente, telefono, email, puntos = client_data
                    self.combo_client.set(nombre_cliente)
                    self.entry_phone.delete(0, tk.END)
                    self.entry_phone.insert(0, telefono)
                    self.entry_email.delete(0, tk.END)
                    self.entry_email.insert(0, email)
                    self.entry_puntos.delete(0, tk.END)
                    self.entry_puntos.insert(0, puntos)
                
                self.entry_subtotal.delete(0, tk.END)
                self.entry_subtotal.insert(0, subtotal)
                self.entry_iva.delete(0, tk.END)
                self.entry_iva.insert(0, round(subtotal * self.iva_rate, 2))
                self.entry_total.delete(0, tk.END)
                self.entry_total.insert(0, total)

                for item in self.treeview.get_children():
                    self.treeview.delete(item)

                cursor.execute("""
                    SELECT ac.id_articulo, a.nombre, a.precio, ac.cantidad, ac.subtotal
                    FROM articulos_compras ac
                    JOIN articulos a ON ac.id_articulo = a.id_articulo
                    WHERE ac.id_compra = %s
                """, (id_compra,))
                products_data = cursor.fetchall()
                for product in products_data:
                    id_articulo, nombre, precio, cantidad, subtotal_item = product
                    self.treeview.insert("", "end", values=(id_articulo, nombre, precio, cantidad, subtotal_item))
            else:
                messagebox.showinfo("No encontrado", "No se encontró una venta con el folio especificado.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")
        finally:
            cursor.close()


            
    def show_ticket(self, descuento=0):
        ticket_details = "----- TICKET DE COMPRA -----\n"
        ticket_details += f"Folio: {self.entry_folio.get()}\n"
        ticket_details += f"Fecha: {self.entry_date.get_date()}\n"
        ticket_details += f"Cliente: {self.combo_client.get()}\n"
        ticket_details += "Productos:\n"
        
        for item in self.treeview.get_children():
            item_values = self.treeview.item(item, 'values')
            ticket_details += f"- {item_values[1]} (Cantidad: {item_values[3]}, Importe: {item_values[4]})\n"
        
        ticket_details += f"\nSubtotal: {self.entry_subtotal.get()}\n"
        ticket_details += f"IVA: {self.entry_iva.get()}\n"
        
        if descuento > 0:
            ticket_details += f"Descuento aplicado: {descuento}%\n"
            puntos_acumulados = 0  
        else:
            puntos_acumulados = self.entry_puntosAcumulados.get()  

        ticket_details += f"Total: {self.entry_total.get()}\n"
        ticket_details += f"Puntos acumulados: {puntos_acumulados}\n"
        ticket_details += "---------------------------"

        messagebox.showinfo("Ticket de Compra", ticket_details)


        
    def update_cliente_puntos(self, aplicar_descuento=False):
        cursor = self.connection.cursor()

        if aplicar_descuento:
            # Si se aplicó descuento, restar los 20 puntos
            cursor.execute("UPDATE cliente SET puntos = %s WHERE id_cliente = %s", (self.puntos_cliente, self.cliente_id))
        else:
            # Si no se aplicó descuento, acumular los nuevos puntos
            cursor.execute("UPDATE cliente SET puntos = puntos + %s WHERE id_cliente = %s", (self.puntos, self.cliente_id))

        self.connection.commit()

