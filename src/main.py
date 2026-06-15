import os

import flet as ft
import style
import base_de_donnee
from generateur_passe import Generateur_MDP
from views import accueil, consultation, stock_initial, approvisionement, ventes, recapitulatif, benefice_brute, dettes

base_de_donnees = base_de_donnee.SQLiteManager()


def main(page: ft.Page):
    page.title = "Salcom Compta"
    page.padding = 0

    page.window = ft.Window(
        width=1265,
        min_width=1265,
        height=700,
        min_height=700,
        
    )

    dossier_utilisateur = os.path.expanduser("~")
    chemin_fichier_pdf = os.path.join(dossier_utilisateur, "DocumentsSa", "suiviStock_CG", "doc_pdf")
    os.makedirs(chemin_fichier_pdf, exist_ok=True)

    Generateur_MDP.set_mot_de_passe()

    for f in os.listdir(chemin_fichier_pdf):
        try:
            os.remove(f"{chemin_fichier_pdf}\\{f}")
        except Exception as e:
            print(e)

    # page.

    page.fonts = {
        "Montserrat" : "/police/Montserrat/Montserrat.ttf"
    }

    page.theme = style.theme_clair
    page.dark_theme = style.theme_sombre

    theme_bd = base_de_donnees.get_theme()
    page.theme_mode = ft.ThemeMode.DARK if theme_bd==0 else ft.ThemeMode.LIGHT
    
    base_de_donnees.creation_table()

    style_clic_1 = ft.TextStyle(
        font_family='Montserrat',
        size=18,
        weight=ft.FontWeight.W_900,
        color=ft.Colors.ON_PRIMARY
    )

    def style_icon_clic_1(ic:ft.IconData):
        return ft.Icon(
            ic,
            color=ft.Colors.ON_PRIMARY,
            size=30
        )
    
    def changer_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon=ft.Icons.LIGHT_MODE
            base_de_donnees.maj_theme(0)
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon=ft.Icons.DARK_MODE
            base_de_donnees.maj_theme(1)
        
        page.update()

    def style_defaut_btn():
        def style_icon_defaut_1(ic:ft.IconData):
            return ft.Icon(
                ic,
                color="#FFFFFF",
                size=25
            )
        style_defaut_1 = ft.TextStyle(
            font_family='Montserrat',
            size=15,
            weight=ft.FontWeight.W_500,
            color="#FFFFFF"
        )
        
        #CONSULTATION
        container_consultation.content.title.style=style_defaut_1
        container_consultation.content.leading = style_icon_defaut_1(ft.Icons.FIND_IN_PAGE)

        #STOCK
        container_gestion_de_stock.content.title.style=style_defaut_1
        container_gestion_de_stock.content.leading = style_icon_defaut_1(ft.Icons.INVENTORY)
        container_gestion_de_stock.content.icon_color=ft.Colors.WHITE
        container_gestion_de_stock.content.collapsed_icon_color="#FFFFFF"
        
        for lt in container_gestion_de_stock.content.controls:
            lt.title.style.color ="#FFFFFF"
            lt.title.style.weight=ft.FontWeight.W_400

        #COMPTABILITE
        container_comptabilite.content.title.style=style_defaut_1
        container_comptabilite.content.leading = style_icon_defaut_1(ft.Icons.ACCOUNT_BALANCE)
        container_comptabilite.content.icon_color=ft.Colors.WHITE
        container_comptabilite.content.collapsed_icon_color="#FFFFFF"

        for lt in container_comptabilite.content.controls:
            lt.title.style.color ="#FFFFFF"
            lt.title.style.weight=ft.FontWeight.W_400

        #MOIS
        container_gestion_mois.content.title.style=style_defaut_1
        container_gestion_mois.content.leading = style_icon_defaut_1(ft.Icons.HOME_ROUNDED)

    def clic_btn_menu(e,indice_btn:int):
        style_defaut_btn()
        mois_travail = base_de_donnees.get_mois_travail()
        if mois_travail == -1:
            if indice_btn != 8:
                page.show_dialog(
                    ft.AlertDialog(
                        title="Erreur",
                        content=ft.Text(
                            value="Veuilez d'abord enrégistrer un mois de travail"
                        )
                    )
                )
                current_expanded["active"] = None
                container_gestion_de_stock.content.expanded = (current_expanded["active"] == "stock")
                container_comptabilite.content.expanded = (current_expanded["active"] == "compta")

                container_gestion_mois.content.title.style=style_clic_1
                container_gestion_mois.content.leading = style_icon_clic_1(ft.Icons.HOME_ROUNDED)
                container_principal.content = accueil.accueil(base_de_donnees)
        else:
            if indice_btn == 1:
                container_consultation.content.title.style=style_clic_1
                container_consultation.content.leading = style_icon_clic_1(ft.Icons.FIND_IN_PAGE)
                
                container_principal.content = consultation.consultation(base_de_donnees,mois_travail)
            elif indice_btn == 2:
                container_gestion_de_stock.content.title.style=style_clic_1
                container_gestion_de_stock.content.leading = style_icon_clic_1(ft.Icons.INVENTORY)
                
                container_gestion_de_stock.content.controls[0].title.style.color = ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.controls[0].title.style.weight = ft.FontWeight.W_600
                container_gestion_de_stock.content.icon_color=ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.collapsed_icon_color=ft.Colors.ON_PRIMARY

                current_expanded["active"] = None
                container_gestion_de_stock.content.expanded = (current_expanded["active"] == "stock")
                container_comptabilite.content.expanded = (current_expanded["active"] == "compta")

                container_principal.content = stock_initial.stock_initial(base_de_donnees,mois_travail)
            elif indice_btn == 3:
                container_gestion_de_stock.content.title.style=style_clic_1
                container_gestion_de_stock.content.leading = style_icon_clic_1(ft.Icons.INVENTORY)
                
                container_gestion_de_stock.content.controls[1].title.style.color = ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.controls[1].title.style.weight = ft.FontWeight.W_600
                container_gestion_de_stock.content.icon_color=ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.collapsed_icon_color=ft.Colors.ON_PRIMARY
                
                container_principal.content = approvisionement.approvisionement(base_de_donnees,mois_travail)
            elif indice_btn == 4:
                container_gestion_de_stock.content.title.style=style_clic_1
                container_gestion_de_stock.content.leading = style_icon_clic_1(ft.Icons.INVENTORY)
                
                container_gestion_de_stock.content.controls[2].title.style.color = ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.controls[2].title.style.weight = ft.FontWeight.W_600
                container_gestion_de_stock.content.icon_color=ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.collapsed_icon_color=ft.Colors.ON_PRIMARY
                
                container_principal.content = ventes.ventes(base_de_donnees,mois_travail)
            elif indice_btn == 5:
                container_gestion_de_stock.content.title.style=style_clic_1
                container_gestion_de_stock.content.leading = style_icon_clic_1(ft.Icons.INVENTORY)
                
                container_gestion_de_stock.content.controls[3].title.style.color = ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.controls[3].title.style.weight = ft.FontWeight.W_600
                container_gestion_de_stock.content.icon_color=ft.Colors.ON_PRIMARY
                container_gestion_de_stock.content.collapsed_icon_color=ft.Colors.ON_PRIMARY
                
                container_principal.content = recapitulatif.recupitulatif(base_de_donnees,mois_travail)
            elif indice_btn == 6:
                container_comptabilite.content.title.style=style_clic_1
                container_comptabilite.content.leading = style_icon_clic_1(ft.Icons.ACCOUNT_BALANCE)

                container_comptabilite.content.controls[0].title.style.color = ft.Colors.ON_PRIMARY
                container_comptabilite.content.controls[0].title.style.weight = ft.FontWeight.W_600
                container_comptabilite.content.icon_color=ft.Colors.ON_PRIMARY
                container_comptabilite.content.collapsed_icon_color=ft.Colors.ON_PRIMARY
                
                container_principal.content = benefice_brute.benefice_brute(base_de_donnees,mois_travail)
            elif indice_btn == 7:
                container_comptabilite.content.title.style=style_clic_1
                container_comptabilite.content.leading = style_icon_clic_1(ft.Icons.ACCOUNT_BALANCE)

                container_comptabilite.content.controls[1].title.style.color = ft.Colors.ON_PRIMARY
                container_comptabilite.content.controls[1].title.style.weight = ft.FontWeight.W_600
                container_comptabilite.content.icon_color=ft.Colors.ON_PRIMARY
                container_comptabilite.content.collapsed_icon_color=ft.Colors.ON_PRIMARY
                
                container_principal.content = dettes.dettes(base_de_donnees,mois_travail)
            elif indice_btn == 8:
                container_gestion_mois.content.title.style=style_clic_1
                container_gestion_mois.content.leading = style_icon_clic_1(ft.Icons.HOME_ROUNDED)
                container_principal.content = accueil.accueil(base_de_donnees)

            current_expanded["active"] = None
            container_gestion_de_stock.content.expanded = (current_expanded["active"] == "stock")
            container_comptabilite.content.expanded = (current_expanded["active"] == "compta")
    
    current_expanded = {"active" : None}
    def logique_deroulement(e, menu:str):
        if e.control.expanded == True:
            current_expanded["active"] = menu
        else:
            if current_expanded["active"] == menu:
                current_expanded["active"] = None
        
        container_gestion_de_stock.content.expanded = (current_expanded["active"] == "stock")
        container_comptabilite.content.expanded = (current_expanded["active"] == "compta")
        e.control.page.update()

    container_logo = ft.Container(
        content=ft.Image(
            src="LOGO.png",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        align=ft.Alignment.CENTER,
        padding=ft.Padding.only(top=10,bottom=10,left=5,right=5),
    )
    
    container_consultation = ft.Container(
        content = ft.ListTile(
            title=ft.Text(
                "CONSULTATION",
                style=ft.TextStyle(
                    font_family='Montserrat',
                    size=15,
                    weight=ft.FontWeight.W_500,
                    color="#FFFFFF"
                ),
                no_wrap=True
            ),
            leading=ft.Icon(
                ft.Icons.FIND_IN_PAGE,
                color="#FFFFFF",
                size=25
            ),
            on_click=lambda e : clic_btn_menu(e,1)
        ),
        padding=ft.Padding.only(bottom=5),
    )

    container_gestion_de_stock = ft.Container(
        content = ft.ExpansionTile(
            on_change=lambda e : logique_deroulement(e,'stock'),
            leading=ft.Icon(
                ft.Icons.INVENTORY,
                color="#FFFFFF"
            ),
            icon_color=ft.Colors.TRANSPARENT,
            collapsed_icon_color=ft.Colors.TRANSPARENT,
            
            bgcolor=ft.Colors.WHITE_10,
            title=ft.Text(
                "G. DE STOCK",
                style=ft.TextStyle(
                    font_family='Montserrat',
                    size=15,
                    weight=ft.FontWeight.W_500,
                    color="#FFFFFF"
                ),
                no_wrap=True
            ),
            controls=[
                ft.ListTile(
                    title=ft.Text(
                        "S. INITIAL",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,2),
                    content_padding=ft.Padding(left=50)
                ),
                ft.ListTile(
                    title=ft.Text(
                        "APPRO.",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,3),
                    content_padding=ft.Padding(left=50)
                ),
                ft.ListTile(
                    title=ft.Text(
                        "VENTES",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,4),
                    content_padding=ft.Padding(left=50)
                ),
                ft.ListTile(
                    title=ft.Text(
                        "RECAPITULATIF",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,5),
                    content_padding=ft.Padding(left=50)
                ),  
            ],
        ),
        padding=ft.Padding.only(bottom=5),
    )

    container_comptabilite = ft.Container(
        content = ft.ExpansionTile(
            on_change=lambda e : logique_deroulement(e,'compta'),
            leading=ft.Icon(
                ft.Icons.ACCOUNT_BALANCE,
                color="#FFFFFF",
                size=25
            ),
            icon_color=ft.Colors.TRANSPARENT,
            collapsed_icon_color=ft.Colors.TRANSPARENT,
            
            bgcolor=ft.Colors.WHITE_10,
            title=ft.Text(
                "COMPTABILITE",
                style=ft.TextStyle(
                    font_family='Montserrat',
                    size=15,
                    weight=ft.FontWeight.W_500,
                    color="#FFFFFF"
                ),
                no_wrap=True
            ),
            controls=[
                ft.ListTile(
                    title=ft.Text(
                        "B. BRUTE",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,6),
                    content_padding=ft.Padding(left=50)
                ),
                ft.ListTile(
                    title=ft.Text(
                        "DETTES",
                        style=ft.TextStyle(
                            font_family='Montserrat',
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color="#FFFFFF"
                        ),
                        no_wrap=True
                    ),
                    on_click=lambda e : clic_btn_menu(e,7),
                    content_padding=ft.Padding(left=50)
                ),  
            ],
        ),
        padding=ft.Padding.only(bottom=5),
    )

    container_gestion_mois = ft.Container(
        content = ft.ListTile(
            title=ft.Text(
                "ACCUEIL",
                style=ft.TextStyle(
                    font_family='Montserrat',
                    size=15,
                    weight=ft.FontWeight.W_500,
                    color="#FFFFFF"
                ),
                no_wrap=True
            ),
            leading=ft.Icon(
                ft.Icons.HOME_ROUNDED,
                color="#FFFFFF",
                size=25
            ) ,
            on_click=lambda e : clic_btn_menu(e,8)
        )
    )

    container_mode = ft.Container(
        content=ft.IconButton(
            icon = ft.Icons.LIGHT_MODE if theme_bd==0 else ft.Icons.DARK_MODE,
            on_click=changer_theme
        ),
        padding=ft.Padding.only(bottom=20,left=10)
    )
    
    bloc_logo_menu = ft.Container(
        # bgcolor=ft.Colors.PRIMARY,
        width=270,
        content=ft.Column(
            controls=[
                container_logo,
                container_gestion_mois,
                container_gestion_de_stock,
                container_comptabilite,
                container_consultation,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )
    
    min_width_menu = 50
    expand_width_menu = 270
    
    def agrandissement(e):
        bloc_lateral.width = expand_width_menu if e.data == True else min_width_menu
        bloc_lateral.update()

        if e.data == False:
            container_gestion_de_stock.content.collapsed_icon_color = ft.Colors.TRANSPARENT
            container_comptabilite.content.collapsed_icon_color = ft.Colors.TRANSPARENT
        else:
            container_gestion_de_stock.content.collapsed_icon_color = container_gestion_de_stock.content.title.style.color
            container_comptabilite.content.collapsed_icon_color = container_comptabilite.content.title.style.color

        current_expanded["active"] = None
        container_gestion_de_stock.content.expanded = (current_expanded["active"] == "stock")
        container_comptabilite.content.expanded = (current_expanded["active"] == "compta")

        container_comptabilite.update()
        container_gestion_de_stock.update()     

    bloc_lateral = ft.Container(
        bgcolor=ft.Colors.PRIMARY,
        width=min_width_menu,
        animate=ft.Animation(400,ft.AnimationCurve.DECELERATE),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        on_hover=lambda e : agrandissement(e),
        content=ft.Column(
            controls=[
                bloc_logo_menu,
                container_mode
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )

    container_principal = ft.Container(
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        alignment=ft.Alignment.TOP_CENTER,
        expand=True,
        padding=ft.Padding.only(left=90,top=20,bottom=20,right=20)
    )

    layout = ft.Stack(
        controls = [
            container_principal,
            bloc_lateral
        ],
        expand=True,
    )

    container_gestion_mois.content.title.style=style_clic_1
    container_gestion_mois.content.leading = style_icon_clic_1(ft.Icons.HOME_ROUNDED)
    container_principal.content = accueil.accueil(base_de_donnees)
    
    page.add(
        layout
    )


ft.run(main,view=ft.AppView.FLET_APP)
