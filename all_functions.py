from hugchat import hugchat
from hugchat.login import Login
import speech_recognition as sr
import time
import pyaudio
import json

import random
import sys
import Video
import pyttsx3
import flet as ft
from  vosk import Model, KaldiRecognizer





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
        return email, passwort
    except FileNotFoundError:
        print(f"Datei '{dateiname}' nicht gefunden.")
    except IndexError:
        print("Datei hat nicht das erwartete Format (E-Mail in Zeile 1, Passwort in Zeile 2).")

def schreibe_email_passwort(dateiname, email, passwort):
    """
    Schreibt E-Mail und Passwort in eine Textdatei.
    
    Args:
        dateiname (str): Name der Textdatei
        email (str): E-Mail-Adresse
        passwort (str): Passwort
    """
    try:
        with open(dateiname, 'w') as f:
            f.write(email + "\n")
            f.write(passwort)
        print(f"E-Mail und Passwort wurden in '{dateiname}' geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben in die Datei: {e}")

def resource_path(relative_path):
    import os
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        #PyInstaller creates a temp folder and stores path in MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generate_random_number():
    # Bestimme zufällig die Anzahl der Ziffern (1 bis 1000)
    num_digits = random.randint(1, 1000)
    # Erzeuge die erste Ziffer (1-9) damit die Zahl nicht mit 0 anfängt
    first_digit = random.randint(1, 9)
    # Erzeuge die restlichen Ziffern (0-9)
    remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    # Kombiniere die erste Ziffer mit den restlichen Ziffern
    random_number = str(first_digit) + remaining_digits    
    return random_number


        
def initialize_hugchat(email, passwd):    
    try:
        print("initialize_hugchat: " + email + passwd)
        # Cookies im lokalen Verzeichnis speichern
        cookie_path_dir = (resource_path("./cookies_snapshot")   )         
        # Einloggen bei Huggingface und Autorisieren von HugChat
        sign = Login(email, passwd)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        
        # Create your ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

        return chatbot
    except Exception as e:
        print(f"Fehler bei der Initialisierung von Huggingface: {e}")
        return None

#chatbot = initialize_hugchat(hugchat.email, hugchat.passwd)

def no_stream_chat(chatbot, user_input, conversation):
    # Non stream response
    query_result_no_stream = chatbot.chat(user_input, conversation)
    print(query_result_no_stream) # or query_result.text or query_result["text"]

def stream_chat(chatbot, user_input):
    # Stream response
    for resp in chatbot.query(
        user_input,
        stream=True
    ):
        print(resp)

def web_chat(chatbot, user_input):
    # Web search (new feature)
    query_result_web = chatbot.query(user_input, web_search=True)
    print(query_result_web)
    for source in query_result_web.web_search_sources:
        print(source.link)
        print(source.title)
        print(source.hostname)

def hugchat_new_conversation(chatbot):
    # Create a new conversation
    chatbot.new_conversation(switch_to = True) # switch to the new conversation
    
    print("New Conversation with Hugchat")

def all_conversation_list(chatbot):
    # Get conversations on the server that are not from the current session (all your conversations in huggingchat)
    conversation_list = chatbot.get_remote_conversations(replace_conversation_list=True)
    print(conversation_list)

def local_conversation_list(chatbot):
    # Get conversation list(local)
    conversation_list = chatbot.get_conversation_list()   
    print(conversation_list)

def get_hugchat_models(chatbot):
    # Get the available models (not hardcore)
    models = chatbot.get_available_llm_models()
    
    print(models)

def switch_to_hugchat_model(chatbot, index):
    # Switch model with given index
    chatbot.switch_llm(index) # Switch to the first model index = 0 # Switch to the second model Index = 1 usw.
    #print("Switched to Model mit Index= " + index)

def get_info_current_conversation(chatbot):
    # Get information about the current conversation
    info = chatbot.get_conversation_info()
    print(info.id, info.title, info.model, info.system_prompt, info.history)

def hugchat_assistent_list(chatbot):
    assistant_list = chatbot.get_assistant_list_by_page(page=0)
    print(assistant_list)

def new_conversation_assistent(chatbot, assistent_name):
    # Assistant
    assistant = chatbot.search_assistant(assistant_name=assistent_name) # assistant name list in https://huggingface.co/chat/assistants 
    print(assistant)       
    chatbot.new_conversation(assistant=assistant, switch_to=True) # create a new conversation with assistant
    print("New Conversation with Assistent: " + assistent_name)

def delete_all_hugchat_conversations(chatbot):
    input= input("Do you realy want to delete all coversations?Y/N")
    if input == "Y":
        input= input("Do you reeeeaaaaaaaly want to delete all coversations?yes/No")
        if input == "Yes":
            # [DANGER] Delete all the conversations for the logged in user
            chatbot.delete_all_conversations()
            print("All Conversation deleted")
        else:
            pass
    else:
        print("No Conversation deleted")


            
