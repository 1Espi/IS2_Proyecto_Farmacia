import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import utilities.connection as dbconn
from tkinter import END, messagebox, ttk



class ArticulosFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Articulos", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por ID de Articulo").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=1, column=1, pady=5, padx=10)
       

        self.buscar = tk.Button(self, text="Buscar", command=self.buscar)
        self.buscar.grid(row=1, column=2, padx=10)

       
        tk.Label(self, text="ID del Articulo").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.id= tk.Entry(self, state='readonly')  
        self.id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre del Articulo").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.nombre = tk.Entry(self)
        self.nombre.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Precio").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.precio = tk.Entry(self)
        self.precio.grid(row=4, column=1, pady=5, padx=10)

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
        id = self.entry_id.get()
        self.id.config(state='normal')
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT  * from articulos  WHERE id_articulo = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result:
                self.id.delete(0, tk.END)
                self.id.insert(0, result[0])
                self.id.config(state='disabled') 
                self.nombre.delete(0, tk.END)
                self.nombre.insert(0, result[1])
                self.precio.delete(0, tk.END)
                self.precio.insert(0, result[2])
              
            else:
                messagebox.showerror("Error", "Articulo no encontrado")
                self.limpiar_campos()
                
        except:
            messagebox.showerror("Error", "Articulo no encontrado")
            self.limpiar_campos()

    def crear(self):
        id = self.id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()
        
        if id:
            messagebox.showerror("Error", "Debes presionar primero nuevo")
            return
        if not nombre or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "INSERT INTO articulos(nombre, precio) VALUES (%s, %s)"
            valores = (nombre, precio)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "Articulo guardado exitosamente")
            self.limpiar_campos() 
        except:
            messagebox.showinfo("Éxito", "Articulo no guardado")
        """
        except connection as err:
            messagebox.showerror("Error", f"Error al guardar el usuario: {err}")
            print(f"Error al guardar el usuario: {err}")"""
    def modificar(self):
        id = self.entry_id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()

        if not nombre or not precio or not id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "UPDATE articulos SET  nombre = %s, precio = %s WHERE id_articulo = %s"
            valores = (nombre, precio, id)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "Articulo actualizado exitosamente")
            self.limpiar_campos() 
            
        except:
            messagebox.showinfo("Éxito", "Articulo no actualizado")
        
    def eliminar(self):
        id = self.id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "DELETE FROM articulos WHERE id_articulo = %s"
            cursor.execute(query, (id,))
            connection.commit()
            messagebox.showinfo("Éxito", "Articulo eliminado exitosamente")
            self.limpiar_campos() 
            self.entry_id.delete(0, tk.END)
        except:
            messagebox.showinfo("Éxito", "Articulo no eliminado")
            
    def cancelar(self):
        self.limpiar_campos()
        
    def limpiar_campos(self):
        self.id.config(state='normal')  
        self.id.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.id.config(state='disabled') 
  