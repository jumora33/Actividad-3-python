import math
import tkinter as tk
from tkinter import messagebox

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0
CANTIDAD_NOTAS = 5


class CalculadoraNotas:
    """Guarda las notas y calcula los datos estadísticos."""

    def __init__(self, notas):
        self.notas = notas

    def promedio(self):
        return sum(self.notas) / len(self.notas)

    def desviacion_estandar(self):
        prom = self.promedio()
        suma = 0
        for nota in self.notas:
            suma += (nota - prom) ** 2
        return math.sqrt(suma / len(self.notas))

    def mayor(self):
        return max(self.notas)

    def menor(self):
        return min(self.notas)


class VentanaNotas(tk.Tk):
    """Ventana principal con la interfaz gráfica."""

    def __init__(self):
        super().__init__()
        self.title("Notas de un estudiante")
        self.resizable(False, False)

        self.campos_notas = []
        self.crear_componentes()

    def crear_componentes(self):
  
        marco_notas = tk.LabelFrame(self, text="Ingrese las cinco notas", padx=10, pady=10)
        marco_notas.pack(padx=15, pady=10, fill="x")

        for i in range(CANTIDAD_NOTAS):
            etiqueta = tk.Label(marco_notas, text=f"Nota {i + 1}:")
            etiqueta.grid(row=i, column=0, sticky="e", pady=3)
            campo = tk.Entry(marco_notas, width=12)
            campo.grid(row=i, column=1, padx=10, pady=3)
            self.campos_notas.append(campo)

    
        marco_botones = tk.Frame(self)
        marco_botones.pack(pady=5)
        tk.Button(marco_botones, text="Calcular", width=12,
                  command=self.calcular).grid(row=0, column=0, padx=5)
        tk.Button(marco_botones, text="Limpiar", width=12,
                  command=self.limpiar).grid(row=0, column=1, padx=5)

     
        marco_resultados = tk.LabelFrame(self, text="Resultados", padx=10, pady=10)
        marco_resultados.pack(padx=15, pady=10, fill="x")

        self.lbl_promedio = tk.Label(marco_resultados, text="Promedio: ")
        self.lbl_desviacion = tk.Label(marco_resultados, text="Desviación estándar: ")
        self.lbl_mayor = tk.Label(marco_resultados, text="Mayor nota: ")
        self.lbl_menor = tk.Label(marco_resultados, text="Menor nota: ")

        for etiqueta in (self.lbl_promedio, self.lbl_desviacion,
                         self.lbl_mayor, self.lbl_menor):
            etiqueta.pack(anchor="w")

    def mostrar_alerta(self, mensaje, campo):
        """Muestra un mensaje de alerta y deja el cursor en el campo con error."""
        messagebox.showwarning("Alerta", mensaje)
        campo.focus_set()
        campo.select_range(0, tk.END)

    def leer_notas(self):
        """Lee y valida las notas. Devuelve la lista o None si hay error."""
        notas = []
        for i, campo in enumerate(self.campos_notas):
            texto = campo.get().replace(",", ".").strip()

    
            if texto == "":
                self.mostrar_alerta(f"La nota {i + 1} no ha sido ingresada.", campo)
                return None

        
            try:
                nota = float(texto)
            except ValueError:
                self.mostrar_alerta(
                    f"El dato de la nota {i + 1} no es numérico: '{texto}'.", campo)
                return None

        
            if not math.isfinite(nota):
                self.mostrar_alerta(
                    f"El dato de la nota {i + 1} no es numérico: '{texto}'.", campo)
                return None

            if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
                self.mostrar_alerta(
                    f"La nota {i + 1} debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}.",
                    campo)
                return None

            notas.append(nota)
        return notas

    def calcular(self):
        notas = self.leer_notas()
        if notas is None:
            return

        calculadora = CalculadoraNotas(notas)
        self.lbl_promedio.config(text=f"Promedio: {calculadora.promedio():.2f}")
        self.lbl_desviacion.config(
            text=f"Desviación estándar: {calculadora.desviacion_estandar():.2f}")
        self.lbl_mayor.config(text=f"Mayor nota: {calculadora.mayor():.1f}")
        self.lbl_menor.config(text=f"Menor nota: {calculadora.menor():.1f}")

    def limpiar(self):
        for campo in self.campos_notas:
            campo.delete(0, tk.END)
        self.lbl_promedio.config(text="Promedio: ")
        self.lbl_desviacion.config(text="Desviación estándar: ")
        self.lbl_mayor.config(text="Mayor nota: ")
        self.lbl_menor.config(text="Menor nota: ")


if __name__ == "__main__":
    ventana = VentanaNotas()
    ventana.mainloop()
