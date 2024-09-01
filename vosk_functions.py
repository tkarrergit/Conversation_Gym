import pyaudio
from  vosk import Model, KaldiRecognizer
import all_functions
import time
import json
import utilitys

app_starts_count = int(0)

smal_model = "assets/vosk-model-small-de-zamia-0.3"
big_model = "assets/vosk-model-de-0.21"
#big Model"assets/vosk-model-de-0.21"
vosk_model_path = smal_model

stop_flag = False


def vosk_model_init():
        if app_starts_count < 1 :
            vosk_model_path = smal_model
        else:
            vosk_model_path = big_model
        time.sleep(3)
        model = Model(utilitys.resource_path(vosk_model_path)) #Resource Pfad nutzen wie beim Console Assistent
        vosk_recognizer = KaldiRecognizer(model, 32000)
        return vosk_recognizer

def Vosk_Voice_to_text(vosk_recognizer):
    
    cap = pyaudio.PyAudio()
    stream = cap.open(input=True, format=pyaudio.paInt16, channels=1, rate=32000, frames_per_buffer=2048)
    stream.start_stream()
    
    # Verwenden des Mikrofons zum Aufnehmen von Audio
    while True:
        starttime = time.time()
        data = stream.read(4096)
        if vosk_recognizer.AcceptWaveform(data):
            text = vosk_recognizer.Result()
            result = json.loads(text)
            vosktext = result['text']
            
            print(f"Erkannter Text: {vosktext}")
            endtime = time.time()
            duration = endtime-starttime
            print (" Voskerkennung Dauer : " + str(duration) )          
            return vosktext

#'Words to remove von get_user_input(vosk_recognizer)'
words_to_remove = ["laura", "marie", "anna", "lena", "hanna", "emma","paul", "lukas", "leon", "max", "simon", "tim", "david"]

def get_user_input(vosk_recognizer):
    
    while stop_flag == False:
        
        while stop_flag == False:
            
            input_text = Vosk_Voice_to_text(vosk_recognizer)  # Make sure Vosk_Voice_to_text returns the recognized text
            
            if input_text:
                print(input_text)
                
                print(f"Erkannter Text: {input_text}", 1, "left")  # Füge diese Debugging-Ausgabe hinzu
                print("\033[F\033[K", end="")
                time.sleep(2)
                break  # Exit the loop if there is valid input

        input_text_lower = input_text.lower()

        if any(word in input_text_lower for word in words_to_remove):
            # Use a list comprehension to remove the specified words

            text = ' '.join(word for word in input_text.split() if word.lower() not in words_to_remove)
            return text
            #return True