import flet as ft
import keyboard 
import shared
import Video
import all_functions
import auswahlmenue
import settings
import gespraechs_editor
import time
import update_conversation_record_container as cr
import coaching_gespraech
import utilitys

def coaching_button(e, page:ft.Page):
        global gespraechs_editor_flag
        gespraechs_editor_flag  = False   
        antwort = coaching_gespraech.coaching_gespraech_vorbereitung(page) 
        klient = utilitys.person_namen()
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
                                                                    content=ft.Row([cr.cl],vertical_alignment = ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER),
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
             
        coaching_gespraech.coaching_gespraech(antwort, klient, page)

def auswahl_button(e):              
        auswahlmenue.auswahlmenue()

def meeting_button(e, page:ft.Page):
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
        coaching_gespraech.sprachsteuerung(assistant)

def nichts(e):
        pass
        
def auswahl_button_coaching(e, page:ft.Page):
    #user_input = "Gib mir eine Zusammenfassung des Coachinggesprächs. Diese soll die Charakterisierung und die Coachingziele des Klienten und die Ergebnisse des Coachings enthalten."
    #antwort = hf.hugchat_assistent(chatbot, user_input, new_conversation)
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
                on_click=coaching_button(page),                                  
                
                
                ),
            ]),
                
            ),                
                        
        
            
    time.sleep(2)
    
    auswahlmenue.auswahlmenue(shared.email, shared.passwort, page)

def save_data(e, page:ft.Page):#shared.email und shared.passwort
        
        shared.email = shared.email_field.value
        shared.passwort = shared.password_field.value
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

def einstellungen_button(e, page:ft.Page):
        shared.email, shared.passwort, app_starts_count = all_functions.lese_email_passwort()
        email_field, password_field = utilitys.email_passwort_field(shared.email, shared.passwort)

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
                                        on_click=shared.email_shared.passwort_ändern
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

def gespraechs_editor_button(e):
        global gespraechs_bezeichnung, gespraechs_anweisung, dateiname, inhalt_textfeld_1, inhalt_textfeld_2 
        global gespraeche
        gespraeche = shared.gespraeche       
        dateiname = 'assets/Gespraeche.txt'     
        gespraechs_editor.lade_inhalt_gespraeche_Datei()   
        gespraechs_bezeichnung = ft.TextField(label="Gesprächsname")
        gespraechs_anweisung = ft.TextField(label="Gesprächs-Promt",multiline=True,min_lines=10,
            max_lines=10,)
        inhalt_textfeld_1 = ""
        inhalt_textfeld_2 = ""
        gespraechs_editor.gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2)


    #EMAIL und shared.PASSWORT eingabe Anfang
    
def email_passwort_ändern(e, page:ft.Page):
    shared.email_field.value = ""  # Löscht den Inhalt des Email-Feldes
    shared.email_field.read_only = False
    

    shared.password_field.value = ""  # Löscht den Inhalt des shared.Passwort-Feldes
    shared.email_field.read_only = False
    
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
                            shared.email_field, 
                            shared.password_field, 
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
                                        on_click=auswahl_button,)
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
