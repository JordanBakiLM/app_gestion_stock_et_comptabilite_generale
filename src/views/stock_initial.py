import re
import flet as ft
from base_de_donnee import SQLiteManager
from pdf import PDF

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
            e.control.value = "0"
        else:
            valeur_formatee = "{:,}".format(int(bon)).replace(",", " ")
            e.control.value = valeur_formatee
        e.control.update()

    quantite = ft.TextField(
        value="0",
        label="Quantité",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.RIGHT,
        width=200,
        disabled=True
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
        value="0"
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
                            width=380,
                            style=ft.TextStyle(
                                size=12,
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
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=prix_unitaire.value,
                            width=110,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=to,
                            width=135,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                ]
            )
            
            tableau_stock_initial.rows.append(nouvelle_ligne)
            tableau_stock_initial.update()

            libelle.value = ""
            prix_unitaire.value = "0"

            prix_unitaire.update()
            libelle.update()
            quantite.update()

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
    tt = 0
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
                    width=380,
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
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Pu",
                    text_align=ft.TextAlign.RIGHT,
                    width=110,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Total",
                    text_align=ft.TextAlign.RIGHT,
                    width=135,
                    style=ft.TextStyle(
                        size=15,
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
                            width=380,
                            style=ft.TextStyle(
                                size=12,
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
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][3],
                            width=110,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_stock_initial[i][4],
                            width=135,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
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

    def print_stock_initial():
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)
        
        aa = mois_travail.replace("_", " ")
        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Stock initinial du mois de {aa}", 0, 1, 'L')

        
        #tableau - entete
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(13, 187, 246)
        pdf.set_draw_color(42, 41, 41)

        pdf.ln(5)
        pdf.set_font('ArrialNarrow', 'B', 14)

        pdf.cell(110, 10, 'Libellé', 1, 0, 'L', 1)
        pdf.cell(20, 10, 'Quantité', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'P.U', 1, 0, 'R', 1)
        pdf.cell(35, 10, 'Total', 1, 1, 'R', 1)

        #tableau - contenu
        pdf.set_font('ArrialNarrow', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(42, 41, 41)
        for li in tableau_stock_initial.rows:
            lib = li.cells[0].content.value
            qqq = li.cells[1].content.value
            ppp = li.cells[2].content.value
            ttt = li.cells[3].content.value

            pdf.cell(110, 8, lib, 1, 0, 'L', 1)
            pdf.cell(20, 8, qqq, 1, 0, 'R', 1)
            pdf.cell(25, 8, ppp, 1, 0, 'R', 1)
            pdf.cell(35, 8, ttt, 1, 1, 'R', 1)
        
        pdf.ouvrir_fchier()

    fab_print_container = ft.Container(
        align=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon_color=ft.Colors.SECONDARY,
            icon=ft.Icons.EDIT_DOCUMENT,
            icon_size=30,
            tooltip=ft.Tooltip(
                message="Editer votre stock initial",
            ),
            on_click = print_stock_initial
        ),
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
                fab_print_container                
            ]
        )
    )