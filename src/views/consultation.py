import re
import flet as ft
import flet_charts as ftch
from base_de_donnee import SQLiteManager

def consultation(base_de_donnee:SQLiteManager, mois_travail):
    
    element = ["C. debut","APP.","C.A.","C.R.","BENEF B.","C. final"]

    cards = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Card(
                content=ft.Container(
                    bgcolor=ft.Colors.SURFACE,
                    width=150,
                    height=100,
                    padding=8,
                    border_radius=10,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                value=e,
                                style=ft.TextStyle(
                                    size=25,
                                    weight=ft.FontWeight.W_800,
                                ),
                                align=ft.Alignment.CENTER,
                            ),
                            ft.Text(
                                value="",
                                style=ft.TextStyle(
                                    size=18,
                                    weight=ft.FontWeight.W_600,
                                ),
                                align=ft.Alignment.CENTER,
                            )
                        ]
                    ),
                ),
                elevation=20,
            )
            for e in element
        ]
    )

    chiffres = base_de_donnee.chiffres(mois_travail)
    for i in range(len(cards.controls)):
        cards.controls[i].content.content.controls[1].value = chiffres[i]
    
    bloc_totaux = ft.Container(
        content=cards,
    )

    
    data_bd = base_de_donnee.data_diagramme()
    data_im = [["",0],["",0],["",0],["",0],["",0],["",0],["",0],["",0],["",0],["",0],["",0],["",0],]
    max = 0
    for i in range(len(data_bd)):
        data_im[i][0] = data_bd[i][0]
        data_im[i][1] = data_bd[i][1]

        if data_im[i][1] > max:
            max = data_im[i][1]

    chart = ftch.BarChart(
        groups=[
            ftch.BarChartGroup(
                x=azz+1,
                rods=[
                    ftch.BarChartRod(
                        to_y=data_im[azz][1],
                        bg_to_y=max + max/5,
                        width=22,
                        color=ft.Colors.ON_PRIMARY,
                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.SECONDARY),
                    ),
                ]
            )
            for azz in range(len(data_im))
        ],
        bottom_axis=ftch.ChartAxis(
            labels=[
                ftch.ChartAxisLabel(
                    value=azz+1,
                    label=ft.Text(
                        data_im[azz][0],
                        style=ft.TextStyle(
                            size=9
                        )
                    ),
                )
                for azz in range(len(data_im))
            ]
        )
    )
    
    
    # BarChartRod()(
    #     bar_groups=[
    #         ftch.BarChartGroup(
    #             x=0, # Index du mois (0 pour Janvier, etc.)
    #             bar_rods=[
    #                 ftch.BarChartRod(
    #                     from_y=0,
    #                     to_y=150000, # Ton CA ici
    #                     width=20,
    #                     color=ft.Colors.BLUE,
    #                     border_radius=5, # <--- COINS ARRONDIS ICI
    #                 ),
    #             ],
    #         ),
    #         # Répète pour les autres mois...
    #     ],
    #     border=ft.border.all(1, ft.Colors.GREY_200),
    #     left_axis=ftch.ChartAxis(labels_size=40, title=ft.Text("Chiffre d'Affaires")),
    #     bottom_axis=ftch.ChartAxis(labels_size=30),
    #     horizontal_grid_lines=ftch.ChartGridLines(color=ft.Colors.GREY_100),
    # )









































    bloc_diagramme = ft.Container(
        content=chart,
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
                bloc_totaux,
                ft.Divider(),
                bloc_diagramme
            ]
        )
    )