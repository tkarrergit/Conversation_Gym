import settings
import all_functions
import flet as ft
import sys
import vosk_functions
import utilitys



vosk_recognizer = vosk_functions.vosk_model_init()


dateiname_config = utilitys.resource_path("assets/config.txt")
dateiname_gespraeche = utilitys.resource_path("assets/Gespraeche.txt")
#Stimmauswahl aus folgenden möglichkeiten
#gtts
#coqui_tts
#google_cloud_tts funktioniert nur mit Anmeldung bisher noch nicht
#pyttsx3
email = ""
passwort = ""

email_field = ft.TextField(label="E-Mail")
password_field = ft.TextField(label="shared.Passwort", password=True)


stimme = "pyttsx3"

 


assistant = settings.meeting

list_video_mann = ft.VideoMedia(utilitys.resource_path("assets/Frau.mp4"))#ft.VideoMedia(utilitys.resource_path("assets/Mann.mp4"))
list_video_frau = ft.VideoMedia(utilitys.resource_path("assets/Frau.mp4"))#, ft.VideoMedia("assets/Frau2.mp4")]
video_path = list_video_frau

frau_namen_list =["laura", "marie", "anna", "lena", "hanna", "emma"]
mann_namen_list =["laura", "marie", "anna", "lena", "hanna", "emma"]#["paul", "lukas", "leon", "max", "simon", "tim", "david"]
geschlecht_list = ["maennlich", "weiblich"]

gespraechs_nummer = 0
gespraeche = []
gespraechs_editor_flag = True
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

