#!/usr/bin/env python

#Versión Python 3.5.3
from picamera import PiCamera
from funcionescamara import *
from server import *
import time
import os
from ftplib import FTP
import os.path
import shutil


#Configuración
ip_server = "192.168.18.43" #Casa: 192.168.0.19 , Instituto: 172.25.238.32
ruta_streaming = "/home/pi/Documents/pistreaming/server.py"
ruta_dictation = "/home/pi/Documents/dictation.txt" #El archivo lo genera el reconocimiento de voz y por defecto se guarda en descargas
    #Ruta del fichero de dictation.txt generado por reconocimiento de voz, no cambiar, lo crea si no existe
ruta_d = "/home/heimdall/Documentos"
    #Ruta de alojamiento en el servidor, no cambiar
ruta_img = "/home/pi/Documents/modulo_img"
    #Crea el directorio si no existe de modulo_img

# Muestar el día, mes, año y hora acutal
fecha_act = time.strftime('%d-%m-%y_%H:%M:%S')

#Reproduce mensaje por altavoz
os.system('echo "Iniciando modulo imagen" | festival --tts')

try:
    if not os.path.exists(ruta_dictation):
        os.system('touch {}' .format(ruta_dictation))
except:
    print('Error en crear dictation.txt')

try:
    if not os.path.exists(ruta_img):
        os.system('mkdir {}' .format(ruta_img))
        
    else:
        #Coprueba que el direcotrio no este vacio.
        if not os.stat("{}" .format(ruta_img)).st_size == 0:
            ruta_img_antigua = "/home/pi/Documents/modulo_img_antigua"
            #Renombra el directorio que existe por modulo_img_antigua
            os.rename("{}".format(ruta_img),"{}".format(ruta_img_antigua)) #Renombra un archivo o carpeta.
            #Vuelve a crear el directorio vacio
            os.system('mkdir {}' .format(ruta_img))
            
            #Suber los datos antiguo al servidor.
            try:
                #Transfiere el directorio antiguo al servidor
                os.system('sshpass -p "raspberry" scp -r {} heimdall@{}:{}/{}' .format(ruta_img_antigua, ip_server, ruta_d, fecha_act))
            except:
                print("Error en transferencia directorio antiguo.")
            #Elimina el directorio ruta_img_antigua
            shutil.rmtree('{}'.format(ruta_img_antigua))
        
except:
    print("Error al crear directorio {}" .format(ruta_img))

