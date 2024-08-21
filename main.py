import flet as ft
import time
import all_functions
from all_functions import sr_speech_to_text
import Video
import settings
from  vosk import Model, KaldiRecognizer
import shared
import random
import keyboard
import update_conversation_record_container as cr
import hugchat_functions as hf
import auswahlmenue
import button_functions

#Huggingchat Assistanten Funktion    
global stimme  


#----------Code-Gliederung----------
#1.0    Interne Funktionen                              Konnten aufgrund von doppelten (hinher Import) Importen nicht in all_functions.py.
#2.0    Main Window
#2.1    Funktionen innerhalb der APP
#2.1.1  Coaching Vorbereitung
#2.1.2  Coaching schruftlicher Chatverlauf
#2.2    Auswahlmenue.auswahlmenue
  



"""
def check_hugchat(shared.email, shared.passwort):
    newconversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, settings.coaching)
    print(newconversation and chatbot)
    hf.hugchat_assistent_stream(chatbot, "Wie heißt du", newconversation)
"""

#Stimmauswahl Funktion 
 




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



    

    
    
    def lese_email_passwort(dateiname):
        """
        Liest E-Mail und shared.Passwort aus einer Textdatei.
        
        Args:
            dateiname (str): Name der Textdatei
            
        Returns:
            tuple: E-Mail und shared.Passwort als Tupel
        """
        try:
            with open(dateiname, 'r') as f:
                inhalt = f.readlines()
                shared.email = inhalt[0].strip()
                shared.passwort = inhalt[1].strip()
                shared.app_starts_count = inhalt[2].strip()
            return shared.email, shared.passwort, shared.app_starts_count
        except FileNotFoundError:
            print(f"Datei '{dateiname}' nicht gefunden.")
        except IndexError:
            print("Datei hat nicht das erwartete Format (E-Mail in Zeile 1, shared.Passwort in Zeile 2).")
        except Exception as e:
            print(f"Error: {e}")
    
    """
    shared.email, shared.passwort, shared.app_starts_count= lese_email_passwort("config.txt")
    assistant = settings.coachee
    new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant)
    print(new_conversation)
    print(chatbot)
    print(stimme)
    sprich_stream_chat_satz(chatbot, "Hallo wie geht es dir", new_conversation)

    """
    shared.email, shared.passwort, shared.app_starts_count = lese_email_passwort(all_functions.resource_path("assets/config.txt"))
    shared.app_starts_count = int(shared.app_starts_count)
    #print(shared.email, shared.passwort)
    if shared.app_starts_count < 1 :
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
    

    if shared.app_starts_count < 1 :
        shared.vosk_model_path = shared.smal_model
    else:
        shared.vosk_model_path = shared.big_model
    time.sleep(3)
    model = Model(all_functions.resource_path(shared.vosk_model_path)) #Resource Pfad nutzen wie beim Console Assistent
    vosk_recognizer = KaldiRecognizer(model, 32000)

    #EMAIL und shared.PASSWORT eingabe Anfang

    def email_passwort_field():
        
        if shared.email and shared.passwort:
            email_field = ft.TextField(label="E-Mail",value=shared.email, read_only=True)
            password_field = ft.TextField(label="shared.Passwort", value=shared.passwort, password=True, read_only=True)
            return email_field, password_field
        else:
            email_field = ft.TextField(label="E-Mail")
            password_field = ft.TextField(label="shared.Passwort", password=True)
            return email_field, password_field
        
    email_field = ft.TextField(label="E-Mail")
    password_field = ft.TextField(label="shared.Passwort", password=True)
    
    def email_passwort_ändern(e):
        email_field.value = ""  # Löscht den Inhalt des Email-Feldes
        email_field.read_only = False
        
    
        password_field.value = ""  # Löscht den Inhalt des shared.Passwort-Feldes
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
                                            on_click=button_functions.auswahl_button,)
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

    def save_data(e):#shared.email und shared.passwort
        
        shared.email = email_field.value
        shared.password = password_field.value
        shared.app_starts_count = shared.app_starts_count + 1

        if shared.email and shared.password:
            try:
                with open(all_functions.resource_path("assets/config.txt"), "w") as file:
                    file.write(f"{shared.email}\n{shared.password}\n{shared.app_starts_count}")
                    
                snack_bar = ft.Text("Daten erfolgreich gespeichert!", bgcolor=ft.colors.GREEN)
                page.add(snack_bar)
                all_functions.pyttsx3_tts("Bitte nach dem speichern das Programm neu starten.")
                #shared.email, shared.passwort = lese_email_passwort(all_functions.resource_path("assets/config.txt"))
            except Exception as e:
                snack_bar = ft.Text(f"Fehler beim Speichern: {e}", bgcolor=ft.colors.RED)
                page.add(snack_bar)
        else:            
            snack_bar = ft.Text(f"Bitte E-Mail und shared.Passwort eingeben.", bgcolor=ft.colors.RED)
            page.add(snack_bar)
       
    
    save_button = ft.ElevatedButton("Speichern", on_click=save_data)
    aendern_button = ft.ElevatedButton("Ändern", on_click=email_passwort_ändern)

    #EMAIL und shared.PASSWORT eingabe Ende

    

    

    

    


            

    def coaching_gespraech_vorbereitung():
        
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
        new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant)        
        ramdom_length_number = all_functions.generate_random_number()
        user_input = str(ramdom_length_number)
        antwort = hf.hugchat_assistent(chatbot, user_input, new_conversation)
        return antwort
        
    def coaching_gespraech(antwort, klient):
        global new_conversation, chatbot
        assistant = settings.coaching        
        print(antwort)
        print("gespraechs_editor_flag " + str(gespraechs_editor_flag))
        if gespraechs_editor_flag == False:   
            new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant)  
            user_input = antwort + " Du gibst die Person nicht wieder sondern verkörperst sie ab jetzt. Du wartest auf die Begrüßung des Coaches. Du sagst das du " + klient + " heißt, begrüßt den Coach und das du dich auf das Coaching freust und sonst nichts."
        elif gespraechs_editor_flag == True:
            new_conversation, chatbot = hf.hugchat_initialize_no_assistant(shared.email, shared.passwort)
            user_input = antwort + "Du sagst das du " + klient + " heißt"
        sprachsteuerung_coaching(user_input, chatbot, new_conversation)

    def sprachsteuerung_coaching(user_input, chatbot, new_conversation): 
        
        hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
        
        while shared.stop_flag == False:       
            user_input = all_functions.get_user_input(vosk_recognizer)
            cr.update_input(user_input)
            page.add(cr.cl)
            #user_input = sr_speech_to_text() 
            if shared.stop_flag==False:       
                hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
                page.add(cr.cl)
    

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
        
    def sprachsteuerung(assistant):         
        new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant)
        while shared.stop_flag == False:       
            user_input = all_functions.get_user_input(vosk_recognizer)
            #user_input = sr_speech_to_text() 
            if shared.stop_flag==False:       
                hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
                page.add(cr.cl)
    
        
        
        #page.update()

    auswahlmenue.auswahlmenue(shared.email, shared.passwort)
    
      
 

ft.app(main,assets_dir=all_functions.resource_path("assets"))
#check_hugchat()