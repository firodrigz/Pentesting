#!/usr/bin/env python3
# pip install pytube termcolor

from pytube import YouTube
from termcolor import colored
import os
import signal
import sys

def def_handler(sig, frame):
    print(colored(f"\n\n[!] Saliendo...\n", 'red'))
    sys.exit(1)

# Ctrl+C   
signal.signal(signal.SIGINT, def_handler)

def descargar_video(link, opcion):
    try:        
        yt = YouTube(link)

        if opcion == 2:  # Descargar solo el audio
            # Obtener la mejor calidad de audio disponible
            audio_stream = yt.streams.get_audio_only()
            # Ruta de salida para el directorio actual
            output_path = os.path.join(os.getcwd(), "Descargas_Audio")
            print(colored("[+] Descargando solo el audio...", 'blue'))
            print(colored(f'[*] Descargando: {yt.title}', 'yellow'))
            audio_file = audio_stream.download(output_path=output_path, filename='audio.mp3')
            print(colored('[+] Descarga completada', 'green'))
            print(colored(f"[+] Ruta de descarga: {output_path}", "green"))
        else:  # Descargar el video con audio
            # Obtener la mejor calidad de video y audio disponible
            video_audio_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
            # Ruta de salida para el directorio actual
            output_path = os.path.join(os.getcwd(), "Descargas_Video")
            print(colored("[+] Descargando video con audio...", 'blue'))
            print(colored(f'[*] Descargando: {yt.title}', 'yellow'))
            video_audio_file = video_audio_stream.download(output_path=output_path, filename='video.mp4')
            print(colored('[+] Descarga completada', 'green'))
            print(colored(f"[+] Ruta de descarga: {output_path}", "green"))
    except Exception as e:
        print(colored("[+] Error al descargar el video:", 'red'), e)

if __name__ == '__main__':
    print(colored("\n[+] YouTube video Downloader\n", 'cyan'))

    link = input(colored("\n[+] Ingrese el enlace del video de YouTube: ", 'green'))

    print(colored("Seleccione una opción:", 'yellow'))
    print("1. Descargar video con audio")
    print("2. Descargar solo el audio")

    opcion = int(input(colored("\n[+] Ingrese el número de la opción deseada: ", 'green')))
    
    descargar_video(link, opcion)