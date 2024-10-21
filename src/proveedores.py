import tkinter as tk
from tkinter import ttk
import utilities.connection as connfile
from tkinter import messagebox
import re

class MostrarProveedores(tk.Frame):  
    def __init__(self, parent, container, lista: list, proveedorWidget: ttk.Combobox):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()
        self.connection = connfile.connect_db()
        container.geometry("425x300")  

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Proveedores", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

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

        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=0, columnspan=4, pady=20)

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

        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO proveedores (compania, telefono, correo) VALUES (%s, %s, %s) RETURNING id_proveedor", (compania, telefono, correo))
            self.connection.commit()
            new_id = cursor.fetchone()[0]
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, new_id)
            self.entry_id.config(state='readonly')
            messagebox.showinfo("Éxito", "Proveedor guardado exitosamente.")
            self.cancel()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")
        finally:
            cursor.close()

    def search_prov(self):
        compania = self.entry_search.get() 
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM proveedores WHERE compania = '{compania}'")
            result = cursor.fetchone()
            if result:
                self.entry_id.config(state='normal')
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, result[0])
                self.entry_id.config(state='readonly')

                self.entry_compania.config(state="normal")
                self.entry_compania.delete(0, tk.END)
                self.entry_compania.insert(0, result[1])

                self.entry_telefono.config(state="normal")
                self.entry_telefono.delete(0, tk.END)
                self.entry_telefono.insert(0, result[2])

                self.entry_correo.config(state="normal")
                self.entry_correo.delete(0, tk.END)
                self.entry_correo.insert(0, result[3])

                self.update_buttons_state("modify")
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

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE proveedores SET compania=%s, telefono=%s, correo=%s WHERE id_proveedor=%s",
                (compania, telefono, correo, prov_id)
            )
            self.connection.commit()
            messagebox.showinfo("Éxito", "Proveedor modificado exitosamente.")
            self.cancel()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo modificar el proveedor\n{e}")
        finally:
            cursor.close()

    def cancel(self):
        self.update_buttons_state("init")
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

    def update_buttons_state(self, state):
        """Actualizar el estado de los botones según el estado."""
        if state == "init":
            self.create_button.config(state='normal')
            self.save_button.config(state='disabled')
            self.update_button.config(state='disabled')
            self.cancel_button.config(state='disabled')
        elif state == "create":
            self.create_button.config(state='disabled')
            self.save_button.config(state='normal')
            self.update_button.config(state='disabled')
            self.cancel_button.config(state='normal')
        elif state == "modify":
            self.create_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.update_button.config(state='normal')
            self.cancel_button.config(state='normal')

