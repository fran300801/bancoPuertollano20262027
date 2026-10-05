import os

from models import Cliente, Deposito, CuentaBancaria
from logs import Log

log = Log()


def __init__(self, numCliente):
    self.numCliente = numCliente
    self.cuenta = CuentaBancaria()
    self.deposito = Deposito()


    def getSaldoTotal(self):
        return self.cuenta.saldo + self.deposito.saldo

def cargarCliente(tipo):
    while True:
        num = input("Introduce el número de cliente: ")

        if len(num) != 6 or not num.isdigit():
            print("El formato introducido no es correcto")
            continue

        if tipo == "movimientos":
            return leerFichero(num)

        elif tipo == "guardado":
            return cargarClienteGuardado(num)


def leerFichero(numCliente):
    log.escribir("INFO", f"INICIO CARGA DE CLIENTE: {numCliente}")

    cliente = Cliente(numCliente)
    contador = 0

    try:
        with open(f"ficherosClientes/{numCliente}.txt", "r") as f:

            numLinea = 0
            linea = f.readline()

            while linea:
                numLinea += 1

                if linea.strip() == "":
                    linea = f.readline()
                    continue
                try:
                    datos = linea.strip().split(";")

                    cantidad = float(datos[0])
                    operacion = datos[1]
                    destino = datos[2]

                    if destino == "Cuenta" and operacion == "Ingreso":
                        cliente.cuenta.ingresar(cantidad)
                        contador +=1
                    elif destino == "Cuenta" and operacion == "Retirada":
                        cliente.cuenta.retirar(cantidad)
                        contador +=1
                    elif destino == "Deposito" and operacion == "Ingreso":
                        cliente.deposito.ingresar(cantidad)
                        contador +=1
                    elif destino == "Deposito" and operacion == "Retirada":
                        cliente.deposito.retirar(cantidad)
                        contador +=1
                    else:
                        log.escribir("Warning", f"Movimiento no se realizara")
                except (ValueError, IndexError):
                    log.escribir("ERROR",f"MOVIMIENTO NO VÁLIDO IGNORADO (cliente {numCliente}, "f"línea {numLinea}): '{linea.strip()}'")

                linea = f.readline()

        # Guardamos el estado final del cliente
        cliente.guardar()


        log.escribir("INFO", f"CLIENTE CARGADO CORRECTAMENTE: {numCliente}")
        mensaje= f"Movimientos procesados: {contador}"
        print(mensaje)
        log.escribir("INFO",mensaje)

        print("Datos del cliente cargados correctamente")

        print(f"Cliente: {cliente.getNumero()}")
        print(f"Saldo cuenta: {cliente.getCuenta().getSaldo()} €")
        print(f"Saldo depósito: {cliente.getDeposito().getSaldo()} €")
        print(f"Saldo total: {cliente.getSaldoTotal()} €")
        return cliente

    except FileNotFoundError:
        log.escribir("ERROR",f"FICHERO DE MOVIMIENTOS INEXISTENTE PARA EL CLIENTE: {numCliente}")
        print("El usuario no tiene ninguna cuenta con el banco")
        return None





def cargarClienteGuardado(numCliente):

    try:
        with open(f"datosClientes/{numCliente}.txt", "r") as f:

            numero = f.readline().strip()
            datos = numero.split(";")

            cliente = Cliente(datos[0])

            cliente.cuenta.saldo = float(datos[1])
            cliente.deposito.saldo = float(datos[2])
            print(f"Saldo cuenta: {cliente.cuenta.saldo} €")
            print(f"Saldo depósito: {cliente.deposito.saldo} €")
            print(f"Saldo total: {cliente.getSaldoTotal()} €")

            return cliente

    except FileNotFoundError:
        log.escribir("ERROR", f"Intento de consulta de cliente no cargado: {numCliente}")
        print("Primero tienes que cargar los datos de este cliente")
        return None