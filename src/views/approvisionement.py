import re
import flet as ft
from base_de_donnee import SQLiteManager
from generateur_passe import Generateur_MDP
from pdf import PDF

def approvisionement(base_de_donnee:SQLiteManager,mois_travail:str):
    dernier_mois = base_de_donnee.get_dernier_mois()

    id_motif = 0

    # libelle
    def choix_article(e):
        p = "{:,}".format(int(libelle.value.split("**")[2])).replace(",", " ")
        prix_unitaire.value = p

    tous_les_elements = base_de_donnee.CRUD_stock_initial(1,(mois_travail,))
    libelle = ft.Dropdown(
        label="Libllé article",
        options=[
            ft.DropdownOption(
                key=f"{lib[0]}**{lib[1]}**{lib[3]}",
                text = lib[1],
            )
            for lib in tous_les_elements
        ],
        width=360,
        border_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700),
        on_select=choix_article,
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
        label="Quantité",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_change_value,
        text_align=ft.TextAlign.RIGHT,
        width=150,
        value="0"
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
        width=150,
        disabled=True
    )

    #boutton ajouter

    def ouvrir_boite_dialog(titre, message):
        return ft.AlertDialog(
            title=titre,
            content=ft.Text(
                value=message
            )
        )

    def ajout_approvisionement(e):
        if libelle.value == None:
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez entrer le libellé de l'article"))
        elif quantite.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le quantité de l'artice"))
        elif prix_unitaire.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le prix unitaire de l'article"))
        else:
            qu = int(quantite.value.replace(" ",""))
            p = int(prix_unitaire.value.replace(" ",""))
            data = (libelle.value.split("**")[1],qu,p,libelle.value.split("**")[0],mois_travail)
            dernier_id = base_de_donnee.CRUD_approvisionement(0,data)

            e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Approvisionement ajouté avec succès"))

            to = int(quantite.value.replace(" ","")) * int(prix_unitaire.value.replace(" ",""))
            to = "{:,}".format(to).replace(",", " ")
            nouvelle_ligne = ft.DataRow(
                cells= [
                    ft.DataCell(
                        content=ft.Text(
                            value=libelle.value.split("**")[1],
                            width=350,
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
                            width=90,
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
                            width=115,
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
                                    icon=ft.Icons.EDIT,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Modifier",
                                    ),
                                    data=dernier_id,
                                    on_click = lambda btn : saisi_MDP(btn,"Modifier")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Supprimer",
                                    ),
                                    data=dernier_id,
                                    on_click = lambda btn : saisi_MDP(btn,"Supprimer")
                                ),
                            ]
                        )                       
                    )
                ]
            )
            
            tableau_approvisionement.rows.append(nouvelle_ligne)
            tableau_approvisionement.update()

            libelle.value = ""
            quantite.value = "0"
            prix_unitaire.value = ""

            libelle.update()
            quantite.update()
            prix_unitaire.update()

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
        width=150,
        align=ft.Alignment.CENTER,        
        bgcolor=ft.Colors.ON_PRIMARY,        
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=ajout_approvisionement
    )

    #bloc ajouut
    bloc_ajout_approvisionement=ft.Container(
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
    
    liste_approvisionement = []
    az = base_de_donnee.CRUD_approvisionement(1,(mois_travail,))
    for element in az:
        id_ap = element[0]
        l = element[1]
        q = "{:,}".format(int(element[2])).replace(",", " ")
        pu = "{:,}".format(int(element[3])).replace(",", " ")
        id_el = element[4]
        to = int(q.replace(" ","")) * int(pu.replace(" ",""))
        to = "{:,}".format(to).replace(",", " ")
        liste_approvisionement.append((id_ap,l,q,pu,to,id_el))

    def saisi_MDP(btn, choix: str):
        def fermeture_dialog(e):
            e.control.page.pop_dialog()

        def check_mdp(b, p:str):
            check = Generateur_MDP.comparer_mot_de_passe(p)
            if check == False:
                b.control.page.show_dialog(
                    ft.AlertDialog(
                        modal=False,
                        title="Erreur",
                        content=ft.Text(
                            "Mot de passe insorrect, veuillez réessayer"
                        ),
                        actions=[
                            ft.TextButton(
                                "OK",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.SECONDARY
                                ),
                                on_click=fermeture_dialog
                            ),
                        ]
                    )
                )
            else:
                fermeture_dialog(btn)

                def modif_app(bt, n):
                    fermeture_dialog(btn)

                    nou_q = n.replace(" ", "")
                    nou_q = int(nou_q)
                    data = (nou_q,btn.control.data,)
                    base_de_donnee.CRUD_approvisionement(2, data)
                    btn.control.page.show_dialog(
                        ft.AlertDialog(
                            modal=False,
                            title="Action réussie",
                            content=ft.Text(
                                "Approvisionement modifié avec succès"
                            ),
                        )
                    )

                    for li in tableau_approvisionement.rows:
                        bloc_icon = li.cells[4]
                        data_ligne = bloc_icon.content.controls[0].data
                        if data_ligne == btn.control.data:
                            nq = int(nouvelle_qte.value.replace(" ", ""))
                            pu = int(li.cells[2].content.value.replace(" ", ""))
                            tot = nq*pu

                            nq = "{:,}".format(nq).replace(",", " ")
                            tot = "{:,}".format(tot).replace(",", " ")

                            
                            li.cells[1].content.value = nq
                            li.cells[3].content.value = tot

                            tableau_approvisionement.update()
                            break

                if choix == "Modifier":

                    qq = "0"
                    for li in tableau_approvisionement.rows:
                        bloc_icon = li.cells[4]
                        data_ligne = bloc_icon.content.controls[0].data
                        if data_ligne == btn.control.data:
                            qq = li.cells[1].content.value
                            break

                    nouvelle_qte = ft.TextField(
                        label="Nouvelle quantité",
                        border_color=ft.Colors.SECONDARY,
                        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
                        cursor_color=ft.Colors.SECONDARY,
                        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        on_change=on_change_value,
                        text_align=ft.TextAlign.RIGHT,
                        width=150,
                        value=qq,
                        on_submit= lambda e : modif_app(e, nouvelle_qte.value)
                    )

                    btn.control.page.show_dialog(
                        ft.AlertDialog(
                            modal=False,
                            title="Saisissez la nouvelle quantité",
                            content=nouvelle_qte,
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
                                    on_click = lambda bt : modif_app(bt, nouvelle_qte.value)
                                ),
                            ]
                        )
                    )
                    
                else:
                    data = (btn.control.data,)
                    base_de_donnee.CRUD_approvisionement(3,data)
                    btn.control.page.show_dialog(
                        ft.AlertDialog(
                            modal=False,
                            title="Action réussie",
                            content=ft.Text(
                                "Approvisionement suprimé avec succès"
                            ),
                        )
                    )

                    for li in tableau_approvisionement.rows:
                        bloc_icon = li.cells[4]
                        data_ligne = bloc_icon.content.controls[0].data
                        if data_ligne == btn.control.data:
                            tableau_approvisionement.rows.remove(li)
                            tableau_approvisionement.update()
                            break

        mdp = ft.TextField(
            label="Mot de passe",
            autofocus=True,
            border_color=ft.Colors.SECONDARY,
            label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
            cursor_color=ft.Colors.SECONDARY,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
            width=50,
            password=True,
            on_submit=lambda txtF : check_mdp(txtF, mdp.value)
        )

        btn.control.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title="Saisissez le mot de passe pour éffectuer cette action",
                content=mdp,
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
                        on_click = lambda btn : check_mdp(btn, mdp.value)
                    ),
                ],
                
            )
        )
        
    tableau_approvisionement = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=350,
                    style=ft.TextStyle(
                        size=15,
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
                    width=90,
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
                    width=115,
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
                    width=10,
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
                            value=liste_approvisionement[i][1],
                            width=350,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_approvisionement[i][2],
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
                            value=liste_approvisionement[i][3],
                            width=90,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_approvisionement[i][4],
                            width=115,
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
                                    icon=ft.Icons.EDIT,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Modifier",
                                    ),
                                    data=liste_approvisionement[i][0],
                                    on_click = lambda btn : saisi_MDP(btn,"Modifier")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Supprimer",
                                    ),
                                    data=liste_approvisionement[i][0],
                                    on_click = lambda btn : saisi_MDP(btn,"Supprimer")
                                ),
                            ]
                        )                       
                    )
                ]
            )
            for i in range (len(liste_approvisionement))
        ]
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_approvisionement],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    def print_appro():
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)
        
        aa = mois_travail.replace("_", " ")
        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Approvisionement du mois de {aa}", 0, 1, 'L')

        
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
        for li in tableau_approvisionement.rows:
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
                message="Editer vos approvisionements",
            ),
            on_click = print_appro
        ),
    )


    return ft.Container(
        disabled=not(mois_travail==dernier_mois),
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                bloc_ajout_approvisionement,
                ft.Divider(),
                container_table,
                fab_print_container
            ]
        )
    )