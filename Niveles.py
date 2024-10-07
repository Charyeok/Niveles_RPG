import tkinter as tk
from tkinter import messagebox
import json
import os

class Nivel:
    def __init__(self, nombre, xp_necesario):
        self.nombre = nombre
        self.xp_necesario = xp_necesario

class Usuario:
    def __init__(self, nombre):
        self.nombre_usuario = os.getlogin() # gets the system user
        self.nombre = nombre
        self.nivel_actual = 1
        self.xp_actual = 0
        self.niveles = self.crear_niveles()

    def crear_niveles(self):
        return [
            Nivel("Hermes", 0),
            Nivel("Anubis", 100),
            Nivel("Thor", 200),
            Nivel("Susanoo", 300),
            Nivel("Atenea", 400),
            Nivel("Quetzalcóatl", 500),
            Nivel("Freyja", 600),
            Nivel("Odin", 700),
            Nivel("Zeus", 800),
            Nivel("Amateratsu", 900)
        ]

    #range difficulty
    def agregar_tarea(self, dificultad): 
        if dificultad in ['facil', 'Facil','easy']:
            xp_ganado =  20

        elif dificultad in ['intermedia', 'medium', 'intermedio']:
            xp_ganado = 50
        
        elif dificultad in ['dificil', 'hard', 'Dificil']:
            xp_ganado = 100

        else:
            return 0

        self.xp_actual += xp_ganado
        self.verificar_nivel()
        return xp_ganado

    def verificar_nivel(self):
        while self.nivel_actual < len(self.niveles) and self.xp_actual >= self.niveles[self.nivel_actual].xp_necesario:
            self.nivel_actual += 1


    def guardar_progreso(self):    
        datos = {
            "nombre": self.nombre,
            "xp_actual": self.xp_actual,
            "nivel_actual": self.nivel_actual
        }
        #Path = user's documents folder
        with open(f"C://Users//{self.nombre_usuario}//Documents//{self.nombre}.json", "w") as archivo: 
            json.dump(datos, archivo)


    #Path = user's documents folder
    def cargar_progreso(self):
        if os.path.exists("C://Users//{self.nombre_usuario}//Documents//{self.nombre}.json"):
            with open("C://Users//{self.nombre_usuario}//Documents//{self.nombre}.json", "r") as archivo:
                datos = json.load(archivo)
                self.xp_actual = datos["xp_actual"]
                self.nivel_actual = datos["nivel_actual"]

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Niveles")
        self.geometry("300x300")
        self.usuario = None

        self.label_usuario = tk.Label(self, text="Nombre de usuario:")
        self.label_usuario.pack(pady=10)

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.label_contraseña = tk.Label(self, text="Contraseña:")
        self.label_contraseña.pack(pady=10)

        self.entry_contraseña = tk.Entry(self, show='*')
        self.entry_contraseña.pack(pady=5)

        self.boton_login = tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.boton_login.pack(pady=10)

        self.boton_registrar = tk.Button(self, text="Registrar", command=self.registrar_usuario)
        self.boton_registrar.pack(pady=5)

    def iniciar_sesion(self):
        nombre = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        if os.path.exists(f"{nombre}.json"):
            with open(f"{nombre}.json", "r") as archivo:
                datos = json.load(archivo)
                if datos.get("contraseña") == contraseña:
                    self.usuario = Usuario(nombre)
                    self.usuario.xp_actual = datos["xp_actual"]
                    self.usuario.nivel_actual = datos["nivel_actual"]
                    self.abrir_ventana_usuario()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "El usuario no existe.")

    def registrar_usuario(self):
        nombre = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()

        if os.path.exists(f"{nombre}.json"):
            messagebox.showerror("Error", "El usuario ya existe.")
        else:
            self.usuario = Usuario(nombre)
            self.usuario.guardar_progreso()
            with open(f"{nombre}.json", "w") as archivo:
                json.dump({"contraseña": contraseña, "xp_actual": 0, "nivel_actual": 1}, archivo)
            messagebox.showinfo("Éxito", "Usuario registrado con éxito.")

    def abrir_ventana_usuario(self):
        self.destroy()  # Cierra la ventana de inicio de sesión
        ventana_usuario = VentanaUsuario(self.usuario)


class VentanaUsuario(tk.Toplevel):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title("Panel del Usuario")
        self.geometry("400x400")

        self.label_nivel = tk.Label(self, text=f"Nivel: {self.usuario.niveles[self.usuario.nivel_actual - 1].nombre}")
        self.label_nivel.pack(pady=10)

        self.label_usuario = tk.Label(self, text=f"Bienvenido, {self.usuario.nombre}!")
        self.label_usuario.pack(pady=5)

        self.label_dificultad = tk.Label(self, text="Dificultad de la tarea:")
        self.label_dificultad.pack(pady=10)

        self.entry_dificultad = tk.Entry(self)
        self.entry_dificultad.pack(pady=5)

        self.boton_agregar_tarea = tk.Button(self, text="Agregar Tarea", command=self.agregar_tarea)
        self.boton_agregar_tarea.pack(pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar Progreso", command=self.guardar_progreso)
        self.boton_guardar.pack(pady=5)

    def agregar_tarea(self):
        dificultad = self.entry_dificultad.get().lower()
        xp_ganado = self.usuario.agregar_tarea(dificultad)

        if xp_ganado > 0:
            messagebox.showinfo("Éxito", f"Tarea {dificultad} completada. Ganaste {xp_ganado} XP!")
            self.label_nivel.config(text=f"Nivel: {self.usuario.niveles[self.usuario.nivel_actual - 1].nombre}")
        else:
            messagebox.showerror("Error", "Dificultad no válida. Usa 'fácil', 'intermedia' o 'difícil'.")

    def guardar_progreso(self):
        self.usuario.guardar_progreso()
        messagebox.showinfo("Éxito", "Progreso guardado con éxito.")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
