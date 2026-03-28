import flet as ft
from base_de_donnee import SQLiteManager

def benefice_brute(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    bb = base_de_donnee.benefice_brut(mois_travail)
    for b in bb:
        print(b)

    # ------------------- LISTE
    tableau_stock_initial = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=205,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="SI",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="App",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. E",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=13,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Ven.",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Det.",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. S",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=13,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="SF",
                    text_align=ft.TextAlign.RIGHT,
                    width=40,
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
        ],
        # rows=[
        #     ft.DataRow(
        #         cells= [
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value=stock[i][1],
        #                     width=205,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_400,
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][2])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_400,
                                
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][3])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_400,
                                
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][4])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_700,
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][5])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_400,
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][6])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_400,
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][5] + stock[i][6])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_700,
        #                     )
        #                 )
        #             ),
        #             ft.DataCell(
        #                 content=ft.Text(
        #                     value="{:,}".format(int(stock[i][7])).replace(",", " "),
        #                     width=40,
        #                     text_align=ft.TextAlign.RIGHT,
        #                     style=ft.TextStyle(
        #                         size=13,
        #                         weight=ft.FontWeight.W_700,
        #                     )
        #                 )
        #             ),
        #         ]
        #     )
        #     for i in range (len(stock))
        # ]
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
                container_table,
            ]
        )
    )