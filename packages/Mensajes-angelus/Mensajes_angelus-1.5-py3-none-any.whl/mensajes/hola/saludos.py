import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una actualización de la version")

def generar_array(numeros):
    return np.arange(numeros)

#print(__name__)

class Saludo:
    def __init__(self):
        print("Saludos desde __init__")

if __name__ == '__main__':
    print(generar_array(5))

