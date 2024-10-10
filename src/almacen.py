import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import utilities.connection as dbconn
from tkinter import END, messagebox, ttk



class AlmacenFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Almacén", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por ID de Producto").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=1, column=1, pady=5, padx=10)
       

        self.buscar = tk.Button(self, text="Buscar", command=self.buscar)
        self.buscar.grid(row=1, column=2, padx=10)

       
        tk.Label(self, text="ID del Producto").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.id= tk.Entry(self, state='readonly')  
        self.id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre del Producto").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.nombre = tk.Entry(self)
        self.nombre.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Cantidad").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.cantidad = tk.Entry(self)
        self.cantidad.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Minimos").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.min = tk.Entry(self)
        self.min.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Maximos").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.max = tk.Entry(self)
        self.max.grid(row=6, column=1, pady=5, padx=10)

        tk.Label(self, text="Estado").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.status = ttk.Combobox(self, values=["Disponible", "Agotado"])
        self.status.grid(row=7, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20)
        
        self.nuevo_button = tk.Button(button_frame, text="Nuevo", command=self.nuevo, width=10)
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.create_button = tk.Button(button_frame, text="Crear", command=self.crear, width=10)
        self.create_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", command=self.modificar, width=10)
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", command=self.eliminar, width=10)
        self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.cancelar, width=10)
        self.cancel_button.grid(row=0, column=4, padx=10)
        
    def nuevo(self):
        self.limpiar_campos()
        
    def buscar(self):
        producto_id = self.entry_id.get()
        self.id.config(state='normal')
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT  * from almacen  WHERE id = %s"
            cursor.execute(query, (producto_id,))
            result = cursor.fetchone()
            
            if result:
                self.id.delete(0, tk.END)
                self.id.insert(0, result[0])
                self.id.config(state='disabled') 
                self.nombre.delete(0, tk.END)
                self.nombre.insert(0, result[1])
                self.cantidad.delete(0, tk.END)
                self.cantidad.insert(0, result[2])
                self.min.delete(0, tk.END)
                self.min.insert(0, result[3])
                self.max.delete(0, tk.END)
                self.max.insert(0, result[4])
                self.status.delete(0, tk.END)
                self.status.insert(0, result[5])
            else:
                messagebox.showerror("Error", "Producto no encontrado")
                self.limpiar_campos()
                
        except:
            messagebox.showerror("Error", "Producto no encontrado")
            self.limpiar_campos()

    def crear(self):
        id = self.id.get()
        nombre = self.nombre.get()
        cantidad = self.cantidad.get()
        minimo = self.min.get()
        maximo = self.max.get()
        
        if not cantidad <= minimo:
            status = '{"Disponible"}'
        else:
            status = '{"Agotado"}'
        if id:
            messagebox.showerror("Error", "Debes presionar primero nuevo")
            return
        if not nombre or not cantidad or not minimo or not maximo or not status:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "INSERT INTO almacen (nombre, cantidad,  mininmo, maximo, disponible) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, cantidad, minimo, maximo, status)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "Producto guardado exitosamente")
            self.limpiar_campos() 
        except:
            messagebox.showinfo("Éxito", "Producto no guardado")
        """
        except connection as err:
            messagebox.showerror("Error", f"Error al guardar el usuario: {err}")
            print(f"Error al guardar el usuario: {err}")"""
    def modificar(self):
        id = self.entry_id.get()
        nombre = self.nombre.get()
        cantidad = self.cantidad.get()
        minimo = self.min.get()
        maximo = self.max.get()
        status = self.status.get()
        if status == "Disponible":
            status = '{"Disponible"}'
        else:
            status = '{"Agotado"}'

        if not nombre or not cantidad or not minimo or not maximo or not status or not id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "UPDATE almacen SET  nombre = %s, cantidad = %s,  mininmo = %s, maximo = %s, disponible = %s WHERE id = %s"
            valores = (nombre, cantidad, minimo, maximo, status, id)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
            self.limpiar_campos() 
            
        except:
            messagebox.showinfo("Éxito", "Producto no actualizado")
        
      
    def eliminar(self):
        id = self.id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "DELETE FROM almacen WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
            self.limpiar_campos() 
        except:
            messagebox.showinfo("Éxito", "Producto no eliminado")
    def cancelar(self):
        self.limpiar_campos(self)
    def limpiar_campos(self):
        self.id.config(state='normal') 
        self.status.config(state='normal') 
        self.id.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.min.delete(0, tk.END)
        self.max.delete(0, tk.END)
        self.status.delete(0, tk.END)
        self.id.config(state='disabled') 
        self.status.config(state='disabled') 