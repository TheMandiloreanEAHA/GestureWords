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
    page.title = 'GestureWords'
    page.theme_mode = 'light'
    page.window_width = 400
    page.window_height = 200
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
                        aud_text = r.recognize_google(audio, language='en-EN')
                       
                        if aud_text == 'active':
                            print("¿Qué deseas escribir?")
                            #playsound("D:/UV/7.Semestre/IntUsrAv/PracticasPython/PruebaProyecto/ProyectoInterfaces/prueba_Chida/nota3.mp3")
                            # Construye la ruta completa al archivo "nota3.mp3" usando la ruta del script   
                            ruta_nota = os.path.join(directorio_script, "nota3.mp3")
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
                        tts = gTTS("Lo siento, no pude entenderte", lang='es')
                        tts.save("error1.mp3")
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
    
        #Instanciamos la solución de MediaPipe (Hands)
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils #Para dibujar los resultados

        #Configurar la captura de video con OpenCV
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

        #--------------------------------Función calcuclar distancia ---------------------------------#
        def calculate_distance(x1, y1, x2, y2):
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            return np.linalg.norm(p1 - p2)
        #---------------------------------------------------------------------------------------------#
        #--------------------------------Funcion para hacer click-------------------------------------#
        def detect_finger_down(hand_landmarks):
            finger_down = False
            color_base = (255, 0, 112)
            color_index = (255, 198, 82)
            x_base1 = int(hand_landmarks.landmark[0].x * width)
            y_base1 = int(hand_landmarks.landmark[0].y * height)
            x_base2 = int(hand_landmarks.landmark[9].x * width)
            y_base2 = int(hand_landmarks.landmark[9].y * height)
            x_index = int(hand_landmarks.landmark[8].x * width)
            y_index = int(hand_landmarks.landmark[8].y * height)
            d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2)
            d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index)
            if d_base_index < d_base:
                finger_down = True
                color_base = (255, 0, 255)
                color_index = (255, 0, 255)
            cv2.circle(output, (x_base1, y_base1), 5, color_base, 2)
            cv2.circle(output, (x_index, y_index), 5, color_index, 2)
            cv2.line(output, (x_base1, y_base1), (x_base2, y_base2), color_base, 3)
            cv2.line(output, (x_base1, y_base1), (x_index, y_index), color_index, 3)
            return finger_down
        #---------------------------------------------------------------------------------------------#
        #--------------------------------Funcion para hacer enter-------------------------------------#
        def detect_hand_closed(hand_landmarks):
            x_index = int(hand_landmarks.landmark[8].x * width)
            y_index = int(hand_landmarks.landmark[8].y * height)
            x_middle_base = int(hand_landmarks.landmark[0].x * width)
            y_middle_base = int(hand_landmarks.landmark[0].y * height)
            
            # Calcular la distancia entre la punta del dedo índice y la base del dedo medio
            distance = calculate_distance(x_index, y_index, x_middle_base, y_middle_base)

            # Puedes ajustar este umbral según sea necesario
            threshold = 30

            # Si la distancia es menor que el umbral, consideramos que la mano está cerrada
            return distance < threshold
        #---------------------------------------------------------------------------------------------#
        with mp_hands.Hands(
        static_image_mode = False,
        max_num_hands = 1,
        min_detection_confidence = 0.5  
        ) as hands:
            
            while correrProgramaGes:
                #Crear ventana
                ret, frame = cap.read()
                if ret == False:
                    break
                height, width, _ = frame.shape
                frame = cv2.flip(frame,1)

                #Dibujamos el área proporcional
                area_width = width - X_Y_INI *2
                area_height = int(area_width / relacion_aspecto)
                aux_image = np.zeros(frame.shape, np.uint8)

                #Crear el recuadro con los puntos encontrados
                aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (X_Y_INI + area_width, X_Y_INI + area_height), (255,0,0), -1)
                output = cv2.addWeighted(frame, 1, aux_image, 0.7,0)

                #Convertimos el frame en código rgb
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resultado = hands.process(frame_rgb)

                #Si detecta una manos
                if resultado.multi_hand_landmarks is not None:
                    for hand_landmarks in resultado.multi_hand_landmarks:
                        #Obtener las coordenadas de la mano
                        x = int(hand_landmarks.landmark[9].x * width)


                        y = int(hand_landmarks.landmark[9].y * height)
                        xm = np.interp(x,(X_Y_INI, X_Y_INI+ area_width), (PANTALLA_X_INI, PANTALLA_X_FIN))
                        ym = np.interp(y,(X_Y_INI, X_Y_INI+ area_height), (PANTALLA_Y_INI, PANTALLA_Y_FIN))

                        #Mover el mouse
                        pyautogui.moveTo(int(xm), int(ym))
                        if detect_finger_down(hand_landmarks):
                            pyautogui.click()
                        if detect_hand_closed(hand_landmarks):
                            # Acción a realizar cuando la mano está cerrada (por ejemplo, presionar la tecla Enter)
                            pyautogui.press('enter')

                        #Pner un circulo a donde movimos la mano
                        cv2.circle(output, (x,y), 10, color_mouse, 3)
                        cv2.circle(output, (x,y), 5, color_mouse, -1)
                
                #Mostrar pantalla 
                cv2.imshow('output', output)

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
            switchVoz.label = ("Interacción con la Voz: Activa")
            correrProgramaVoz = True
            
        else:
            switchVoz.label = ("Interacción con la Voz: Inactiva")
            correrProgramaVoz = False
        if switchGes.value == True:
            switchGes.label = ("Interacción con la mano: Activa")
            correrProgramaGes = True
        else:
            switchGes.label = ("Interacción con la mano: Inactiva")
            correrProgramaGes = False
        #Actualizamos la página     
        page.update()
    
    # Crea dos hilos para ejecutar las funciones en paralelo
    hilo_voz = threading.Thread(target=interfaz_voz)
    hilo_gestual = threading.Thread(target=interfaz_gestual)

    # Inicia los hilos
    hilo_voz.start()
    hilo_gestual.start()

    t = ft.Text()
    switchVoz = ft.Switch(label="Interacción con la Voz: Activa", value=True, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz de Voz
    switchGes = ft.Switch(label="Interacción con la mano: Activa", value=True, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz Gestual

    switchVoz.thumb_color={
    ft.MaterialState.HOVERED: ft.colors.WHITE,
    ft.MaterialState.FOCUSED: ft.colors.RED,
    ft.MaterialState.DEFAULT: ft.colors.BLACK,}

    btn = ft.ElevatedButton(text="Aplicar", on_click=button_clicked)

    

    page.add(switchVoz, switchGes, btn, t)

if __name__ == '__main__':
    ft.app(target=main)

#azulfuncionando