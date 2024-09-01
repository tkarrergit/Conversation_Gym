import flet as ft
import button_functions

def auswahlmenue(email, passwort, page:ft.Page):
       
        zugangsdaten_hinweis = ft.Text("",size=20, color=ft.colors.RED)
        if email == "maxmustermann@max.de" and passwort == "mustermann":
            zugangsdaten_hinweis = ft.Container(ft.Text("Für die Nutzung registriere dich bei https://huggingface.co und gib die Zugangsdaten unter Einstellungen ein!",size=20, color=ft.colors.WHITE),bgcolor=ft.colors.RED, border_radius=10,)    
        images = ft.GridView(
            height = 300,
            width=300,
            expand=3,
            runs_count=5,
            max_extent=100,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        ) 
        
        page.clean()
        for i in range(0, 0):
            images.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/900/300?{i}",
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.add(
            ft.Column([
            
                ft.Container(
                ft.Row([
                    ft.Container(
                    ft.Text(
                            "Conversation Gym",
                            size=100,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.ORANGE_400,
                            weight=ft.FontWeight.NORMAL, 
                            text_align=ft.CrossAxisAlignment.CENTER),

                        height = 150,
                        width=1620,
                        bgcolor=ft.colors.ORANGE_400,
                        alignment=ft.alignment.center,
                        border_radius=10,) ],alignment=ft.MainAxisAlignment.CENTER),                   
                ),
                ft.Container(
                ft.Row([
                    ft.Text(
                            "choose your simulation...",
                            size=40,
                            color=ft.colors.ORANGE_400,                            
                            weight=ft.FontWeight.NORMAL, 
                            text_align=ft.CrossAxisAlignment.CENTER),

                ],alignment=ft.MainAxisAlignment.CENTER),
                ),
                ft.Row([
                    
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Coaching",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260, 
                            border_radius=10,                            
                            alignment=ft.alignment.center,
                            ),
                    
                    margin=10,                    
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=lambda _: button_functions.coaching_button(_, page),                                       
                    image_src = f"https://picsum.photos/300/600?{1}",
                    ),
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Moderation",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                    margin=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=button_functions.nichts,                                       
                    image_src = f"https://picsum.photos/300/600?{2}", image_fit ="cover",
                    ),
                ft.Container(
                    content=ft.Container(
                                ft.Column([
                                    ft.Container(
                                        ft.Text(
                                            "Bewerbungs-",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ),
                                    alignment=ft.alignment.center
                                    ),  

                                    ft.Container(
                                        ft.Text(
                                            "gespräch",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ), 
                                    alignment=ft.alignment.center
                                    ) ,                       
                                ]),
                            margin=10,
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                margin=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                height = 600,
                width=300,
                border_radius=10,
                on_click=button_functions.nichts,                                       
                image_src = f"https://picsum.photos/300/600?{3}", image_fit ="cover",                
                            
                ),
                ft.Container(
                    content=ft.Container(
                                ft.Column([
                                    ft.Container(
                                        ft.Text(
                                            "Gesprächs-",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ),
                                    alignment=ft.alignment.center
                                    ),  

                                    ft.Container(
                                        ft.Text(
                                            "Editor",                                
                                            size=40,
                                            color=ft.colors.WHITE,
                                            text_align = ft.MainAxisAlignment.CENTER,
                                        ), 
                                    alignment=ft.alignment.center
                                    ) ,                       
                                ]),
                            margin=10,
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                margin=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                height = 600,
                width=300,
                border_radius=10,
                on_click=button_functions.gespraechs_editor_button,                                       
                image_src = f"https://picsum.photos/300/600?{4}", image_fit ="cover",
                ),
                ft.Container(
                    content=ft.Container(ft.Text(
                                "Einstellungen",
                                size=40,
                                color=ft.colors.WHITE,
                                text_align = ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.colors.ORANGE_400, 
                            blend_mode=50, 
                            height = 130,
                            width=260,
                            border_radius=10,                             
                            alignment=ft.alignment.center,
                            ),

                    margin=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    height = 600,
                    width=300,
                    border_radius=10,
                    on_click=button_functions.einstellungen_button,                                       
                    image_src = f"https://picsum.photos/300/600?{5}", image_fit ="cover",
                    ),
                ],alignment=ft.MainAxisAlignment.CENTER),                                     
            ft.Row([zugangsdaten_hinweis],alignment=ft.MainAxisAlignment.CENTER)
           
          ]) 
        )
        