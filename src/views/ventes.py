import re
import flet as ft
from base_de_donnee import SQLiteManager
from generateur_passe import Generateur_MDP
from pdf import PDF

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
        quantite.value = "1" if maximum_article >= 1 else 0
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
            e.control.value = "0"
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
        elif val < 1:
            val = val + 1
        quantite.value = str(val)
        quantite.update()

    def choix_dette():
        if dette.value == True:
            crencier.disabled = True
            crencier.value = ""
        else:
            crencier.disabled = False
        crencier.update()

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
        value="1",
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
        value="0"
    )

    montant_intrant = ft.TextField(
        label="Intrant",
        value="0",
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
        label="Payé",
        fill_color=ft.Colors.SURFACE,
        on_change=choix_dette
    )

    crencier = ft.TextField(
        label="Créancier",
        border_color=ft.Colors.SECONDARY,
        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
        cursor_color=ft.Colors.SECONDARY,
        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.LEFT,
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

    def ajout_vente(e):
        if libelle.value == None:
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez entrer le libellé de l'article"))
        elif quantite.value == "0":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le quantité de l'artice"))
        elif prix_unitaire.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le prix unitaire de l'article"))
        elif montant_intrant.value == "":
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le montant des intrants"))
        elif crencier.value == "" and dette.value == False:
            e.control.page.show_dialog(ouvrir_boite_dialog("Erreur", "Veuillez renseigner le nom du créancier"))
        else:
            def nouvelle_ligne_tableau(dernier_id,li,q,p,intr):
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
                                width=250,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=q,
                                width=60,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                    
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=p,
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
                                value=tot1,
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
                                value=intr,
                                width=80,
                                text_align=ft.TextAlign.RIGHT,
                                style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_400,
                                )
                            )
                        ),
                        ft.DataCell(
                            content=ft.Text(
                                value=tot2,
                                width=100,
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
                tableau_ventes.rows.append(nouvelle_ligne)
                tableau_ventes.update()
                
            nonlocal id_article
            data = (
                libelle.text,
                int(quantite.value.replace(" ","")),
                int(prix_unitaire.value.replace(" ","")),
                int(montant_intrant.value.replace(" ","")),
                id_article,
                1 if dette.value == False else 0,
                crencier.value if dette.value == False else "SALCOM",
                " " if dette.value == False else mois_travail
            )

            nonlocal maximum_article
            maximum_article = 0
            id_article = 0
            dernier_id = base_de_donnee.CRUD_ventes(0,data)
            e.control.page.show_dialog(ouvrir_boite_dialog("Ajout","Vente ajoutée avec succès"))
            
            if dette.value == True:
                nouvelle_ligne_tableau(dernier_id,libelle.text,quantite.value,prix_unitaire.value,montant_intrant.value)
            
            libelle.value = None
            quantite.value = "1"
            prix_unitaire.value = "0"
            montant_intrant.value = "0"
            dette.value = True
            crencier.value = ""

            libelle.update()
            quantite.update()
            prix_unitaire.update()
            montant_intrant.update()
            dette.update()
            crencier.update()

            nonlocal stock
            stock = base_de_donnee.stock(mois_travail)
            libelle.options = [
                ft.DropdownOption(
                    key=f"{s[0]}**{s[7]}",
                    text = s[1],
                )
                for s in stock
            ]
            libelle.update()

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
                            crencier,
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

                if choix == "Modifier":

                    def modif_ven():
                        cr = nouveau_crencier.value
                        cr.replace(" ", "")
                        if nouvelle_dette.value == False and cr == "":
                            nouveau_crencier.value = ""
                            nouveau_crencier.border_color = "red"
                            nouveau_crencier.update()
                        else:
                            data = (
                                int(str(nouvelle_qte.value.replace(" ", ""))),
                                int(str(nouveau_prix_unitaire.value.replace(" ", ""))),
                                int(str(nouveau_montant_intrant.value.replace(" ", ""))),
                                1 if nouvelle_dette.value==False else 0,
                                nouveau_crencier.value if nouvelle_dette.value==False else "SALCOM",
                                " " if nouvelle_dette.value == False else mois_travail,
                                btn.control.data
                            )
                            base_de_donnee.CRUD_ventes(21,data)

                            nonlocal stock
                            stock = base_de_donnee.stock(mois_travail)
                            libelle.options = [
                                ft.DropdownOption(
                                    key=f"{s[0]}**{s[7]}",
                                    text = s[1],
                                )
                                for s in stock
                            ]
                            libelle.update()

                            if nouvelle_dette.value == False:
                                for li in tableau_ventes.rows:
                                    bloc_icon = li.cells[6]
                                    data_ligne = bloc_icon.content.controls[0].data
                                    if data_ligne == btn.control.data:
                                        tableau_ventes.rows.remove(li)
                                        break
                            else:
                                for li in tableau_ventes.rows:
                                    bloc_icon = li.cells[6]
                                    data_ligne = bloc_icon.content.controls[0].data
                                    if data_ligne == btn.control.data:
                                        li.cells[1].content.value = nouvelle_qte.value
                                        li.cells[2].content.value = nouveau_prix_unitaire.value
                                        li.cells[4].content.value = nouveau_montant_intrant.value

                                        qqq = int(str(nouvelle_qte.value).replace(" ", ""))
                                        pppu = int(str(nouveau_prix_unitaire.value).replace(" ", ""))
                                        pppi = int(str(nouveau_montant_intrant.value).replace(" ", ""))
                                        t1 = qqq*pppu
                                        t2 = qqq*pppi
                                        li.cells[3].content.value = "{:,}".format(t1).replace(",", " ")
                                        li.cells[5].content.value = "{:,}".format(t2).replace(",", " ")
                                        
                                        break
                            tableau_ventes.update()
                            
                            fermeture_dialog(btn)
                            
                            btn.control.page.show_dialog(
                                ft.AlertDialog(
                                    modal=False,
                                    title="Action réussie",
                                    content=ft.Text(
                                        "Vente modifiée avec succès"
                                    ),
                                )
                            )

                    libele_a_modifier = ""
                    max_temp = 0
                    qte_a_modifier = 0

                    qq = "0"
                    ppu = "0"
                    ppi = "0"

                    for li in tableau_ventes.rows:
                        bloc_icon = li.cells[6]
                        data_ligne = bloc_icon.content.controls[0].data
                        if data_ligne == btn.control.data:
                            libele_a_modifier = li.cells[0].content.value
                            qte_a_modifier = int(str(li.cells[1].content.value).replace(" ", ""))
                            
                            qq = li.cells[1].content.value
                            ppu = li.cells[2].content.value
                            ppi = li.cells[4].content.value
                            
                            break

                    for d in libelle.options:
                        if d.text == libele_a_modifier:
                            m = int(d.key.split("**")[1])
                            max_temp = m + qte_a_modifier

                    def changer_nouvelle_quantite(n):
                        val = nouvelle_qte.value
                        val = int(val)
                        val = val + n
                        if val > max_temp:
                            val = val - 1
                        elif val < 1:
                            val = val + 1
                        nouvelle_qte.value = str(val)
                        nouvelle_qte.update()

                    def choix_dette():
                        if nouvelle_dette.value == True:
                            nouveau_crencier.disabled = True
                            nouveau_crencier.value = ""
                        else:
                            nouveau_crencier.disabled = False
                            
                        nouveau_crencier.update()

                    nouvelle_qte = ft.TextField(
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
                        value=qq,
                        read_only=True,
                        prefix=ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            icon_size=7,
                            visual_density=ft.VisualDensity.COMPACT,
                            padding=0,
                            on_click=lambda : changer_nouvelle_quantite(-1)
                        ),
                        suffix=ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_size=7,
                            visual_density=ft.VisualDensity.COMPACT,
                            padding=0,
                            on_click=lambda : changer_nouvelle_quantite(1)
                        )
                    )

                    nouveau_prix_unitaire = ft.TextField(
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
                        value=ppu
                    )

                    nouveau_montant_intrant = ft.TextField(
                        label="Intrant",
                        value=ppi,
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

                    nouvelle_dette = ft.Checkbox(
                        value=True,
                        label="Payé",
                        fill_color=ft.Colors.SURFACE,
                        on_change=choix_dette
                    )

                    nouveau_crencier = ft.TextField(
                        label="Créancier",
                        border_color=ft.Colors.SECONDARY,
                        label_style=ft.TextStyle(color=ft.Colors.SECONDARY),
                        cursor_color=ft.Colors.SECONDARY,
                        text_style=ft.TextStyle(weight=ft.FontWeight.W_700,),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        text_align=ft.TextAlign.LEFT,
                        width=150,
                        disabled=True,
                    )
                          
                    btn.control.page.show_dialog(
                        ft.AlertDialog(
                            modal=False,
                            title="Saisissez les nouvelles valeurs",
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    nouvelle_qte,
                                    nouveau_prix_unitaire,
                                    nouveau_montant_intrant,
                                    nouvelle_dette,
                                    nouveau_crencier
                                ],
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
                                    on_click = modif_ven
                                ),
                            ]
                        )
                    )
                    
                else:
                    data = (btn.control.data,)
                    base_de_donnee.CRUD_ventes(3,data)

                    fermeture_dialog(btn)

                    btn.control.page.show_dialog(
                        ft.AlertDialog(
                            modal=False,
                            title="Action réussie",
                            content=ft.Text(
                                "Vente suprimée avec succès"
                            ),
                        )
                    )

                    nonlocal stock
                    stock = base_de_donnee.stock(mois_travail)
                    libelle.options = [
                        ft.DropdownOption(
                            key=f"{s[0]}**{s[7]}",
                            text = s[1],
                        )
                        for s in stock
                    ]
                    libelle.update()

                    for li in tableau_ventes.rows:
                        bloc_icon = li.cells[6]
                        data_ligne = bloc_icon.content.controls[0].data
                        if data_ligne == btn.control.data:
                            tableau_ventes.rows.remove(li)
                            tableau_ventes.update()
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

    
    tableau_ventes = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text(
                    value="Libellé",
                    width=250,
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
                    width=60,
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
                    width=100,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Int.",
                    text_align=ft.TextAlign.RIGHT,
                    width=80,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_800,
                    )
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    value="Tot. I",
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
                            value=liste_ventes[i][1],
                            width=250,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][2],
                            width=60,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                                
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][3],
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
                            value=liste_ventes[i][4],
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
                            value=liste_ventes[i][5],
                            width=80,
                            text_align=ft.TextAlign.RIGHT,
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_400,
                            )
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            value=liste_ventes[i][6],
                            width=100,
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
                                    data=liste_ventes[i][0],
                                    on_click = lambda btn : saisi_MDP(btn,"Modifier")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_size=15,
                                    tooltip=ft.Tooltip(
                                        message="Supprimer",
                                    ),
                                    data=liste_ventes[i][0],
                                    on_click = lambda btn : saisi_MDP(btn,"Supprimer")
                                ),
                            ]
                        )                       
                    )
                ]
            )
            for i in range (len(liste_ventes))
        ]
    )

    container_table = ft.Container(
        content=ft.Column(
            controls=[tableau_ventes],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        ),
        expand=True,
        border_radius=15,
        padding=10,
        bgcolor=ft.Colors.SURFACE
    )

    def print_ventes(): 
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        
        #En-tete
        pdf.image("src/assets/Entete_portrait.png", 10, 10, 190)
        
        aa = mois_travail.replace("_", " ")
        pdf.ln(47)
        pdf.set_font('ArrialNarrow', 'B', 14)
        pdf.cell(100, 10, f"Ventes du mois de {aa}", 0, 1, 'L')

        
        #tableau - entete
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(13, 187, 246)
        pdf.set_draw_color(42, 41, 41)

        pdf.ln(5)
        pdf.set_font('ArrialNarrow', 'B', 14)

        pdf.cell(85, 10, 'Libellé', 1, 0, 'L', 1)
        pdf.cell(15, 10, 'Qté', 1, 0, 'R', 1)
        pdf.cell(20, 10, 'P.U', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Total', 1, 0, 'R', 1)
        pdf.cell(20, 10, 'Int.', 1, 0, 'R', 1)
        pdf.cell(25, 10, 'Tot int.', 1, 1, 'R', 1)

        #tableau - contenu
        pdf.set_font('ArrialNarrow', '', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(42, 41, 41)
        for li in tableau_ventes.rows:
            lib = li.cells[0].content.value
            qqq = li.cells[1].content.value
            ppp = li.cells[2].content.value
            tt1 = li.cells[3].content.value
            iii = li.cells[4].content.value
            tt2 = li.cells[5].content.value

            pdf.cell(85, 8, lib, 1, 0, 'L', 1)
            pdf.cell(15, 8, qqq, 1, 0, 'R', 1)
            pdf.cell(20, 8, ppp, 1, 0, 'R', 1)
            pdf.cell(25, 8, tt1, 1, 0, 'R', 1)
            pdf.cell(20, 8, iii, 1, 0, 'R', 1)
            pdf.cell(25, 8, tt2, 1, 1, 'R', 1)
        
        pdf.ouvrir_fchier()

    fab_print_container = ft.Container(
        align=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon_color=ft.Colors.SECONDARY,
            icon=ft.Icons.EDIT_DOCUMENT,
            icon_size=30,
            tooltip=ft.Tooltip(
                message="Editer vos ventes",
            ),
            on_click = print_ventes
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