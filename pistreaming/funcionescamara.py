#Versión Python 3.5.3
from picamera import PiCamera
import time
import os
from ftplib import FTP
import signal #funcion de ctrl+c
import sys #funcion de ctrl+c
import shutil

#Configuración:
ip_server = "192.168.18.43" #Casa: 192.168.0.19 , Instituto: 172.25.238.32
ruta_dictation = "/home/pi/Documents/dictation.txt" #El fichero lo genera el reconocimiento de voz y por defecto se guarda en descargas
dictation2 = "/home/pi/Documents/dictation2.txt" #Este fichero se utiliza para limpiar el fichero de dictation.txt y tiene que estar en la misam ruta.

# Muestra el día, mes, año y hora acutal
fch_act = time.strftime('%d-%m-%y_%H:%M:%S')


# Iniciar vista previa en forma local, la variable tvp indica el tiempo de ejecucción
def vistaprevia(tvp):
    try:
            camera = PiCamera()
            camera.start_preview()
            os.system('echo "Camara iniciada" | festival --tts')
            time.sleep(tvp)
            camera.stop_preview()
    except:
        os.system('echo "Error funcion vistaprevia" | festival --tts')
        print("Error funcion vistaprevia")

# Iniciar captura de imagen, 'num_img' indica cuanta capturas y 'ruta_img' es la ruta donde se guarda las imagenes ej: /home/pi/image
def captura_imagen(num_img_ci, ruta_img):
    try:
        camera = PiCamera()
        camera.start_preview()
        os.system('echo "Iniciando capturas" | festival --tts')
        # camera.resolution = (2592, 1944)
        for i in range(num_img_ci):
            time.sleep(4)
            camera.capture("{}/image{}-{}.jpg".format(ruta_img, i, fch_act))
        camera.stop_preview()
        os.system('echo "Capturas finalizadas" | festival --tts')
    except:
        os.system('echo "Error funcion captura imagen" | festival --tts')
        print("Error funcion captura imagen")

#Genera un video a partir de las imagenes de un directorio, 'ruta_img' indica la ruta del directorio, ej: /home/pi/image y ruta_destino indica directorio destiono donde lo guarda.
def generar_video(ruta_img, ruta_destino):
    try:
        os.system('ffmpeg -r 3 -i {}/image%01d.jpg -r 30 {}/video_{}.mp4' .format(ruta_img, ruta_destino, fch_act))
    except:
        os.system('echo "Error funcion generar video en funcionescamara.py" | festival --tts')
        print("Error funcion generar video")

# Iniciar grabación de video, la variable 'tgv' indica el tiempo y 'ruta_v' indica la ruta donde se guarda el video ej: /home/pi/video
# Para reproducir video utilizar: omxplayer ruta/video.h264 en la terminal
def grabacion_video(tgv, ruta_v):
    try:
        camera = PiCamera()
        camera.start_preview()
        os.system('echo "Iniciando video" | festival --tts')
        camera.start_recording("{}/video-{}.h264" .format(ruta_v,fch_act))
        time.sleep(tgv)
        camera.stop_recording()
        camera.stop_preview()
        os.system('echo "Video finalizado" | festival --tts')
    except:
        os.system('echo "Error funcion grabacion video" | festival --tts')
        print("Error funcion grabacion video")

#Sube archvio al servidor ftp, 'ruta_fch_local' indica la ruta y archivo local y 'nmbre_fch' indica el nombre que se le va a dar al archivo para guardarlo en el ftp.
def subir_ftp(ruta_fch_local,nombre_fch):
    try:
        ftp = FTP('{}' .format(ip_server),'heimdall', 'raspberry') #Conecta con el servidor
        ftp.cwd('/home/heimdall/Documentos/images') #Cambia directorio raiz en el servidor
        lectura = open(ruta_fch_local, 'rb') #Lee el la ruta y el archivo local
        ftp.storlines('STOR ' + nombre_fch, lectura) #Sube al servidor el archivo local leído.
        ftp.quit() # Cierra la conexión.
    except:
        os.system('echo "Error funcion subir ftp" | festival --tts')
        print("No se ha podido conectar al servidor")

#Transfiere archivos al server-heimdall, 'fch_o' indica ruta y archivo local ej: "/home/pi/Documents/Raul/prueba.txt" y 'fch_d' indica ruta destino en el servidor ej: "/home/heimdall/Escritorio"
#Tiene que isntalar comando "sudo apt-get install sshpass"
def subir_scp(fch_o, fch_d):
    try:
        os.system('sshpass -p "raspberry" scp -r {} heimdall@{}:{}' .format(fch_o, ip_server, fch_d))
    except:
        os.system('echo "Error funcion subir scp" | festival --tts')
        print("Error funcion subir scp")
   
#Borra la entrada del reconocimiento de voz del fichero dictation.txt
def borrado_entrada(buscar):
    try:
        #El comando sed encuentra el páramentero buscar en el fichero, el segundo parámetro indica el que se va a sustituri y el tercer parámetro por el que lo sustituye.
        os.system('sed "/{}/ s/{}//g" {} > {}' .format(buscar, buscar, ruta_dictation, dictation2))
        os.system('rm -r {}' .format(ruta_dictation))
        os.rename('{}' .format(dictation2), '{}' .format(ruta_dictation))
    except:
        print('Error en función borrado entrada')

#Puesta ha cero, reset
def reset_camara():
    try:
        #Borra directorios
        if os.path.exists(ruta_img_antigua):
            shutil.rmtree('{}'.format(ruta_img_antigua))
        if os.path.exists(ruta_dictation):
            shutil.rmtree('{}'.format(ruta_dictation))
        if os.path.exists('/home/pi/Documents/transferencia_video'):
            shutil.rmtree('/home/pi/Documents/transferencia_video')
        if os.path.exists('/home/pi/Documents/transferencia_img'):
            shutil.rmtree('/home/pi/Documents/transferencia_img')
        if os.path.exists('{}' .format(dictation2)):
            shutil.rmtree('{}' .format(dictation2))
    except:
        print('Error en reset')


"""
#####################En prueba
#Para servicio streaming con CTRL+C
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C')
#signal.pause()
"""
