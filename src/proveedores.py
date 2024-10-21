import tkinter as tk
from tkinter import ttk
import utilities.connection as connfile
from tkinter import messagebox
import re

class MostrarProveedores(tk.Frame):  
    def __init__(self, parent, container, lista: list, proveedorWidget: ttk.Combobox):
        super().__init__(container)
        self.parent = parent
        
        self.lista_articulos = []
        self.lista_combobox = []
        self.lista_agregados = []
        
        self.connection = connfile.connect_db()
        self.setup_ui()
        container.geometry("1000x300")  

    def setup_ui(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT id_articulo, nombre FROM articulos"
            cursor.execute(query)
            self.lista_articulos = cursor.fetchall()
            
            for articulo in self.lista_articulos:
                self.lista_combobox.append(articulo[1])
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron recabar los articulos\n{e}")
        
        title = tk.Label(self, text="Gestión de Proveedores", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=100, pady=10)

        tk.Label(self, text="Buscar por nombre:").grid(row=1, column=0, sticky='e', padx=10, pady=5)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar", command=self.search_prov)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

        # ID (será autoincremental, solo para lectura)
        tk.Label(self, text="Id:").grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.entry_id = tk.Entry(self, state='readonly')  
        self.entry_id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Compañía:").grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.entry_compania = tk.Entry(self)
        self.entry_compania.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Telefono:").grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.entry_telefono = tk.Entry(self)
        self.entry_telefono.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Correo:").grid(row=5, column=0, sticky='e', padx=10, pady=5)
        self.entry_correo = tk.Entry(self)
        self.entry_correo.grid(row=5, column=1, pady=5, padx=10)
        
        self.treeview = ttk.Treeview(self, style="",columns=("Codigo", "Nombre"), show="headings")
        self.treeview.column("Codigo", anchor="center")
        self.treeview.column("Nombre", anchor="center")
        
        self.treeview.heading("Codigo", text="Codigo")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.grid(row=1, column=3, pady=10, padx=10, rowspan=6, columnspan=2)
        self.treeview.bind('<ButtonRelease-1>', self.select_product)
        
        ultima_col = 5
        
        tk.Label(self, text="Nombre:").grid(row=1, column=ultima_col, padx=5)
        self.articulos = ttk.Combobox(self, values=self.lista_combobox, width=20, state="disabled")
        self.articulos.grid(row=2, column=ultima_col, padx=5)
        self.articulos.bind("<<ComboboxSelected>>", self.combo_selection)
        
        tk.Label(self, text="Id:").grid(row=3, column=ultima_col, padx=10)
        self.entry_id_articulo = tk.Entry(self, state="readonly")
        self.entry_id_articulo.grid(row=4, column=ultima_col, padx=10)

        self.add_button = tk.Button(self, text="Agregar", command=self.add_product)
        self.add_button.grid(row=5, column=ultima_col, padx=10, pady=5)

        self.remove_button = tk.Button(self, text="Quitar", command=self.remove_product)
        self.remove_button.grid(row=6, column=ultima_col, padx=10, pady=5)

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)

        self.create_button = tk.Button(button_frame, text="Crear", width=10, command=self.create_prov)
        self.create_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(button_frame, text="Guardar", width=10, command=self.save_prov)
        self.save_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10, command=self.update_prov)
        self.update_button.grid(row=0, column=2, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10, command=self.cancel)
        self.cancel_button.grid(row=0, column=3, padx=10)

        self.update_buttons_state("init")
        
    def create_prov(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        cursor = self.connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(id_proveedor), 0) + 1 FROM proveedores")
        next_id = cursor.fetchone()[0]
        self.entry_id.insert(0, next_id)

        self.entry_id.config(state='readonly')

        self.entry_compania.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

        self.update_buttons_state("create")

    def save_prov(self):
        def es_correo_valido(correo):
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(patron, correo) is not None
        
        compania = self.entry_compania.get()
        telefono = self.entry_telefono.get()
        correo = self.entry_correo.get()

        if not all([compania, telefono, correo]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        
        if telefono.isdigit():
            if len(telefono) != 10:
                messagebox.showerror("Error", "Ingrese un numero de telefono valido")
                return
        else:
            messagebox.showerror("Error", "Ingrese un numero para el telefono")
            return
        
        if not es_correo_valido(correo):
            messagebox.showerror("Error", "Ingrese un correo valido")
            return
        
        if len(self.lista_agregados) == 0:
            messagebox.showerror("Error", "Ingrese al menos un articulo")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO proveedores (compania, telefono, correo) VALUES (%s, %s, %s) RETURNING id_proveedor", (compania, telefono, correo))
            id_proveedor = cursor.fetchone()[0]
            
            for articulo in self.lista_agregados:
                cursor.execute("INSERT INTO articulos_proveedores (id_proveedor, id_articulo) VALUES (%s, %s)", (id_proveedor, articulo[0]))
            
            
            self.lista_agregados = []
            self.lista_combobox = self.lista_articulos.copy()
            self.articulos.config(values=self.lista_combobox)
            
            messagebox.showinfo("Éxito", "Proveedor guardado exitosamente.")
            self.cancel()
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el proveedor: {e}")
        finally:
            cursor.close()

    def search_prov(self):
        compania = self.entry_search.get().strip()  # Eliminamos espacios adicionales
    
        if not compania:
            messagebox.showerror("Error", "Ingrese un nombre a buscar")
            return
            
        cursor = self.connection.cursor()
        try:
            # Hacemos que la consulta sea insensible a mayúsculas/minúsculas
            cursor.execute("SELECT * FROM proveedores WHERE LOWER(compania) = LOWER(%s)", (compania,))
            result = cursor.fetchone()

            if result is None:
                messagebox.showerror("Error", "No se encontró el nombre de la empresa")
                return
            
            cursor.execute(f"SELECT * FROM articulos_proveedores WHERE id_proveedor = %s", (str(result[0]),))
            product_ids = cursor.fetchall()
            
            self.lista_agregados = []
            for register in product_ids:
                cursor.execute("SELECT id_articulo, nombre FROM articulos WHERE id_articulo=%s", (str(register[1])))
                value = cursor.fetchone()
                self.lista_agregados.append(value)
            
            if result and product_ids:
                self.entry_id.config(state='normal')
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, str(result[0]))
                self.entry_id.config(state='readonly')

                self.entry_compania.config(state="normal")
                self.entry_compania.delete(0, tk.END)
                self.entry_compania.insert(0, str(result[1]))

                self.entry_telefono.config(state="normal")
                self.entry_telefono.delete(0, tk.END)
                self.entry_telefono.insert(0, str(result[2]))

                self.entry_correo.config(state="normal")
                self.entry_correo.delete(0, tk.END)
                self.entry_correo.insert(0, str(result[3]))

                self.load_added_products()
                self.update_buttons_state("modify")
                
                self.lista_combobox = self.lista_articulos.copy()
                self.lista_combobox = [elemento for elemento in self.lista_combobox if elemento not in self.lista_agregados]
                
                self.lista_combobox = [nombre for id, nombre in self.lista_combobox]
                
                self.articulos.config(values=self.lista_combobox)
                self.articulos.set("")
                
                self.entry_id_articulo.config(state="normal")
                self.entry_id_articulo.delete(0, tk.END)
                self.entry_id_articulo.config(state="disabled")
            else:
                messagebox.showinfo("Info", "No se encontró ningún proveedor con ese nombre.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el proveedor\n{e}")
        finally:
            cursor.close()

    def update_prov(self):
        prov_id = self.entry_id.get()
        compania = self.entry_compania.get()
        telefono = self.entry_telefono.get()
        correo = self.entry_correo.get()

        if not all([prov_id, compania, telefono, correo]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        
        if len(self.lista_agregados) == 0:
            messagebox.showerror("Error", "Debe agregar al menos un producto")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE proveedores SET compania=%s, telefono=%s, correo=%s WHERE id_proveedor=%s",
                (compania, telefono, correo, prov_id)
            )
            
            cursor.execute(
                "DELETE FROM articulos_proveedores WHERE id_proveedor=%s",
                (prov_id,)
            )
            
            for articulo in self.lista_agregados:
                cursor.execute(
                    "INSERT INTO articulos_proveedores (id_proveedor, id_articulo) VALUES (%s, %s)",
                    (prov_id, articulo[0])
                )
            
            messagebox.showinfo("Éxito", "Proveedor modificado exitosamente.")

            self.cancel()
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo modificar el proveedor\n{e}")
        finally:
            cursor.close()

    def cancel(self):
        self.lista_agregados = []
        self.load_added_products()
        self.lista_combobox = self.lista_articulos.copy()
        self.articulos.config(values=self.lista_combobox)
        self.update_buttons_state("cancel")
        self.entry_id.config(state="normal")
        self.entry_correo.config(state="normal")
        self.entry_telefono.config(state="normal")
        self.entry_compania.config(state="normal")
        self.entry_search.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_compania.delete(0, tk.END)
        self.entry_search.delete(0, tk.END)

        self.entry_id.config(state="disabled")
        self.entry_correo.config(state="disabled")
        self.entry_telefono.config(state="disabled")
        self.entry_compania.config(state="disabled")
        
        self.update_buttons_state("cancel")

    def update_buttons_state(self, state):
        """Actualizar el estado de los botones según el estado."""
        if state == "init":
            self.entry_id.config(state="disabled")
            self.entry_compania.config(state="disabled")
            self.entry_telefono.config(state="disabled")
            self.entry_correo.config(state="disabled")
            self.articulos.config(state="disabled")
            self.entry_id_articulo.config(state="disabled")
            
            self.add_button.config(state='disabled')
            self.remove_button.config(state="disabled")
            self.create_button.config(state='normal')
            self.save_button.config(state='disabled')
            self.update_button.config(state='disabled')
            self.cancel_button.config(state='disabled')
        elif state == "create":
            self.entry_id.config(state="disabled")
            self.entry_compania.config(state="normal")
            self.entry_telefono.config(state="normal")
            self.entry_correo.config(state="normal")
            self.articulos.config(state="readonly")
            self.entry_id_articulo.config(state="disabled")
            
            self.add_button.config(state='normal')
            self.create_button.config(state='disabled')
            self.save_button.config(state='normal')
            self.update_button.config(state='disabled')
            self.cancel_button.config(state='normal')
        elif state == "modify":
            self.entry_id.config(state="disabled")
            self.entry_compania.config(state="normal")
            self.entry_telefono.config(state="normal")
            self.entry_correo.config(state="normal")
            self.articulos.config(state="readonly")
            self.entry_id_articulo.config(state="disabled")
            
            self.add_button.config(state='normal')
            self.create_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.update_button.config(state='normal')
            self.cancel_button.config(state='normal')
        elif state == "cancel":
            self.entry_id.config(state="disabled")
            self.entry_compania.config(state="disabled")
            self.entry_telefono.config(state="disabled")
            self.entry_correo.config(state="disabled")
            self.articulos.config(state="disabled")
            self.entry_id_articulo.config(state="disabled")
            
            self.add_button.config(state='disabled')
            self.remove_button.config(state="disabled")
            self.create_button.config(state='normal')
            self.save_button.config(state='disabled')
            self.update_button.config(state='disabled')
            self.cancel_button.config(state='normal')
            
    def load_added_products(self):
        try:
            self.treeview.delete(*self.treeview.get_children())
                        
            for articulo in self.lista_agregados:
                self.treeview.insert(parent='', index='end', iid=articulo[0], values=(articulo[0],articulo[1]))
            
        except Exception as e:
            messagebox.showerror("Error", f'No se pudieron cargar los articulos:\n{e}')
            return
        
    def combo_selection(self, event):
        opcion = self.articulos.get()
        identificador = None
        for articulo in self.lista_articulos:
            if articulo[1] == opcion:
                identificador = articulo[0]
        
        self.entry_id_articulo.config(state='normal')
        self.entry_id_articulo.delete(0, tk.END)
        self.entry_id_articulo.insert(0, identificador)
        self.entry_id_articulo.config(state='disabled')
        
    def select_product(self, event):
        self.remove_button.config(state="normal")
        
    def add_product(self):
        nombre = self.articulos.get()
        id = self.entry_id_articulo.get()
        
        if not nombre or not id:
            messagebox.showerror("Error", "Seleccione un articulo")
            return
        
        if nombre in self.lista_combobox:
            self.lista_combobox.remove(nombre)
            
        self.articulos.config(state="normal")
        self.articulos.set("")
        self.articulos.config(values=self.lista_combobox)
        
        self.entry_id_articulo.config(state="normal")
        self.entry_id_articulo.delete(0, tk.END)
        self.entry_id_articulo.config(state="disabled")

        self.lista_agregados.append((id, nombre))
        self.load_added_products()
        
    def remove_product(self):
        curId = self.treeview.focus()
        if curId:
            try:
                print("ENTRA AL IF")
                curItem = self.treeview.item(curId)
                index = None
                for i in range(len(self.lista_agregados)):
                    if str(self.lista_agregados[i][0]) == str(curItem['values'][0]):
                        index = i
                        break
                print(f'Indice: {index}')
                if index is not None:  # Cambiado para verificar si no es None
                    self.lista_combobox.append(self.lista_agregados[index][1])
                    self.articulos.config(values=self.lista_combobox)
                    
                    self.lista_agregados.pop(index)
                    self.load_added_products()
                print(f'Lista agregados: {self.lista_agregados}')
                self.articulos.config(state="normal")
                self.articulos.set("")
            except Exception as e:
                messagebox.showerror("Error", f'No se pudo quitar el articulo\n{e}')
                return
                
        self.remove_button.config(state="disabled")