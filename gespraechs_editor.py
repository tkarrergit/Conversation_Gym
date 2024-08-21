import flet as ft
import button_functions
import shared
import Video

class Gespräch:
    def __init__(self, id, name, promt):
        self.id = id
        self.name = name
        self.promt = promt

    def to_string(self):
        return f"{self.id},{self.name},{self.promt} "

    @staticmethod
    def from_string(data):
        id, name, promt = data.split(',')
        return Gespräch(int(id), name, promt)



    

#Anfang speicher_auswahl_button´s

# Eine Liste, um die Zustände der Speicher-Auswahl-Container-Buttons zu speichern
container_states = [False] * 10
# Eine Liste, um die speicher_auswahl_button´s zu speichern
speicher_auswahl_button = []
#Die Liste wird mit sechs speicher_auswahl_button´s befüllt
for i in range(10):
    text = ft.Text(f"{i + 1}")
    container = ft.Container(
        width=54,
        height=30,
        bgcolor="white",
        border_radius=10,
        alignment=ft.alignment.center,
        content=text,
        on_click=lambda e, index=i: on_speicher_slot_click(e, index, dateiname)
    )
    speicher_auswahl_button.append(container)

def on_speicher_slot_click(e, index, dateiname, page:ft.Page):
    global speicher_slot_nummer  
            
    # Alle Container auf die Grundfarbe und Flagge zurücksetzen
    for i in range(10):
        if i != index:
            speicher_auswahl_button[i].bgcolor = "white" 
            container_states[i] = False
        else:
            speicher_auswahl_button[i].bgcolor = "blue"
            container_states[i] = True                     
            speicher_slot_nummer = i + 1
            lade_gespraech(dateiname)
            
    
    # Seite neu rendern
    page.update()

#Ende speicher_auswahl_button´s

def löschen_vor_speichern(dateiname):
    # Lesen der Datei und speichern aller Zeilen in einer Liste
    with open(dateiname, 'r') as file:
        lines = file.readlines()
        # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

    # Finden der ersten Zeile, die mit '1' beginnt
    line_to_delete = -1
    for index, line in enumerate(lines):
        if line.startswith(str(speicher_slot_nummer)):
            line_to_delete = index
            break

    # Wenn eine solche Zeile gefunden wurde, löschen
    if line_to_delete != -1:
        del lines[line_to_delete]

        # Entsprechendes Gespräch aus der Liste 'gespraeche' löschen
        if line_to_delete < len(gespraeche):
            del gespraeche[line_to_delete]

    # Schreiben der geänderten Zeilen zurück in die Datei
    with open(dateiname, 'w') as file:
        file.writelines(lines)
        # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

def speichere_gespraeche(gespraeche, dateiname):
    with open(dateiname, 'w') as f:
        for gespraech in gespraeche:
            f.write(gespraech.to_string() + '\n')

def erstelle_und_speichere_neues_gespraech(e):        
    name = gespraechs_bezeichnung.value
    promt = gespraechs_anweisung.value
    neues_id = speicher_slot_nummer
    neues_gespraech = Gespräch(neues_id, name, promt)        
    gespraeche.append(neues_gespraech)
    löschen_vor_speichern(dateiname)
    speichere_gespraeche(gespraeche, dateiname)
    gespraechs_editor_seite()
    print(gespraeche)             
    return gespraeche

def ändere_gespraech(gespraeche, gespraech_id, neuer_name, neuer_promt):
    for gespraech in gespraeche:
        if gespraech.id == gespraech_id:
            gespraech.name = neuer_name
            gespraech.promt = neuer_promt
            return gespraeche
    raise ValueError(f"Gespräch mit ID {gespraech_id} nicht gefunden")
"""
def gespraeche_liste():
    gespraech_liste = []
    for gespraech in gespraeche:
        gespraech_liste.append (gespraech.name)
    return gespraech_liste"""

