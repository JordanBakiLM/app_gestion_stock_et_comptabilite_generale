import re
import flet as ft
from base_de_donnee import SQLiteManager

def accueil(base_de_donnee:SQLiteManager, mois_travail):
    def changement_mois():
        base_de_donnee.update_mois_travail(choix_mois.value)

    tous_les_mois = base_de_donnee.get_tous_les_mois()
    choix_mois = ft.Dropdown(
        label="Choix du mois du travail",
        options=[ft.DropdownOption(m) for m in tous_les_mois],
        expand=True,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
        on_text_change=changement_mois
    )

    choix_mois.value = mois_travail

    bloc_choix = ft.Container(
        content=choix_mois,
        width=float('inf'),
    )



    return ft.Container(
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_choix,
                ft.Divider(),
                # bloc_totaux,
                ft.Divider(),
                # bloc_diagramme
            ]
        )
    )