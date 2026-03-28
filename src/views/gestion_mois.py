import flet as ft
from datetime import datetime
from base_de_donnee import SQLiteManager
import re

def gestion_mois(base_de_donnee:SQLiteManager):

    # mois
    liste_mois=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Decembre"]

    mois = ft.Dropdown(
        label="Mois",
        options=[ft.DropdownOption(m) for m in liste_mois],
        width=250,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
    )

    # année modif
    annee_modif = ""

    # argent
    def on_change_value(e):
        valeur_brute = e.control.value.replace(" ","")
        bon = re.sub(r'\D', '',valeur_brute)                

        if bon == "":
            e.control.value = ""
        else:
            valeur_formatee = "{:,}".format(int(bon)).replace(",", " ")
            e.control.value = valeur_formatee
        e.control.update()
        
    argent = ft.TextField(
        label="Argent en caisse",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=" FCFA",
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=250,
    )

    #boutton ajouter

    def ouvrir_boite_dialog(titre, message):
        return ft.AlertDialog(
            title=titre,
            content=ft.Text(
                value=message
            )
        )

    def ajout_mois_bd(e):
        if mois.value == None:
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez choisir un mois"))
        elif argent.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner la somme en caisse"))
        else:
            if e.control.content.value == "Ajouter":
                annee_actuelle = datetime.now().year
                mois_annee = f"{mois.value}_{annee_actuelle}"
                argent_mois = int(argent.value.replace(" ",""))
                data = (mois_annee,argent_mois)
                insertion = base_de_donnee.CRU_mois(0,data)

                if insertion == 1:
                    e.control.page.show_dialog(ouvrir_boite_dialog("Ajout", "Votre mois a été ajouté avec succès"))
                    # base_de_donnee.initialisation_classique_mois(mois_annee)
                    # base_de_donnee.initialisation_vente_mois(mois_annee)

                    nouvelle_ligne = ft.DataRow(
                        cells= [
                            ft.DataCell(
                                content=ft.Text(
                                    value=mois.value,
                                    style=ft.TextStyle(
                                        size=16,
                                        weight=ft.FontWeight.W_400,
                                    )
                                )
                            ),
                            ft.DataCell(
                                content=ft.Text(
                                    value=annee_actuelle,
                                    style=ft.TextStyle(
                                        size=16,
                                        weight=ft.FontWeight.W_400,
                                    )
                                )
                            ),
                            ft.DataCell(
                                content=ft.Text(
                                    value=argent.value,
                                    width=150,
                                    text_align=ft.TextAlign.RIGHT,
                                    style=ft.TextStyle(
                                        size=16,
                                        weight=ft.FontWeight.W_400,
                                    )
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                    icon_size=25,
                                    tooltip=ft.Tooltip(
                                        message="",
                                    ) 
                                )
                            )
                        ]
                    )

                    tableau_mois.rows.insert(0,nouvelle_ligne)
                    gestion_modification()


                    mois.value = None
                    mois.update()

                    argent.value = ""
                    argent.update()

                else:
                    e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Le mois que vous avez choisi existe deja pour cette année"))
            else:
                bouton_ajout.content.value = "Ajouter"
                mois.disabled=False
                mois_annee = f"{mois.value}_{annee_modif}"                
                argent_mois = int(argent.value.replace(" ",""))
                data = (mois_annee,argent_mois)
                modification = base_de_donnee.CRU_mois(2,data)

                if modification == 1:
                    e.control.page.show_dialog(ouvrir_boite_dialog("Modification", "Votre mois a été modifié avec succès"))

                    ligne = tableau_mois.rows[0]
                    ligne.cells[2].content.value = argent.value
                    
                    mois.value = None
                    mois.update()

                    argent.value = ""
                    argent.update()


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
        width=250,
        align=ft.Alignment.CENTER,        
        bgcolor=ft.Colors.ON_PRIMARY,        
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=ajout_mois_bd
    )

    #bloc ajouut
    bloc_ajout_mois=ft.Container(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.Container(
                    content = ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            mois,
                            argent,
                            bouton_ajout
                        ],
                    ),
                    padding=ft.Padding.only(bottom=20)
                ),
            ]
        )   
    )


    # ------------------- LISTE MOIS

    def gestion_modification():
        for i in range(len(tableau_mois.rows)):
            if i == 0:
                m = tableau_mois.rows[i].cells[0].content.value
                a = tableau_mois.rows[i].cells[1].content.value
                c = tableau_mois.rows[i].cells[2].content.value
                ic = tableau_mois.rows[i].cells[3].content

                ic.tooltip.message="Modifier le montant de ce mois"
                ic.on_click = lambda e : preparer_modification(m,a,c)                
                
            else:
                ic = tableau_mois.rows[i].cells[3].content
                ic.tooltip.message="Impossible de modifier ce mois"
                ic.disabled=True


    
    def preparer_modification(m,a,c):
        nonlocal annee_modif

        mois.value = m
        argent.value = c
        annee_modif = a
        bouton_ajout.content.value = "Mettre à jour"
        mois.disabled=True


    
    liste_mois = []
    az = base_de_donnee.CRU_mois(1)
    for element in az:
        m = element[0].split("_")[0]
        a = element[0].split("_")[1]
        c = "{:,}".format(int(element[1])).replace(",", " ")
        liste_mois.append((m,a,c))

    liste_mois.reverse()

    tableau_mois = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Mois",
                    width=150,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Année",
                    width=150,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Caisse (FCFA)",
                    text_align=ft.TextAlign.CENTER,
                    width=150,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(ft.Text(" ")),
        ],
        rows=[
            ft.DataRow(
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_mois[i][0],
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value = liste_mois[i][1],
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=(liste_mois[i][2]),
                            width=150,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT_NOTE_ROUNDED,
                            icon_size=25,
                            tooltip=ft.Tooltip(
                                message="",
                            ) 
                        )
                    )
                ]
            )
            for i in range (len(liste_mois))
        ]
    )

    

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_mois],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    gestion_modification()


    return ft.Container(
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_ajout_mois,
                ft.Divider(),
                container_table,
            ]
        )
    )