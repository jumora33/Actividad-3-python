import math
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox, ttk



class FiguraGeometrica(ABC):
    """Clase base: toda figura sabe calcular su volumen y su superficie."""

    nombre = "Figura"
    parametros = []  

    @abstractmethod
    def volumen(self):
        pass

    @abstractmethod
    def superficie(self):
        pass


class Cilindro(FiguraGeometrica):
    nombre = "Cilindro"
    parametros = ["Radio (cm)", "Altura (cm)"]

    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def volumen(self):
        return math.pi * self.radio ** 2 * self.altura

    def superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)


class Esfera(FiguraGeometrica):
    nombre = "Esfera"
    parametros = ["Radio (cm)"]

    def __init__(self, radio):
        self.radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self.radio ** 3

    def superficie(self):
        return 4 * math.pi * self.radio ** 2


class Piramide(FiguraGeometrica):
    """Pirámide de base cuadrada."""
    nombre = "Pirámide"
    parametros = ["Base (cm)", "Altura (cm)", "Apotema (cm)"]

    def __init__(self, base, altura, apotema):
        self.base = base
        self.altura = altura
        self.apotema = apotema

    def volumen(self):
        return self.base ** 2 * self.altura / 3

    def superficie(self):
        return self.base ** 2 + 2 * self.base * self.apotema


class Cubo(FiguraGeometrica):
    nombre = "Cubo"
    parametros = ["Arista (cm)"]

    def __init__(self, arista):
        self.arista = arista

    def volumen(self):
        return self.arista ** 3

    def superficie(self):
        return 6 * self.arista ** 2


class Prisma(FiguraGeometrica):
    """Prisma rectangular."""
    nombre = "Prisma"
    parametros = ["Largo (cm)", "Ancho (cm)", "Altura (cm)"]

    def __init__(self, largo, ancho, altura):
        self.largo = largo
        self.ancho = ancho
        self.altura = altura

    def volumen(self):
        return self.largo * self.ancho * self.altura

    def superficie(self):
        return 2 * (self.largo * self.ancho
                    + self.largo * self.altura
                    + self.ancho * self.altura)



