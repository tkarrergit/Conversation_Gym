import multiprocessing.process
import flet as ft
import time
import all_functions
from all_functions import initialize_hugchat
from all_functions import sr_speech_to_text
import Video
import settings
import base64
import threading
import multiprocessing
import re
import sys
from  vosk import Model, KaldiRecognizer
import shared
import random
import keyboard

#Huggingchat Assistanten Funktion    
global stimme  


#----------Code-Gliederung----------
#1.0    Interne Funktionen                              Konnten aufgrund von doppelten (hinher Import) Importen nicht in all_functions.py.
#2.0    Main Window
#2.1    Funktionen innerhalb der APP
#2.1.1  Coaching Vorbereitung
#2.1.2  Coaching schruftlicher Chatverlauf
#2.2    Auswahlmenue
  

def hugchat_assistent(chatbot, user_input, new_conversation):  
    if user_input:  
        
        starttime = time.time()
        antwort = chatbot.chat(user_input, conversation = new_conversation)    
        print(antwort)
        endtime = time.time()
        duration = endtime -starttime
        print(duration)
        return antwort 
    else:
        pass


"""
def check_hugchat(email, passwort):
    newconversation, chatbot = hugchat_initialize(email, passwort, settings.coaching)
    print(newconversation and chatbot)
    hugchat_assistent_stream(chatbot, "Wie heißt du", newconversation)
"""

#Stimmauswahl Funktion 
 
stimme =shared.stimme

def stimme_auswahl_tts(stimme, antwort):
    print(stimme)
    if stimme =="gtts":
        all_functions.gtts_tts(antwort, language='de')
    elif stimme == "coqui_tts":
        all_functions.coqui_tts(antwort)
    elif stimme == "google_cloud_tts":
        all_functions.google_Cloud_tts(antwort, language_code='de-DE', voice_name=None, output_file='output.mp3')
    elif stimme == "pyttsx3":
        print(Video.videos)
        #Video.play(Video.videos[3])
        all_functions.pyttsx3_tts(antwort)
        #Video.seek(Video.videos[3])
        #Video.pause(Video.videos[3])


#2.0    Main Window

def main(page:ft.Page):
    
    page.window_width = 1820
    page.window_height = 1000
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  

    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "fonts/OpenSans-Regular.ttf",
    }

