import tkinter as tk
from tkinter import messagebox, ttk
import utilities.connection as dbconn
from .menu import Menu

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Log in")
        self.root.minsize(300, 200)

        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Username:").grid(row=0, column=0, pady=5)
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        tk.Button(self.root, text="Acceder", command=self.login).pack(pady=10)

        # Variable para almacenar el perfil del usuario
        self.user_info = {}
        self.root.mainloop()

    def login(self):
        username = self.entry_username.get()
        input_password = self.entry_password.get()

        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT ID, username, password, perfil, nombre FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:
                stored_password = user[2]
                
                if input_password == stored_password:
                    self.user_info['ID'] = user[0]
                    self.user_info['USERNAME'] = user[1]
                    self.user_info['PERFIL'] = user[3]
                    self.user_info['NOMBRE'] = user[4]
                    self.root.destroy()
                    menu = Menu(self.user_info)
                    menu.open_main_menu()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

            cursor.close()
            con.close()

        except Exception as e:
            messagebox.showerror("Ocurrió un error", f"Error: {e}")