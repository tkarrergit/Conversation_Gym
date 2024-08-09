import settings

import flet as ft
import sys

def resource_path(relative_path):
    import os
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        #PyInstaller creates a temp folder and stores path in MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#Stimmauswahl aus folgenden möglichkeiten
#gtts
#coqui_tts
#google_cloud_tts funktioniert nur mit Anmeldung bisher noch nicht
#pyttsx3
stimme = "pyttsx3"

smal_model = "assets/vosk-model-small-de-zamia-0.3"
big_model = "assets/vosk-model-small-de-zamia-0.3"
#"assets/vosk-model-de-0.21"
vosk_model_path = big_model 

stop_flag = False
assistant = settings.meeting

list_video_mann = ft.VideoMedia(resource_path("assets/Mann.mp4"))
list_video_frau = ft.VideoMedia(resource_path("assets/Frau.mp4"))#, ft.VideoMedia("assets/Frau2.mp4")]
video_path = list_video_frau

frau_namen_list =["laura", "marie", "anna", "lena", "hanna", "emma"]
mann_namen_list =["paul", "lukas", "leon", "max", "simon", "tim", "david"]
geschlecht_list = ["maennlich", "weiblich"]

gespraechs_nummer = 0

import random

def generate_random_number():
    # Bestimme zufällig die Anzahl der Ziffern (1 bis 1000)
    num_digits = random.randint(1, 1000)
    # Erzeuge die erste Ziffer (1-9) damit die Zahl nicht mit 0 anfängt
    first_digit = random.randint(1, 9)
    # Erzeuge die restlichen Ziffern (0-9)
    remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    # Kombiniere die erste Ziffer mit den restlichen Ziffern
    random_number = str(first_digit) + remaining_digits
    print(num_digits)
    return random_number

# Beispielverwendung

