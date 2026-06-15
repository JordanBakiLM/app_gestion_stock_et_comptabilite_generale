import flet as ft
from base_de_donnee import SQLiteManager
from pdf import PDF

def recupitulatif(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    stock = base_de_donnee.stock(mois_travail)

    # ------------------- LISTE
    tableau_rcapitulatif_stock = ft.DataTable(
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
                    value="SI",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="App",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. E",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Ven.",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Det.",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. S",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="SF",
                    text_align=ft.TextAlign.RIGHT,
                    width=50,
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
                            value=stock[i][1],
                            width=205,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][2])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][3])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][4])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_700,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][5])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][6])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][5] + stock[i][6])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_700,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value="{:,}".format(int(stock[i][7])).replace(",", " "),
                            width=50,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=10,
                                weight=ft.FontWeight.W_700,
                            )
                        )
                    ),
                ]
            )
            for i in range (len(stock))
        ]
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_rcapitulatif_stock],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    def print_recapitulatif():
        # données du tableau

        pdf = PDF('L', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_paysage.png", 10, 10, 277)
        
        aa = mois_travail.replace("_", " ")
        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Récapitulatif du stock du mois de {aa}", 0, 1, 'L')

        
        #tableau - entete
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(13, 187, 246)
        pdf.set_draw_color(42, 41, 41)

        pdf.ln(5)
        pdf.set_font('ArrialNarrow', 'B', 14)

        pdf.cell(102, 10, 'Libellé', 1, 0, 'L', 1)
        pdf.cell(25, 10, 'S. init.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'App.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Total E.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Ventes', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Dettes.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Total s.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'S. final', 1, 1, 'R', 1)

        #tableau - contenu
        pdf.set_font('ArrialNarrow', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(42, 41, 41)
        for li in tableau_rcapitulatif_stock.rows:
            lib = li.cells[0].content.value
            si = li.cells[1].content.value
            ap = li.cells[2].content.value
            te = li.cells[3].content.value
            ve = li.cells[4].content.value
            de = li.cells[5].content.value
            ts = li.cells[6].content.value
            sf = li.cells[7].content.value


            pdf.cell(102, 8, lib, 1, 0, 'L', 1)
            pdf.cell(25, 8, str(si), 1, 0, 'R', 1)
            pdf.cell(25, 8, str(ap), 1, 0, 'R', 1)

            pdf.set_font('ArrialNarrow', 'B', 12)
            pdf.cell(25, 8, str(te), 1, 0, 'R', 1)
            pdf.set_font('ArrialNarrow', '', 12)


            pdf.cell(25, 8, str(ve), 1, 0, 'R', 1)
            pdf.cell(25, 8, str(de), 1, 0, 'R', 1)

            pdf.set_font('ArrialNarrow', 'B', 12)
            pdf.cell(25, 8, str(ts), 1, 0, 'R', 1)
            pdf.cell(25, 8, str(sf), 1, 1, 'R', 1)
            pdf.set_font('ArrialNarrow', '', 12)
        
        pdf.ouvrir_fchier()

    fab_print_container = ft.Container(
        align=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon_color=ft.Colors.SECONDARY,
            icon=ft.Icons.EDIT_DOCUMENT,
            icon_size=30,
            tooltip=ft.Tooltip(
                message="Editer le récapitulatif de votre stock",
            ),
            on_click = print_recapitulatif
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