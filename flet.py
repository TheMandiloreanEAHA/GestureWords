import flet as ft

def main(page):
    def button_clicked(e):
        if switchVoz.value == True:
            switchVoz.label = ("Interacción con la Voz: Activa")
        else:
             switchVoz.label = ("Interacción con la Voz: Inactiva")
        if switchGes.value == True:
             switchGes.label = ("Interacción con la mano: Activa")
        else:
             switchGes.label = ("Interacción con la mano: Inactiva")
        page.update()

    t = ft.Text()
    switchVoz = ft.Switch(label="Interacción con la Voz: Inactiva", value=False, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz de Voz 
    switchGes = ft.Switch(label="Interacción con la mano: Inactiva", value=False, label_position=ft.LabelPosition.LEFT)#Switch de Interfaz Gestual

    switchVoz.thumb_color={
    ft.MaterialState.HOVERED: ft.colors.GREEN,
    ft.MaterialState.FOCUSED: ft.colors.RED,
    ft.MaterialState.DEFAULT: ft.colors.BLACK,}
   
    btn = ft.ElevatedButton(text="Aplicar", on_click=button_clicked)

    page.add(switchVoz, switchGes, btn, t)

ft.app(target=main)
