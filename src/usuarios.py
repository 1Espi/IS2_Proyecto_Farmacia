import tkinter as tk
from tkinter import ttk, messagebox
import utilities.connection as dbconn  

class UsuariosFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()
        self.connection = self.connect_db()

    def connect_db(self):
        try:
            con = dbconn.connection()
            connection = con.open() 
            return connection
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Usuarios", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Nombre").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar", command=self.search_user)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

        # ID (será autoincremental, solo para lectura)
        tk.Label(self, text="ID").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self, state='readonly')  
        self.entry_id.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(self, text="Username").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Password").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_password = tk.Entry(self, show='*')  # Para ocultar el texto de la contraseña
        self.entry_password.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Perfil").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.combo_perfil = ttk.Combobox(self, values=["Admin", "Gerente", "Cajero"], state="readonly")
        self.combo_perfil.grid(row=6, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=7, column=0, columnspan=4, pady=20)

        self.create_button = tk.Button(button_frame, text="Crear", width=10, command=self.create_user)
        self.create_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(button_frame, text="Guardar", width=10, command=self.save_user)
        self.save_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10, command=self.update_user)
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", width=10, command=self.delete_user)
        self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10, command=self.cancel)
        self.cancel_button.grid(row=0, column=4, padx=10)

        self.update_buttons_state("init")

    def create_user(self):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        
                
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, tk.END)
        cursor = self.connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM usuarios")
        next_id = cursor.fetchone()[0]
        self.entry_id.insert(0, next_id)

        self.entry_id.config(state='readonly')

        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.combo_perfil.set('')  

        self.update_buttons_state("create")

    def save_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        nombre = self.entry_nombre.get()
        perfil = self.combo_perfil.get()

        if not all([username, password, nombre, perfil]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (username, password, nombre, perfil) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, password, nombre, perfil)
            )
            self.connection.commit()
            new_id = cursor.fetchone()[0]
            self.entry_id.config(state='normal')
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, new_id)
            self.entry_id.config(state='readonly')
            messagebox.showinfo("Éxito", "Usuario guardado exitosamente.")
            self.cancel()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")
        finally:
            cursor.close()

    def search_user(self):
        username = self.entry_search.get().strip()  
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                self.entry_id.config(state='normal')
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, result[0])
                self.entry_id.config(state='readonly')

                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, result[1])

                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, result[2])

                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, result[3])

                self.combo_perfil.set(result[4])  

                self.update_buttons_state("modify")
            else:
                messagebox.showinfo("Info", "No se encontró ningún usuario con ese nombre.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el usuario: {e}")
        finally:
            cursor.close()

    def update_user(self):
        user_id = self.entry_id.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        nombre = self.entry_nombre.get()
        perfil = self.combo_perfil.get()

        if not all([user_id, username, password, nombre, perfil]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET username=%s, password=%s, nombre=%s, perfil=%s WHERE id=%s",
                (username, password, nombre, perfil, user_id)
            )
            self.connection.commit()
            messagebox.showinfo("Éxito", "Usuario modificado exitosamente.")
            self.cancel()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo modificar el usuario: {e}")
        finally:
            cursor.close()

    def delete_user(self):
        user_id = self.entry_id.get()

        if not user_id:
            messagebox.showerror("Error", "Primero busca un usuario para eliminar.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
            self.connection.commit()
            self.create_user()  
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            self.cancel()
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")
        finally:
            cursor.close()

    def cancel(self):
        self.update_buttons_state("init")
        self.entry_id.config(state="normal")
        self.entry_nombre.config(state="normal")
        self.entry_password.config(state="normal")
        self.entry_username.config(state="normal")
        self.entry_search.config(state="normal")
        self.combo_perfil.set('')                
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_search.delete(0, tk.END)

        self.entry_id.config(state="disable")

    def update_buttons_state(self, state):
        """Actualizar el estado de los botones según el estado."""
        if state == "init":
            self.create_button.config(state='normal')
            self.save_button.config(state='disabled')
            self.update_button.config(state='disabled')
            self.delete_button.config(state='disabled')
            self.cancel_button.config(state='disabled')
        elif state == "create":
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