def gespraechs_editor_gespraech_starten(e, page:ft.Page):
    global gespraechs_editor_flag
    gespraechs_editor_flag = True
    klient = person_namen()
    antwort = gespraechs_anweisung.value
    print("gespraechs_anweisung.value = " + gespraechs_anweisung.value)
    print("Antwort = " + antwort)
    
    coaching_video_row, meeting_video_row = Video.video_row()  
    print("coaching_video_row" + str(coaching_video_row))
    shared.stop_flag = False

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
                                            on_click=button_functions.auswahl_button_coaching,                                       
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
            
    coaching_gespraech(shared.email, shared.passwort, antwort, klient)



def gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2):
    global gespraechs_bezeichnung, gespraechs_anweisung       
    gespraechs_bezeichnung = ft.TextField(label="Gesprächsname", value=inhalt_textfeld_1)
    gespraechs_anweisung = ft.TextField(label="Gesprächs-Promt", value=inhalt_textfeld_2,multiline=True,min_lines=10,
        max_lines=10,)
    
    
    #gespraechs_liste = ft.Dropdown(),  Dropdown ergibt einen error zusammen mit ft.Stack
    
    #ft.TextField(label="Gesprächsliste",value="\n".join(gespraech_liste),multiline=True,min_lines=1,
    #    max_lines=2,)
    page.clean()
    page.add(ft.Stack([
                ft.Container(
                    ft.Container(
                        ft.Column([
                            ft.Text("Gesprächs-Editor",
                                        size=20,
                                        color=ft.colors.WHITE,
                                        ),
                            gespraechs_bezeichnung, 
                            gespraechs_anweisung,                        
                            # gespraechs_liste,
                            ft.Row(controls=speicher_auswahl_button),
                            ft.Row([
                                ft.Container(ft.Text("Starten"),
                                                                        
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.WHITE,
                                    height = 30,
                                    width=150,
                                    border_radius=10,
                                    on_click=gespraechs_editor_gespraech_starten
                                ),
                                ft.Container(ft.Text("Laden"),
                                                                        
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.WHITE,
                                    height = 30,
                                    width=150,
                                    border_radius=10,
                                    on_click=erstelle_und_speichere_neues_gespraech
                                ),
                                ft.Container(ft.Text("Speichern"),
                                                                        
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.WHITE,
                                    height = 30,
                                    width=150,
                                    border_radius=10,
                                    on_click=erstelle_und_speichere_neues_gespraech
                                ),
                                ft.Container(ft.Text("Ändern"),
                                                                            
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.WHITE,
                                    height = 30,
                                    width=150,
                                    border_radius=10,
                                    on_click=email_passwort_ändern
                                ),         
                            ],alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([
                                ft.Container(ft.Text("Zurück zur Auswahl"),
                                                                                
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.WHITE,
                                        height = 30,
                                        width=330,
                                        border_radius=10,
                                        on_click=button_functions.auswahl_button),
                            ],alignment=ft.MainAxisAlignment.CENTER),
                            
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),  
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.ORANGE,
                    height = 650,
                    width=650,
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



def lade_inhalt_gespraeche_Datei():        
    with open(dateiname, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        gespraeche.append(line)

def lade_gespraech(dateiname):   
    
    with open(dateiname, 'r') as file:
        lines = file.readlines()
        # Die Datei wird automatisch geschlossen, wenn der 'with'-Block endet

    for line in lines:
        line_string = ''.join(map(str, line))
        print (line_string)
        if line_string.startswith(str(speicher_slot_nummer)):
            line = line_string.strip()
            if line:
                gespraech = Gespräch.from_string(line)
                print(gespraech.name)
                print(gespraech.promt)
                inhalt_textfeld_1 = gespraech.name
                inhalt_textfeld_2 = gespraech.promt
                gespraechs_editor_seite(inhalt_textfeld_1, inhalt_textfeld_2)
            
    