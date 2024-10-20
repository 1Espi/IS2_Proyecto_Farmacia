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

       
        tk.Label(self, text="ID del articulo:", anchor='e').grid(row=1, column=0, sticky='e', padx=10, pady=5)
        self.id= tk.Entry(self, state='readonly', width=40)  
        self.id.grid(row=1, column=1, pady=5, padx=10, sticky='e', )

        tk.Label(self, text="Nombre del articulo:", anchor='e').grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.nombre = tk.Entry(self, state='readonly', width=40)
        self.nombre.grid(row=2, column=1, pady=5, padx=10, sticky='e')

        tk.Label(self, text="Precio:", anchor='e').grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.precio = tk.Entry(self, state='readonly', width=40)
        self.precio.grid(row=3, column=1, pady=5, padx=10, sticky='e')
        
        tk.Label(self, text="Cantidad:", anchor='e').grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.cantidad = tk.Entry(self, state='readonly', width=40)
        self.cantidad.grid(row=4, column=1, pady=5, padx=10, sticky='e')
        
        tk.Label(self, text="Maximos:", anchor='e').grid(row=5, column=0, sticky='e', padx=10, pady=5)
        self.maximos = tk.Entry(self, state='readonly', width=40)
        self.maximos.grid(row=5, column=1, pady=5, padx=10, sticky='e')
        
        tk.Label(self, text="Minimos:", anchor='e').grid(row=6, column=0, sticky='e', padx=10, pady=5)
        self.minimos = tk.Entry(self, state='readonly', width=40)
        self.minimos.grid(row=6, column=1, pady=5, padx=10, sticky='e')
        
        self.treeview = ttk.Treeview(self, columns=("Codigo", "Nombre", "Precio", "Cantidad", "Maximos", "Minimos"), show="headings")
        self.treeview.column("Codigo", anchor="center")
        self.treeview.column("Nombre", anchor="center")
        self.treeview.column("Precio", anchor="center")
        self.treeview.column("Cantidad", anchor="center")
        self.treeview.column("Maximos", anchor="center")
        self.treeview.column("Minimos", anchor="center")
        
        self.treeview.heading("Codigo", text="Codigo")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Precio", text="Precio")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Maximos", text="Maximos")
        self.treeview.heading("Minimos", text="Minimos")
        self.treeview.grid(row=1, column=2, pady=5, padx=10, rowspan=6, columnspan=2)
        
        self.treeview.bind('<ButtonRelease-1>', self.seleccionar_articulo)
        
        tk.Label(self, text="Buscar por nombre:", justify='center', anchor="center").grid(row=7, column=2, padx=10, pady=5, sticky='e')
        self.entry_id = tk.Entry(self, width=40)
        self.entry_id.grid(row=7, column=3, pady=5, padx=10, sticky='w')
        self.entry_id.bind("<KeyRelease>", self.filtrar_datos)

        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.nuevo_button = tk.Button(button_frame, text="Nuevo", command=self.nuevo, width=10, state='normal')
        self.nuevo_button.grid(row=0, column=0, padx=10)

        self.create_button = tk.Button(button_frame, text="Crear", command=self.crear, width=10, state='disabled')
        self.create_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", command=self.modificar, width=10, state='disabled')
        self.update_button.grid(row=0, column=2, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.cancelar, width=10, state='disabled')
        self.cancel_button.grid(row=0, column=3, padx=10)
        self.cargar_articulos()
        
    def nuevo(self):
        try:
            self.limpiar_campos()
            connection = connfile.connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT COALESCE(MAX(id_articulo), 0) + 1 FROM articulos")
            id_articulo = cursor.fetchone()
            
            self.id.insert(0, id_articulo)
            self.id.config(state='readonly')
            self.cantidad.insert(0, '0')
            self.cantidad.config(state='readonly')
            
            self.nuevo_button.config(state="disabled")
            self.create_button.config(state="normal")
            self.update_button.config(state="disabled")
            self.cancel_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo cargar un ID para el nuevo articulo, intente de nuevo:\n{e}')

    def crear(self):
        id = self.id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()
        cantidad = self.cantidad.get()
        maximos = self.maximos.get()
        minimos = self.minimos.get()

        if not nombre or not precio or not id or not cantidad or not maximos or not minimos:
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
        
        if not maximos.isdigit():
            messagebox.showerror("Error", "El tope máximo tiene que ser un número entero")
            return

        if not minimos.isdigit():
            messagebox.showerror("Error", "El tope mínimo tiene que ser un número entero")
            return
        
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "INSERT INTO articulos(nombre, precio, cantidad, maximos, minimos) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, precio, cantidad, maximos, minimos)
            cursor.execute(query, valores)
            connection.commit()
            
            self.cargar_articulos()
            self.filtrar_datos(event=None)
            
            messagebox.showinfo("Éxito", "Articulo guardado exitosamente")
            self.cancelar() 
        except Exception as e:
            messagebox.showerror("Error", f'No se pudo agregar el articulo\n{e}')
    
    def modificar(self):
        id = self.id.get()
        nombre = self.nombre.get()
        precio = self.precio.get()
        cantidad = self.cantidad.get()
        maximos = self.maximos.get()
        minimos = self.minimos.get()

        if not nombre or not precio or not id or not cantidad or not maximos or not minimos:
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
        
        if not maximos.isdigit():
            messagebox.showerror("Error", "El tope máximo tiene que ser un número entero")
            return

        if not minimos.isdigit():
            messagebox.showerror("Error", "El tope mínimo tiene que ser un número entero")
            return
        
        try:
            connection = connfile.connect_db()
            cursor = connection.cursor()
            query = "UPDATE articulos SET nombre = %s, precio = %s, cantidad = %s, maximos = %s, minimos = %s WHERE id_articulo = %s"
            valores = (nombre, precio, cantidad, maximos, minimos, id)
            cursor.execute(query, valores)
            connection.commit()
            
            self.cargar_articulos()
            self.filtrar_datos(event=None)
            
            messagebox.showinfo("Éxito", "Articulo actualizado exitosamente")
            self.cancelar()
            
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f'No se pudo actualizar el articulo:\n{e}')
            
    def cancelar(self):
        self.limpiar_campos()
        
        self.id.config(state='readonly')  
        self.nombre.config(state="readonly")
        self.precio.config(state="readonly")
        self.cantidad.config(state="readonly")
        self.maximos.config(state="readonly")
        self.minimos.config(state="readonly")
        
        self.nuevo_button.config(state="normal")
        self.create_button.config(state="disabled")
        self.update_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        
    def limpiar_campos(self):
        self.id.config(state='normal')  
        self.nombre.config(state="normal")
        self.precio.config(state="normal")
        self.cantidad.config(state="normal")
        self.maximos.config(state="normal")
        self.minimos.config(state="normal")
        self.id.delete(0,tk.END)
        self.nombre.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.maximos.delete(0, tk.END)
        self.minimos.delete(0, tk.END)
  
  
    def cargar_articulos(self):
        try:
            dbconn = connfile.connect_db()
            cursor = dbconn.cursor()
            
            query = "SELECT * FROM articulos ORDER BY id_articulo"
            cursor.execute(query)
            self.lista_articulos = cursor.fetchall()
            
            self.treeview.delete(*self.treeview.get_children())
                        
            for articulo in self.lista_articulos:
                self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2], articulo[3], articulo[4], articulo[5]))
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
                self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2], articulo[3], articulo[4], articulo[5]))
        else:
            for articulo in self.lista_articulos:
                if regex.search(articulo[1].lower()):
                    self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1],articulo[2], articulo[3], articulo[4], articulo[5]))

    def seleccionar_articulo(self, event):
        curId = self.treeview.focus()
        if curId:
            curItem = self.treeview.item(curId)
            
            self.limpiar_campos()
            
            self.id.insert(0, curItem["values"][0])
            self.nombre.insert(0, curItem["values"][1])
            self.precio.insert(0, curItem["values"][2])
            self.cantidad.insert(0, curItem["values"][3])
            self.maximos.insert(0, curItem["values"][4])
            self.minimos.insert(0, curItem["values"][5])
            
            self.id.config(state='disabled')
            if self.parent.user_info["PERFIL"].lower() == 'admin':
                self.cantidad.config(state="normal")
            else:
                self.cantidad.config(state="readonly")
                
            self.nuevo_button.config(state="disabled")
            self.create_button.config(state="disabled")
            self.update_button.config(state="normal")
            self.cancel_button.config(state="normal")
            