def sr_speech_to_text():
    # Erstelle ein Recognizer-Objekt
    r = sr.Recognizer()
    text_flag = False
    while True:
        
        if text_flag == False:
            # Nehme Audio vom Mikrofon auf
            starttime = time.time()
            with sr.Microphone() as source:
                print("Sprich etwas:")                 
                start_time = time.time()
                try:
                    audio = r.listen(source, timeout=1, phrase_time_limit=10)                    
                except sr.WaitTimeoutError:
                    print("Zeitüberschreitung bei der Audioaufnahme.")
                    continue
                except:
                    print("Unerwarteter Fehler bei der Audioaufnahme.")
                    continue
                

            # Erkenne Sprache mithilfe von Google Speech Recognition
            try:                
                text = r.recognize_google(audio, language="de-DE")
                print("Du hast gesagt: " + text)
                endtime = time.time()
                duration= endtime-starttime
                print("spracheingabe Dauer: " + str(duration))
                if text:
                    text_flag = True
                    return text
            except sr.UnknownValueError:
                print("Tut mir leid, ich habe das nicht verstanden.")
            except sr.RequestError as e:
                print("Fehler bei der Spracherkennung; {0}".format(e))
        if text_flag == True:
            break

"""
#from google.cloud import texttospeech

def google_Cloud_tts(antwort, language_code='de-DE', voice_name=None, output_file='output.mp3'):
    
    #Konvertiert den gegebenen Text in Sprache und speichert sie in einer Datei.
    
    #Args:
        #text (str): Der Text, der in Sprache umgewandelt werden soll.
        #language_code (str, optional): Der Sprachcode. Standardmäßig ist es Deutsch ('de-DE').
        #voice_name (str, optional): Der Name der gewünschten Stimme. Standardmäßig wird die Standardstimme verwendet.
        #output_file (str, optional): Der Name der Ausgabedatei. Standardmäßig ist es 'output.mp3'.
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=antwort)

    # Konfiguration der Stimme
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name  # Name der gewünschten Stimme
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)


#from gtts import gTTS

def gtts_tts(antwort, language='de'):
    
    #Konvertiert den gegebenen Text in Sprache und spielt ihn ab.
    
    #Args:
       # text (str): Der Text, der in Sprache umgewandelt werden soll.
        #language (str, optional): Die Sprache, in die der Text umgewandelt werden soll. Standardmäßig ist es Deutsch ('de').
    
    # Text-to-Speech-Objekt erstellen
    tts = gTTS(text=antwort, lang=language, slow=False)

    # Datei speichern
    tts.save("output.mp3")

    # Datei abspielen
    play_sound('output.wav')


from TTS.api import TTS
#models:
#ganz schlecht:
#tts_models/de/thorsten/tacotron2-DCA
#gut:
#tts_models/de/thorsten/vits
#tts_models/de/thorsten/tacotron2-DDC
#schecht:
#tts_models/de/css10/vits-neon

def coqui_tts(antwort):
    print("coqui_tts ankunft")
    tts = TTS(model_name='tts_models/de/thorsten/tacotron2-DDC')
    tts.tts_to_file(text=antwort)
    

    
    import pygame

    def play_sound(sound_file):
        
        #Spielt einen Ton über den Pygame-Mixer ab.
        
        #Args:
        #    sound_file (str): Der Dateipfad der Tondatei, die abgespielt werden soll.
        
        # Initialisiere den Pygame-Mixer
        pygame.mixer.init()
        
        try:
            # Lade die Tondatei
            sound = pygame.mixer.Sound(sound_file)
            
            # Spiele den Ton ab
            sound.play()
            
            # Warte, bis der Ton fertig ist
            while pygame.mixer.get_busy():
                continue
        
        except pygame.error as e:
            print(f"Fehler beim Abspielen des Tons: {e}")
        
        finally:
            # Beende den Pygame-Mixer
            pygame.mixer.quit()
    play_sound('output.wav')


#coqui_tts("Hallo ich bin dein Klient. Ich freue mich dich kennen zu lernen. Schoen bei dir zu sein.")
"""



def get_voices_list():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print (str(voices))

def pyttsx3_tts(antwort):    
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    #alle stimmen abrufen
    voices = engine.getProperty('voices')    
    # Set the voice properties
    engine.setProperty('rate', 200)  # Speech rate (words per minute)
    engine.setProperty('pitch', 2.0)  #change the pitch (0.0 - 2.0; 1.0 is default)
    engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
    engine.setProperty('voice', 'de')  # Voice language (en, es, fr, etc.)
    engine.setProperty('voice', voices[0].id) #0 deutsch; 1 englisch; 2 englisch; 3 spanisch; 4 spanisch;
            
    print("Antwort: " + antwort)  
    #Video.play(Video.videos[1])
    # Speak the text    
    engine.say(antwort)    
    
    # Wait until the speech is finished
    engine.runAndWait()  
    #Video.pause(Video.videos[1]) 
    #Video.seek(Video.videos[1])
    
    print("Tschüß pyttsx3")

def stimme_auswahl_tts(stimme, antwort):
    print(stimme)
    """
    if stimme =="gtts":
        gtts_tts(antwort, language='de')
    elif stimme == "coqui_tts":
        coqui_tts(antwort)
    elif stimme == "google_cloud_tts":
        google_Cloud_tts(antwort, language_code='de-DE', voice_name=None, output_file='output.mp3')
    """
    if stimme == "pyttsx3":
        print(Video.videos)
        #Video.play(Video.videos[3])
        pyttsx3_tts(antwort)
        #Video.seek(Video.videos[3])
        #Video.pause(Video.videos[3])
#pyttsx3_tts("Hallo du da")

