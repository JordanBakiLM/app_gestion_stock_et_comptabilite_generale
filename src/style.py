import flet as ft

police = {
    "Montserrat" : "assets/police/Montserrat.ttf"
}

theme_clair = ft.Theme(
    font_family = "Montserrat",
    color_scheme = ft.ColorScheme(
        primary = '#041732',
        on_primary = "#0DBBF6",
        secondary_container = '#EFF3F9', #fond total
        secondary = '#000000', #ecriture
        surface = "#DFDFDF" #fond des elements
    )
)

theme_sombre = ft.Theme(
    font_family = "Montserrat",
    color_scheme = ft.ColorScheme(
        primary = '#041732',
        on_primary = '#0DBBF6',
        secondary_container = "#292727", #fond total
        secondary = '#FFFFFF', #ecriture
        surface = "#383737" #fond des elements
    )
)