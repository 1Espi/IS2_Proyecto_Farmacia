import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import utilities.connection as connfile
import re

from tkinter import END, messagebox, ttk



class ArticulosFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.lista_articulos = None
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Articulos", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por nombre:", justify='center', anchor="center").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.grid(row=1, column=1, pady=5, padx=10, sticky='e')
        self.entry_id.bind("<KeyRelease>", self.filtrar_datos)
       

        #self.buscar = tk.Button(self, text="Buscar", command=self.buscar)
        #self.buscar.grid(row=1, column=2, padx=10)

       
        tk.Label(self, text="ID del articulo:", anchor='e').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.id= tk.Entry(self, state='readonly', width=40)  
        self.id.grid(row=2, column=1, pady=5, padx=10, sticky='e', )

        tk.Label(self, text="Nombre del articulo:", anchor='e').grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.nombre = tk.Entry(self, width=40)
        self.nombre.grid(row=3, column=1, pady=5, padx=10, sticky='e')

        tk.Label(self, text="Precio:", anchor='e').grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.precio = tk.Entry(self, width=40)
        self.precio.grid(row=4, column=1, pady=5, padx=10, sticky='e')
        
        self.treeview = ttk.Treeview(self, columns=("Codigo", "Nombre", "Precio"), show="headings")
        self.treeview.column("Codigo", anchor="center")
        self.treeview.column("Nombre", anchor="center")
        self.treeview.column("Precio", anchor="center")
        
        self.treeview.heading("Codigo", text="Codigo")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Precio", text="Precio")
        self.treeview.grid(row=0, column=7, pady=5, padx=10, rowspan=10)
        
        self.treeview.bind('<ButtonRelease-1>', self.seleccionar_articulo)
        

        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20)
        
        self.nuevo_button = tk.Button(button_frame, text="Nuevo", command=self.nuevo, width=10)
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.create_button = tk.Button(button_frame, text="Crear", command=self.crear, width=10)
        self.create_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", command=self.modificar, width=10)
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", command=self.eliminar, width=10)
        #self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.cancelar, width=10)
        self.cancel_button.grid(row=0, column=3, padx=10)
        self.cancelar()
        self.cargar_articulos()
        
    def nuevo(self):
        try:
            self.limpiar_campos()
            connection = connfile.connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT COALESCE(MAX(id_articulo), 0) + 1 FROM articulos")
            id_articulo = cursor.fetchone()
            
            self.entry_id.config(state="disabled")
            self.id.config(state='normal')  
            self.id.delete(0, tk.END)
            self.id.insert(0, id_articulo)
            self.id.config(state='disabled') 
            self.nombre.config(state='normal') 
            self.precio.config(state='normal') 
            
            self.nuevo_button.config(state="disabled")
            self.create_button.config(state="normal")
            self.update_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.cancel_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo cargar un ID para el nuevo articulo, intente de nuevo:\n{e}')
        
    def buscar(self):
        try:
            id = self.entry_id.get()
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "SELECT  * from articulos  WHERE id_articulo = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result:
                self.id.config(state='normal')
                self.id.delete(0, tk.END)
                self.id.insert(0, result[0])
                self.id.config(state='disabled') 
                self.nombre.delete(0, tk.END)
                self.nombre.insert(0, result[1])
                self.precio.delete(0, tk.END)
                self.precio.insert(0, result[2])
                
                
                self.nuevo_button.config(state="disabled")
                self.create_button.config(state="disabled")
                self.update_button.config(state="normal")
                self.delete_button.config(state="normal")
                self.cancel_button.config(state="normal")
              
            else:
                messagebox.showerror("Error", "Articulo no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo realizar la busqueda:\n{e}')
            self.cancelar()

    def crear(self):
        id = self.id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()

        if not nombre or not precio or not id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        isnumber = None
        try:
            float(precio)  # Intenta convertir a float
            isnumber = True
        except ValueError:
            isnumber = False
        
        if not isnumber:
            messagebox.showerror("Error", "El precio tiene que ser un número")
            return
        
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "INSERT INTO articulos(nombre, precio) VALUES (%s, %s)"
            valores = (nombre, precio)
            cursor.execute(query, valores)
            connection.commit()
            
            self.cargar_articulos()
            self.filtrar_datos(event=None)
            
            messagebox.showinfo("Éxito", "Articulo guardado exitosamente")
            self.cancelar() 
        except:
            messagebox.showerror("Error", "NO se pudo agregar el articulo")
    
    def modificar(self):
        id = self.id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()

        if not nombre or not precio or not id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        isnumber = None
        try:
            float(precio)  # Intenta convertir a float
            isnumber = True
        except ValueError:
            isnumber = False
        
        if not isnumber:
            messagebox.showerror("Error", "El precio tiene que ser un número")
            return
        
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "UPDATE articulos SET nombre = %s, precio = %s WHERE id_articulo = %s"
            valores = (nombre, precio, id)
            cursor.execute(query, valores)
            connection.commit()
            
            self.cargar_articulos()
            self.filtrar_datos(event=None)
            
            messagebox.showinfo("Éxito", "Articulo actualizado exitosamente")
            self.cancelar()
            
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f'No se pudo actualizar el articulo:\n{e}')
        
    def eliminar(self):
        id = self.id.get()
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "DELETE FROM articulos WHERE id_articulo = %s"
            cursor.execute(query, (id,))
            connection.commit()
            messagebox.showinfo("Éxito", "Articulo eliminado exitosamente")
            self.cancelar()
            self.entry_id.delete(0, tk.END)
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f"Articulo no eliminado: {e}")
            
    def cancelar(self):
        self.limpiar_campos()
        
        self.entry_id.config(state="normal")
        self.id.config(state="disabled")
        self.nombre.config(state="disabled")
        self.precio.config(state="disabled")
        
        self.nuevo_button.config(state="normal")
        self.create_button.config(state="disabled")
        self.update_button.config(state="disabled")
        self.delete_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        
    def limpiar_campos(self):
        self.id.config(state='normal')  
        self.nombre.config(state="normal")
        self.precio.config(state="normal")
        self.id.delete(0,tk.END)
        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.id.config(state='disabled')
        self.nombre.config(state="disabled")
        self.precio.config(state="disabled")
  
  
    def cargar_articulos(self):
        try:
            dbconn = connfile.connect_db()
            cursor = dbconn.cursor()
            
            query = "SELECT * FROM articulos ORDER BY id_articulo"
            cursor.execute(query)
            self.lista_articulos = cursor.fetchall()
            
            self.treeview.delete(*self.treeview.get_children())
                        
            for articulo in self.lista_articulos:
                self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2]))
            pass
        except Exception as e:
            messagebox.showerror("Error", f'No se pudieron cargar los articulos:\n{e}')
            
    def filtrar_datos(self, event):
        query = self.entry_id.get().lower()
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        try:
            regex = re.compile(query)
        except re.error:
            return
        
        if not query:
            for articulo in self.lista_articulos:
                self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2]))
        else:
            for articulo in self.lista_articulos:
                if regex.search(articulo[1].lower()):
                    self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2]))

    def seleccionar_articulo(self, event):
        curId = self.treeview.focus()
        if curId:
            curItem = self.treeview.item(curId)
            self.id.config(state='normal')  
            self.nombre.config(state="normal")
            self.precio.config(state="normal")
            self.id.delete(0,tk.END)
            self.nombre.delete(0, tk.END)
            self.precio.delete(0, tk.END)
            self.id.insert(0, curItem["values"][0])
            self.nombre.insert(0, curItem["values"][1])
            self.precio.insert(0, curItem["values"][2])
            self.id.config(state='disabled')
            self.nuevo_button.config(state="disabled")
            self.create_button.config(state="disabled")
            self.update_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.cancel_button.config(state="normal")
            