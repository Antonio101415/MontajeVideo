#Versión Python 3.5.3
from funcionescamara import *
from os import listdir
import time
import os
import os.path
import shutil

# Muestra el día, mes, año y hora acutal
fch_act = time.strftime('%d-%m-%y_%H:%M:%S')

try:
    #Comprueba que exista la carpeta transferencia_img para crear el video.
    while True:
        #Leer el directorio Documentos que es donde se crea el directorio transferencia_img.
        for fichero in os.listdir("/home/pi/Documents"):
            if fichero == "transferencia_img":
                #Genera un video a partir de las imagenes de un directorio, 'ruta_img' indica la ruta del directorio, ej: /home/pi/image y ruta_destino indica directorio destiono donde lo guarda.
                generar_video("/home/pi/Documents/transferencia_img", "/home/heimdall/Documentos/video")
                #Borra la carpeta transferencia_img cunado termina que generar el video
                shutil.rmtree('/home/pi/Documents/transferencia_img')
except:
    print('Error en genera el video en generar_video.py')
