# Conversation Gym

**Status:** 
Early Development / Beta Features

**Entwicklungszeitraum:** 
		April, 2024 bis September, 2024

**Technologien:** 
- **Python** – Hauptsprache des Projekts, ideal für die schnelle Entwicklung und Flexibilität.
- **Flet** – Framework zur Entwicklung von interaktiven GUIs, mit dem ich fortgeschrittene Benutzeroberflächen realisiere.
- **Vosk** – Offline-Spracherkennung für eine datenschutzfreundliche und zuverlässige Sprachinteraktion.
- **Pyttsx3** – Offline-Sprachausgabe, ermöglicht eine realistische und interaktive Kommunikation mit dem Benutzer.
- **HuggingChat** (Soulter/hugging-chat-api) – Integration eines Open-Source-Sprachmodells, das vielseitige Einsatzmöglichkeiten in künftigen Weiterentwicklungen des Projekts bietet.
---

## **Projektbeschreibung** 
**Conversation Gym** ist eine Anwendung, die es Nutzer:innen ermöglicht, berufliche Gesprächssituationen wie Coaching-Sitzungen, Bewerbungsgespräche und Meetings zu simulieren und zu trainieren. Diese Anwendung nutzt fortschrittliche Technologien wie Spracherkennung und Sprachmodell-Integration, um eine realistische und interaktive Übungserfahrung zu bieten. 

Dieses Projekt wurde von mir entwickelt, um die Erstellung von GUI-Anwendungen mit Flet zu üben und um in meiner Ausbildung zum Systemischen-Coach die vielfältigen Methoden und Techniken frühzeitig praxisnah üben zu können.

Obwohl das Projekt noch unvollständig ist, dient es mir als wertvolles Beispiel für: 
- eine GUI-Anwendung.
- die Einbindung von Videos.
- die Erstellung von Chat-Apps 
- für die Strukturierung eines Projekts.

---
## **Lernfortschritte** 

**Was ich gelernt habe:** 
- Erweiterte Kenntnisse im **Flet-Framework** zur **GUI-Entwicklung** und der Gestaltung interaktiver Benutzeroberflächen.
- Erste praktische Erfahrungen im **Einbinden von Videos** in eine GUI und die Erstellung von **Chat-Anwendungen**.
- Vertiefte Kenntnisse in der **Integration von Spracherkennungs- (Vosk) und Sprachausgabe-Tools (pyttsx3)** für datenschutzfreundliche Anwendungen.
- Wertvolle Erfahrungen in der **Strukturierung und Organisation von Code** sowie im Umgang mit **Versionierung und Bibliotheksmanagement** (z. B. durch das Update von Bibliotheken wie huggchat).
- Erfahrung in der **Umwandlung von Python-Projekten in ausführbare Windows-Programme** mit **auto-py-to-exe**.
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
- Dieses Projekt nutzt **huggchat**, welches gelegentlich Updates benötigt, die die Funktionalität vorübergehend beeinträchtigen können. Ein Update der Bibliothek erfolgt über pip install --upgrade huggchat.
- Weitere Updates von verwendeten Bibliotheken sind ebenfalls regelmäßig erforderlich. (siehe Requirements.txt)

## **Zukünftige Entwicklungen (Optional)**  
- Erweiterte Anpassungsmöglichkeiten im Gesprächseditor, um eine vollständigere Anpassung von Gesprächsszenarien zu ermöglichen.
- Einführung von verschiedenen Sprachmodellen zur Verbesserung der Gesprächsführung und der Interaktivität.
- Anbindung an eine Datenbank (z. B. SQLite), um die Verwaltung von Nutzerdaten und Gesprächsverläufen zu ermöglichen.
- Optimierung der Benutzeroberfläche, sodass erstellte Gespräche direkt im Auswahlmenü des Gesprächseditors angezeigt werden können.
## Screenshots
![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_1.jpg?raw=true)

![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_2.jpg?raw=true)

![image](https://github.com/tkarrergit/Conversation_Gym/blob/main/Coversation_Gym_Screenshot_3.jpg?raw=true)
