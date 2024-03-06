import os
import re
import socket
import subprocess

# Instalar las dependencias al inicio del script
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install requests beautifulsoup4")


# Constantes de colores
class Colors:
    BLUE = "\033[94m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

def logo():
    ascii_logo = f"""{Colors.BLUE}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣶⣾⣿⣿⣿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣿⣿⣿⣷⣶⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣠⡴⠾⠟⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠷⢦⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠋⠁⠀⠀⢀⣀⣤⣶⣖⣒⣒⡲⠶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⢖⣒⣒⣲⣶⣤⣀⡀⠀⠀⠈⠙⠂⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⢖⣫⣷⣿⣿⣿⣿⣿⣿⣶⣤⡙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢋⣤⣾⣿⣿⣿⣿⣿⣿⣾⣝⡲⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣄⣀⣠⢿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠻⢿⣿⣿⣦⣳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⣴⣿⣿⡿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⡻⣄⣀⣤⠀⠀⠀
⠀⠀⠀⠈⠟⣿⣿⣿⡿⢻⣿⣿⣿⠃⠀⠀⠀⠀⠙⣿⣿⣿⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⣿⣿⣿⠋⠀⠀⠀⠀⠘⣿⣿⣿⡟⢿⣿⣿⣟⠻⠁⠀⠀⠀
⠤⣤⣶⣶⣿⣿⣿⡟⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡏⠀⠀⠀⠀⠀⠀⣹⣿⣿⣷⠈⢻⣿⣿⣿⣶⣦⣤⠤
⠀⠀⠀⠀⠀⢻⣟⠀⠀⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⣿⣿⠀⠀⣿⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⣆⠀⢹⣿⠟⢿⣿⣦⣤⣤⣴⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡿⢷⣤⣤⣤⣴⣿⣿⣿⣿⡇⠀⣰⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠂⠀⠙⢀⣀⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠁⠀⣻⣿⣿⣿⣿⣿⣿⠏⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡈⠻⠿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⢿⣿⣿⣿⠿⠛⢁⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠛⣶⣦⣤⣤⣤⡤⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢤⣤⣤⣤⣶⣾⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    {Colors.RESET}{Colors.GREEN}
    \t▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    \t█{Colors.GREEN}[+] Author: firodrigz{Colors.RESET}                  {Colors.GREEN}█{Colors.GREEN}
    \t█{Colors.GREEN}[+] Follow me on Github: firodrigz{Colors.RESET}     {Colors.GREEN}█{Colors.GREEN}
    \t█{Colors.GREEN}[+] Version: 1.1{Colors.RESET}                       {Colors.GREEN}█{Colors.GREEN}
    \t█{Colors.GREEN}[+] Date: 06-03-2024{Colors.RESET}                   {Colors.GREEN}█{Colors.GREEN}
    \t▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """
    print(ascii_logo)


def subdominios(lista, destino):
    total_subdominios = len(lista)
    existente = []

    for elemento in lista:
        subdominio = f"{elemento}.{destino}"  
            
        url = f"http://{subdominio}"
        try:
            respuesta = requests.get(url, timeout=2)
            
            if respuesta.status_code == 200:
                print(f"El subdominio {subdominio} está alcanzable (código de respuesta 200).")
                existente.append(subdominio)


        except requests.RequestException as e:
            pass

    return existente


def encuentra_ip(subdominios_existentes):
    for elemento in subdominios_existentes:
        direccion_ip = socket.gethostbyname(elemento)
        print(f"La dirección IP del subdominio {elemento} es: {direccion_ip}")


