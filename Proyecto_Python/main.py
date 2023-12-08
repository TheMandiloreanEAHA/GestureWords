#-------------------------------Escribe como si fuera el teclado utilizando una interfaz de voz-------------------------------#

#------------------------------Importar librerías Para el reconocimiento de voz
import time
import speech_recognition as sr
import pynput
from playsound import playsound #Esta es para el efecto de estado de la interfaz
from gtts import gTTS #convertir texto a voz
import os #Convertir rutas absolutas a relativas
#------------------------------Importar librerias para el reconocimiento gestual
#OpenCV
#Librería de visión por computadora libre
#ayuda al reconocimiento de imagenes y la detección de movimientos
import cv2

#Mediapipe
#Solución manos de 21 puntos de referencia
#detecta las manos y los dedos
import mediapipe as mp

#math
#Biblioteca para cosas de matemáticas y así
from math import acos, degrees

#numpy
#Biblioteca para crear vectores y matrices
import numpy as np

#pyautogui
#Biblioteca para el soporte administrar operaciones del mouse y teclado
import pyautogui
# Desactivar la función de fail-safe
pyautogui.FAILSAFE = False
#-------------------------------------------Improtar librería para crear hilos
#threading
#Biblioteca para crear y administrar hilos
import threading

#-------------------------------------------Importar librería para crear la interfaz gráfica
#flet
#Biblioteca para crear y agregar diseño a la Interfaz gráfica
import flet as ft
import time #Librería para controlar tiempos de pausa
#------------------------------------------------------------------------- Funciones ----------------------------------------------------------------------------#
#Crear variables globales para terminar el proceso o iniciar los procesos
correrProgramaVoz = True
correrProgramaGes = True
# Obtén la ruta al directorio del script
directorio_script = os.path.dirname(os.path.abspath(__file__))


