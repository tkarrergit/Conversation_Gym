import flet as ft
import settings
import hugchat_functions as hf
import update_conversation_record_container as cr
import all_functions
import shared
import vosk_functions

            

def coaching_gespraech_vorbereitung(page:ft.Page):    
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
    new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant, page)        
    ramdom_length_number = all_functions.generate_random_number()
    user_input = str(ramdom_length_number)
    antwort = hf.hugchat_assistent(chatbot, user_input, new_conversation)
    return antwort
    
def coaching_gespraech(antwort, klient, page):
    global new_conversation, chatbot
    assistant = settings.coaching        
    print(antwort)
    print("gespraechs_editor_flag " + str(shared.gespraechs_editor_flag))
    if shared.gespraechs_editor_flag == False:   
        new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant, page)  
        user_input = antwort + " Du gibst die Person nicht wieder sondern verkörperst sie ab jetzt. Du wartest auf die Begrüßung des Coaches. Du sagst das du " + klient + " heißt, begrüßt den Coach und das du dich auf das Coaching freust und sonst nichts."
    elif shared.gespraechs_editor_flag == True:
        new_conversation, chatbot = hf.hugchat_initialize_no_assistant(shared.email, shared.passwort, page)
        user_input = antwort + "Du sagst das du " + klient + " heißt"
    sprachsteuerung_coaching(user_input, chatbot, new_conversation, page)

def sprachsteuerung_coaching(user_input, chatbot, new_conversation, page: ft.Page): 
    
    hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
    
    while vosk_functions.stop_flag == False:       
        user_input = vosk_functions.get_user_input(shared.vosk_recognizer)
        cr.update_input(user_input, page)
        page.add(cr.cl)
        #user_input = sr_speech_to_text() 
        if vosk_functions.stop_flag==False:       
            hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
            page.add(cr.cl)



    
def sprachsteuerung(assistant, page:ft.Page):         
    new_conversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, assistant, page)
    while vosk_functions.stop_flag == False:       
        user_input = vosk_functions.get_user_input(shared.vosk_recognizer)
        #user_input = sr_speech_to_text() 
        if vosk_functions.stop_flag==False:       
            hf.hugchat_assistent_stream(chatbot, user_input, new_conversation)
            page.add(cr.cl)