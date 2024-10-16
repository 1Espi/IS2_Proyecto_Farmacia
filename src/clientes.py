import tkinter as tk
from tkinter import ttk

class ClientesFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Clientes", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Buscar por Nombre").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=1, column=1, pady=5, padx=10)
        
        self.search_button = tk.Button(self, text="Buscar", width=10)
        self.search_button.grid(row=1, column=2, padx=10, pady=5)
        
        # ID del usuario que creo al cliente (solo lectura sera autoincremental)
        tk.Label(self, text="Nombre usuario").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self, state='readonly')  
        self.entry_id.grid(row=2, column=1, pady=5, padx=10)

        # ID del Cliente (solo lectura sera autoincremental)
        tk.Label(self, text="ID Cliente").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.entry_id = tk.Entry(self, state='readonly')  
        self.entry_id.grid(row=3, column=1, pady=5, padx=10)

        tk.Label(self, text="Nombre").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(self, text="Correo").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=5, column=1, pady=5, padx=10)

        tk.Label(self, text="Teléfono").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=6, column=1, pady=5, padx=10)

        #al crear el cliente estara bloqueado debido a que se colocara automatico en 0
        tk.Label(self, text="Puntos acumulados").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.entry_points = tk.Entry(self)
        self.entry_points.grid(row=7, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20)

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
