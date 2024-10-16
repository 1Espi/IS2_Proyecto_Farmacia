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
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM articulos"
            cursor.execute(query)
            result = cursor.fetchall()
            lista = []
            
            for i in result:
                lista.append(i[0])
        except:
            pass
        title = tk.Label(self, text="Gestión de Almacén", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por ID de Almacen").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=1, column=1, pady=5, padx=10)
       

        self.buscar = tk.Button(self, text="Buscar", command=self.buscar)
        self.buscar.grid(row=1, column=2, padx=10)

       
        tk.Label(self, text="ID del Almacen").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.id_almacen= tk.Entry(self, state='readonly')  
        self.id_almacen.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="ID del articulo").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        estado_options = lista
        self.id_articulo = ttk.Combobox(self, values=estado_options)
        self.id_articulo.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Cantidad").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.cantidad = tk.Entry(self)
        self.cantidad.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Minimos").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.min = tk.Entry(self)
        self.min.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Maximos").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.max = tk.Entry(self)
        self.max.grid(row=6, column=1, pady=5, padx=10)

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
        self.id_almacen.config(state='normal')
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT  * from almacen  WHERE id_almacen = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result:
                self.id_almacen.delete(0, tk.END)
                self.id_almacen.insert(0, result[0])
                self.id_almacen.config(state='disabled') 
                self.id_articulo.delete(0, tk.END)
                self.id_articulo.insert(0, result[1])
                self.cantidad.delete(0, tk.END)
                self.cantidad.insert(0, result[2])
                self.min.delete(0, tk.END)
                self.min.insert(0, result[3])
                self.max.delete(0, tk.END)
                self.max.insert(0, result[4])
            else:
                messagebox.showerror("Error", "El id del almacen se encontro")
                self.limpiar_campos()
                
        except:
            messagebox.showerror("Error", "El id del almacen no se encontro")
            self.limpiar_campos()

    def crear(self):
        id_almacen = self.id_almacen.get()
        id_articulo = self.id_articulo.get()
        cantidad = self.cantidad.get()
        minimo = self.min.get()
        maximo = self.max.get()
        
        if id_almacen:
            messagebox.showerror("Error", "Debes presionar primero nuevo")
            return
        if not id_articulo or not cantidad or not minimo or not maximo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor3 = connection.cursor()
            query3 = "SELECT  * from articulos  WHERE id_articulo = %s"
            cursor3.execute(query3, (id_articulo,))
            result2 = cursor3.fetchone()
            if not result2:
                messagebox.showerror("Error", "Este articulo no existe")
                return
            
            else:
            
                con = dbconn.connection()
                connection = con.open()
                cursor2 = connection.cursor()
                query2 = "SELECT  * from almacen  WHERE id_articulo = %s"
                cursor2.execute(query2, (id_articulo,))
                result = cursor2.fetchone()
                if result:
                    messagebox.showerror("Error", "Este articulo ya esta ingresado en el almacen")
                    return
                else:
                    con = dbconn.connection()
                    connection = con.open()
                    cursor = connection.cursor()
                    query = "INSERT INTO almacen (id_articulo, cantidad, minimo, maximo) VALUES (%s, %s, %s, %s)"
                    valores = (id_articulo, cantidad, minimo, maximo)
                    cursor.execute(query, valores)
                    connection.commit()
                    
                    messagebox.showinfo("Éxito", "El articulo se guardo exitosamente en el almacen")
                    self.limpiar_campos() 
 
        except:
            messagebox.showinfo("Éxito", "El articulo no se guardo exitosamente en el almacen")
        
    def modificar(self):
        id = self.entry_id.get()
        id_articulo = self.id_articulo.get()
        cantidad = self.cantidad.get()
        minimo = self.min.get()
        maximo = self.max.get()

        if not id_articulo or not cantidad or not minimo or not maximo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "UPDATE almacen SET  id_articulo = %s, cantidad = %s,  minimo = %s, maximo = %s  WHERE id_almacen = %s"
            valores = (id_articulo, cantidad, minimo, maximo, id)
            cursor.execute(query, valores)
            connection.commit()
            
            messagebox.showinfo("Éxito", "El articulo se actualizo exitosamente  en el almacen")
            self.limpiar_campos() 
            
        except:
            messagebox.showinfo("Éxito", "El articulo no se actualizo exitosamente  en el almacen")
        
      
    def eliminar(self):
        id = self.entry_id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "DELETE FROM almacen WHERE id_almacen = %s"
            cursor.execute(query, (id,))
            connection.commit()
            messagebox.showinfo("Éxito", "El articulo se elimino exitosamente  en el almacen")
            self.limpiar_campos() 
        except:
            messagebox.showinfo("Éxito", "El articulo no se elimino exitosamente  en el almacen")
    def cancelar(self):
        self.limpiar_campos(self)
    def limpiar_campos(self):
        self.id_almacen.config(state='normal') 
        self.id_almacen.delete(0, tk.END)
        self.id_articulo.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.min.delete(0, tk.END)
        self.max.delete(0, tk.END)
        self.id_almacen.config(state='disabled') 