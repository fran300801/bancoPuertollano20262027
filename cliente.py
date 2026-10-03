from models import Cliente
from logs import Log

log = Log()

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

def getSaldoTotal(self):
    return self.cuenta.getSaldo() + self.deposito.getSaldo()

def guardar(self):
    if not os.path.exists("datosClientes"):
        os.mkdir("datosClientes")

    with open(f"datosClientes/{self.numero}.txt", "w") as f:
        f.write(f"{self.numero}\n")
        f.write(f"{self.cuenta.getSaldo()}\n")
        f.write(f"{self.deposito.getSaldo()}\n")

def cargarClienteGuardado(numCliente):

    try:
        with open(f"datosClientes/{numCliente}.txt", "r") as f:

            numero = f.readline().strip()
            saldoCuenta = float(f.readline().strip())
            saldoDeposito = float(f.readline().strip())

            cliente = Cliente(numero)

            cliente.cuenta.saldo = saldoCuenta
            cliente.deposito.saldo = saldoDeposito

            return cliente

    except FileNotFoundError:
        log.escribir("ERROR", f"Intento de consulta de cliente no cargado: {numCliente}")
        print("Primero tienes que cargar los datos de este cliente")
        return None