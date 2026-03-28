import re
import flet as ft
from base_de_donnee import SQLiteManager

def ventes(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    stock = base_de_donnee.stock(mois_travail)

    maximum_article = int(0)
    id_article = int(0)

    # libelle
    def choix_article(e):
        nonlocal maximum_article
        nonlocal id_article
        maximum_article = int(libelle.value.split("**")[1])
        quantite.value = "0"
        id_article = int(libelle.value.split("**")[0])


    libelle = ft.Dropdown(
        label="Libllé article",
        options=[
            ft.DropdownOption(
                key=f"{s[0]}**{s[7]}",
                text = s[1],
            )
            for s in stock
        ],
        width=300,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
        on_select=choix_article,
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

    def changer_quantite(n):
        val = quantite.value
        val = int(val)
        val = val + n
        if val > maximum_article:
            val = val - 1
        elif val < 0:
            val = val + 1
        quantite.value = str(val)
        quantite.update()

    quantite = ft.TextField(
        label="Qté",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        dense=True,
        content_padding=ft.Padding(left=2,right=2,top=12,bottom=12),
        width=140,
        value="0",
        read_only=True,
        prefix=ft.IconButton(
            icon=ft.Icons.REMOVE,
            icon_size=7,
            visual_density=ft.VisualDensity.COMPACT,
            padding=0,
            on_click=lambda : changer_quantite(-1)
        ),
        suffix=ft.IconButton(
            icon=ft.Icons.ADD,
            icon_size=7,
            visual_density=ft.VisualDensity.COMPACT,
            padding=0,
            on_click=lambda : changer_quantite(1)
        )
    )

    prix_unitaire = ft.TextField(
        label="Prix u",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=" FCFA",
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=140,
    )

    montant_intrant = ft.TextField(
        label="Intrant",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=" FCFA",
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=140,
    )

    dette = ft.Checkbox(
        value=True,
        fill_color=ft.Colors.SURFACE
    )

    #boutton ajouter

    def ouvrir_boite_dialog(titre, message):
        return ft.AlertDialog(
            title=titre,
            content=ft.Text(
                value=message
            )
        )

    def ajout_vente(e):
        if libelle.value == None:
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez entrer le libellé de l'article"))
        elif quantite.value == "0":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le quantité de l'artice"))
        elif prix_unitaire.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le prix unitaire de l'article"))
        elif montant_intrant.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le montant des intrants"))
        else:
            def nouvelle_ligne_tableau(li,q,p,intr):
                q = "{:,}".format(int(q)).replace(",", " ")
                tot1 = int(q.replace(" ",""))*int(p.replace(" ",""))
                tot1 = "{:,}".format(int(tot1)).replace(",", " ")
                tot2 = int(q.replace(" ",""))*int(intr.replace(" ",""))
                tot2 = "{:,}".format(int(tot2)).replace(",", " ")

                nouvelle_ligne = ft.DataRow(
                    cells= [
                        ft.DataCell(
                            content=ft.Text(
                                value=li,
                                width=280,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=q,
                                width=45,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                    
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=p,
                                width=45,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                    
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=tot1,
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
                                value=intr,
                                width=45,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=16,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=tot2,
                                width=70,
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
                
            if dette.value == False:
                def fermeture_dialog(e):
                    e.control.page.pop_dialog()

                def ajout_creancier(e):
                    val = crencier.value
                    val2 = val.replace(" ","")
                    if val2 != "" :
                        nonlocal id_article
                        data = (
                            libelle.text,
                            int(quantite.value.replace(" ","")),
                            int(prix_unitaire.value.replace(" ","")),
                            int(montant_intrant.value.replace(" ","")),
                            id_article,
                            1,
                            val,
                            mois_travail
                        )
                        nonlocal maximum_article
                        maximum_article = 0
                        id_article = 0
                        base_de_donnee.CRUD_ventes(0,data)
                        fermeture_dialog(e)
                        e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Vente ajoutée avec succès"))
                        libelle.value = None
                        quantite.value = "0"
                        prix_unitaire.value = ""
                        montant_intrant.value = ""
                        dette.value = True
                    else:
                        crencier.value = ""
                        crencier.border_color = "red"
                
                crencier = ft.TextField(
                    label="Créancier",
                    autofocus=True,
                    border_color=ft.Colors.SECONDARY,
                    label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
                    cursor_color=ft.Colors.SECONDARY,
                    text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    text_align=ft.TextAlign.LEFT,
                    width=150,
                )

                e.control.page.show_dialog(
                    ft.AlertDialog(
                        modal=True,
                        title="Nom du créancier",
                        content=crencier,
                        actions=[
                            ft.TextButton(
                                "Annuler",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.SECONDARY
                                ),
                                on_click=fermeture_dialog
                            ),
                            ft.TextButton(
                                "Valider",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.SECONDARY
                                ),
                                on_click=ajout_creancier
                            ),
                        ]
                        
                    )
                )
            else:
                nonlocal id_article
                data = (
                    libelle.text,
                    int(quantite.value.replace(" ","")),
                    int(prix_unitaire.value.replace(" ","")),
                    int(montant_intrant.value.replace(" ","")),
                    id_article,
                    0,
                    "SALCOM",
                    mois_travail
                )
                nonlocal maximum_article
                maximum_article = 0
                id_article = 0
                base_de_donnee.CRUD_ventes(0,data)
                e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Vente ajoutée avec succès"))
                
                q="{:,}".format(int(quantite.value)).replace(",", " ")
                nouvelle_ligne_tableau(libelle.text,q,prix_unitaire.value,montant_intrant.value)
                
                idl = libelle.value.split("**")[0]
                maxl = libelle.value.split("**")[1]
                new_max = int(maxl) - int(quantite.value)
                for e in libelle.options:
                    if e.key == libelle.value:
                        e.key = f"{idl}**{new_max}"
                        break

                libelle.value = None
                quantite.value = "0"
                prix_unitaire.value = ""
                montant_intrant.value = ""
                dette.value = True

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
        width=120,
        align=ft.Alignment.CENTER,        
        bgcolor=ft.Colors.ON_PRIMARY,        
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=ajout_vente
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
                            montant_intrant,
                            dette,
                            bouton_ajout
                        ],
                    ),
                    padding=ft.Padding.only(bottom=20)
                ),
            ]
        )   
    )


    # ------------------- LISTE
    
    liste_ventes = []
    az = base_de_donnee.CRUD_ventes(1,(mois_travail,0))
    for element in az:
        id_ve = element[0]
        l = element[1]
        q = "{:,}".format(int(element[2])).replace(",", " ")
        pu = "{:,}".format(int(element[3])).replace(",", " ")
        to = int(q.replace(" ","")) * int(pu.replace(" ",""))
        to = "{:,}".format(to).replace(",", " ")
        intrant = "{:,}".format(int(element[4])).replace(",", " ")
        toi = int(q.replace(" ","")) * int(intrant.replace(" ",""))
        toi= "{:,}".format(toi).replace(",", " ")
        id_el = element[5]
        liste_ventes.append((id_ve,l,q,pu,to,intrant,toi,id_el))

    tableau_stock_initial = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=280,
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
                    width=45,
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
                    width=45,
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
                    width=70,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Int.",
                    text_align=ft.TextAlign.RIGHT,
                    width=45,
                    style=ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. I",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
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
                            value=liste_ventes[i][1],
                            width=280,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][2],
                            width=45,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][3],
                            width=45,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][4],
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
                            value=liste_ventes[i][5],
                            width=45,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][6],
                            width=70,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                ]
            )
            for i in range (len(liste_ventes))
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