class VentanaFiguras(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Volumen y superficie de figuras geométricas")
        self.resizable(False, False)

        self.figuras = {
            "Cilindro": Cilindro,
            "Esfera": Esfera,
            "Pirámide": Piramide,
            "Cubo": Cubo,
            "Prisma": Prisma,
        }
        self.dibujos = {
            "Cilindro": self.dibujar_cilindro,
            "Esfera": self.dibujar_esfera,
            "Pirámide": self.dibujar_piramide,
            "Cubo": self.dibujar_cubo,
            "Prisma": self.dibujar_prisma,
        }
        self.campos = []

        self.crear_componentes()
        self.cambiar_figura()

    def crear_componentes(self):
       
        marco_figura = tk.Frame(self)
        marco_figura.pack(padx=15, pady=(12, 5), fill="x")
        tk.Label(marco_figura, text="Figura:").pack(side="left")
        self.combo_figuras = ttk.Combobox(marco_figura, values=list(self.figuras),
                                          state="readonly", width=16)
        self.combo_figuras.current(0)
        self.combo_figuras.pack(side="left", padx=8)
      
        self.combo_figuras.bind("<<ComboboxSelected>>", self.cambiar_figura)

       
        marco_medio = tk.Frame(self)
        marco_medio.pack(padx=15, pady=5)
        self.lienzo = tk.Canvas(marco_medio, width=220, height=180,
                                bg="white", highlightthickness=1,
                                highlightbackground="#999")
        self.lienzo.grid(row=0, column=0, padx=(0, 15))

        self.marco_datos = tk.LabelFrame(marco_medio, text="Datos (en centímetros)",
                                         padx=10, pady=10)
        self.marco_datos.grid(row=0, column=1, sticky="n")

        
        marco_botones = tk.Frame(self)
        marco_botones.pack(pady=5)
       
        tk.Button(marco_botones, text="Calcular", width=12,
                  command=self.calcular).grid(row=0, column=0, padx=5)
        tk.Button(marco_botones, text="Limpiar", width=12,
                  command=self.limpiar).grid(row=0, column=1, padx=5)

       
        marco_res = tk.LabelFrame(self, text="Resultados", padx=10, pady=10)
        marco_res.pack(padx=15, pady=(5, 12), fill="x")
        self.lbl_volumen = tk.Label(marco_res, text="Volumen: ")
        self.lbl_superficie = tk.Label(marco_res, text="Superficie: ")
        self.lbl_volumen.pack(anchor="w")
        self.lbl_superficie.pack(anchor="w")

   
    def cambiar_figura(self, evento=None):
        """Reconstruye los campos de datos y la imagen según la figura elegida."""
        nombre = self.combo_figuras.get()
        clase = self.figuras[nombre]

        for widget in self.marco_datos.winfo_children():
            widget.destroy()
        self.campos = []

        for i, etiqueta in enumerate(clase.parametros):
            tk.Label(self.marco_datos, text=etiqueta + ":").grid(
                row=i, column=0, sticky="e", pady=3)
            campo = tk.Entry(self.marco_datos, width=10)
            campo.grid(row=i, column=1, padx=8, pady=3)
      
            campo.bind("<Return>", self.calcular)
            self.campos.append(campo)

        self.campos[0].focus_set()
        self.dibujar_figura(nombre)
        self.limpiar_resultados()

    def mostrar_alerta(self, mensaje, campo):
        messagebox.showwarning("Alerta", mensaje)
        campo.focus_set()
        campo.select_range(0, tk.END)

    def leer_datos(self):
        """Lee y valida los datos. Devuelve la lista o None si hay error."""
        clase = self.figuras[self.combo_figuras.get()]
        valores = []
        for etiqueta, campo in zip(clase.parametros, self.campos):
            texto = campo.get().replace(",", ".").strip()
            nombre_dato = etiqueta.split(" (")[0]

            if texto == "":
                self.mostrar_alerta(f"El dato '{nombre_dato}' no ha sido ingresado.", campo)
                return None
            try:
                valor = float(texto)
            except ValueError:
                self.mostrar_alerta(
                    f"El dato '{nombre_dato}' no es numérico: '{texto}'.", campo)
                return None
            if not math.isfinite(valor):
                self.mostrar_alerta(
                    f"El dato '{nombre_dato}' no es numérico: '{texto}'.", campo)
                return None
            if valor <= 0:
                self.mostrar_alerta(
                    f"El dato '{nombre_dato}' debe ser mayor que cero.", campo)
                return None
            valores.append(valor)
        return valores

    def calcular(self, evento=None):
        valores = self.leer_datos()
        if valores is None:
            return

        figura = self.figuras[self.combo_figuras.get()](*valores)
        self.lbl_volumen.config(text=f"Volumen: {figura.volumen():.2f} cm³")
        self.lbl_superficie.config(text=f"Superficie: {figura.superficie():.2f} cm²")

    def limpiar_resultados(self):
        self.lbl_volumen.config(text="Volumen: ")
        self.lbl_superficie.config(text="Superficie: ")

    def limpiar(self):
        for campo in self.campos:
            campo.delete(0, tk.END)
        self.limpiar_resultados()
        self.campos[0].focus_set()


    def dibujar_figura(self, nombre):
        self.lienzo.delete("all")
        self.dibujos[nombre]()
        self.lienzo.create_text(110, 168, text=nombre, font=("Arial", 11, "bold"))

    def _caja(self, x, y, ancho, alto, dx, dy):
        """Dibuja una caja en perspectiva (sirve para el cubo y el prisma)."""
        c = self.lienzo
        c.create_polygon(x, y, x + dx, y - dy, x + dx + ancho, y - dy, x + ancho, y,
                         fill="#cfe3f5", outline="#333", width=2)        
        c.create_polygon(x + ancho, y, x + dx + ancho, y - dy,
                         x + dx + ancho, y - dy + alto, x + ancho, y + alto,
                         fill="#8fb8de", outline="#333", width=2)         
        c.create_rectangle(x, y, x + ancho, y + alto,
                           fill="#b4d0ec", outline="#333", width=2)        

    def dibujar_cubo(self):
        self._caja(45, 70, 80, 80, 40, 40)

    def dibujar_prisma(self):
        self._caja(30, 75, 110, 70, 55, 40)

    def dibujar_cilindro(self):
        c = self.lienzo
        c.create_oval(60, 120, 160, 150, fill="#b4d0ec", outline="#333", width=2)
        c.create_rectangle(60, 40, 160, 135, fill="#b4d0ec", outline="")
        c.create_line(60, 40, 60, 135, width=2)
        c.create_line(160, 40, 160, 135, width=2)
        c.create_oval(60, 25, 160, 55, fill="#cfe3f5", outline="#333", width=2)

    def dibujar_esfera(self):
        c = self.lienzo
        c.create_oval(45, 15, 175, 145, fill="#b4d0ec", outline="#333", width=2)
        c.create_oval(45, 65, 175, 95, outline="#333", dash=(4, 3))
        c.create_line(110, 80, 175, 80, width=2, fill="#c0392b")
        c.create_text(143, 72, text="r", fill="#c0392b")

    def dibujar_piramide(self):
        c = self.lienzo
        cima = (118, 20)
        a, b, cc, d = (55, 135), (150, 135), (190, 108), (95, 108)
        c.create_line(*cima, *d, dash=(4, 3))
        c.create_line(*d, *a, dash=(4, 3))
        c.create_line(*d, *cc, dash=(4, 3))
        c.create_polygon(*cima, *b, *cc, fill="#8fb8de", outline="#333", width=2)
        c.create_polygon(*cima, *a, *b, fill="#b4d0ec", outline="#333", width=2)


if __name__ == "__main__":
    ventana = VentanaFiguras()
    ventana.mainloop()