try:
    camera = PiCamera()
    camera.start_preview()
    #camera.resolution = (2592, 1944)
    
    #Crea un bucle creando captura de imagen
    contador = 0
    while True:
        time.sleep(4)
        nombre_img = "{}/image{}.jpg".format(ruta_img, contador)
        camera.capture("{}".format(nombre_img))
        contador += 1
        
        #Inicia transferencia cada 100 imagenes al servidor
        try:
            if contador == 10:
                #Transfier la carpeta modulo_img al servidor
                transferencia_img = "/home/pi/Documents/transferencia_img"
                #Renombra directorio modulo_img con nombre transferencia para enviar al servidor
                os.rename("{}" .format(ruta_img),"{}" .format(transferencia_img))
                os.system('rm -r {}' .format(ruta_img))
                #Vuelve a crear el directorio modulo_img
                os.system('mkdir {}' .format(ruta_img))
                #Llama fichero python transferencia_img.py para que se produzca la transferencia al servidor
                os.system('python3 transferencia_img.py')
                contador = 0
        except:
            print("Error en renombrar directorio modulo_img y llamada a transferencia")
        
        #Inicia la grabación del video con la frase "Python grabar vídeo"
        lectura = open('{}' .format(ruta_dictation))
        if 'Python grabar vídeo' in lectura.read():
            lectura.close()
            #Comprueba que el directorio transferencia_video exista
            if not os.path.exists("/home/pi/Documents/transferencia_video"):
                #Crea el directorio transferencia_video
                os.system('mkdir /home/pi/Documents/transferencia_video')
    
            #La variable tgb indica el tiempo de grabación de video y ruta_v la ruta donde se guarda.
            tgv = 4
            ruta_v = "/home/pi/Documents/transferencia_video"
            #Inicia la cámara, la vista previa, lanza festival por voz.
            os.system('echo "Iniciando video" | festival --tts')
            try:
                #Transfier la carpeta modulo_img al servidor
                transferencia_img = "/home/pi/Documents/transferencia_img"
                #Renombra directorio modulo_img con nombre transferencia para enviar al servidor
                os.rename("{}" .format(ruta_img),"{}" .format(transferencia_img))
                os.system('rm -r {}' .format(ruta_img))
                #Vuelve a crear el directorio modulo_img
                os.system('mkdir {}' .format(ruta_img))
                #Llama fichero python transferencia_img.py para que se produzca la transferencia al servidor
                os.system('python3 transferencia_img.py')
                
                #Empieza a grabar.
                camera.start_recording("{}/video-{}.h264" .format(ruta_v,fch_act))
                #camera.wait_recording(30)
                
                #time.sleep(tgv)
                #Para la grabación
                while True:
                    #Lee el fichero si encuentra "Python para grabación"
                    lectura = open('{}' .format(ruta_dictation))
                    if 'Python para grabación' in lectura.read():
                        lectura.close()
                        camera.stop_recording()
                        camera.stop_preview()
                        camera.close()
                        camera = PiCamera()
                        camera.start_preview()
                        os.system('echo "Video finalizado" | festival --tts')
                        
                        #Borra la entrada del reconocimiento de voz del fichero dictation.txt
                        borrado_entrada("Python grabar vídeo")
                        borrado_entrada("Python para grabación")
                        #Llama fichero python transferencia_video.py para que se produzca la transferencia al servidor
                        os.system('python3 transferencia_video.py')
                        #Inicia la prevista porque la función grabar_video la deja cerrada.
                        #camera.start_preview()
                        break
                   
            except:
                os.system('echo "Error funcion grabacion video" | festival --tts')
                print("Error funcion grabacion video")
    


        #Inicia servicio streaming con la frase "Python inicia streaming"
        lectura = open('{}' .format(ruta_dictation))
        if 'Python inicia streaming' in lectura.read():
            lectura.close()
            try:
                #Transfier la carpeta modulo_img al servidor
                transferencia_img = "/home/pi/Documents/transferencia_img"
                #Renombra directorio modulo_img con nombre transferencia para enviar al servidor
                os.rename("{}" .format(ruta_img),"{}" .format(transferencia_img))
                os.system('rm -r {}' .format(ruta_img))
                #Vuelve a crear el directorio modulo_img
                os.system('mkdir {}' .format(ruta_img))
                #Llama fichero python transferencia_img.py para que se produzca la transferencia al servidor
                os.system('python3 transferencia_img.py')
                
                #Para la prevista de la cámara porque la siguiente funcion grabar_video lo vuelve abrir.
                camera.stop_preview()
                camera.close()
                #Reproduce sonido de inicio de streaming
                os.system('echo "Iniciando streaming" | festival --tts')
                #Llama al server.py para iniciar servicio de streaming
                os.system('python3 {}' .format(ruta_streaming))
                #Para streaming
                while True:
                    #Ruta donde guarda orde de "Python parar streaming".
                    orden = "/home/pi/Documents/parar_streaming.txt"
                    if os.path.exists(orden):
                        lectura2 = open('{}' .format(orden))
                        if 'Streaming parado' in lectura2.read():
                            lectura.close()
                            #Borra fichero parar_streaming.txt si existe
                            if os.path.exists('/home/pi/Documents/parar_streaming.txt'):
                                os.system('rm /home/pi/Documents/parar_streaming.txt')
                            #Para la prevista de la cámara porque la siguiente funcion grabar_video lo vuelve abrir.
                            #camera.stop_preview()
                            #camera.close()
                            #Inicia la prevista porque la función grabar_video la deja cerrada.
                            camera = PiCamera()
                            camera.start_preview()
                            #Borra la entrada del reconocimiento de voz del fichero dictation.txt
                            borrado_entrada("Python inicia streaming")
                            borrado_entrada("Python parar streaming")
                            #Lanza voz de servicio streaming parado.
                            os.system('echo "Servicio streaming parado" | festival --tts')
                            break
        
            except:
                print('Error en parar streaming')
        #Inicia reset de los directorios
        lectura = open('{}' .format(ruta_dictation))
        if 'Python inicia reset' in lectura.read():
            lectura.close()
            #Reproduce sonido de inicio de reset
            os.system('echo "Iniciando reset" | festival --tts')
            reset_camara()
            os.system('echo "Finalizado reset" | festival --tts')
except:
    print("Error funcion captura imagen")
finally:
    #camera.stop_preview()
    #camera.close()
    print('Camara apagada')
    
