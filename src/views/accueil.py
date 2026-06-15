import flet as ft
from datetime import datetime
from base_de_donnee import SQLiteManager
from pdf import PDF
import re

def accueil(base_de_donnee:SQLiteManager):

    def changement_mois():
        base_de_donnee.update_mois_travail(choix_mois.value)

    tous_les_mois = base_de_donnee.get_tous_les_mois()
    choix_mois = ft.Dropdown(
        label="Choix du mois de travail",
        options=[ft.DropdownOption(m) for m in tous_les_mois],
        expand=True,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
        on_text_change=changement_mois
    )

    dernier_mois = base_de_donnee.get_dernier_mois()
    if dernier_mois != "":
        choix_mois.value = dernier_mois

    bloc_choix = ft.Container(
        content=choix_mois,
        width=float('inf'),
    )

    # ------------------- FORMULAIRE AJOUT
        
    # mois
    liste_mois=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Decembre"]

    mois = ft.Dropdown(
        label="Nouveau mois",
        options=[ft.DropdownOption(m) for m in liste_mois],
        width=250,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
    )

    # argent
    dernier_mois = base_de_donnee.get_dernier_mois()
    v = 0
    if dernier_mois != "":
        chiffres = base_de_donnee.chiffres(dernier_mois)
        v = chiffres[5]

    argent_debut = ft.TextField(
        value=v,
        disabled=True,
        label="Caisse debut",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        suffix=" FCFA",
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
        else:
            annee_actuelle = datetime.now().year
            mois_annee = f"{mois.value}_{annee_actuelle}"
            debut_mois = int(str(argent_debut.value).replace(" ",""))
            data = (mois_annee,debut_mois)
            insertion = base_de_donnee.CRU_mois(0,data)

            if insertion == 1:
                e.control.page.show_dialog(ouvrir_boite_dialog("Ajout", "Votre mois a été ajouté avec succès"))

                nouvelle_ligne = ft.DataRow(
                    cells= [
                        ft.DataCell(
                            content=ft.Text(
                                value=mois.value,
                                width=90,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=annee_actuelle,
                                width=60,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=argent_debut.value,
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
                                value="0",
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
                                value="0",
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
                                value=argent_debut.value,
                                width=70,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.ADD,
                                        icon_size=15,
                                        tooltip=ft.Tooltip(
                                            message="Ajouter",
                                        ),
                                        data=f"{mois.value}_{annee_actuelle}",
                                        on_click = lambda btn : ajout_retrait(btn,1)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE,
                                        icon_size=15,
                                        tooltip=ft.Tooltip(
                                            message="Retirer",
                                        ),
                                        data=f"{mois.value}_{annee_actuelle}",
                                        on_click = lambda btn : ajout_retrait(btn,-1)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.RECEIPT_LONG,
                                        icon_size=15,
                                        tooltip=ft.Tooltip(
                                            message="Détails",
                                        ),
                                        data=f"{mois.value}_{annee_actuelle}",
                                        on_click = lambda btn : listing(btn)
                                    )
                                ]
                            )                       
                        )
                    ]
                )
                
                choix_mois.options.insert(0,ft.DropdownOption(mois_annee))
                choix_mois.value = mois_annee
                choix_mois.update()
                
                tableau_mois.rows.insert(0,nouvelle_ligne)
                actualiser_icone()

                tableau_mois.update()


                mois.value = None
                mois.update()

            else:
                e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Le mois que vous avez choisi existe deja pour cette année"))
            
    
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
                            argent_debut,
                            bouton_ajout
                        ],
                    ),
                    padding=ft.Padding.only(bottom=20)
                ),
            ]
        )   
    )


    # ------------------- LISTE MOIS

    def actualiser_icone():
        for li in tableau_mois.rows:
            bloc_icon = li.cells[6]
            mois_annee_ligne = bloc_icon.content.controls[0].data

            dernier_mois = base_de_donnee.get_dernier_mois()
            if mois_annee_ligne != dernier_mois:
                li.cells[6].content.controls[0].disabled = True
                li.cells[6].content.controls[1].disabled = True
    
    def ajout_retrait(btn,a:int):
        titre = "Ajout" if a==1 else "Retrait"
        ma= btn.control.data

        def on_change_value(e):
            valeur_brute = e.control.value.replace(" ","")
            bon = re.sub(r'\D', '',valeur_brute)                

            if bon == "":
                e.control.value = ""
            else:
                valeur_formatee = "{:,}".format(int(bon)).replace(",", " ")
                e.control.value = valeur_formatee
            e.control.update()


        def fermeture_dialog(e):
            e.control.page.pop_dialog()

        def mouvement():
            if libelle_ajout_retrait.value.replace(" ","") == "":
                libelle_ajout_retrait.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le libellé de l'opération"))
            elif montant_ajout_retrait.value.replace(" ","") == "":
                montant_ajout_retrait.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le montant de l'opération"))
            else:
                ty_m = "Ajout" if a==1 else "Retrait"
                li_m = libelle_ajout_retrait.value
                mo_m = int(montant_ajout_retrait.value.replace(" ",""))
                maintenant = datetime.now().strftime("%d/%m/%Y")
                ma_m = ma
                data = (ty_m,li_m,mo_m,maintenant,ma_m)

                base_de_donnee.CRU_mouvement_mois(state=0,data=data)

                libelle_ajout_retrait.page.pop_dialog()

                for li in tableau_mois.rows:
                    bloc_icon = li.cells[6]
                    mois_annee_ligne = bloc_icon.content.controls[0].data
                    if mois_annee_ligne == ma:
                        c_f = int(str(li.cells[5].content.value).replace(" ",""))
                        s_a = int(str(li.cells[3].content.value).replace(" ",""))
                        s_r = int(str(li.cells[4].content.value).replace(" ",""))

                        mon = int(montant_ajout_retrait.value.replace(" ",""))
                        if a == -1:
                            s_r = s_r + mon
                        else:
                            s_a = s_a + mon

                        c_f = c_f + (a*mon)

                        li.cells[5].content.value = "{:,}".format(int(c_f)).replace(",", " ")
                        li.cells[3].content.value = "{:,}".format(int(s_a)).replace(",", " ")
                        li.cells[4].content.value = "{:,}".format(int(s_r)).replace(",", " ")

                        tableau_mois.update()

                        break

        libelle_ajout_retrait = ft.TextField(
            label="Libellé",
            autofocus=True,
            border_color=ft.Colors.SECONDARY,
            label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
            cursor_color=ft.Colors.SECONDARY,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
            width=300,
        )

        montant_ajout_retrait = ft.TextField(
            label="Montant",
            border_color=ft.Colors.SECONDARY,
            label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
            cursor_color=ft.Colors.SECONDARY,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.RIGHT,
            on_change=on_change_value,
            width=150,
        )

        btn.control.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=titre,
                content=ft.Row(
                    controls=[
                        libelle_ajout_retrait,
                        montant_ajout_retrait
                    ]
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
                        "Valider",
                        style=ft.ButtonStyle(
                            color=ft.Colors.SECONDARY
                        ),
                        on_click=mouvement
                    ),
                ]
                
            )
        )
   
    def listing(btn):
        liste_listing = []
        az = base_de_donnee.CRU_mouvement_mois(1, (btn.control.data,))
        for element in az:
            t = element[0]
            l = element[1]
            m = "{:,}".format(int(element[2])).replace(",", " ")
            d = element[3]

            liste_listing.append((t,l,m,d))
        
        tableau_listing = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        value="Type",
                        width=50,
                        style=ft.TextStyle(
                            size=15,
                            weight=ft.FontWeight.W_800,
                        )
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        value="Libellé",
                        width=200,
                        style=ft.TextStyle(
                            size=15,
                            weight=ft.FontWeight.W_800,
                        )
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        value="Montant",
                        text_align=ft.TextAlign.RIGHT,
                        width=70,
                        style=ft.TextStyle(
                            size=15,
                            weight=ft.FontWeight.W_800,
                        )
                    )
                ), 
                ft.DataColumn(
                    ft.Text(
                        value="Date",
                        text_align=ft.TextAlign.RIGHT,
                        width=80,
                        style=ft.TextStyle(
                            size=15,
                            weight=ft.FontWeight.W_800,
                        )
                    )
                ),                
            ],
            rows=[
                ft.DataRow(
                    cells= [
                        ft.DataCell(
                            content=ft.Text(
                                value=liste_listing[i][0],
                                width=50,
                                style=ft.TextStyle(
                                    size=13,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value = liste_listing[i][1],
                                width=200,
                                style=ft.TextStyle(
                                    size=13,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=(liste_listing[i][2]),
                                width=70,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    color=ft.Colors.RED_900 if liste_listing[i][0]=="Retrait" else ft.Colors.GREEN_900,
                                    size=13,
                                    weight=ft.FontWeight.W_700,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value = liste_listing[i][3],
                                width=80,
                                style=ft.TextStyle(
                                    size=13,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                    ]
                )
                for i in range (len(liste_listing))
            ]
        )

        def print_listing():            
            pdf = PDF('P', 'mm', 'A4')
            pdf.alias_nb_pages()
            pdf.add_page()

            #En-tete
            pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)
            
            aa = btn.control.data.replace("_", " ")
            pdf.ln(47)
            pdf.set_font('ArrialNarrow', 'B', 14)
            pdf.cell(100, 10, f"Listing des mouvements du mois de {aa}", 0, 1, 'L')

            
            #tableau - entete
            pdf.set_text_color(255, 255, 255)
            pdf.set_fill_color(13, 187, 246)
            pdf.set_draw_color(42, 41, 41)

            pdf.ln(5)
            pdf.set_font('ArrialNarrow', 'B', 14)

            pdf.cell(25, 10, 'Type', 1, 0, 'C', 1)
            pdf.cell(105, 10, 'Libellé', 1, 0, 'L', 1)
            pdf.cell(35, 10, 'Montant', 1, 0, 'R', 1)
            pdf.cell(25, 10, 'Date', 1, 1, 'R', 1)

            #tableau - contenu
            pdf.set_font('ArrialNarrow', '', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(255, 255, 255)
            pdf.set_draw_color(42, 41, 41)
            for li in tableau_listing.rows:
                typ = li.cells[0].content.value
                lib = li.cells[1].content.value
                mtn = li.cells[2].content.value
                dat = li.cells[3].content.value

                pdf.cell(25, 8, typ, 1, 0, 'C', 1)
                pdf.cell(105, 8, lib, 1, 0, 'L', 1)

                pdf.set_font('ArrialNarrow', 'B', 12)
                if typ == "Ajout":
                    pdf.set_text_color(0, 128, 0)
                else:
                    pdf.set_text_color(255, 0, 0)
                pdf.cell(35, 8, mtn, 1, 0, 'R', 1)
                
                pdf.set_font('ArrialNarrow', '', 12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(25, 8, dat, 1, 1, 'R', 1)
            
            pdf.ouvrir_fchier()

            btn.control.page.pop_dialog()

        fab_print_container = ft.Container(
            align=ft.Alignment.CENTER_RIGHT,
            content=ft.IconButton(
                icon_color=ft.Colors.SECONDARY,
                icon=ft.Icons.EDIT_DOCUMENT,
                icon_size=30,
                tooltip=ft.Tooltip(
                    message="Editer vos mouvements",
                ),
                on_click = print_listing
            ),
        )

        container_table = ft.Container(
            content=ft.Column(
                controls=[
                    tableau_listing,
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            height=250,
            border_radius=15,
            padding=10,
            bgcolor=ft.Colors.SURFACE
        )

        btn.control.page.show_dialog(
            ft.AlertDialog(
                title="Listing",
                content=ft.Container(
                    height=300,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            container_table,
                            fab_print_container
                        ]
                    )
                )          
            )
        )
    
    liste_mois = []
    az = base_de_donnee.CRU_mois(1)
    for element in az:
        m = element[0].split("_")[0]
        a = element[0].split("_")[1]
        c_d = "{:,}".format(int(element[1])).replace(",", " ")

        mouv = base_de_donnee.mouvement_mois_ajout_retrait(f"{m}_{a}")
        aj = "{:,}".format(int(mouv[0])).replace(",", " ")
        ret = "{:,}".format(int(mouv[1])).replace(",", " ")

        c = base_de_donnee.get_caisse(f"{m}_{a}")
        c_f = "{:,}".format(int(c+mouv[0]-mouv[1])).replace(",", " ")
        liste_mois.append((m,a,c_d,aj,ret,c_f))

    liste_mois.reverse()

    tableau_mois = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Mois",
                    width=90,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Année",
                    width=60,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="C. debut",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Ajout",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="Retrait",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(
                ft.Text(
                    value="C. final",
                    text_align=ft.TextAlign.RIGHT,
                    width=70,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                )
            ),
            ft.DataColumn(ft.Text(" ", width=100)),
        ],
        rows=[
            ft.DataRow(
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_mois[i][0],
                            width=90,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value = liste_mois[i][1],
                            width=60,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=(liste_mois[i][2]),
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
                            value=(liste_mois[i][3]),
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
                            value=(liste_mois[i][4]),
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
                            value=(liste_mois[i][5]),
                            width=70,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Ajouter",
                                    ),
                                    data=f"{liste_mois[i][0]}_{liste_mois[i][1]}",
                                    on_click = lambda btn : ajout_retrait(btn,1)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Retirer",
                                    ),
                                    data=f"{liste_mois[i][0]}_{liste_mois[i][1]}",
                                    on_click = lambda btn : ajout_retrait(btn,-1)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.RECEIPT_LONG,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Détails",
                                    ),
                                    data=f"{liste_mois[i][0]}_{liste_mois[i][1]}",
                                    on_click = lambda btn : listing(btn)
                                )
                            ]
                        )                       
                    )
                ]
            )
            for i in range (len(liste_mois))
        ]
    )

    actualiser_icone()
    
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


    return ft.Container(
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_choix,
                ft.Divider(),
                bloc_ajout_mois,
                ft.Divider(),
                container_table,
            ]
        )
    )