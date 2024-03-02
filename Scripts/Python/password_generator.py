import secrets
import string

LETRAS = string.ascii_letters
DIGITOS = string.digits
PUNTUACION = string.punctuation

def obtener_longitud_contraseña():
    while True:
        try:
            longitud = int(input("Seleccione la longitud de su contraseña: "))
            if longitud <= 0:
                print("La longitud debe ser un número positivo.")
            else:
                return longitud
        except ValueError:
            print("Por favor, ingrese un número válido.")

def crear_contraseña(longitud):
    caracteres = LETRAS + DIGITOS + PUNTUACION
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contraseña

longitud = obtener_longitud_contraseña()
print(crear_contraseña(longitud))
