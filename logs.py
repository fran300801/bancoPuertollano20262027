from datetime import datetime
import os


class Log:

    TIPOS_VALIDOS = ("INFO", "WARNING", "ERROR")

    def __init__(self):
        fecha = datetime.now().strftime("%Y%m%d")
        self.ruta = f"log/{fecha}-banco.log"

        if not os.path.exists("log"):
            os.mkdir("log")

    def escribir(self, tipo, mensaje):

        tipo = str(tipo).strip().upper()

        if tipo not in self.TIPOS_VALIDOS:
            tipo = "INFO"

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.ruta, "a") as fichero:
            fichero.write(f"[{fecha_hora}] [{tipo.upper()}] {mensaje}\n")