#2.1.2  Coaching schruftlicher Chatverlauf

    cl = ft.Column(
                alignment= ft.MainAxisAlignment.START,
                horizontal_alignment =  ft.CrossAxisAlignment.CENTER,          
                spacing=15,
                height=200,
                width=960,
                scroll=ft.ScrollMode.ALWAYS,   
        )

    def update_response(output):
        cl.controls.append(
            ft.Container(
                content=ft.TextField(
                    value=output, 
                    label="Klient", 
                    label_style= ft.TextStyle(
                                        size=16, 
                                        color=ft.colors.BLACK,
                                        font_family="Open Sans"), 
                    text_style= ft.TextStyle(
                                        size=14, 
                                        font_family="Open Sans", 
                                        color=ft.colors.BLACK), 
                            bgcolor=ft.colors.BLUE_100, 
                            width=800, 
                            multiline=True, 
                            border_radius=10
                        ), margin=ft.margin.only(left=100),
                width=800,
            )
        )
        cl.auto_scroll = True
        page.add(cl)

    def update_input(input):
        cl.controls.append(
            ft.Container(
                content=ft.TextField(
                            value=input, label="Coach", label_style= ft.TextStyle(size=16, color=ft.colors.BLACK, font_family="Open Sans"), 
                            text_style= ft.TextStyle(size=14, font_family="Open Sans", color=ft.colors.BLACK), 
                                                bgcolor=ft.colors.BLUE_50, width=800, multiline=True, border_radius=10), margin=ft.margin.only(right=100),
                width=800,
            )
        )
        cl.auto_scroll = True
        page.add(cl)    

    def hugchat_initialize(email, passwort, assistant):
        try:
            chatbot = initialize_hugchat(email, passwort,)
            tomconversation = chatbot.new_conversation(assistant=assistant) 
            return tomconversation, chatbot
        except Exception as e:
            all_functions.pyttsx3_tts("Anmeldung fehlgeschlagen. Bitte starten sie die App neu und überprüfen sie ihre Anmeldedaten.")
            auswahlmenue(email, passwort)

    def hugchat_initialize_no_assistant(email, passwort):
        try:
            chatbot = initialize_hugchat(email, passwort)
            tomconversation = chatbot.new_conversation() 
            return tomconversation, chatbot
        except Exception as e:
            all_functions.pyttsx3_tts("Anmeldung fehlgeschlagen. Bitte starten sie die App neu und überprüfen sie ihre Anmeldedaten.")
            auswahlmenue(email, passwort)

    def hugchat_assistent_stream(chatbot, user_input, newconversation):
        try:           
            sprich_stream_chat_satz(chatbot, user_input, newconversation)
        except:
            print("No Input")

    def sprich_stream_chat_satz(chatbot, user_input, conversation):
        #Spricht jeden vollständigen Satz der Antwort einen nach dem anderen.
        # Initialisiere eine leere Zeichenkette für den zusammenhängenden Text    
        full_response = ""
        current_sentence = ""
        satzflag = True
        starttime = time.time()
        # Stream response
        print("Hallo sprich_stream_chat_satz for-schleife")
        try: 
            for resp in chatbot.query(
                user_input,
                stream=True, 
                conversation = conversation,
            ):  
                if resp:
                    print("YES")
                    print(resp)
                # Überprüfe, ob resp nicht None ist, bevor auf resp['type'] zugegriffen wird
                if resp is not None and resp.get('type') == 'stream':
                    token = resp['token']
                    current_sentence += token
                    try:    
                        # Check if the current token ends with a sentence-ending punctuation
                        if re.search(r'[.!?]', token):
                            
                            # Print and speak the complete sentence
                            cleaned_sentence = re.sub(r'\x00', '', current_sentence)  # Remove NULL characters
                            print(cleaned_sentence, end=" ")                
                            sys.stdout.flush()
                            full_response += cleaned_sentence
                            if shared.stop_flag==False:
                                update_response(cleaned_sentence)
                                Video.play(Video.videos[0])
                                
                    
                                stimme_auswahl_tts(stimme, cleaned_sentence)

                                Video.pause(Video.videos[0]) 
                                Video.seek(Video.videos[0])
                            current_sentence = ""
                    except Exception as e:
                        print(f"ERROR: {e}")
                 

            # Falls der letzte Satz kein Satzzeichen hatte, trotzdem sprechen
            if current_sentence:
                cleaned_sentence = re.sub(r'\x00', '', current_sentence)  # Remove NULL characters
                all_functions.pyttsx3_tts(cleaned_sentence)
                
        except Exception as e:
                        print(f"ERROR: {e}")
                        stimme_auswahl_tts(stimme, "Dein Klient ist gerade nicht erreichbar....versuch es gleich nochmal....")
    
    def lese_email_passwort(dateiname):
        """
        Liest E-Mail und Passwort aus einer Textdatei.
        
        Args:
            dateiname (str): Name der Textdatei
            
        Returns:
            tuple: E-Mail und Passwort als Tupel
        """
        try:
            with open(dateiname, 'r') as f:
                inhalt = f.readlines()
                email = inhalt[0].strip()
                passwort = inhalt[1].strip()
                app_starts_count = inhalt[2].strip()
            return email, passwort, app_starts_count
        except FileNotFoundError:
            print(f"Datei '{dateiname}' nicht gefunden.")
        except IndexError:
            print("Datei hat nicht das erwartete Format (E-Mail in Zeile 1, Passwort in Zeile 2).")
        except Exception as e:
            print(f"Error: {e}")
    global app_starts_count
    """
    email, passwort, app_starts_count= lese_email_passwort("config.txt")
    assistant = settings.coachee
    new_conversation, chatbot = hugchat_initialize(email, passwort, assistant)
    print(new_conversation)
    print(chatbot)
    print(stimme)
    sprich_stream_chat_satz(chatbot, "Hallo wie geht es dir", new_conversation)

    """
    email, passwort, app_starts_count = lese_email_passwort(all_functions.resource_path("assets/config.txt"))
    app_starts_count = int(app_starts_count)
    #print(email, passwort)
    if app_starts_count < 1 :
        text= ""
    else:
        text= "Offline Spracherkennung wird vorbereitet..."

     
    page.clean()
    page.add(
        ft.Column([
            ft.Container(
                ft.Row([
                    ft.Text(
                            "Conversation Gym",
                            size=100,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.ORANGE_400,
                            weight=ft.FontWeight.NORMAL, 
                            text_align= ft.TextAlign.CENTER),

                ],alignment=ft.MainAxisAlignment.CENTER),
                
                

            ),
            ft.Container(
                ft.Row([
                    ft.Text(
                            "Pimp up your skill´s",
                            size=40,
                            color=ft.colors.ORANGE_400,                            
                            weight=ft.FontWeight.NORMAL, 
                            text_align=ft.CrossAxisAlignment.CENTER),

                ],alignment=ft.MainAxisAlignment.CENTER),
                
                

            ),
            ft.Container(
                ft.Row ([
                    
                    ft.Text(
                            text, 
                            text_align=ft.MainAxisAlignment.START )   


                ],alignment=ft.MainAxisAlignment.CENTER),
            ),
        ])
    )
    

    if app_starts_count < 1 :
        shared.vosk_model_path = shared.smal_model
    else:
        shared.vosk_model_path = shared.big_model
    time.sleep(3)
    model = Model(all_functions.resource_path(shared.vosk_model_path)) #Resource Pfad nutzen wie beim Console Assistent
    vosk_recognizer = KaldiRecognizer(model, 32000)

    #EMAIL und PASSWORT eingabe Anfang

    def email_passwort_field(email, passwort):
        
        if email and passwort:
            email_field = ft.TextField(label="E-Mail",value=email, read_only=True)
            password_field = ft.TextField(label="Passwort", value=passwort, password=True, read_only=True)
            return email_field, password_field
        else:
            email_field = ft.TextField(label="E-Mail")
            password_field = ft.TextField(label="Passwort", password=True)
            return email_field, password_field
        
    email_field = ft.TextField(label="E-Mail")
    password_field = ft.TextField(label="Passwort", password=True)
    
    def email_passwort_ändern(e):
        email_field.value = ""  # Löscht den Inhalt des Email-Feldes
        email_field.read_only = False
        
    
        password_field.value = ""  # Löscht den Inhalt des Passwort-Feldes
        email_field.read_only = False
        
        page.clean()
        page.add(ft.Stack([
                    ft.Container(
                        ft.Container(
                            ft.Column(
                                [
                                ft.Text("HuggingChat Zugangsdaten",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            ),
                                email_field, 
                                password_field, 
                                ft.Row([
                                    ft.Container(ft.Text("Speichern"),                                                                               
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=save_data
                                    ),
                                    ft.Container(ft.Text("Ändern"),
                                        margin=20,                                        
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=email_passwort_ändern
                                    ),                             
                                ], alignment = ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Container(ft.Text("Zurück zur Auswahl"),                                                                               
                                            alignment=ft.alignment.center,
                                            bgcolor=ft.colors.WHITE,
                                            height = 30,
                                            width=330,
                                            border_radius=10,
                                            on_click=auswahl_button),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                
                                ],
                                width=400,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),  
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.ORANGE,
                        height = 300,
                        width=350,
                        border_radius=10,
                        ),
                        
                        
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 800,
                    width=1400,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1400/800?{3}",
                    ),            
                ]),              
        )        

    def save_data(e):#email und passwort
        global app_starts_count
        email = email_field.value
        password = password_field.value
        app_starts_count = app_starts_count + 1

        if email and password:
            try:
                with open(all_functions.resource_path("assets/config.txt"), "w") as file:
                    file.write(f"{email}\n{password}\n{app_starts_count}")
                    
                snack_bar = ft.Text("Daten erfolgreich gespeichert!", bgcolor=ft.colors.GREEN)
                page.add(snack_bar)
                all_functions.pyttsx3_tts("Bitte nach dem speichern das Programm neu starten.")
                #email, passwort = lese_email_passwort(all_functions.resource_path("assets/config.txt"))
            except Exception as e:
                snack_bar = ft.Text(f"Fehler beim Speichern: {e}", bgcolor=ft.colors.RED)
                page.add(snack_bar)
        else:            
            snack_bar = ft.Text(f"Bitte E-Mail und Passwort eingeben.", bgcolor=ft.colors.RED)
            page.add(snack_bar)
       
    
    save_button = ft.ElevatedButton("Speichern", on_click=save_data)
    aendern_button = ft.ElevatedButton("Ändern", on_click=email_passwort_ändern)

    #EMAIL und PASSWORT eingabe Ende

    def coaching_button(e):
        global gespraechs_editor_flag
        gespraechs_editor_flag  = False   
        antwort = coaching_gespraech_vorbereitung(email, passwort) 
        klient = person_namen()
        print(klient)  
        print("2: " + str(shared.video_path) )  
        coaching_video_row, meeting_video_row = Video.video_row()     
        print("Nach Video Row " + str(Video.videos))
        shared.stop_flag = False
        stop = True
        all_functions.pyttsx3_tts("Dein Klient ist bereit, drücke Leertaste wenn auch du soweit bist.")
        while stop:
            if keyboard.is_pressed('space'):
                stop = False
            else:
                pass

        page.clean() 
        
        page.add(
        ft.Stack([
            ft.Row([ft.Container(
                content=ft.Container(
                            ft.Column([
                                ft.Row([
                                    coaching_video_row,                           

                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Container(
                                            content=ft.Text(
                                                        "Zurück zur Auswahl",
                                                        size=30,
                                                        font_family="Open Sans", 
                                                        color=ft.colors.BLACK
                                                    ),
                                            
                                            #margin=10,
                                            #padding=10,
                                            alignment=ft.alignment.center, 
                                            bgcolor=ft.colors.WHITE38,
                                            height = 50,
                                            width=960,                                    
                                            border_radius=10,
                                            on_click=auswahl_button_coaching,                                       
                                            #image_src = f"https://picsum.photos/900/100?{1}",
                                            ),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Container(                                                                       
                                            content = ft.ExpansionPanelList(   
                                                
                                                expand_icon_color=ft.colors.AMBER,
                                                elevation=8,
                                                divider_color=ft.colors.AMBER,                                                                                                       
                                                controls=[
                                                    ft.ExpansionPanel(
                                                        header=ft.ListTile(title=ft.Text(f"Dialogfenster",size=30, text_align = ft.TextAlign.CENTER, font_family="Open Sans", color=ft.colors.BLACK)),
                                                        content =                                       
                                                                ft.Container(
                                                                                                                                                                                                                    
                                                                    height=280, 
                                                                    width=960,
                                                                    bgcolor=ft.colors.WHITE38,
                                                                    border_radius=10,
                                                                    content=ft.Row([cl],vertical_alignment = ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),
                                                                ) ,
                                        
                                                    
                                                    bgcolor=ft.colors.WHITE38,
                                                    expanded=True,
                                                    ),
                                                ],
                                                ),
                                                                            
                                    height=300, 
                                    width=960,
                                    bgcolor=ft.colors.WHITE38,
                                    border_radius=10,
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER,                                    
                                ),
                            ],alignment=ft.MainAxisAlignment.CENTER), 
                            height=960, 
                            width=1000,
                            bgcolor=ft.colors.WHITE24,
                            border_radius=10,
                            ),             
                        
                
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                height = 960,
                width=1800,
                border_radius=10,                                                           
                image_src = f"https://picsum.photos/1800/960?{1}",
                
                )],alignment=ft.MainAxisAlignment.CENTER),                
                        
        ],alignment=ft.MainAxisAlignment.CENTER))
             
        coaching_gespraech(email, passwort, antwort, klient)

    def meeting_button(e):
        assistant = settings.coachee
        shared.stop_flag = False
        page.clean()
        page.add(
            ft.Stack([
                ft.Column([
                    ft.Row([
                    Video.meetig_video_row,
                    

                    ]),
                    Video.video_big,
                ft.Row([
                    ft.ElevatedButton(text= "Zurück zur Auswahl",on_click=auswahl_button)
                ],alignment=ft.MainAxisAlignment.CENTER)  
                ]) ]))
        sprachsteuerung(assistant)
        
    def auswahl_button_coaching(e):
        #user_input = "Gib mir eine Zusammenfassung des Coachinggesprächs. Diese soll die Charakterisierung und die Coachingziele des Klienten und die Ergebnisse des Coachings enthalten."
        #antwort = hugchat_assistent(chatbot, user_input, new_conversation)
        #print(antwort)           
        shared.stop_flag = True
        page.clean()
        page.add(ft.Stack([
                    ft.Container(
                        ft.Row ([ft.Container(ft.Text(
                                "Klient wird verabschiedet und macht einen Folgetermin aus...dies kann einen Moment dauern...vielen Dank für deine Geduld...",
                                size=20,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 60,
                            width=1160,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                            
                        ],alignment=ft.MainAxisAlignment.CENTER),
                          
                        
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 960,
                    width=1800,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1800/960?{1}",
                    on_click=coaching_button,                                  
                    
                    
                    ),
                ]),
                    
                ),                
                          
            
                
        time.sleep(2)
        
        auswahlmenue(email, passwort)

    def auswahl_button(e):              
        auswahlmenue(email, passwort)

    def einstellungen_button(e):
        email, passwort, app_starts_count = lese_email_passwort(all_functions.resource_path("assets/config.txt"))
        email_field, password_field = email_passwort_field(email, passwort)

        page.clean()
        page.add(ft.Stack([
                    ft.Container(
                        ft.Container(
                            ft.Column([
                                ft.Text("HuggingChat Zugangsdaten",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            ),
                                email_field, 
                                password_field, 
                                ft.Row([
                                    ft.Container(ft.Text("Speichern"),
                                                                            
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=save_data
                                    ),
                                    ft.Container(ft.Text("Ändern"),
                                        margin=20,                                        
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=email_passwort_ändern
                                    ),         
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Container(ft.Text("Zurück zur Auswahl"),
                                                                                    
                                            alignment=ft.alignment.center,
                                            bgcolor=ft.colors.WHITE,
                                            height = 30,
                                            width=330,
                                            border_radius=10,
                                            on_click=auswahl_button),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                             ),  
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.ORANGE,
                        height = 300,
                        width=350,
                        border_radius=10,
                        ),
                        
                        
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 800,
                    width=1400,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1400/800?{3}",
                    
                    ),
                
            
                    
                ]),
                 
                
            
        )


    class Gespräch:
        def __init__(self, id, name, promt):
            self.id = id
            self.name = name
            self.promt = promt

        def to_string(self):
            return f"{self.id},{self.name},{self.promt} "

        @staticmethod
        def from_string(data):
            id, name, promt = data.split(',')
            return Gespräch(int(id), name, promt)
    
    

        
    
#Anfang speicher_auswahl_button´s

    # Eine Liste, um die Zustände der Speicher-Auswahl-Container-Buttons zu speichern
    container_states = [False] * 10
    # Eine Liste, um die speicher_auswahl_button´s zu speichern
    speicher_auswahl_button = []
    #Die Liste wird mit sechs speicher_auswahl_button´s befüllt
    for i in range(10):
        text = ft.Text(f"{i + 1}")
        container = ft.Container(
            width=54,
            height=30,
            bgcolor="white",
            border_radius=10,
            alignment=ft.alignment.center,
            content=text,
            on_click=lambda e, index=i: on_speicher_slot_click(e, index, dateiname)
        )
        speicher_auswahl_button.append(container)

    def on_speicher_slot_click(e, index, dateiname):
        global speicher_slot_nummer  
             
        # Alle Container auf die Grundfarbe und Flagge zurücksetzen
        for i in range(10):
            if i != index:
                speicher_auswahl_button[i].bgcolor = "white" 
                container_states[i] = False
            else:
                speicher_auswahl_button[i].bgcolor = "blue"
                container_states[i] = True                     
                speicher_slot_nummer = i + 1
                lade_gespraech(dateiname)
                
        
        # Seite neu rendern
        page.update()

    #Ende speicher_auswahl_button´s

    def löschen_vor_speichern(dateiname):
        # Lesen der Datei und speichern aller Zeilen in einer Liste
        with open(dateiname, 'r') as file:
            lines = file.readlines()
            # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

        # Finden der ersten Zeile, die mit '1' beginnt
        line_to_delete = -1
        for index, line in enumerate(lines):
            if line.startswith(str(speicher_slot_nummer)):
                line_to_delete = index
                break

        # Wenn eine solche Zeile gefunden wurde, löschen
        if line_to_delete != -1:
            del lines[line_to_delete]

            # Entsprechendes Gespräch aus der Liste 'gespraeche' löschen
            if line_to_delete < len(gespraeche):
                del gespraeche[line_to_delete]

        # Schreiben der geänderten Zeilen zurück in die Datei
        with open(dateiname, 'w') as file:
            file.writelines(lines)
            # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

    def speichere_gespraeche(gespraeche, dateiname):
        with open(dateiname, 'w') as f:
            for gespraech in gespraeche:
                f.write(gespraech.to_string() + '\n')

    def erstelle_und_speichere_neues_gespraech(e):        
        name = gespraechs_bezeichnung.value
        promt = gespraechs_anweisung.value
        neues_id = speicher_slot_nummer
        neues_gespraech = Gespräch(neues_id, name, promt)        
        gespraeche.append(neues_gespraech)
        löschen_vor_speichern(dateiname)
        speichere_gespraeche(gespraeche, dateiname)
        gespraechs_editor_seite()
        print(gespraeche)             
        return gespraeche

    def ändere_gespraech(gespraeche, gespraech_id, neuer_name, neuer_promt):
        for gespraech in gespraeche:
            if gespraech.id == gespraech_id:
                gespraech.name = neuer_name
                gespraech.promt = neuer_promt
                return gespraeche
        raise ValueError(f"Gespräch mit ID {gespraech_id} nicht gefunden")
    """
    def gespraeche_liste():
        gespraech_liste = []
        for gespraech in gespraeche:
            gespraech_liste.append (gespraech.name)
        return gespraech_liste"""

    def gespraechs_editor_gespraech_starten(e):
        global gespraechs_editor_flag
        gespraechs_editor_flag = True
        klient = person_namen()
        antwort = gespraechs_anweisung.value
        print("gespraechs_anweisung.value = " + gespraechs_anweisung.value)
        print("Antwort = " + antwort)
        
        coaching_video_row, meeting_video_row = Video.video_row()  
        print("coaching_video_row" + str(coaching_video_row))
        shared.stop_flag = False

        page.clean()
        page.add(
            ft.Stack([
                ft.Row([ft.Container(
                    content=ft.Container(
                                ft.Column([
                                    ft.Row([
                                        coaching_video_row,                           

                                    ],alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        ft.Container(
                                                content=ft.Text(
                                                            "Zurück zur Auswahl",
                                                            size=30,
                                                            font_family="Open Sans", 
                                                            color=ft.colors.BLACK
                                                        ),
                                                
                                                #margin=10,
                                                #padding=10,
                                                alignment=ft.alignment.center, 
                                                bgcolor=ft.colors.WHITE38,
                                                height = 50,
                                                width=960,                                    
                                                border_radius=10,
                                                on_click=auswahl_button_coaching,                                       
                                                #image_src = f"https://picsum.photos/900/100?{1}",
                                                ),
                                    ],alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        ft.Container(                                                                       
                                                content = ft.ExpansionPanelList(   
                                                    
                                                    expand_icon_color=ft.colors.AMBER,
                                                    elevation=8,
                                                    divider_color=ft.colors.AMBER,                                                                                                       
                                                    controls=[
                                                        ft.ExpansionPanel(
                                                            header=ft.ListTile(title=ft.Text(f"Dialogfenster",size=30, text_align = ft.TextAlign.CENTER, font_family="Open Sans", color=ft.colors.BLACK)),
                                                            content =                                       
                                                                    ft.Container(
                                                                                                                                                                                                                        
                                                                        height=280, 
                                                                        width=960,
                                                                        bgcolor=ft.colors.WHITE38,
                                                                        border_radius=10,
                                                                        content=ft.Row([cl],vertical_alignment = ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),
                                                                    ) ,
                                            
                                                        
                                                        bgcolor=ft.colors.WHITE38,
                                                        expanded=True,
                                                        ),
                                                    ],
                                                    ),
                                                                               
                                        height=300, 
                                        width=960,
                                        bgcolor=ft.colors.WHITE38,
                                        border_radius=10,
                                        ),
                                    ],alignment=ft.MainAxisAlignment.CENTER,                                    
                                    ),
                                ],alignment=ft.MainAxisAlignment.CENTER), 
                                height=960, 
                                width=1000,
                                bgcolor=ft.colors.WHITE24,
                                border_radius=10,
                                ),             
                            
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 960,
                    width=1800,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1800/960?{1}",
                    
                    )],alignment=ft.MainAxisAlignment.CENTER),                
                          
            ],alignment=ft.MainAxisAlignment.CENTER))
             
        coaching_gespraech(email, passwort, antwort, klient)

    

    def gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2):
        global gespraechs_bezeichnung, gespraechs_anweisung       
        gespraechs_bezeichnung = ft.TextField(label="Gesprächsname", value=inhalt_textfeld_1)
        gespraechs_anweisung = ft.TextField(label="Gesprächs-Promt", value=inhalt_textfeld_2,multiline=True,min_lines=10,
            max_lines=10,)
        
        
        #gespraechs_liste = ft.Dropdown(),  Dropdown ergibt einen error zusammen mit ft.Stack
        
        #ft.TextField(label="Gesprächsliste",value="\n".join(gespraech_liste),multiline=True,min_lines=1,
        #    max_lines=2,)
        page.clean()
        page.add(ft.Stack([
                    ft.Container(
                        ft.Container(
                            ft.Column([
                                ft.Text("Gesprächs-Editor",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            ),
                                gespraechs_bezeichnung, 
                                gespraechs_anweisung,                        
                               # gespraechs_liste,
                                ft.Row(controls=speicher_auswahl_button),
                                ft.Row([
                                    ft.Container(ft.Text("Starten"),
                                                                            
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=gespraechs_editor_gespraech_starten
                                    ),
                                    ft.Container(ft.Text("Laden"),
                                                                            
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=erstelle_und_speichere_neues_gespraech
                                    ),
                                    ft.Container(ft.Text("Speichern"),
                                                                            
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=erstelle_und_speichere_neues_gespraech
                                    ),
                                    ft.Container(ft.Text("Ändern"),
                                                                                
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=150,
                                        border_radius=10,
                                        on_click=email_passwort_ändern
                                    ),         
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                    ft.Container(ft.Text("Zurück zur Auswahl"),
                                                                                    
                                            alignment=ft.alignment.center,
                                            bgcolor=ft.colors.WHITE,
                                            height = 30,
                                            width=330,
                                            border_radius=10,
                                            on_click=auswahl_button),
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                             ),  
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.ORANGE,
                        height = 650,
                        width=650,
                        border_radius=10,
                        ),
                        
                        
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 800,
                    width=1400,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1400/800?{3}",
                    
                    ),
                
            
                    
                ]),
                 
                
            
        )

    def gespraechs_editor_button(e):
        global gespraechs_bezeichnung, gespraechs_anweisung, dateiname, inhalt_textfeld_1, inhalt_textfeld_2 
        global gespraeche
        gespraeche = []        
        dateiname = 'assets/Gespraeche.txt'     
        lade_inhalt_gespraeche_Datei()   
        gespraechs_bezeichnung = ft.TextField(label="Gesprächsname")
        gespraechs_anweisung = ft.TextField(label="Gesprächs-Promt",multiline=True,min_lines=10,
            max_lines=10,)
        inhalt_textfeld_1 = ""
        inhalt_textfeld_2 = ""
        gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2)

    def lade_inhalt_gespraeche_Datei():        
        with open(dateiname, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            gespraeche.append(line)

    def lade_gespraech(dateiname):   
        
        with open(dateiname, 'r') as file:
            lines = file.readlines()
            # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

        for line in lines:
            line_string = ''.join(map(str, line))
            print (line_string)
            if line_string.startswith(str(speicher_slot_nummer)):
                line = line_string.strip()
                if line:
                    gespraech = Gespräch.from_string(line)
                    print(gespraech.name)
                    print(gespraech.promt)
                    inhalt_textfeld_1 = gespraech.name
                    inhalt_textfeld_2 = gespraech.promt
                    gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2)
             
                

    def coaching_gespraech_vorbereitung(email, passwort):
        
        page.clean()
        page.add(ft.Stack([
                    ft.Container(
                        ft.Row ([ft.Container(
                                    ft.Column([
                                        ft.Row ([
                                            ft.Text(
                                            "Wilkommen in der Welt deines Coachee!",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                            ),
                                         ],alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row ([   
                                            ft.Text(
                                            "Dein Klient wird gerade individuell für dich erstellt...dies kann einen Moment dauern...vielen Dank für deine Geduld...",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                            ),
                                        ],alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row ([   
                                            ft.Text(
                                            "Im folgenden einige kleine Hinweise zur Benutzung.",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                            ),
                                        ],alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row ([   
                                            ft.Text(                    
                                            """1. Wenn dein Coachee etwas gesagt hat kann es einige wenige Sekunden dauern bis deine Stimme wieder erkannt
    wird.
2. In jeder deiner Äußerungen sollte der Name des Klienten enthalten sein. Äußerungen ohne den Namen deines 
    Klienten werden nicht an den Klienten weitergeleitet.
3. Solltest du Anregungen zum weiteren Verlauf des Coachings brauchen, sag Hilfe. Dann steht dir die künstliche 
    Intelligenz für alle deine Rückfragen zur Stelle. Nenne dennoch in jeder Anfrage den Namen des Klienten damit 
    sie beantwortet wird.
4. Am Ende des Coaching Gespräches kannst du dir ein Feedback geben lassen. Bitte deinen Klienten einfach um 
    eine Auswertung des Gespräches.
5. Derzeit sind Einzelsitzungen möglich. In folgenden Versionen werden wenn gewünscht auch mehrere Sitzungen 
    mit einem Klienten möglich sein.""",
                                            size=20,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                            ),
                                        ],alignment=ft.MainAxisAlignment.CENTER),
                                    ]),
                                    bgcolor=ft.colors.ORANGE_400, 
                                    blend_mode=50, 
                                    height = 480,
                                    width=1060,
                                    border_radius=10,                             
                                    alignment=ft.alignment.center,
                                ),
                                                        

                        ],alignment=ft.MainAxisAlignment.CENTER),
                          
                        
                    
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 960,
                    width=1800,
                    border_radius=10,                                                           
                    image_src = f"https://picsum.photos/1800/960?{1}",
                    #on_click=coaching_button,                                   
                                       
                    ),
                ]),
                    
                )
        assistant = settings.coachee        
        new_conversation, chatbot = hugchat_initialize(email, passwort, assistant)        
        ramdom_length_number = all_functions.generate_random_number()
        user_input = str(ramdom_length_number)
        antwort = hugchat_assistent(chatbot, user_input, new_conversation)
        return antwort
        
    def coaching_gespraech(email, passwort, antwort, klient):
        global new_conversation, chatbot
        assistant = settings.coaching        
        print(antwort)
        print("gespraechs_editor_flag " + str(gespraechs_editor_flag))
        if gespraechs_editor_flag == False:   
            new_conversation, chatbot = hugchat_initialize(email, passwort, assistant)  
            user_input = antwort + " Du gibst die Person nicht wieder sondern verkörperst sie ab jetzt. Du wartest auf die Begrüßung des Coaches. Du sagst das du " + klient + " heißt, begrüßt den Coach und das du dich auf das Coaching freust und sonst nichts."
        elif gespraechs_editor_flag == True:
            new_conversation, chatbot = hugchat_initialize_no_assistant(email, passwort)
            user_input = antwort + "Du sagst das du " + klient + " heißt"
        sprachsteuerung_coaching(user_input, chatbot, new_conversation)

    def sprachsteuerung_coaching(user_input, chatbot, new_conversation): 
        
        hugchat_assistent_stream(chatbot, user_input, new_conversation)
        
        while shared.stop_flag == False:       
            user_input = all_functions.get_user_input(vosk_recognizer)
            update_input(user_input)
            #user_input = sr_speech_to_text() 
            if shared.stop_flag==False:       
                hugchat_assistent_stream(chatbot, user_input, new_conversation)
    

    def person_namen():
        
        geschlecht = random.choice(shared.geschlecht_list)
        if geschlecht == "maennlich":
            print("Mann")
            person = random.choice(shared.mann_namen_list)
            shared.video_path = shared.list_video_mann
            print(shared.video_path)
            return person
        else:
            print("Frau")
            person = random.choice(shared.frau_namen_list)
            shared.video_path = shared.list_video_frau
            print(shared.video_path)
            return person
        
    def sprachsteuerung(email, passwort, assistant):         
        new_conversation, chatbot = hugchat_initialize(email, passwort, assistant)
        while shared.stop_flag == False:       
            user_input = all_functions.get_user_input(vosk_recognizer)
            #user_input = sr_speech_to_text() 
            if shared.stop_flag==False:       
                hugchat_assistent_stream(chatbot, user_input, new_conversation)
    
    def nichts(e):
        pass

    def auswahlmenue(email, passwort):
       
        zugangsdaten_hinweis = ft.Text("",size=20, color=ft.colors.RED)
        if email == "maxmustermann@max.de" and passwort == "mustermann":
            zugangsdaten_hinweis = ft.Container(ft.Text("Für die Nutzung registriere dich bei https://huggingface.co und gib die Zugangsdaten unter Einstellungen ein!",size=20, color=ft.colors.WHITE),bgcolor=ft.colors.RED, border_radius=10,)    
        images = ft.GridView(
            height = 300,
            width=300,
            expand=3,
            runs_count=5,
            max_extent=100,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        ) 
        
        page.clean()
        for i in range(0, 0):
            images.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/900/300?{i}",
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.add(
            ft.Column([
            
                ft.Container(
                ft.Row([
                    ft.Container(
                    ft.Text(
                            "Conversation Gym",
                            size=100,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.ORANGE_400,
                            weight=ft.FontWeight.NORMAL, 
                            text_align=ft.CrossAxisAlignment.CENTER),

                        height = 150,
                        width=1620,
                        bgcolor=ft.colors.ORANGE_400,
                        alignment=ft.alignment.center,
                        border_radius=10,) ],alignment=ft.MainAxisAlignment.CENTER),                   
                ),
                ft.Container(
                ft.Row([
                    ft.Text(
                            "choose your simulation...",
                            size=40,
                            color=ft.colors.ORANGE_400,                            
                            weight=ft.FontWeight.NORMAL, 
                            text_align=ft.CrossAxisAlignment.CENTER),

                ],alignment=ft.MainAxisAlignment.CENTER),
                ),
                ft.Row([
                    
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Coaching",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260, 
                            border_radius=10,                            
                            alignment=ft.alignment.center,
                            ),
                    
                    margin=10,                    
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=coaching_button,                                       
                    image_src = f"https://picsum.photos/300/600?{1}",
                    ),
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Moderation",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                    margin=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=nichts,                                       
                    image_src = f"https://picsum.photos/300/600?{2}", image_fit ="cover",
                    ),
                ft.Container(
                    content=ft.Container(
                                ft.Column([
                                    ft.Container(
                                        ft.Text(
                                            "Bewerbungs-",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ),
                                    alignment=ft.alignment.center
                                    ),  

                                    ft.Container(
                                        ft.Text(
                                            "gespräch",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ), 
                                    alignment=ft.alignment.center
                                    ) ,                       
                                ]),
                            margin=10,
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                margin=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                height = 600,
                width=300,
                border_radius=10,
                on_click=nichts,                                       
                image_src = f"https://picsum.photos/300/600?{3}", image_fit ="cover",                
                            
                ),
                ft.Container(
                    content=ft.Container(
                                ft.Column([
                                    ft.Container(
                                        ft.Text(
                                            "Gesprächs-",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ),
                                    alignment=ft.alignment.center
                                    ),  

                                    ft.Container(
                                        ft.Text(
                                            "Editor",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ), 
                                    alignment=ft.alignment.center
                                    ) ,                       
                                ]),
                            margin=10,
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                margin=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                height = 600,
                width=300,
                border_radius=10,
                on_click=gespraechs_editor_button,                                       
                image_src = f"https://picsum.photos/300/600?{4}", image_fit ="cover",
                ),
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Einstellungen",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                    margin=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=einstellungen_button,                                       
                    image_src = f"https://picsum.photos/300/600?{5}", image_fit ="cover",
                    ),
                ],alignment=ft.MainAxisAlignment.CENTER),                                     
            ft.Row([zugangsdaten_hinweis],alignment=ft.MainAxisAlignment.CENTER)
           
          ]) 
        )
        
        
        #page.update()

    auswahlmenue(email, passwort)
    
    
         
    
    
    
        

                
    


ft.app(main,assets_dir=all_functions.resource_path("assets"))
#check_hugchat()