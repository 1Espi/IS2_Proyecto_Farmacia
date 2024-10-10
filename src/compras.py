import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import utilities.connection as dbconn
from .mostrar_compra import MostrarCompra
from tkinter import END, messagebox, ttk


class ComprasFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Compras", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Folio").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.buscar_folio = tk.Entry(self)
        self.buscar_folio.grid(row=1, column=1, pady=5, padx=10)
        
        self.buscar_button = tk.Button(self, text="Buscar")
        self.buscar_button.grid(row=1, column=2, padx=10)

        # Folio de compra (Sera el id unico, podemos hacerlo autoincremental o que se genere uno automatico y distinto con el datetime)
        tk.Label(self, text="Folio de Compra").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.folio = tk.Entry(self, state='readonly') 
        self.folio.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Proveedor").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.proveedor = tk.Entry(self)
        self.proveedor.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Producto").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.producto = tk.Entry(self)
        self.producto.grid(row=4, column=1, pady=5, padx=10)

        # Al salir de ingresar la cantidad o precio por unidad podemos agregar un tipo onblur para que justo lo coloquemos se calcule el total de compra
        tk.Label(self, text="Cantidad").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.cantidad = tk.Entry(self)
        self.cantidad.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Precio por Unidad").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.precio = tk.Entry(self)
        self.precio.grid(row=6, column=1, pady=5, padx=10)
        
        fecha_hoy = datetime.today()
        tk.Label(self, text="Fecha de Compra").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.fecha = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2,
                               year=fecha_hoy.year, month=fecha_hoy.month, day=fecha_hoy.day)  # El estado 'readonly' bloquea el campo
        self.fecha.grid(row=7, column=1, pady=5, padx=10)

        #El campo sera solo de lectura
        tk.Label(self, text="Total de Compra").grid(row=9, column=0, sticky='w', padx=10, pady=5)
        self.total = tk.Entry(self, state='readonly') 
        self.total.grid(row=9, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=11, column=0, columnspan=4, pady=20)

        self.nuevo_button = tk.Button(button_frame, text="Nuevo", width=10, command=self.nuevo)
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.guardar_button = tk.Button(button_frame, text="Guardar", width=10, command=self.guardar)
        self.guardar_button.grid(row=0, column=1, padx=10)

        self.modificar_button = tk.Button(button_frame, text="Modificar", width=10)
        self.modificar_button.grid(row=0, column=2, padx=10)

        self.eliminar_button = tk.Button(button_frame, text="Eliminar", width=10)
        self.eliminar_button.grid(row=0, column=3, padx=10)

        self.cancelar_button = tk.Button(button_frame, text="Cancelar", width=10)
        self.cancelar_button.grid(row=0, column=4, padx=10)
        
        self.mostrar_button = tk.Button(button_frame, text="Mostrar Compras", width=15, command=self.abrir_mostrar_compras)
        self.mostrar_button.grid(row=1, column=5, padx=10)
    
    def abrir_mostrar_compras(self):
        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Mostrar registros de compras")  # Establecer el título de la ventana
        mostrar_compra = MostrarCompra(self.parent, nueva_ventana)
        mostrar_compra.pack(fill='both', expand=True)
         
    def calculate_total(self):
        try:
            quantity = int(self.cantidad.get())
            price_per_unit = float(self.precio.get())
            total = quantity * price_per_unit
            self.total.config(state='normal')
            self.total.delete(0, tk.END)
            self.total.insert(0, f"{total:.2f}")
            self.total.config(state='readonly')
        except ValueError:
            pass  
    def guardar(self):
        folio = self.folio.get()
        proveedor = self.proveedor.get()
        producto = self.producto.get()
        cantidad = self.cantidad.get()
        precio = self.precio.get()
        fecha = self.fecha.get()
        fecha_update = self.fecha_update.get()
        total = self.total.get()
        estado = self.estado.get()
        print("fecha: ")
        print(fecha)
        self.calculate_total()
        
        if folio:
            messagebox.showerror("Error", "Debes presionar primero nuevo")
            return
        if not proveedor or not producto or not cantidad or not precio or not estado:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            fecha2 = datetime.strptime(fecha, "%d/%m/%y").strftime("%Y-%m-%d")         
            fecha_update2 = datetime.strptime(fecha_update, "%d/%m/%y").strftime("%Y-%m-%d")
             
        except ValueError as e:
            messagebox.showerror("Error al formatear las fechas: {e}")
        print("fecha2: ")
        print(fecha2)   
        """
        fecha_hoy = datetime.now().date()
        if str(fecha2) < str(fecha_hoy):
            messagebox.showerror("La fecha de entrada debe ser superior a la de hoy")
            return
        if str(fecha_update2) < str(fecha2):
            messagebox.showerror("La fecha de salida debe ser superior a la de entrada")
            return"""
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "INSERT INTO compras (proveedor_id, producto_id, cantidad,  precio, fecha, total) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (proveedor, producto, cantidad, precio, fecha2, total)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "Producto guardado exitosamente")
            self.limpiar_campos() 
            """
            except:
            messagebox.showinfo("Éxito", "Producto no guardado")"""
        
        except connection as err:
            messagebox.showerror("Error", f"Error al guardar el usuario: {err}")
            print(f"Error al guardar el usuario: {err}")
            
    def nuevo(self):
        self.limpiar_campos()
        
    def limpiar_campos(self):
        self.folio.config(state='normal')
        self.folio.delete(0, tk.END)
        self.proveedor.delete(0, tk.END)
        self.producto.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.precio.delete(0, tk.END)       
        self.total.delete(0, tk.END)
        self.estado.delete(0, tk.END)
        self.folio.config(state='disabled') 
        