def main(page: ft.Page) -> None:
    # Construye la ruta completa al archivo usando la ruta del script   
    ruta_nota = os.path.join(directorio_script, "nota1.mp3")
    # Reproduce el archivo de audio
    playsound(ruta_nota)

    page.title = 'GestureWords'
    page.theme_mode = 'light'
    page.window_width = 410
    page.window_height = 400
    page.window_resizable = False
    page.window_maximizable = False
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = "center"
    # Establece la posición de la ventana en el centro de la pantalla del escritorio
    page.window_left = 600
    page.window_top = 200
    page.window_focused = True



    #--- Define la función de la interfaz de voz ---#
    def interfaz_voz():
        # Código de la interfaz de voz
        #Jalamos la variable global
        global correrProgramaVoz

        #Declaramos el reconocedor
        r = sr.Recognizer()
        #Iniciamos ciclo para que esté siempre en escucha
        while True:
            #Si es False, debería pausar el hilo
            if correrProgramaVoz == True:
                #Activar el microfono como recurso que estará en escucha
                with sr.Microphone() as source:
                    print('Identificate, por favor...')
                    #Guardamos lo que ha escuchado el microfono en una variable
                    r.adjust_for_ambient_noise(source)
                    r.timeout = 2
                    audio = r.listen(source)

                    try:
                        aud_text = r.recognize_google(audio, language='es-ES ')                       
                        if aud_text == 'dictar':
                            print("¿Qué deseas escribir?")
                            #playsound("D:/UV/7.Semestre/IntUsrAv/PracticasPython/PruebaProyecto/ProyectoInterfaces/prueba_Chida/nota3.mp3")
                            # Construye la ruta completa al archivo "nota3.mp3" usando la ruta del script   
                            ruta_nota = os.path.join(directorio_script, "nota2.mp3")
                            # Reproduce el archivo de audio
                            playsound(ruta_nota)
                            
                            #Generamos un nuevo recurso 
                            audio2 = r.listen(source)
                            sentencia = r.recognize_google(audio2, language='es-ES')
                            print('La sentencia dictada fue: {}'.format(sentencia))

                            
                            keyboard = pynput.keyboard.Controller()
                            for caracter in sentencia:
                                # Agregamos un delay de 0.1 segundos entre cada tecla
                                time.sleep(0.1)
                                keyboard.press(caracter)
                                keyboard.release(caracter)

                        else:
                            print('Acceso denegado, tu dijiste: {}'.format(aud_text))
                    except sr.UnknownValueError:
                        print("No se pudo entender el audio")
                        #Construye el audio de error
                        tts = gTTS("Lo siento, no pude entenderte", lang='es')
                        ruta_error = os.path.join(directorio_script, "error1.mp3")
                        tts.save(ruta_error)
                        # Construye la ruta completa al archivo usando la ruta del script 
                        ruta_nota = os.path.join(directorio_script, "nota3.mp3")
                        # Reproduce el archivo de audio
                        playsound(ruta_nota)
                        playsound("error1.mp3")
                    except sr.RequestError as e:
                        print(f"Error al hacer la solicitud a Google: {e}")
                    except Exception as e:
                        print(f"Error general: {e}")

            time.sleep(1)
    #--- Define la función de la interfaz gestual ---# 
    def interfaz_gestual():
        #Código de la interfaz gestual        
        global correrProgramaGes #Jalamos la variable global    

        def palm_centroid(coordinates_list):
            coordinates = np.array(coordinates_list)
            centroid = np.mean(coordinates, axis=0)
            centroid = int(centroid[0]), int(centroid[1])
            return centroid

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        #Definir los puntos de la pantalla
        PANTALLA_X_INI = 0
        PANTALLA_Y_INI = 0
        PANTALLA_X_FIN = 2000
        PANTALLA_Y_FIN = 1000

        #Color del puntero
        color_mouse = (255, 0, 255)
        relacion_aspecto = (PANTALLA_X_FIN - PANTALLA_X_INI) / (PANTALLA_Y_FIN - PANTALLA_Y_INI)

        #Margen del area azul
        X_Y_INI = 100

        # Pulgar
        thumb_points = [1, 2, 4]

        # Índice, medio, anular y meñique
        palm_points = [0, 1, 2, 5, 9, 13, 17]
        fingertips_points = [8, 12, 16, 20]
        finger_base_points =[6, 10, 14, 18]

        with mp_hands.Hands(
            model_complexity=1,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            while True:
                if correrProgramaGes == True:
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    frame = cv2.flip(frame, 1)
                    height, width, _ = frame.shape
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(frame_rgb)
                    thickness = [2, 2, 2, 2, 2]

                    #Dibujamos el área proporcional
                    area_width = width - X_Y_INI *2
                    area_height = int(area_width / relacion_aspecto)
                    aux_image = np.zeros(frame.shape, np.uint8)

                    #Crear el recuadro con los puntos encontrados
                    aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + area_width, X_Y_INI + area_height), (255,0,0), -1)
                    output = cv2.addWeighted(frame, 1, aux_image, 0.7,0)

                    #Convertimos el frame en código rgb
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    if results.multi_hand_landmarks:
                        coordinates_thumb = []
                        coordinates_palm = []
                        coordinates_ft = []
                        coordinates_fb = []
                        for hand_landmarks in results.multi_hand_landmarks:
                                #Obtener las coordenadas de la mano
                                x = int(hand_landmarks.landmark[9].x * width)
                                y = int(hand_landmarks.landmark[9].y * height)
                                xm = np.interp(x,(X_Y_INI, X_Y_INI+ area_width), (PANTALLA_X_INI, PANTALLA_X_FIN))
                                ym = np.interp(y,(X_Y_INI, X_Y_INI+ area_height), (PANTALLA_Y_INI, PANTALLA_Y_FIN))

                                #Mover el mouse
                                pyautogui.moveTo(int(xm), int(ym))
                                for index in thumb_points:
                                    x = int(hand_landmarks.landmark[index].x * width)
                                    y = int(hand_landmarks.landmark[index].y * height)
                                    coordinates_thumb.append([x, y])
                                
                                for index in palm_points:
                                    x = int(hand_landmarks.landmark[index].x * width)
                                    y = int(hand_landmarks.landmark[index].y * height)
                                    coordinates_palm.append([x, y])
                                
                                for index in fingertips_points:
                                    x = int(hand_landmarks.landmark[index].x * width)
                                    y = int(hand_landmarks.landmark[index].y * height)
                                    coordinates_ft.append([x, y])
                                
                                for index in finger_base_points:
                                    x = int(hand_landmarks.landmark[index].x * width)
                                    y = int(hand_landmarks.landmark[index].y * height)
                                    coordinates_fb.append([x, y])
                                ##########################
                                # Pulgar
                                p1 = np.array(coordinates_thumb[0])
                                p2 = np.array(coordinates_thumb[1])
                                p3 = np.array(coordinates_thumb[2])

                                l1 = np.linalg.norm(p2 - p3)
                                l2 = np.linalg.norm(p1 - p3)
                                l3 = np.linalg.norm(p1 - p2)

                                # Calcular el ángulo
                                angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
                                thumb_finger = np.array(False)
                                if angle > 150:
                                    thumb_finger = np.array(True)
                                
                                ################################
                                # Índice, medio, anular y meñique
                                nx, ny = palm_centroid(coordinates_palm)
                                cv2.circle(frame, (nx, ny), 3, (0, 255, 0), 2)
                                coordinates_centroid = np.array([nx, ny])
                                coordinates_ft = np.array(coordinates_ft)
                                coordinates_fb = np.array(coordinates_fb)

                                # Distancias
                                d_centrid_ft = np.linalg.norm(coordinates_centroid - coordinates_ft, axis=1)
                                d_centrid_fb = np.linalg.norm(coordinates_centroid - coordinates_fb, axis=1)
                                dif = d_centrid_ft - d_centrid_fb
                                fingers = dif > 0
                                fingers = np.append(thumb_finger, fingers)
                                
                                #Pner un circulo a donde movimos la mano
                                cv2.circle(output, (x,y), 10, color_mouse, 3)
                                cv2.circle(output, (x,y), 5, color_mouse, -1)

                                
                                if(fingers[0] == False):
                                    pyautogui.press('enter')
                                    print("Enter")
                                    time.sleep(2)
                                if(fingers[1]== False):
                                    pyautogui.click()
                                    print("click")

                                for (i, finger) in enumerate(fingers):
                                    if finger == True:
                                        thickness[i] = -1
                                mp_drawing.draw_landmarks(
                                    frame,
                                    hand_landmarks,
                                    mp_hands.HAND_CONNECTIONS,
                                    mp_drawing_styles.get_default_hand_landmarks_style(),
                                    mp_drawing_styles.get_default_hand_connections_style())

                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                
        cap.release()
        cv2.destroyAllWindows()    
    
        
    
    def button_clicked(e):
        #Declaramos la variables global que controlan los hilos
        global correrProgramaVoz 
        global correrProgramaGes
        #Iniciamos las validaciones
        if switchVoz.value == True:
            switchVoz.label = ("Interacción con la Voz: Activa                      ")
            correrProgramaVoz = True
            voz_icon.color = "#0061A4"            
        else:
            switchVoz.label = ("Interacción con la Voz: Inactiva                    ")
            correrProgramaVoz = False
            voz_icon.color = "#73777F"

        if switchGes.value == True:
            switchGes.label = ("Interacción con la mano: Activa                   ")
            correrProgramaGes = True
            gest_icon.color = "#0061A4" 
        else:
            switchGes.label = ("Interacción con la mano: Inactiva                 ")
            correrProgramaGes = False
            gest_icon.color = "#73777F"
        #Actualizamos la página     
        page.update()
    
    # Crea dos hilos para ejecutar las funciones en paralelo
    hilo_voz = threading.Thread(target=interfaz_voz)
    hilo_gestual = threading.Thread(target=interfaz_gestual)

    # Inicia los hilos
    hilo_voz.start()
    hilo_gestual.start()

    #Icono de ayuda 
    ayuda = ft.IconButton(
                    icon=ft.icons.QUESTION_MARK,
                    icon_color="#0061A4",
                    icon_size=20,
                    tooltip="Documentación",
                    url= "https://uvmx-my.sharepoint.com/:w:/g/personal/zs20018188_estudiantes_uv_mx/EeP7neGxfYNBh3et3a942f4BOe8t--5u6ikNwphfnKXbVA?e=oguJX3"
                )

    t = ft.Text(
            "Para dictar, debes decir la palabra mágica: Dictar",
            size=10,
            color=ft.colors.BLUE,
            weight=ft.FontWeight.BOLD,
            italic=True,
        )

    switchVoz = ft.Switch(label="Interacción con la Voz: Activa                      ", value=True, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz de Voz
    switchGes = ft.Switch(label="Interacción con la mano: Activa                   ", value=True, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz Gestual

    btn = ft.ElevatedButton(text="Aplicar", on_click=button_clicked)    

    tf_creditos = ft.TextField(label="Creditos", disabled=True, multiline=True, value="Creado por:\nManquitos Yahir De la caña Pérez\nErick A. Hernández Aburto\nAlex Antonio Terrones Pacheco")

    voz_icon = ft.Icon(name=ft.icons.MIC, color="#0061A4", size="30")
    gest_icon = ft.Icon(name=ft.icons.BACK_HAND_SHARP, color="#0061A4", size="30")

    

    row_voz = ft.Row(controls=[
                switchVoz,
                voz_icon
            ])
    
    row_gest = ft.Row(controls=[
                switchGes,
                gest_icon
            ])
    
    row_btn_Y_ayuda = ft.Row(controls=[
                                btn,
                                ayuda
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) 
        
    page.add(row_voz, t, row_gest, row_btn_Y_ayuda, ft.Text(" "),tf_creditos)

   

if __name__ == '__main__':
    ft.app(target=main)
