#Versión Python 3.5.3
from funcionescamara import subir_scp
import os
import shutil

#Transfiere archivos al server-heimdall, 'fch_o' indica ruta y archivo local ej: "/home/pi/Documents/Raul/prueba.txt" y 'fch_d' indica ruta destino en el servidor ej: "/home/heimdall/Escritorio"
try:
    subir_scp("/home/pi/Documents/transferencia_img", "/home/heimdall/Documentos")
    if os.path.exists('/home/pi/Documents/transferencia_img'):
        shutil.rmtree('/home/pi/Documents/transferencia_img')
except:
    print("Error en transferencia del directorio transferencia_img")