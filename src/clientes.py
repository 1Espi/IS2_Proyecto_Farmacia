import tkinter as tk
from tkinter import ttk, messagebox
import utilities.connection as dbconn  # Conexión gestionada por .env

class ClientesFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()
        self.connection = self.connect_db()
        self.update_buttons_state("initial")  # Estado inicial de los botones

    def connect_db(self):
        # Conexión usando utilities.connection
        try:
            con = dbconn.connection()
            connection = con.open()  # Método open() para abrir la conexión desde la utilidad
            return connection
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Clientes", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Nombre").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar", width=10, command=self.search_client)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)
        
        tk.Label(self, text="ID Cliente").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self, state='readonly')  
        self.entry_id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Correo").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Teléfono").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Puntos acumulados").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_points = tk.Entry(self, state='readonly')
        self.entry_points.grid(row=6, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=4, pady=20)

        self.create_button = tk.Button(button_frame, text="Nuevo", width=10, command=self.new_client)
        self.create_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(button_frame, text="Guardar", width=10, command=self.save_client, state='disabled')
        self.save_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10, command=self.update_client, state='disabled')
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", width=10, command=self.delete_client, state='disabled')
        self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10, command=self.cancel, state='disabled')
        self.cancel_button.grid(row=0, column=4, padx=10)

    def update_buttons_state(self, state):
        if state == "initial":
            self.create_button.config(state='normal')
            self.save_button.config(state='disabled')
            self.update_button.config(state='disabled')
            self.delete_button.config(state='disabled')
            self.cancel_button.config(state='disabled')
        elif state == "new":
            self.create_button.config(state='disabled')
            self.save_button.config(state='normal')
            self.update_button.config(state='disabled')
            self.delete_button.config(state='disabled')
            self.cancel_button.config(state='normal')
        elif state == "modify":
            self.create_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.update_button.config(state='normal')
            self.delete_button.config(state='normal')
            self.cancel_button.config(state='normal')

    def new_client(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        
        # Obtener el siguiente ID disponible
        cursor = self.connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(id_cliente), 0) + 1 FROM cliente")
        next_id = cursor.fetchone()[0]
        self.entry_id.insert(0, next_id)
        self.entry_id.config(state='readonly')

        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        
        self.entry_points.config(state='normal')
        self.entry_points.delete(0, tk.END)
        self.entry_points.insert(0, "0")
        self.entry_points.config(state='readonly')

        self.update_buttons_state("new")  # Cambiar el estado de los botones

    def save_client(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        if not all([name, email, phone]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO cliente (nombre, telefono, email, puntos) VALUES (%s, %s, %s, %s) RETURNING id_cliente",
                (name, phone, email, 0)
            )
            self.connection.commit()
            new_id = cursor.fetchone()[0]
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, new_id)
            self.entry_id.config(state='readonly')
            messagebox.showinfo("Éxito", "Cliente guardado exitosamente.")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")
        finally:
            cursor.close()

    def search_client(self):
        name = self.entry_search.get()
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM cliente WHERE nombre = %s", (name,))
            result = cursor.fetchone()
            if result:
                self.entry_id.config(state='normal')
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, result[0])
                self.entry_id.config(state='readonly')

                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, result[1])

                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, result[3])

                self.entry_phone.delete(0, tk.END)
                self.entry_phone.insert(0, result[2])

                self.entry_points.config(state='normal')
                self.entry_points.delete(0, tk.END)
                self.entry_points.insert(0, result[4])
                self.entry_points.config(state='readonly')

                # Cambiar el estado a "modify"
                self.update_buttons_state("modify")
            else:
                messagebox.showinfo("Info", "No se encontró ningún cliente con ese nombre.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el cliente: {e}")
        finally:
            cursor.close()

    def update_client(self):
        client_id = self.entry_id.get()
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        if not all([client_id, name, email, phone]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE cliente SET nombre=%s, telefono=%s, email=%s WHERE id_cliente=%s",
                (name, phone, email, client_id)
            )
            self.connection.commit()
            messagebox.showinfo("Éxito", "Cliente modificado exitosamente.")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")
        finally:
            cursor.close()
            self.cancel()  # Regresar al estado inicial

    def delete_client(self):
        client_id = self.entry_id.get()

        if not client_id:
            messagebox.showerror("Error", "No se ha seleccionado ningún cliente.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (client_id,))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
        finally:
            cursor.close()
            self.cancel()  # Regresar al estado inicial

    def cancel(self):
        self.entry_id.config(state='readonly')
        self.entry_id.config(state="normal")
        self.entry_points.config(state="normal")
        self.entry_id.delete(0, tk.END)
        
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

        self.entry_points.config(state='normal')
        self.entry_points.delete(0, tk.END)
        self.entry_points.config(state='readonly')
        self.entry_id.config(state="disable")
        self.entry_points.config(state="disable")

        self.update_buttons_state("initial")  # Regresar al estado inicial

