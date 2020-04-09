#Versión Python 3.5.3
from funcionescamara import subir_scp
import os
import time
import shutil

# Muestra el día, mes, año y hora acutal
fch_act = time.strftime('%d-%m-%y_%H:%M:%S')

#Transfiere archivos al server-heimdall, 'fch_o' indica ruta y archivo local ej: "/home/pi/Documents/Raul/prueba.txt" y 'fch_d' indica ruta destino en el servidor ej: "/home/heimdall/Escritorio"
try:
    subir_scp("/home/pi/Documents/transferencia_video", "/home/heimdall/Documentos/video_grabado_{}" .format(fch_act))
    if os.path.exists('/home/pi/Documents/transferencia_video'):
        shutil.rmtree('/home/pi/Documents/transferencia_video')
except:
    print("Error en transferencia del directorio transferencia_video")