def scraping(dominio):
    try:
        response = requests.get(dominio)
        imprimir=response.raise_for_status() # Lanza una excepción para códigos de error HTTP
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error al analizar el HTML: {e}")
        return

    
    # Configuración para extraer diferentes tipos de datos
    datos_a_extraer = [
        {'tipo': 'enlaces', 'etiqueta': 'a', 'atributo': 'href'},
        {'tipo': 'titulos', 'etiqueta': 'h2'},
        {'tipo': 'correos', 'patron': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'},
        {'tipo': 'telefonos', 'patron': r'\b(?:\+\d{1,2}\s?)?(?:\(\d{1,4}\)|\d{1,4})[-.\s]?\d{1,12}\b'},
        {'tipo': 'direcciones', 'etiqueta': 'address'},
        {'tipo': 'posible versión WordPress', 'etiqueta': 'meta', 'atributo': 'content', 'atributo_name': 'generator'},
        {'tipo': 'imágenes', 'etiqueta': 'img', 'atributo': 'src'},
        {'tipo': 'última fecha modificación', 'etiqueta': 'meta', 'atributo': None, 'atributo_name': 'last-modified'}
    ]

    resultados = {}

    for config in datos_a_extraer:
        tipo = config.get('tipo')
        etiqueta = config.get('etiqueta')
        atributo = config.get('atributo', None)
        atributo_name = config.get('atributo_name', None)
        patron = config.get('patron', None)

        if etiqueta:
            if atributo_name == 'generator':
                elementos = soup.find_all(etiqueta, {'name': atributo_name})
            elif atributo_name == 'last-modified':
                # Modificación para manejar la etiqueta meta con el atributo last-modified
                elementos = soup.find_all('meta', {'http-equiv': 'last-modified'})
            else:
                elementos = soup.find_all(etiqueta)

            if atributo:
                datos = [elemento.get(atributo) for elemento in elementos]
            else:
                datos = [elemento.text.strip() for elemento in elementos]

        elif atributo_name:
            # Búsqueda de meta con atributo_name
            elementos = soup.find_all('meta', {'name': atributo_name})
            datos = [elemento.get('content') for elemento in elementos]

        elif patron:
            # Búsqueda usando expresiones regulares
            texto_completo = soup.get_text()
            datos = re.findall(patron, texto_completo)
        
        resultados[tipo] = datos


        # Filtrar números de teléfono con 4 dígitos o menos
        if 'telefonos' in resultados:
            resultados['telefonos'] = [telefono for telefono in resultados['telefonos'] if len(re.sub(r'\D', '', telefono)) > 4]


    # Imprimir resultados dentro de la función
    for tipo, datos in resultados.items():
        print(f"{tipo}: {datos}")
    

def consulta_whatweb(dominio):
    try:
        # Ejecutar el comando WhatWeb y capturar la salida
        resultado = subprocess.check_output(['whatweb', dominio], text=True)
        return resultado
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar WhatWeb: {e}")
        return None


def cargar_lista_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='latin-1') as archivo:
            return [linea.strip() for linea in archivo.readlines()]
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return []


def obtener_ruta_archivo():
    while True:
        ruta_archivo = input(f"{Colors.BLUE}[+] {Colors.RESET}Ingrese la ruta del diccionario para realizar fuzzing: ")
        if os.path.isfile(ruta_archivo):
            return ruta_archivo
        else:
            print(f"{Colors.RED}[!] {Colors.RESET}¡Archivo no encontrado! Intente nuevamente.")


def menu():

    while True:
        print(f"{Colors.BLUE}\nHelp menu..."+ Colors.RESET)
        print(f"{Colors.BLUE}[+] 1.{Colors.RESET} SUBDOMAIN FUZZING")
        print(f"{Colors.BLUE}[+] 2.{Colors.RESET} SCRAPING")
        print(f"{Colors.BLUE}[+] 3.{Colors.RESET} WHATWEB")
        
        print(f"{Colors.BLUE}[+] 0.{Colors.RESET} EXIT")
        try:
            value = input("\n> ")
            
            if value == "1":                
                dominio_principal = input(f"{Colors.BLUE}[+] {Colors.RESET}Ingrese dominio: ")
                archivo_palabras = obtener_ruta_archivo()
                mi_lista = cargar_lista_desde_archivo(archivo_palabras)
                subdominios_existentes = subdominios(mi_lista, dominio_principal)
                if len(subdominios_existentes) > 0:
                    confirm = input(f"{Colors.BLUE}\n[+] {Colors.RESET}Desea continuar y encontrar las IP? Y/n (presione Enter para seleccionar Y): ") or "Y"
                    if confirm.lower() == "y" or confirm.lower() == "yes":
                        encuentra_ip(subdominios_existentes)
                else:
                    print(f"{Colors.RED}[!] {Colors.RESET}No se encontraron subdominios.")
                            
            elif value == "2":
                dominio = input(f"{Colors.BLUE}[+] {Colors.RESET}Ingrese dominio: ")
                scraping(dominio)

            elif value == "3":
                dominio = input(f"{Colors.BLUE}[+] {Colors.RESET}Ingrese dominio: ")
                resultado_whatweb = consulta_whatweb(dominio)

                if resultado_whatweb is not None:
                    print(f"Resultado de WhatWeb para {dominio}:\n{resultado_whatweb}")
                else:
                    print("No se pudo obtener el resultado de WhatWeb.")

            elif value == "0":
                break
        
        except KeyboardInterrupt:
            print("\nTerminando el programa...")
            break

if __name__ == "__main__":
    logo()
    menu()