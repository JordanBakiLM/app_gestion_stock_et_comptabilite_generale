import sqlite3
import os

class SQLiteManager:
    def __init__(self):
        dossier_utilisateur = os.path.expanduser("~")
        chemin = os.path.join(dossier_utilisateur, "suivi")
        os.makedirs(chemin, exist_ok=True)
        chemin = os.path.join(chemin, "bd2.db")

        self.cheminBD = chemin
        self.cheminBD = "bd2.db"

    # --------------------------- CREATION TABLE
    def creation_table(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                # ----------- theme
                curseur.execute('CREATE TABLE theme(id INTEGER PRIMARY KEY, theme INTEGER)')
                curseur.execute('INSERT INTO theme(id,theme) VALUES (?,?)', (1, 1))

                # ----------- mois
                curseur.execute('CREATE TABLE mois(mois_annee TEXT PRIMARY KEY, caisse INTEGER)')
                curseur.execute('CREATE TABLE mois_travail(id INTEGER PRIMARY KEY AUTOINCREMENT, mois_annee TEXT)')

                # ----------- stock initial
                curseur.execute('CREATE TABLE stock_initial(id INTEGER PRIMARY KEY AUTOINCREMENT, libelle TEXT, qte INTEGER, pu INTEGER, mois_annee TEXT)')

                # ----------- approvisionment
                curseur.execute('CREATE TABLE approvisionement(id_app INTEGER PRIMARY KEY AUTOINCREMENT, libelle TEXT, qte INTEGER, pu INTEGER, id_article INTEGER, mois_annee TEXT, FOREIGN KEY(id_article) REFERENCES stock_initial(id))')

                # ----------- ventes
                curseur.execute('CREATE TABLE ventes(id_ven INTEGER PRIMARY KEY AUTOINCREMENT, libelle TEXT, qte INTEGER, pu INTEGER, intrant INTEGER, id_article INTEGER, dette INTEGER, creancier TEXT, mois_annee TEXT, FOREIGN KEY(id_article) REFERENCES stock_initial(id))')

        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    # --------------------------- THEME
    def maj_theme(self,theme:int):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                curseur.execute('UPDATE theme SET theme = ? WHERE id = ?', (theme, 1))                
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def get_theme(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                theme = curseur.execute('SELECT theme FROM theme WHERE id = ?', (1,)).fetchone()
                return theme[0]               
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    
    # --------------------------- gestion mois
    def CRU_mois(self,state,data=()):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                if state == 0:
                    dernier_mois = self.get_dernier_mois()
                    if dernier_mois != "":
                        sto = self.stock(dernier_mois)
                        for s in sto:
                            if s[7] != 0:
                                curseur.execute('INSERT INTO stock_initial (libelle,qte,pu,mois_annee) VALUES (?,?,?,?)', (s[1],s[7],s[8],data[0]))



                    curseur.execute('INSERT INTO mois (mois_annee,caisse) VALUES (?,?)', data)

                    mt = curseur.execute("SELECT * FROM mois_travail").fetchall()
                    if len(mt)==0:
                        curseur.execute('INSERT INTO mois_travail (mois_annee) VALUES (?)', (data[0],))
                    else:
                        curseur.execute('UPDATE mois_travail set mois_annee = ? WHERE id = ?', (data[0],1))
                    return 1
                elif state == 1:
                    mois_travail = curseur.execute('SELECT * FROM mois').fetchall()
                    return mois_travail
                elif state == 2:
                    curseur.execute('UPDATE mois SET caisse = ? WHERE mois_annee = ?', data)
                    return 1
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()
    
    def get_tous_les_mois(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                dernier_mois = curseur.execute('SELECT * FROM mois').fetchall()
                dernier_mois.reverse()

                tous_les_mois = []
                for dm in dernier_mois:
                    tous_les_mois.append(dm[0])
                
                return tous_les_mois
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def get_dernier_mois(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                dernier_mois = curseur.execute('SELECT * FROM mois').fetchall()
                if len(dernier_mois) == 0:
                    return ""
                else:
                    dernier_mois.reverse()
                    return dernier_mois[0][0]
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def get_mois_travail(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                mois_travail = curseur.execute('SELECT * FROM mois_travail').fetchall()
                if len(mois_travail)==0:
                    return -1
                else:
                    return mois_travail[0][1]
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def update_mois_travail(self,nm):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                curseur.execute('UPDATE mois_travail set mois_annee = ? WHERE id = ?', (nm,1))
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    # --------------------------- gestion stock initial
    def CRUD_stock_initial(self,state,data=()):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                if state == 0:
                    curseur.execute('INSERT INTO stock_initial (libelle,qte,pu,mois_annee) VALUES (?,?,?,?)', data)
                    return 1
                elif state == 1:
                    stock_init = curseur.execute('SELECT * FROM stock_initial WHERE mois_annee = ?', data).fetchall()
                    return stock_init
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    # --------------------------- gestion approvisionement
    def CRUD_approvisionement(self,state,data=()):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                if state == 0:
                    curseur.execute('INSERT INTO approvisionement (libelle,qte,pu,id_article,mois_annee) VALUES (?,?,?,?,?)', data)
                    return 1
                elif state == 1:
                    stock_init = curseur.execute('SELECT * FROM approvisionement WHERE mois_annee = ?', data).fetchall()
                    return stock_init
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    # --------------------------- gestion ventes
    def CRUD_ventes(self,state,data=()):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                if state == 0:
                    curseur.execute('INSERT INTO ventes (libelle,qte,pu,intrant,id_article,dette,creancier,mois_annee) VALUES (?,?,?,?,?,?,?,?)', data)
                    return 1
                elif state == 1:
                    stock_init = curseur.execute('SELECT * FROM ventes WHERE mois_annee = ? AND dette = ?', data).fetchall()
                    return stock_init
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()    
    
    def stock(self,m_t:str):
        conn = sqlite3.connect(self.cheminBD)
        ret = []
        with conn:
            curseur = conn.cursor()
            stock_init = curseur.execute('SELECT id,libelle,qte,pu FROM stock_initial WHERE mois_annee = ?', (m_t,)).fetchall()
            for el in stock_init:
                app = curseur.execute('SELECT sum(qte) FROM approvisionement WHERE mois_annee = ? AND id_article = ? GROUP BY id_article', (m_t,el[0])).fetchone()
                app = 0 if app == None else app[0]

                tot_en = int(el[2]) + int(app)

                vente = curseur.execute('SELECT sum(qte) FROM ventes WHERE mois_annee = ? AND id_article = ? AND dette = ? GROUP BY id_article', (m_t,el[0],0)).fetchone()
                vente = 0 if vente == None else int(vente[0])

                dette = curseur.execute('SELECT sum(qte) FROM ventes WHERE mois_annee = ? AND id_article = ? AND dette = ? GROUP BY id_article', (m_t,el[0],1)).fetchone()
                dette = 0 if dette == None else int(dette[0])

                final = tot_en - vente - dette
                


                nb = [el[0],el[1],int(el[2]),int(app),tot_en,vente,dette,final,int(el[3])]
                ret.append(nb)

        return ret

    def benefice_brut(self,m_t:str):
        conn = sqlite3.connect(self.cheminBD)
        ret = []
        with conn:
            curseur = conn.cursor()
            stock_init = curseur.execute('SELECT id,libelle,pu FROM stock_initial WHERE mois_annee = ?', (m_t,)).fetchall()
            for el in stock_init:
                ven = curseur.execute('SELECT sum(qte),sum(qte*pu),sum(qte*intrant) FROM ventes WHERE mois_annee = ? AND id_article = ? GROUP BY id_article', (m_t,el[0])).fetchone()
                qte_ven = 0 if ven == None else ven[0]
                tot_ven = 0 if ven == None else ven[1]
                tot_int = 0 if ven == None else ven[2]
                
                tot_achat = int(qte_ven)*int(el[2])

                bb = int(tot_ven) - int(tot_achat) - int(tot_int)



                nb = [el[1],int(qte_ven),int(el[2]),tot_achat,tot_ven,tot_int,bb]
                ret.append(nb)

        return ret
