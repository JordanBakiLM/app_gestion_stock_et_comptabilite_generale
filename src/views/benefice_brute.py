import flet as ft
from base_de_donnee import SQLiteManager
from pdf import PDF

def benefice_brute(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    bb = base_de_donnee.benefice_brut(mois_travail)

    totaux = [0,0,0,0]

    for b in bb:
        totaux[0] = totaux[0] + b[2]
        totaux[1] = totaux[1] + b[3]
        totaux[2] = totaux[2] + b[4]

    # ------------------- LISTE
    tableau_benefice_brute = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=205,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Qte vendue.",
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
                    value="C. d'affaire",
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
                    value="C. revient",
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
                    value="Benef br.",
                    text_align=ft.TextAlign.RIGHT,
                    width=100,
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
                            value=bb[i][0],
                            width=205,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(bb[i][1])).replace(",", " "),
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
                            value="{:,}".format(int(bb[i][2])).replace(",", " "),
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(bb[i][3])).replace(",", " "),
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(bb[i][4])).replace(",", " "),
                            width=100,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    )
                ]
            )
            for i in range (len(bb))
        ]
    )

    tableau_benefice_brute.rows.append(
        ft.DataRow(
            cells= [
                ft.DataCell(
                    content=ft.Text(
                        value="TOTAUX",
                        width=205,
                        style=ft.TextStyle(
                            size=13,
                            weight=ft.FontWeight.W_600,
                        )
                    )
                ),
                ft.DataCell(
                    content=ft.Text(
                        value="",
                        width=70,
                        text_align=ft.TextAlign.RIGHT,
                        style=ft.TextStyle(
                            size=13,
                            weight=ft.FontWeight.W_400,
                            
                        )
                    )
                ),
                ft.DataCell(
                    content=ft.Text(
                        value="{:,}".format(int(totaux[0])).replace(",", " "),
                        width=100,
                        text_align=ft.TextAlign.RIGHT,
                        style=ft.TextStyle(
                            size=13,
                            weight=ft.FontWeight.W_600,
                        )
                    )
                ),
                ft.DataCell(
                    content=ft.Text(
                        value="{:,}".format(int(totaux[1])).replace(",", " "),
                        width=100,
                        text_align=ft.TextAlign.RIGHT,
                        style=ft.TextStyle(
                            size=13,
                            weight=ft.FontWeight.W_600,
                        )
                    )
                ),
                ft.DataCell(
                    content=ft.Text(
                        value="{:,}".format(int(totaux[2])).replace(",", " "),
                        width=100,
                        text_align=ft.TextAlign.RIGHT,
                        style=ft.TextStyle(
                            size=13,
                            weight=ft.FontWeight.W_600,
                        )
                    )
                )
            ]
        )
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_benefice_brute],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    def print_benef_brute():
        # données du tableau

        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)

        
        aa = mois_travail.replace("_", " ")
        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Bénéfice brute du mois de {aa}", 0, 1, 'L')

        
        #tableau - entete
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(13, 187, 246)
        pdf.set_draw_color(42, 41, 41)

        pdf.ln(5)
        pdf.set_font('ArrialNarrow', 'B', 14)

        pdf.cell(95, 10, 'Libellé', 1, 0, 'L', 1)
        pdf.cell(20, 10, 'Q. vend', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'C. Affaire', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'C. Revient', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Bénéf B', 1, 1, 'R', 1)

        #tableau - contenu
        pdf.set_font('ArrialNarrow', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(42, 41, 41)

        taille_tableau = len(tableau_benefice_brute.rows)
        for li in tableau_benefice_brute.rows:
            taille_tableau = taille_tableau - 1

            lib = li.cells[0].content.value
            qv = li.cells[1].content.value
            ca = li.cells[2].content.value
            cr = li.cells[3].content.value
            bb = li.cells[4].content.value
   
            if taille_tableau != 0 :
                pdf.cell(95, 8, lib, 1, 0, 'L', 1)
                pdf.cell(20, 8, str(qv), 1, 0, 'R', 1)
                pdf.cell(25, 8, str(ca), 1, 0, 'R', 1)
                pdf.cell(25, 8, str(cr), 1, 0, 'R', 1)
                pdf.cell(25, 8, str(bb), 1, 1, 'R', 1)
            else:
                pdf.set_font('ArrialNarrow', 'B', 13)
                pdf.cell(115, 8, lib, 1, 0, 'L', 1)
                pdf.cell(25, 8, str(ca), 1, 0, 'R', 1)
                pdf.cell(25, 8, str(cr), 1, 0, 'R', 1)
                pdf.cell(25, 8, str(bb), 1, 1, 'R', 1)
        
        pdf.ouvrir_fchier()


    fab_print_container = ft.Container(
        align=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon_color=ft.Colors.SECONDARY,
            icon=ft.Icons.EDIT_DOCUMENT,
            icon_size=30,
            tooltip=ft.Tooltip(
                message="Editer le bénéfice brute",
            ),
            on_click = print_benef_brute
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