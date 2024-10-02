import tkinter as tk
from tkinter import ttk

class UsuariosFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Usuarios", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Nombre").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar")
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

        # ID (sera autoincremental, solo para lectura)
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

        self.create_button = tk.Button(button_frame, text="Crear", width=10)
        self.create_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(button_frame, text="Guardar", width=10)
        self.save_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(button_frame, text="Modificar", width=10)
        self.update_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar", width=10)
        self.delete_button.grid(row=0, column=3, padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", width=10)
        self.cancel_button.grid(row=0, column=4, padx=10)
