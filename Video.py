import flet as ft
import random
import shared


def play(video):        
    video.play()
        

def pause(video):    
    video.pause()
    

def seek(video):   
    video.seek(-100000)
    

def stop(video):    
    video.stop()
    
    




def assign_numbers(num_men, num_women):
    available_numbers = list(range(1, 10))
    men_numbers = []
    women_numbers = []
    
    for _ in range(num_men):
        if available_numbers:
            number = random.choice(available_numbers)
            men_numbers.append(number)
            available_numbers.remove(number)
    
    for _ in range(num_women):
        if available_numbers:
            number = random.choice(available_numbers)
            women_numbers.append(number)
            available_numbers.remove(number)
    
    return men_numbers, women_numbers
videos_card = []
videos = []

def video_row():
    print("3: " + str(shared.video_path))
    


    num_men = 5
    num_women = 4
    men_numbers, women_numbers = assign_numbers(num_men, num_women)


    
    
    for i in range(1, 10):
        
        print("hallo for " + str(i))
        if i == int("1"):
            video_path = shared.video_path
            print("4: " + str(video_path))
        elif i in men_numbers and not "2":
            video_path = shared.list_video_mann
            print("5: " + str(video_path))
        elif i in women_numbers and not "2":
            video_path = shared.list_video_frau
            print("6: " + str(video_path))
        else:
            # Hier könntest du eine Standardaktion definieren,
            # wenn keine Zuordnung gefunden wird.
            video_path = shared.list_video_frau
            print("7: " + str(video_path))
        
        video = ft.Video(
            expand=True,
            playlist=[video_path],
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.WHITE38,
            aspect_ratio=1 / 1,
            filter_quality="high",
            autoplay=False,
            muted=True
        )
        
        card = ft.Card(
            elevation=30,
            content=ft.Container(
                bgcolor=ft.colors.WHITE38,
                padding=10,
                border_radius=ft.border_radius.all(20),                
                content=(video := video)
            ) , width=960, height=540,
        )
        
        videos_card.append(card)
        videos.append(video)
    print("End: " + str(video_path))
    coaching_video_row = ft.Row([                       
                        videos_card[0],     
                    ],alignment=ft.MainAxisAlignment.CENTER,)

    meetig_video_row = ft.Row(                      
                        videos_card
                    ,width=160, height=90,)
    
    return coaching_video_row, meetig_video_row
        

video_big = ft.Container(
            
                content=ft.Row([
                    ft.Card(
                        elevation=30,
                        content=ft.Container(
                                bgcolor=ft.colors.WHITE,
                                padding=10,
                                border_radius = ft.border_radius.all(20),                    
                                content=ft.Video(
                                        expand=True,
                                        playlist=shared.list_video_mann,                                        
                                        fill_color="white",
                                        aspect_ratio=1 / 1,
                                        filter_quality="high",
                                        autoplay=False,
                                        muted=True       

                                                
                    
                                )                    
                        ), width=640, height=360
                    )
                ],alignment=ft.MainAxisAlignment.CENTER,)
        
                )

 

    