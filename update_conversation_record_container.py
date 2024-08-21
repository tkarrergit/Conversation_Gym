import flet as ft




cl = ft.Column(
            alignment= ft.MainAxisAlignment.START,
            horizontal_alignment =  ft.CrossAxisAlignment.CENTER,          
            spacing=15,
            height=200,
            width=960,
            scroll=ft.ScrollMode.ALWAYS,   
    )

def update_response(output, page:ft.Page):
    cl.controls.append(
        ft.Container(
            content=ft.TextField(
                value=output, 
                label="Klient", 
                label_style= ft.TextStyle(
                                    size=16, 
                                    color=ft.colors.BLACK,
                                    font_family="Open Sans"), 
                text_style= ft.TextStyle(
                                    size=14, 
                                    font_family="Open Sans", 
                                    color=ft.colors.BLACK), 
                        bgcolor=ft.colors.BLUE_100, 
                        width=800, 
                        multiline=True, 
                        border_radius=10
                    ), margin=ft.margin.only(left=100),
            width=800,
        )
    )
    cl.auto_scroll = True
    page.add(cl)
    

def update_input(input, page:ft.Page):
    cl.controls.append(
        ft.Container(
            content=ft.TextField(
                        value=input, label="Coach", label_style= ft.TextStyle(size=16, color=ft.colors.BLACK, font_family="Open Sans"), 
                        text_style= ft.TextStyle(size=14, font_family="Open Sans", color=ft.colors.BLACK), 
                                            bgcolor=ft.colors.BLUE_50, width=800, multiline=True, border_radius=10), margin=ft.margin.only(right=100),
            width=800,
        )
    )
    cl.auto_scroll = True
    page.add(cl)    