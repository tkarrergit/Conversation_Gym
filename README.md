# Conversation Gym

**Status:** 
Early Development / Beta Features

**Entwicklungszeitraum:** 
		April, 2024 bis September, 2024

**Technologien:** 
		Python, Flet, Huggchat, Vosk, pyttsx3

---

## **Projektbeschreibung** 
Conversation Gym ist ein Programm, das es Nutzer:innen ermöglicht, professionelle Gesprächssituationen wie z.B. Coaching-Sitzungen, Meetings, Bewerbungsgespräche und Verkaufsgespräche vorab in einer simulierten Umgebung zu trainieren.

Dieses Projekt wurde von mir entwickelt, um die Erstellung von GUI-Anwendungen mit Flet zu üben und um in meiner Ausbildung zum Systemischen-Coach die vielfältigen Methoden und Techniken frühzeitig praxisnah üben zu können. 

Obwohl das Projekt noch unvollständig ist, dient es mir als wertvolles Beispiel für: 
- eine GUI-Anwendung.
- die Einbindung von Videos.
- die Erstellung von Chat-Apps 
- für die Strukturierung eines Projekts.

---
## **Lernfortschritte** 

**Was ich gelernt habe:** 
- Vielfältige Erfahrungen mit dem Flet-Framework zur GUI-Entwicklung.
- Erste Erfahrungen im Einbinden von Videos in eine GUI.
- Wie sinnvoll eine gut strukturiertes Projekt ist. 
- Welchen Aufwand eine nachträgliche Strukturierung bedeutet.
- Erfahrung in der Umwandlung von Projekten in lauffähige Windowsprogramme mit auto-py-to-exe.
- Das es wichtig ist vorher zu bedenken welche sensiblen Daten vom Commit auszuschließen sind.
---
## **Features**
**Aktuell Implementiert:**
##### **Spracherkennung:**
- Offline-Spracherkennung mit VOSK für eine datensparsame und stabile Umsetzung.
##### **Sprachausgabe:**
- Offline-Sprachausgabe mit pyttsx3.
##### **Sprachmodell:**
- Integration über HuggingChat (Soulter/hugging-chat-api) zur potentiellen Nutzung verschiedener Open-Source-Modelle.
##### **Videocall-Simulation:**
  - Simulierte Gesprächspartner werden als Videocalls eingebunden, um die Immersion zu steigern.
##### **Chat-Ansicht:**
- Dokumentation des Dialogverlaufs in einem Chatfenster.
##### **Gesprächseditor:**
- Erstellen individueller Gesprächsszenarien durch Nutzer:innen (derzeit eingeschränkte Funktionalität).

## **Hinweise zur Bibliotheksverwendung** 
Dieses Projekt verwendet huggchat, welches von Zeit zu Zeit Updates bekommt die vorübergehend die Funktionalität stören und ein Update der Bibliothek über **pip install --upgrade huggchat** notwendig macht. Grundsätzlich gilt das natürlich für alle anderen Bibliotheken auch, es kam nur im Entwicklungszeitraum nicht vor.

## **Zukünftige Entwicklungen (Optional)**  
   - Verbesserte Anpassungsmöglichkeiten im Gesprächseditor.
   - Auswahl der Sprachmodelle.
   - Anbindung an eine Datenbank (z.B. sqlite3)
   - Optimierung der Benutzeroberfläche dahingehend das die im Gesprächseditor entworfenen Gespräche automatisch im Auswahlmenü erscheinen.
## Screenshots
![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_1.jpg?raw=true)

![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_2.jpg?raw=true)

![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_3.jpg?raw=true)
