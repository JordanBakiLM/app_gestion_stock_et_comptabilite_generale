import re
import flet as ft
from base_de_donnee import SQLiteManager
from pdf import PDF

def dettes(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    # ------------------- LISTE
    
    def validation_paiement(e):
        def fermeture_dialog(az):
            az.control.page.pop_dialog()

        def modification(az):
            base_de_donnee.CRUD_ventes(2,(0,"SALCOM",mois_travail,int(e.control.data)),)
            tableau_dettes.rows.remove(e.control.parent.parent)
            tableau_dettes.update()
            fermeture_dialog(az)
        
        e.control.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title="Confirmation",
                content=ft.Text("Confirmez-vous cette action, elle est irréverssible ?"),
                actions=[
                    ft.TextButton(
                        "Annuler",
                        style=ft.ButtonStyle(
                            color=ft.Colors.SECONDARY
                        ),
                        on_click=fermeture_dialog
                    ),
                    ft.TextButton(
                        "OUI",
                        style=ft.ButtonStyle(
                            color=ft.Colors.SECONDARY
                        ),
                        on_click = lambda e : modification(e)
                    ),
                ]
                
            )
        )
    
    liste_dettes = []
    az = base_de_donnee.CRUD_ventes(1,(" ",1))
    for element in az:
        id_de = element[0]
        l = element[1]
        q = "{:,}".format(int(element[2])).replace(",", " ")
        to = int(q.replace(" ","")) * int(element[3])
        to = "{:,}".format(to).replace(",", " ")
        cre = element[7]
        liste_dettes.append((cre,l,q,to,id_de))

    tableau_dettes = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Créancier",
                    width=150,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Article",
                    text_align=ft.TextAlign.LEFT,
                    width=280,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
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
                    value="Total",
                    text_align=ft.TextAlign.RIGHT,
                    width=100,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="",
                    text_align=ft.TextAlign.RIGHT,
                    width=20,
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
                            value=liste_dettes[i][0],
                            width=150,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_dettes[i][1],
                            width=280,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_dettes[i][2],
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
                            value=liste_dettes[i][3],
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.IconButton(
                            icon=ft.Icons.MONEY,
                            tooltip="Valider le paiement de la dette",
                            on_click=validation_paiement,
                            data=liste_dettes[i][4]
                        )
                    )
                ]
            )
            for i in range (len(liste_dettes))
        ]
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_dettes],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    def print_dette():
        # données du tableau

        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)

        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Liste des créanciers du departement", 0, 1, 'L')

        
        #tableau - entete
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(13, 187, 246)
        pdf.set_draw_color(42, 41, 41)

        pdf.ln(5)
        pdf.set_font('ArrialNarrow', 'B', 14)

        pdf.cell(55, 10, 'Créancier', 1, 0, 'L', 1)
        pdf.cell(80, 10, 'Article', 1, 0, 'L', 1)
        pdf.cell(25, 10, 'Qté', 1, 0, 'R', 1)
        pdf.cell(30, 10, 'Total', 1, 1, 'R', 1)

        #tableau - contenu
        pdf.set_font('ArrialNarrow', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(42, 41, 41)

        for li in tableau_dettes.rows:

            cre = li.cells[0].content.value
            art = li.cells[1].content.value
            qqq = li.cells[2].content.value
            ttt = li.cells[3].content.value
   
            pdf.cell(55, 8, cre, 1, 0, 'L', 1)
            pdf.cell(80, 8, str(art), 1, 0, 'L', 1)
            pdf.cell(25, 8, str(qqq), 1, 0, 'R', 1)
            pdf.cell(30, 8, str(ttt), 1, 1, 'R', 1)

        
        pdf.ouvrir_fchier()

    fab_print_container = ft.Container(
        align=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon_color=ft.Colors.SECONDARY,
            icon=ft.Icons.EDIT_DOCUMENT,
            icon_size=30,
            tooltip=ft.Tooltip(
                message="Editer la liste des créancier",
            ),
            on_click = print_dette
        ),
    )


    return ft.Container(
        disabled=not(mois_travail==dernier_mois),
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                container_table,
                fab_print_container
            ]
        )
    )