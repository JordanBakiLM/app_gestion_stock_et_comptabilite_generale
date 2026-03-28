import re
import flet as ft
from base_de_donnee import SQLiteManager

def stock_initial(base_de_donnee:SQLiteManager,mois_travail:str):

    # libelle
    libelle = ft.TextField(
        label="Libellé",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        width=200,
    )

    # id modif
    id_modif = ""

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
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le prix unitair de l'article"))
        else:
            if e.control.content.value == "Ajouter":
                data = (libelle.value,quantite.value,prix_unitaire.value,mois_travail)
                dernier_index = base_de_donnee.CRUD_stock_initial(0,data)

                e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Elément ajouté avec succès"))

                to = int(quantite.value.replace(" ","")) * int(prix_unitaire.value.replace(" ",""))
                to = "{:,}".format(to).replace(",", " ")
                nouvelle_ligne = ft.DataRow(
                    data=dernier_index,
                    cells= [
                        ft.DataCell(
                            content=ft.Text(
                                value=libelle.value,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=quantite.value,
                                width=50,
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
                                width=50,
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
                                width=75,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                    
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                        icon_size=25,
                                        tooltip=ft.Tooltip(
                                            message="Modifier cette ligne",
                                        ),
                                        on_click = lambda e, l=libelle.value, q=quantite.value, pu=prix_unitaire.value, idd=dernier_index : preparer_modification(l,q,pu,idd)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_size=25,
                                        tooltip=ft.Tooltip(
                                            message="Supprimer cette ligne",
                                        ),
                                        # on_click=suppression
                                    )
                                ]
                            )   
                        ),
                    ]
                )
                
                tableau_stock_initial.rows.append(nouvelle_ligne)

                libelle.value = ""
                quantite.value = ""
                prix_unitaire.value = ""

            else:
                bouton_ajout.content.value = "Ajouter"
                data = (libelle.value,quantite.value,prix_unitaire.value,id_modif)
                modification = base_de_donnee.CRUD_stock_initial(2,data)

                if modification == 1:
                    e.control.page.show_dialog(ouvrir_boite_dialog("Modification", "Element modifié avec succès"))

                    for li in tableau_stock_initial.rows:
                        data_ligne = li.data
                        if data_ligne == id_modif:
                            li.cells[0].content.value = libelle.value
                            li.cells[1].content.value = quantite.value
                            li.cells[2].content.value = prix_unitaire.value

                            li.cells[4].content.controls[0].on_click = lambda e, l=libelle.value, q=quantite.value, pu=prix_unitaire.value, idd=id_modif : preparer_modification(l,q,pu,idd)

                            break

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
    bloc_ajout_dette=ft.Container(
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


    # ------------------- LISTE DETTE
    
    def preparer_modification(l,q,pu,idd):
        nonlocal id_modif

        libelle.value = l
        quantite.value = q
        prix_unitaire.value = pu
        id_modif = idd
        bouton_ajout.content.value = "Mettre à jour"

    def suppression(btn):
        def fermeture_dialog(e):
            e.control.page.pop_dialog()

        def sup(e):
            e.control.page.pop_dialog()
            data=(btn.control.data,)
            base_de_donnee.CRUD_dette(3,data)
            for li in tableau_stock_initial.rows:
                bloc_icon = li.cells[2]
                data_ligne = bloc_icon.content.controls[0].data
                if data_ligne == btn.control.data:
                    tableau_stock_initial.rows.remove(li)

                    break
            e.control.page.show_dialog(ouvrir_boite_dialog("Suppréssion", "Suppréssion effectuée avec succès"))

        btn.control.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title='Confirmation',
                content=ft.Text(
                    value='Confirmez-vous cette action?'
                ),
                actions=[
                    ft.TextButton(
                        "Annuler",
                        style=ft.ButtonStyle(
                            color=ft.Colors.SECONDARY
                        ),
                        on_click=fermeture_dialog
                    ),
                    ft.TextButton(
                        "Oui",
                        style=ft.ButtonStyle(
                            color=ft.Colors.SECONDARY
                        ),
                        on_click=sup
                    ),
                ]
                
            )
        )
    
    liste_stock_initial = []
    az = base_de_donnee.CRUD_stock_initial(1,(mois_travail,))
    for element in az:
        id = element[0]
        l = element[1]
        q = element[2]
        pu = element[3]
        to = int(q.replace(" ","")) * int(pu.replace(" ",""))
        to = "{:,}".format(to).replace(",", " ")
        liste_stock_initial.append((id,l,q,pu,to))

    tableau_stock_initial = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=300,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Qté",
                    text_align=ft.TextAlign.CENTER,
                    width=50,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Pu",
                    text_align=ft.TextAlign.CENTER,
                    width=50,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Total",
                    text_align=ft.TextAlign.CENTER,
                    width=75,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(ft.Text(" ")),
        ],
        rows=[
            ft.DataRow(
                data=liste_stock_initial[i][0],
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][1],
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][2],
                            width=50,
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
                            width=50,
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
                            width=75,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                    icon_size=25,
                                    tooltip=ft.Tooltip(
                                        message="Modifier cette ligne",
                                    ),
                                    on_click = lambda e, l=liste_stock_initial[i][1], q=liste_stock_initial[i][2],pu=liste_stock_initial[i][3], idd=liste_stock_initial[i][0] : preparer_modification(l,q,pu,idd)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_size=25,
                                    tooltip=ft.Tooltip(
                                        message="Supprimer cette ligne",
                                    ),
                                    # on_click=suppression
                                )
                            ]
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
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_ajout_dette,
                ft.Divider(),
                container_table,
            ]
        )
    )