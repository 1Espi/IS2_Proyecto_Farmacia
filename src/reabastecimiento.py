import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import utilities.connection as dbconn
from .mostrar_compra import MostrarCompra
from tkinter import END, messagebox, ttk


class ReabastecimientoFrame(tk.Frame):
    def __init__(self, parent, container, user_info):
        super().__init__(container)
        self.parent = parent
        self.user_info = user_info
        self.setup_ui()

    def setup_ui(self):
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM proveedores"
            cursor.execute(query)
            result = cursor.fetchall()
            lista = []
            
            for i in result:
                lista.append(i[0])
        except:
            pass
            
        title = tk.Label(self, text="Gestión de Reabastecieminto del almacen", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por id del Reabastecieminto").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.buscar_id = tk.Entry(self)
        self.buscar_id.grid(row=1, column=1, pady=5, padx=10)
        
        self.buscar_button = tk.Button(self, text="Buscar", command=self.buscar)
        self.buscar_button.grid(row=1, column=2, padx=10)

        tk.Label(self, text="Id reabastecimiento").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.id= tk.Entry(self, state='readonly') 
        self.id.grid(row=2, column=1, pady=5, padx=10)
        

        tk.Label(self, text="Id Proveedor").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        estado_options = lista
        self.proveedor = ttk.Combobox(self, values=estado_options)
        self.proveedor.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Id Usuario").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.usuario = tk.Entry(self)
        self.usuario.grid(row=4, column=1, pady=5, padx=10)
        
        self.usuario.delete(0, tk.END)
        self.usuario.insert(0, self.user_info["ID"])
        self.usuario.config(state='disabled')

        fecha_hoy = datetime.today()
        tk.Label(self, text="Fecha").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.fecha = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2,
                               year=fecha_hoy.year, month=fecha_hoy.month, day=fecha_hoy.day)  
        self.fecha.grid(row=7, column=1, pady=5, padx=10)

        tk.Label(self, text="Monto").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.monto = tk.Entry(self)
        self.monto.grid(row=6, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=11, column=0, columnspan=4, pady=20)

        self.nuevo_button = tk.Button(button_frame, text="Nuevo", width=10, command=self.nuevo)
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.guardar_button = tk.Button(button_frame, text="Guardar", width=10, command=self.guardar)
        self.guardar_button.grid(row=0, column=1, padx=10)

        self.modificar_button = tk.Button(button_frame, text="Modificar", width=10, command=self.modificar)
        self.modificar_button.grid(row=0, column=2, padx=10)

        self.eliminar_button = tk.Button(button_frame, text="Eliminar", width=10, command=self.eliminar)
        self.eliminar_button.grid(row=0, column=3, padx=10)

        self.cancelar_button = tk.Button(button_frame, text="Cancelar", width=10, command=self.cancelar)
        self.cancelar_button.grid(row=0, column=4, padx=10)
        
        self.mostrar_button = tk.Button(button_frame, text="Mostrar Compras", width=15, command=self.abrir_mostrar_compras)
        self.mostrar_button.grid(row=1, column=5, padx=10)
    
    def abrir_mostrar_compras(self):
        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Mostrar registros de los articulos") 
        mostrar_compra = MostrarCompra(self.parent, nueva_ventana)
        mostrar_compra.pack(fill='both', expand=True)
    def buscar(self):
        id = self.buscar_id.get()
        self.id.config(state='normal')
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor2 = connection.cursor()
            query2 = "SELECT  * from reabastecimientos  WHERE id_reabastecimiento = %s"
            cursor2.execute(query2, (id,))
            result2 = cursor2.fetchone()
            
            if result2:
                self.id.delete(0, tk.END)
                self.id.insert(0, result2[0])
                self.id.config(state='disabled')
                self.proveedor.delete(0, tk.END)
                self.proveedor.insert(0, result2[1])
                self.usuario.delete(0, tk.END)
                self.usuario.insert(0, result2[2])
                self.fecha.delete(0, tk.END)
                self.fecha.insert(0, result2[3])
                self.monto.delete(0, tk.END)
                self.monto.insert(0, result2[4])
                
            else:
                
                messagebox.showerror("Error", "El id del abastecimiento no se encontro")
                self.limpiar_campos()
                
        except:
            messagebox.showerror("Error", "Hubo un error en ls conexion")
            self.limpiar_campos()    
    def guardar(self):
        id = self.buscar_id.get()
        proveedor = self.proveedor.get()
        usuario = self.usuario.get()
        fecha = self.fecha.get()
        monto = self.monto.get()
        
        if id:
            messagebox.showerror("Error", "Debes presionar primero nuevo")
            return
        if not proveedor or not usuario or not fecha or not monto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            fecha2 = datetime.strptime(fecha, "%d/%m/%y").strftime("%Y-%m-%d")         
             
        except ValueError as e:
            messagebox.showerror("Error al formatear las fechas: {e}")
  
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor2 = connection.cursor()
            query2 = "INSERT INTO reabastecimientos (id_proveedor, id_usuario, fecha, monto) VALUES (%s, %s, %s, %s)"
            valores2 = (proveedor, self.user_info["ID"], fecha2, monto)
            cursor2.execute(query2, valores2)
            connection.commit()
            
            messagebox.showinfo("Info", "El id del abastecimiento se encontro")
            self.limpiar_campos() 
            """
            except:
            messagebox.showinfo("Éxito", "Producto no guardado")"""
        
        except connection as err:
            messagebox.showerror("Error", "El id del abastecimiento no se encontro")
            print(f"Error al guardar el usuario: {err}")
            
    def nuevo(self):
        self.limpiar_campos()
        
    def modificar(self):
        id = self.buscar_id.get()
        #self.id.config(state='normal')
        
        proveedor = self.proveedor.get()
        usuario = self.usuario.get()
        fecha = self.fecha.get()
        monto = self.monto.get()
        
        if not proveedor or not usuario or not fecha or not monto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            fecha2 = datetime.strptime(fecha, "%d/%m/%y").strftime("%Y-%m-%d")         
             
        except ValueError as e:
            messagebox.showerror("Error al formatear las fechas: {e}")
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "UPDATE reabastecimientos SET  id_proveedor = %s, id_usuario = %s,  fecha = %s, monto = %s  WHERE id_reabastecimiento = %s"
            valores = (proveedor, usuario, fecha2, monto, id)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "El reabastecimiento se actualizo exitosamente  en el almacen")
            self.limpiar_campos() 
            
        except:
            messagebox.showerror("Error", "El id del abastecimiento no se encontro")
        
    def eliminar(self):
        id = self.buscar_id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "DELETE FROM reabastecimientos WHERE id_reabastecimiento = %s"
            cursor.execute(query, (id,))
            connection.commit()
            messagebox.showinfo("Éxito", "El id del abastecimiento se elimino exitosamente")
            self.limpiar_campos() 
            self.buscar_id.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "El id del abastecimiento se elimino exitosamente")
            
    def cancelar(self):
        self.limpiar_campos()
        
    def limpiar_campos(self):
        self.id.config(state='normal')
        self.id.delete(0, tk.END)
        self.proveedor.delete(0, tk.END)
        self.usuario.delete(0, tk.END)
        self.fecha.delete(0, tk.END)
        self.monto.delete(0, tk.END)       
        self.id.config(state='disabled') 
        