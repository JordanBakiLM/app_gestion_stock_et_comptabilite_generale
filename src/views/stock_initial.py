import re
import flet as ft
from base_de_donnee import SQLiteManager

def stock_initial(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    # libelle
    libelle = ft.TextField(
        label="Libellé",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        width=200,
    )

    # montant
    def on_change_value(e):
        valeur_brute = e.control.value.replace(" ","")
        bon = re.sub(r'\D', '',valeur_brute)                

        if bon == "":
            e.control.value = ""
        else:
            valeur_formatee = "{:,}".format(int(bon)).replace(",", " ")
            e.control.value = valeur_formatee
        e.control.update()

    quantite = ft.TextField(
        label="Quantité",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )

    prix_unitaire = ft.TextField(
        label="Prix unitaire",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=" FCFA",
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )

    #boutton ajouter

    def ouvrir_boite_dialog(titre, message):
        return ft.AlertDialog(
            title=titre,
            content=ft.Text(
                value=message
            )
        )

    def ajout_element_stock_bd(e):
        if libelle.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez entrer le libellé de l'article"))
        elif quantite.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le quantité de l'artice"))
        elif prix_unitaire.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le prix unitaire de l'article"))
        else:
            quantite_si = int(str(quantite.value).replace(" ",""))
            prix_unitaire_si = int(str(prix_unitaire.value).replace(" ",""))
            data = (libelle.value,quantite_si,prix_unitaire_si,mois_travail)
            base_de_donnee.CRUD_stock_initial(0,data)

            e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Elément ajouté avec succès"))

            to = int(quantite.value.replace(" ","")) * int(prix_unitaire.value.replace(" ",""))
            to = "{:,}".format(to).replace(",", " ")
            nouvelle_ligne = ft.DataRow(
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=libelle.value,
                            width=400,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=quantite.value,
                            width=70,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=prix_unitaire.value,
                            width=90,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=to,
                            width=115,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                ]
            )
            
            tableau_stock_initial.rows.append(nouvelle_ligne)

            libelle.value = ""
            quantite.value = ""
            prix_unitaire.value = ""

    bouton_ajout = ft.Button(
        content=ft.Text(
            value="Ajouter",
            expand=True,
            style=ft.TextStyle(
                color=ft.Colors.SECONDARY,
                weight=ft.FontWeight.W_700,
                size=17,
            ),
        ),
        width=200,
        align=ft.Alignment.CENTER,        
        bgcolor=ft.Colors.ON_PRIMARY,        
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=ajout_element_stock_bd
    )

    #bloc ajouut
    bloc_ajout_stock_initial=ft.Container(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.Container(
                    content = ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            libelle,
                            quantite,
                            prix_unitaire,
                            bouton_ajout
                        ],
                    ),
                    padding=ft.Padding.only(bottom=20)
                ),
            ]
        )   
    )


    # ------------------- LISTE
    
    liste_stock_initial = []
    az = base_de_donnee.CRUD_stock_initial(1,(mois_travail,))
    for element in az:
        id = element[0]
        l = element[1]
        q = "{:,}".format(int(element[2])).replace(",", " ")
        pu = "{:,}".format(int(element[3])).replace(",", " ")
        to = int(element[2]) * int(element[3])
        to = "{:,}".format(to).replace(",", " ")
        liste_stock_initial.append((id,l,q,pu,to))

    tableau_stock_initial = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=400,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Qté",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Pu",
                    text_align=ft.TextAlign.RIGHT,
                    width=90,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Total",
                    text_align=ft.TextAlign.RIGHT,
                    width=115,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
        ],
        rows=[
            ft.DataRow(
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][1],
                            width=400,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][2],
                            width=70,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][3],
                            width=90,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][4],
                            width=115,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                ]
            )
            for i in range (len(liste_stock_initial))
        ]
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_stock_initial],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )


    return ft.Container(
        disabled=not(mois_travail==dernier_mois),
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_ajout_stock_initial,
                ft.Divider(),
                container_table,
            ]
        )
    )