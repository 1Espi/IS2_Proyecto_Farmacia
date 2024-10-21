import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import utilities.connection as connfile 
from .proveedores import MostrarProveedores
from tkinter import END, messagebox, ttk
import re

class ReabastecimientoFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        
        self.lista_disponibles = []
        self.lista_agregados = []
        self.prev_agregados = []
        self.lista_proveedores = []
        
        self.setup_ui()

    def setup_ui(self):
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "SELECT * FROM proveedores"
            cursor.execute(query)
            result = cursor.fetchall()
            
            for i in result:
                self.lista_proveedores.append((i[0], i[1]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener los proveedores\n{e}")
        
        hor_padd = 5
            
        title = tk.Label(self, text="Gestión de reabastecimientos de articulos", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=100, pady=10)

        tk.Label(self, text="Buscar por folio:").grid(row=1, column=0, sticky='e', padx=hor_padd, pady=5)
        self.buscar_id = tk.Entry(self, width=40)
        self.buscar_id.grid(row=1, column=1, pady=5, padx=hor_padd)
        
        self.buscar_button = tk.Button(self, text="Buscar", command=self.buscar)
        self.buscar_button.grid(row=1, column=2, padx=0, sticky='w')

        tk.Label(self, text="Folio:").grid(row=2, column=0, sticky='e', padx=hor_padd, pady=5)
        self.id= tk.Entry(self, state='readonly', width=40) 
        self.id.grid(row=2, column=1, pady=5, padx=hor_padd)
        
        tk.Label(self, text="Proveedor:").grid(row=3, column=0, sticky='e', padx=hor_padd, pady=5)
        estado_options = []
        for proveedor in self.lista_proveedores:
            estado_options.append(proveedor[1])
        self.proveedor = ttk.Combobox(self, values=estado_options, width=37)
        self.proveedor.grid(row=3, column=1, pady=5, padx=hor_padd)
        
        self.prov_button = tk.Button(self, text="Proveedores", width=10, command=self.abrir_proveedores)
        self.prov_button.grid(row=3, column=2, pady=5, padx=0, sticky='w')

        tk.Label(self, text="Usuario que realiza:").grid(row=4, column=0, sticky='e', padx=hor_padd, pady=5)
        self.usuario = tk.Entry(self, width=40)
        self.usuario.grid(row=4, column=1, pady=5, padx=hor_padd)
        self.usuario.config(state='disabled')

        tk.Label(self, text="Monto:").grid(row=5, column=0, sticky='e', padx=hor_padd, pady=5)
        self.monto = tk.Entry(self, state='readonly', width=40)
        self.monto.grid(row=5, column=1, pady=5, padx=hor_padd)

        fecha_hoy = datetime.today()
        tk.Label(self, text="Fecha:").grid(row=6, column=0, sticky='e', padx=hor_padd, pady=5)
        self.fecha = DateEntry(self, width=37, background='darkblue', foreground='white', borderwidth=2,
                               year=fecha_hoy.year, month=fecha_hoy.month, day=fecha_hoy.day)  
        self.fecha.grid(row=6, column=1, pady=5, padx=hor_padd)
        
        tk.Label(self, text="Filtrar por nombre:").grid(row=1, column=3, sticky='e', padx=hor_padd, pady=5)
        self.filtrar_nombre= tk.Entry(self, width=20) 
        self.filtrar_nombre.grid(row=1, column=4, pady=5, padx=hor_padd, sticky='w')
        self.filtrar_nombre.bind("<KeyRelease>", self.filtrar_datos)
        
        self.treeview_disponibles = ttk.Treeview(self, columns=("Codigo", "Nombre"), show="headings")
        self.treeview_disponibles.column("Codigo", anchor="center")
        self.treeview_disponibles.column("Nombre", anchor="center")
        self.treeview_disponibles.heading("Codigo", text="Codigo")
        self.treeview_disponibles.heading("Nombre", text="Nombre")
        self.treeview_disponibles.grid(row=2, column=3, pady=10, padx=10, rowspan=5, columnspan=2)
        self.treeview_disponibles.bind('<ButtonRelease-1>', self.seleccionar_articulo)
        
        tk.Label(self, text="ID:").grid(row=2, column=5, sticky='e', padx=hor_padd, pady=5)
        self.id_producto= tk.Entry(self, state='readonly', width=20) 
        self.id_producto.grid(row=2, column=6, pady=5, padx=15, sticky='w')
        
        tk.Label(self, text="Nombre:").grid(row=3, column=5, sticky='e', padx=hor_padd, pady=5)
        self.nombre_producto= tk.Entry(self, state='readonly', width=20) 
        self.nombre_producto.grid(row=3, column=6, pady=5, padx=15, sticky='w')
        
        tk.Label(self, text="Cantidad:").grid(row=4, column=5, sticky='e', padx=hor_padd, pady=5)
        self.cantidad_producto= tk.Entry(self, state='readonly', width=20) 
        self.cantidad_producto.grid(row=4, column=6, pady=5, padx=15, sticky='w')

        tk.Label(self, text="Precio por unidad:").grid(row=5, column=5, sticky='e', padx=hor_padd, pady=5)
        self.ppi_producto= tk.Entry(self, state='readonly', width=20) 
        self.ppi_producto.grid(row=5, column=6, pady=5, padx=15, sticky='w')
        
        self.quitar_producto_button = tk.Button(self, text="Quitar", command=self.quitar_producto, width=10, state="disabled")
        self.quitar_producto_button.grid(row=6, column=5, pady=5, padx=hor_padd, sticky='e')

        self.agregar_producto_button = tk.Button(self, text="Agregar", command=self.agregar_producto, width=10)
        self.agregar_producto_button.grid(row=6, column=6, pady=5, padx=hor_padd)
        
        self.treeview_agregados = ttk.Treeview(self, style="",columns=("Codigo", "Nombre", "Cantidad", "Precio Unitario", "Subtotal"), show="headings")
        self.treeview_agregados.column("Codigo", anchor="center")
        self.treeview_agregados.column("Nombre", anchor="center")
        self.treeview_agregados.column("Cantidad", anchor="center")
        self.treeview_agregados.column("Precio Unitario", anchor="center")
        self.treeview_agregados.column("Subtotal", anchor="center")
        
        self.treeview_agregados.heading("Codigo", text="Codigo")
        self.treeview_agregados.heading("Nombre", text="Nombre")
        self.treeview_agregados.heading("Cantidad", text="Cantidad")
        self.treeview_agregados.heading("Precio Unitario", text="Precio Unitario")
        self.treeview_agregados.heading("Subtotal", text="Subtotal")
        self.treeview_agregados.grid(row=8, column=0, pady=10, padx=10, rowspan=3, columnspan=8)
        self.treeview_agregados.bind('<ButtonRelease-1>', self.seleccionar_agregados)

        button_frame = tk.Frame(self)
        button_frame.grid(row=11, column=0, columnspan=20, pady=15)

        self.nuevo_button = tk.Button(button_frame, text="Nuevo", width=10, command=self.nuevo)
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.guardar_button = tk.Button(button_frame, text="Guardar", width=10, command=self.guardar)
        self.guardar_button.grid(row=0, column=1, padx=10)

        self.modificar_button = tk.Button(button_frame, text="Modificar", width=10, command=self.modificar)
        self.modificar_button.grid(row=0, column=2, padx=10)

        self.cancelar_button = tk.Button(button_frame, text="Cancelar", width=10, command=self.cancelar)
        self.cancelar_button.grid(row=0, column=4, padx=10)
        
        self.cancelar()
        self.cargar_articulos()
        self.estado_interfaz("cancelar")
    
    def nuevo(self):
        self.limpiar_campos()
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT COALESCE(MAX(id_reabastecimiento), 0) + 1 FROM reabastecimientos")
            id_articulo = cursor.fetchone()
            self.id.insert(0, id_articulo)
            self.estado_interfaz("nuevo")
            self.usuario.config(state="normal")
            self.usuario.delete(0, tk.END)
            self.usuario.insert(0, self.parent.user_info["USERNAME"])
            self.usuario.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo obtener el siguiente ID\n{e}')
            return
    
    def abrir_proveedores(self):
        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Proveedores") 
        mostrar_proveedores = MostrarProveedores(self.parent, nueva_ventana, self.lista_proveedores, self.proveedor)
        mostrar_proveedores.pack(fill='both', expand=True)
        
    def buscar(self):
        id = self.buscar_id.get()
        self.id.config(state='normal')
        if not id.isdigit():
            messagebox.showerror("Error", "El folio tiene que ser un entero")
            return
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = """
                    SELECT 
                        id_reabastecimiento,
                        id_proveedor,
                        id_usuario,
                        fecha,
                        monto
                    FROM 
                        reabastecimientos
                    WHERE 
                        id_reabastecimiento = %s;
                    """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result:
                val_reabastecimiento = result[0]
                
                lista_filtrada = [nombre for id, nombre in self.lista_proveedores if id == result[1]]
                val_proveedor = lista_filtrada[0] if lista_filtrada else None
                
                val_usuario = result[2]
                
                val_fecha= result[3]
                fecha_obj = datetime.strptime(str(val_fecha), "%Y-%m-%d")
                val_fecha = fecha_obj.strftime("%m/%d/%y")
                
                val_monto = result[4]
                
                query = "SELECT username FROM usuarios WHERE id=%s"
                cursor.execute(query, str(val_usuario))
                val_usuario = cursor.fetchone()[0]
                
                
                
                self.id.config(state="normal")
                self.id.delete(0, tk.END)
                self.id.insert(0, val_reabastecimiento)
                self.id.config(state='disabled')
                
                self.proveedor.config(state="normal")
                self.proveedor.delete(0, tk.END)
                self.proveedor.insert(0, val_proveedor)
                self.proveedor.config(state='disabled')
                
                self.usuario.config(state="normal")
                self.usuario.delete(0, tk.END)
                self.usuario.insert(0, val_usuario)
                self.usuario.config(state='disabled')
                
                self.fecha.set_date(val_fecha)
                
                self.monto.config(state="normal")
                self.monto.delete(0, tk.END)
                self.monto.insert(0, val_monto)
                self.monto.config(state='disabled')
                
                query = """
                        SELECT 
                            ar.id_articulo,
                            a.nombre AS nombre_articulo,
                            ar.cantidad,
                            ar.precio_unitario,
                            ar.subtotal
                        FROM 
                            articulos_reabastecimientos ar
                        JOIN 
                            articulos a ON ar.id_articulo = a.id_articulo
                        WHERE 
                            ar.id_reabastecimiento = %s;
                        """
                        
                cursor.execute(query, (val_reabastecimiento,))
                lista_de_tuplas = cursor.fetchall()
                self.lista_agregados = []
                for tupla in lista_de_tuplas:
                    self.lista_agregados.append((str(tupla[0]), str(tupla[1]), str(tupla[2]), str(tupla[3]), str(tupla[4])))
                self.prev_agregados = self.lista_agregados.copy()
                self.cargar_articulos_agregados()
                self.estado_interfaz("buscar")
            else:
                messagebox.showerror("Error", "No se encontró ese folio")
                self.limpiar_campos()
                self.estado_interfaz("cancelar")
                
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo realizar la busqueda\n{e}')
            self.limpiar_campos()
            self.estado_interfaz("cancelar")
            
    def guardar(self):
        id = self.id.get()
        proveedor = self.proveedor.get()
        usuario = self.parent.user_info["ID"]
        fecha_normal = self.fecha.get()
        monto = self.monto.get()

        resultado = [id for id, nombre in self.lista_proveedores if nombre == proveedor]
        proveedor = resultado[0] if resultado else None

        if not id or not usuario or not fecha_normal or not monto or not proveedor:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Parsear la fecha en formato dd/mm/yy
            fecha_obj = datetime.strptime(fecha_normal, "%m/%d/%y")
            # Convertir la fecha al formato YYYY/MM/DD
            fecha = fecha_obj.strftime("%Y/%m/%d")
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha no válida\n{e}")
            return

        connection = None
        cursor = None
        try:
            connection = connfile.connect_db()  # Conectar a la base de datos
            cursor = connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la base de datos\n{e}")
            return

        try:
            # Inserción en reabastecimientos con RETURNING para obtener el id generado
            query = """
                    INSERT INTO reabastecimientos (id_proveedor, id_usuario, fecha, monto) 
                    VALUES (%s, %s, %s, %s) RETURNING id_reabastecimiento
                    """
            valores = (proveedor, usuario, fecha, monto)
            cursor.execute(query, valores)

            # Obtener el id generado en la tabla reabastecimientos
            id_reabastecimiento = cursor.fetchone()[0]

            # Inserción en articulos_reabastecimientos usando el id_reabastecimiento
            query = """
                    INSERT INTO articulos_reabastecimientos (id_reabastecimiento, id_articulo, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """
            for articulo in self.lista_agregados:
                valores = (id_reabastecimiento, articulo[0], articulo[2], articulo[3], articulo[4])
                cursor.execute(query, valores)
                
            for articulo in self.lista_agregados:
                query = "UPDATE articulos SET cantidad=cantidad + %s WHERE id_articulo = %s"
                valores = (articulo[2], articulo[0])    
                cursor.execute(query, valores)

            # Confirmar la transacción
            connection.commit()

            messagebox.showinfo("Éxito", "Se registró el reabastecimiento")
            self.limpiar_campos()
            self.estado_interfaz("cancelar")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la información\n{e}")
            connection.rollback()  # Deshacer los cambios en caso de error
            return

        
    def modificar(self):
        id = self.id.get()
        proveedor = self.proveedor.get()
        usuario = self.usuario.get()
        fecha_normal = self.fecha.get()
        monto = self.monto.get()

        resultado = [id for id, nombre in self.lista_proveedores if nombre == proveedor]
        proveedor = resultado[0] if resultado else None

        if not id or not usuario or not fecha_normal or not monto or not proveedor:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Parsear la fecha en formato dd/mm/yy
            fecha_obj = datetime.strptime(fecha_normal, "%m/%d/%y")
            # Convertir la fecha al formato YYYY/MM/DD
            fecha = fecha_obj.strftime("%Y/%m/%d")
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha no válida\n{e}")
            return

        connection = None
        cursor = None
        
        try:
            connection = connfile.connect_db()  # Conectar a la base de datos
            cursor = connection.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la base de datos\n{e}")
            return
        
        try:
            # Inserción en reabastecimientos con RETURNING para obtener el id generado
            query = """
                    UPDATE reabastecimientos 
                    SET id_proveedor=%s,
                        fecha=%s,
                        monto=%s
                    WHERE id_reabastecimiento=%s
                    RETURNING id_reabastecimiento
                    """
            valores = (proveedor, fecha, monto, id)
            cursor.execute(query, valores)

            # Obtener el id generado en la tabla reabastecimientos
            id_reabastecimiento = cursor.fetchone()[0]
            
            query = """
                    DELETE FROM articulos_reabastecimientos
                    WHERE id_reabastecimiento=%s
                    """
            cursor.execute(query, (id_reabastecimiento,))

            # Inserción en articulos_reabastecimientos usando el id_reabastecimiento
            query = """
                    INSERT INTO articulos_reabastecimientos (id_reabastecimiento, id_articulo, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """
            for articulo in self.lista_agregados:
                valores = (id_reabastecimiento, articulo[0], articulo[2], articulo[3], articulo[4])
                cursor.execute(query, valores)
                
                
            # Crear un conjunto de IDs de artículos en la nueva lista
            nuevos_ids = {articulo[0] for articulo in self.lista_agregados}

            # 1. Restar las cantidades de artículos que ya no están en self.lista_agregados
            for articulo_previo in self.prev_agregados:
                # Si el ID del artículo previo no está en la lista nueva, lo restamos
                if articulo_previo[0] not in nuevos_ids:
                    cantidad_a_restar = float(articulo_previo[2])

                    # El artículo fue removido, restar toda su cantidad previa
                    query = "UPDATE articulos SET cantidad = cantidad - %s WHERE id_articulo = %s"
                    valores = (cantidad_a_restar, articulo_previo[0])
                    cursor.execute(query, valores)



            # 2. Calcular y aplicar la diferencia en las cantidades de los artículos que están en ambas listas
            for articulo_nuevo in self.lista_agregados:
                articulo_previo = next((a for a in self.prev_agregados if a[0] == articulo_nuevo[0]), None)
                
                if articulo_previo:
                    # Calcular la diferencia si el artículo está en ambas listas
                    diferencia = float(articulo_nuevo[2]) - float(articulo_previo[2])
                else:
                    # Si el artículo no estaba antes, toda la cantidad es nueva
                    diferencia = float(articulo_nuevo[2])
                
                # Actualizar la cantidad en la tabla articulos
                query = "UPDATE articulos SET cantidad = cantidad + %s WHERE id_articulo = %s"
                valores = (diferencia, articulo_nuevo[0])
                cursor.execute(query, valores)


            # Confirmar la transacción
            connection.commit()

            messagebox.showinfo("Éxito", "Se registró el reabastecimiento")
            self.limpiar_campos()
            self.estado_interfaz("cancelar")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la información\n{e}")
            connection.rollback()  # Deshacer los cambios en caso de error
            return
        
    def cancelar(self):
        self.limpiar_campos()
        self.estado_interfaz("cancelar")
        
    def seleccionar_agregados(self, event):
        curId = self.treeview_agregados.focus()
        if curId:
            self.quitar_producto_button.config(state="normal")
        else:
            self.quitar_producto_button.config(state="disabled")
        
    def seleccionar_articulo(self, event):
        curId = self.treeview_disponibles.focus()
        if curId:
            curItem = self.treeview_disponibles.item(curId)

            self.id_producto.config(state="normal")
            self.id_producto.delete(0, tk.END)
            self.id_producto.insert(0, curItem["values"][0])
            self.id_producto.config(state="disabled")
            
            self.nombre_producto.config(state="normal")
            self.nombre_producto.delete(0, tk.END)
            self.nombre_producto.insert(0, curItem["values"][1])
            self.nombre_producto.config(state="disabled")
            
            self.cantidad_producto.delete(0, tk.END)
            self.ppi_producto.delete(0, tk.END)
            
            
    def cargar_articulos(self):
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            
            query = "SELECT id_articulo, nombre FROM articulos ORDER BY id_articulo"
            cursor.execute(query)
            self.lista_articulos = cursor.fetchall()
            
            self.treeview_disponibles.delete(*self.treeview_disponibles.get_children())
                        
            for articulo in self.lista_articulos:
                self.treeview_disponibles.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1]))
            pass
        except Exception as e:
            messagebox.showerror("Error", f'No se pudieron cargar los articulos:\n{e}')
            
    def cargar_articulos_agregados(self):
        try:
            self.treeview_agregados.delete(*self.treeview_agregados.get_children())
                        
            for articulo in self.lista_agregados:
                self.treeview_agregados.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2],articulo[3],articulo[4]))
            
        except Exception as e:
            messagebox.showerror("Error", f'No se pudieron cargar los articulos:\n{e}')
            return
        
    def filtrar_datos(self, event):
        query = self.filtrar_nombre.get().lower()
        for item in self.treeview_disponibles.get_children():
            self.treeview_disponibles.delete(item)
            
        try:
            regex = re.compile(query)
        except re.error:
            return
        
        if not query:
            for articulo in self.lista_articulos:
                self.treeview_disponibles.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1]))
        else:
            for articulo in self.lista_articulos:
                if regex.search(articulo[1].lower()):
                    self.treeview_disponibles.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1]))
                    
                    
    def quitar_producto(self):
        curId = self.treeview_agregados.focus()
        if curId:
            curItem = self.treeview_agregados.item(curId)
            index = None
            for i in range(len(self.lista_agregados)):
                if self.lista_agregados[i][0] == str(curItem['values'][0]):
                    index = i
                    break
            if index is not None:  # Cambiado para verificar si no es None
                self.lista_agregados.pop(index)
                self.cargar_articulos_agregados()
                
            if len(self.lista_agregados) != 0:
                cantidad = 0
                for articulo in self.lista_agregados:
                    cantidad += float(articulo[4])
                    
                self.monto.config(state="normal")
                self.monto.delete(0, tk.END)
                self.monto.insert(0, str(cantidad))
                self.monto.config(state="disabled")
            else:
                self.monto.config(state="normal")
                self.monto.delete(0, tk.END)
                self.monto.config(state="disabled")
            
        self.quitar_producto_button.config(state="disabled")

    def agregar_producto(self):
        id = self.id_producto.get()
        nombre = self.nombre_producto.get()
        cantidad = self.cantidad_producto.get()
        ppi = self.ppi_producto.get()
        
        if not id or not nombre or not cantidad or not ppi:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if not cantidad.isdigit():
            messagebox.showerror("Error", "La cantidad tiene que ser un entero")
            return
        
        isnumber = None
        try:
            float(ppi)  # Intenta convertir a float
            isnumber = True
        except ValueError:
            isnumber = False
        
        if not isnumber:
            messagebox.showerror("Error", "El precio tiene que ser un número")
            return
        
        try:
            self.lista_agregados = [
                articulo for articulo in self.lista_agregados if articulo[0] != id
            ]
            
            subtotal = str(float(cantidad) * float(ppi))
            self.lista_agregados.append((id,nombre,cantidad,ppi, subtotal))
            self.cargar_articulos_agregados()
            self.limpiar_campos_producto()
            
            cantidad = 0
            for articulo in self.lista_agregados:
                cantidad += float(articulo[4])
                
            self.monto.config(state="normal")
            self.monto.delete(0, tk.END)
            self.monto.insert(0, str(cantidad))
            self.monto.config(state="disabled")
            
            
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo agregar el articulo\n{e}')
            return
        
    def limpiar_campos(self):
        self.id.config(state='normal')
        self.proveedor.config(state='normal')
        self.usuario.config(state='normal')
        today = datetime.today().date()
        self.fecha.set_date(today)
        self.fecha.set_date(today)
        self.monto.config(state='normal')
        self.id_producto.config(state='normal')
        self.nombre_producto.config(state='normal')
        self.cantidad_producto.config(state='normal')
        self.ppi_producto.config(state='normal')
        self.id.delete(0, tk.END)
        self.proveedor.delete(0, tk.END)
        self.usuario.delete(0, tk.END)
        self.monto.delete(0, tk.END)
        self.id_producto.delete(0, tk.END)
        self.nombre_producto.delete(0, tk.END)
        self.cantidad_producto.delete(0, tk.END)
        self.ppi_producto.delete(0, tk.END)
        self.lista_agregados = []
        self.cargar_articulos_agregados()
        
    def limpiar_campos_producto(self):
        self.id_producto.config(state='normal')
        self.nombre_producto.config(state='normal')
        self.cantidad_producto.config(state='normal')
        self.ppi_producto.config(state='normal')
        self.id_producto.delete(0, tk.END)
        self.nombre_producto.delete(0, tk.END)
        self.cantidad_producto.delete(0, tk.END)
        self.ppi_producto.delete(0, tk.END)
        self.id_producto.config(state='disabled')
        self.nombre_producto.config(state='disabled')
        self.cantidad_producto.config(state='normal')
        self.ppi_producto.config(state='normal')
        
    def estado_interfaz(self, estado):
        if estado == "cancelar":
            self.id.config(state="disabled")
            self.proveedor.config(state="disabled")
            self.usuario.config(state="disabled")
            self.monto.config(state="disabled")
            
            self.filtrar_nombre.config(state="disabled")

            self.id_producto.config(state="disabled")
            self.nombre_producto.config(state="disabled")
            self.cantidad_producto.config(state="disabled")
            self.ppi_producto.config(state="disabled")
            
            self.nuevo_button.config(state="normal")
            self.guardar_button.config(state="disabled")
            self.modificar_button.config(state="disabled")
            self.cancelar_button.config(state="disabled")
        if estado == "nuevo":
            self.id.config(state="disabled")
            self.proveedor.config(state="readonly")
            self.usuario.config(state="disabled")
            self.monto.config(state="disabled")
            
            self.filtrar_nombre.config(state="normal")

            self.id_producto.config(state="disabled")
            self.nombre_producto.config(state="disabled")
            self.cantidad_producto.config(state="normal")
            self.ppi_producto.config(state="normal")
            
            self.nuevo_button.config(state="disabled")
            self.guardar_button.config(state="normal")
            self.modificar_button.config(state="disabled")
            self.cancelar_button.config(state="normal")
        if estado == "buscar":
            self.id.config(state="disabled")
            self.proveedor.config(state="readonly")
            self.usuario.config(state="disabled")
            self.monto.config(state="disabled")
            
            self.nuevo_button.config(state="disabled")
            self.guardar_button.config(state="disabled")
            self.modificar_button.config(state="normal")
            self.cancelar_button.config(state="normal")
            
            self.filtrar_nombre.config(state="normal")
            
            self.id_producto.config(state="disabled")
            self.nombre_producto.config(state="disabled")
            self.cantidad_producto.config(state="normal")
            self.ppi_producto.config(state="normal")
        if estado == "seleccion":
            self.id_producto.config(state="disabled")
            self.nombre_producto.config(state="disabled")
            self.cantidad_producto.config(state="normal")
            self.ppi_producto.config(state="normal")