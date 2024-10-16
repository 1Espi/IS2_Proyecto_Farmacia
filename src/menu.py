import tkinter as tk
from tkinter import messagebox
from .almacen import AlmacenFrame
from .compras import ComprasFrame
from .ventas import VentasFrame
from .clientes import ClientesFrame
from .usuarios import UsuariosFrame
from .articulos import ArticulosFrame
from .reabastecimiento import ReabastecimientoFrame

class Menu:
    def __init__(self, user_info):
        self.user_info = user_info
        self.current_frame = None  # Para almacenar el frame actual

    def open_main_menu(self):
        self.menu_window = tk.Tk()
        self.menu_window.title("Menú Principal")
        self.menu_window.minsize(500, 300)

        # Contenedor principal
        self.container = tk.Frame(self.menu_window)
        self.container.pack(fill="both", expand=True)

        # Frame para el menú
        self.menu_frame = tk.Frame(self.container)
        self.menu_frame.pack(side="top", fill="x")

        # Etiqueta de bienvenida
        self.welcome_label = tk.Label(self.container, text=f'Hola {self.user_info["NOMBREUSUARIO"]}', font=("Arial", 16))
        self.welcome_label.pack(pady=20)

        # Crear botones para el menú
        self.create_menu_buttons()

        self.menu_window.mainloop()

    def create_menu_buttons(self):
        # Diccionario de acciones según el perfil del usuario
        profile_actions = {
            "admin": ["Articulos", "Almacen", "Compras", "Ventas", "Clientes", "Usuarios", "Cerrar Sesion", "Reabastecimiento"],
            "gerente": ["Articulos", "Ventas", "Clientes", "Cerrar Sesion"],
            "cajero": [ "Articulos", "Ventas", "Cerrar Sesion"]
        }

        actions = profile_actions.get(self.user_info["ROL"].lower())
        if actions:
            for action in actions:
                button = tk.Button(self.menu_frame, text=action, command=lambda a=action: self.handle_menu_action(a))
                button.pack(side="left", padx=5, pady=5)  # Espaciado entre botones
        else:
            messagebox.showerror("Error", "Perfil de usuario no reconocido")
            self.menu_window.destroy()

    def handle_menu_action(self, action):
        if self.current_frame:
            self.current_frame.destroy()  # Eliminar el frame actual
        
        self.welcome_label.forget()

        if action == "Cerrar Sesion":
            self.menu_window.destroy()
            from .login import Login
            Login()
            return

        # Inicializa el frame correspondiente
        frame_class = {
            "Articulos": ArticulosFrame,
            "Comprasss": ComprasFrame,
            "Ventas": VentasFrame,
            "Clientes": ClientesFrame,
            "Usuarios": UsuariosFrame,
            "Almacen": AlmacenFrame,
           "Reabastecimiento": ReabastecimientoFrame
        }.get(action)
        
        if frame_class:
            if action == "Reabastecimiento":
                # Pasar self.user_info cuando sea Reabastecimiento
                self.current_frame = frame_class(self, self.container, self.user_info)
            else:
                self.current_frame = frame_class(self, self.container)
            self.current_frame.pack(fill="both", expand=True)  # Mostrar el nuevo frame

        