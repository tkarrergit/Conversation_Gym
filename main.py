import flet as ft
import time
import all_functions
from all_functions import sr_speech_to_text
import Video
import settings

import shared
import random
import keyboard
import update_conversation_record_container as cr
import hugchat_functions as hf
import auswahlmenue
import button_functions
import utilitys
import vosk_functions
import coaching_gespraech
  
global stimme  


shared.gespraechs_editor_flag = False

shared.email, shared.passwort, vosk_functions.app_starts_count = utilitys.lese_email_passwort()

def check_hugchat():
    newconversation, chatbot = hf.hugchat_initialize(shared.email, shared.passwort, settings.coaching, page)
    print(newconversation and chatbot)
    hf.hugchat_assistent_stream(chatbot, "Wie heißt du", newconversation)


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

    shared.email, shared.passwort, vosk_functions.app_starts_count = utilitys.lese_email_passwort()

    

    app_starts_count = int(vosk_functions.app_starts_count)

    #print(shared.email, shared.passwort)
    if int(vosk_functions.app_starts_count) < int(1) :
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
    
    

    auswahlmenue.auswahlmenue(shared.email, shared.passwort, page)
    
ft.app(main,assets_dir=all_functions.resource_path("assets"))

