import time
import all_functions
import sys
import shared
import Video
import update_conversation_record_container
import re
import auswahlmenue
import vosk_functions

def hugchat_assistent(chatbot, user_input, new_conversation):  
    if user_input:  
        
        starttime = time.time()
        antwort = chatbot.chat(user_input, conversation = new_conversation)
        print("Hallo")    
        print(str(antwort))
        print("Hallo2")
        endtime = time.time()
        duration = endtime -starttime
        print(duration)
        return antwort 
    else:
        antwort = "Leider keinen Input erkannt"
        return antwort 

def hugchat_initialize(email, passwort, assistant, page):
        try:
            chatbot = all_functions.initialize_hugchat(email, passwort,)
            tomconversation = chatbot.new_conversation(assistant=assistant) 
            return tomconversation, chatbot
        except Exception as e:
            all_functions.pyttsx3_tts("Anmeldung fehlgeschlagen. Bitte starten sie die App neu und überprüfen sie ihre Anmeldedaten.")
            auswahlmenue.auswahlmenue(email, passwort, page)

def hugchat_initialize_no_assistant(email, passwort, page):
    try:
        chatbot = all_functions.initialize_hugchat(email, passwort)
        tomconversation = chatbot.new_conversation() 
        return tomconversation, chatbot
    except Exception as e:
        all_functions.pyttsx3_tts("Anmeldung fehlgeschlagen. Bitte starten sie die App neu und überprüfen sie ihre Anmeldedaten.")
        auswahlmenue.auswahlmenue(email, passwort, page)

def hugchat_assistent_stream(chatbot, user_input, newconversation):
    try:           
        sprich_stream_chat_satz(chatbot, user_input, newconversation)
    except:
        print("No Input")

def sprich_stream_chat_satz(chatbot, user_input, conversation, page):
    #Spricht jeden vollständigen Satz der Antwort einen nach dem anderen.
    # Initialisiere eine leere Zeichenkette für den zusammenhängenden Text    
    full_response = ""
    current_sentence = ""
    satzflag = True
    starttime = time.time()
    # Stream response
    print("Hallo sprich_stream_chat_satz for-schleife")
    try: 
        for resp in chatbot._stream_query(
            user_input,                 
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
                        if vosk_functions.stop_flag==False:
                            update_conversation_record_container.update_response(cleaned_sentence, page)
                             
                            Video.play(Video.videos[0])
                            
                
                            all_functions.stimme_auswahl_tts(stimme, cleaned_sentence)

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
                    stimme =shared.stimme
                    all_functions.stimme_auswahl_tts(stimme, "Dein Klient ist gerade nicht erreichbar....versuch es gleich nochmal....")