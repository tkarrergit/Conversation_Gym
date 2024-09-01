import shared
import random
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
        
def email_passwort_field():
        
        if shared.email and shared.passwort:
            email_field = ft.TextField(label="E-Mail",value=shared.email, read_only=True)
            password_field = ft.TextField(label="shared.Passwort", value=shared.passwort, password=True, read_only=True)
            return email_field, password_field
        else:
            email_field = ft.TextField(label="E-Mail")
            password_field = ft.TextField(label="shared.Passwort", password=True)
            return email_field, password_field
        

def lese_email_passwort():
        """
        Liest E-Mail und shared.Passwort aus einer Textdatei.
        
        Args:
            dateiname (str): Name der Textdatei
            
        Returns:
            tuple: E-Mail und shared.Passwort als Tupel
        """
        try:
            with open(shared.dateiname_config, 'r') as f:
                inhalt = f.readlines()
                shared.email = inhalt[0].strip()
                shared.passwort = inhalt[1].strip()
                shared.app_starts_count = inhalt[2].strip()
            return shared.email, shared.passwort, shared.app_starts_count
        except FileNotFoundError:
            print(f"Datei '{shared.dateiname_config}' nicht gefunden.")
        except IndexError:
            print("Datei hat nicht das erwartete Format (E-Mail in Zeile 1, shared.Passwort in Zeile 2).")
        except Exception as e:
            print(f"Error: {e}")