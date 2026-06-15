import sqlite3
import os

class SQLiteManager:
    def __init__(self):
        dossier_utilisateur = os.path.expanduser("~")
        chemin = os.path.join(dossier_utilisateur, "DocumentsSa", "suiviStock_CG")
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
                curseur.execute('CREATE TABLE mois(mois_annee TEXT PRIMARY KEY, caisse_debut INTEGER)')
                curseur.execute('CREATE TABLE mois_travail(id INTEGER PRIMARY KEY AUTOINCREMENT, mois_annee TEXT)')
                curseur.execute('CREATE TABLE mouvement_mois(id INTEGER PRIMARY KEY AUTOINCREMENT, type_mouvement TEXT, libelle TEXT,montant INTEGER,date TEXT,mois_annee TEXT)')


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

                    curseur.execute('INSERT INTO mois (mois_annee,caisse_debut) VALUES (?,?)', data)

                    mt = curseur.execute("SELECT * FROM mois_travail").fetchall()
                    if len(mt)==0:
                        curseur.execute('INSERT INTO mois_travail (mois_annee) VALUES (?)', (data[0],))
                    else:
                        curseur.execute('UPDATE mois_travail set mois_annee = ? WHERE id = ?', (data[0],1))
                    return 1
                elif state == 1:
                    mois_travail = curseur.execute('SELECT * FROM mois').fetchall()
                    return mois_travail
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()
    
    def get_caisse(self,m_a):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                app = curseur.execute('SELECT SUM(qte*pu) from approvisionement WHERE mois_annee = ?', (m_a,)).fetchone()
                app = 0 if app[0] == None else app[0]

                ven = curseur.execute('SELECT SUM(qte*pu) from ventes WHERE mois_annee = ?', (m_a,)).fetchone()
                ven = 0 if ven[0] == None else ven[0]
                
                caisse = curseur.execute('SELECT caisse_debut from mois WHERE mois_annee = ?', (m_a,)).fetchone()
                caisse = 0 if caisse == None else caisse[0]
                caisse = caisse + ven - app

                return caisse
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

    def CRU_mouvement_mois(self,state,data=()):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                if state == 0:
                    curseur.execute('INSERT INTO mouvement_mois (type_mouvement,libelle,montant,date,mois_annee) VALUES (?,?,?,?,?)', data)
                    return 1
                elif state == 1:
                    info_mouvement_mois = curseur.execute('SELECT type_mouvement,libelle,montant,date FROM mouvement_mois WHERE mois_annee = ?', data).fetchall()
                    return info_mouvement_mois
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()
    
    def mouvement_mois_ajout_retrait(self,m_a):
        try:
            conn = sqlite3.connect(self.cheminBD)
            with conn:
                curseur = conn.cursor()
                ajout = curseur.execute('SELECT SUM(montant) from mouvement_mois WHERE mois_annee = ? AND type_mouvement = ?', (m_a,"Ajout")).fetchone()
                ajout = 0 if ajout[0] == None else ajout[0]

                retrait = curseur.execute('SELECT SUM(montant) from mouvement_mois WHERE mois_annee = ? AND type_mouvement = ?', (m_a,"Retrait")).fetchone()
                retrait = 0 if retrait[0] == None else retrait[0]

                return [ajout,retrait]
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
                    return curseur.lastrowid
                elif state == 1:
                    stock_init = curseur.execute('SELECT * FROM approvisionement WHERE mois_annee = ?', data).fetchall()
                    return stock_init
                elif state == 2:
                    curseur.execute('UPDATE approvisionement SET qte = ? WHERE id_app = ?', data).fetchall()
                    return 1
                elif state == 3:
                    curseur.execute('DELETE FROM approvisionement WHERE id_app = ?', data)
                    return 1

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
                    return curseur.lastrowid
                elif state == 1:
                    stock_init = curseur.execute('SELECT * FROM ventes WHERE mois_annee = ? AND dette = ?', data).fetchall()
                    return stock_init
                elif state == 2:
                    curseur.execute('UPDATE ventes SET dette = ?, creancier=?, mois_annee = ? WHERE id_ven = ?', data).fetchall()
                elif state == 21:
                    curseur.execute('UPDATE ventes SET qte = ?, pu = ?, intrant = ?, dette = ?, creancier = ?, mois_annee = ? WHERE id_ven = ?', data).fetchall()
                    return 1
                elif state == 3:
                    curseur.execute('DELETE FROM ventes WHERE id_ven = ?', data)
                    return 1
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()    
    
    def stock(self,m_t:str):
        try:
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

                    dette = curseur.execute('SELECT sum(qte) FROM ventes WHERE id_article = ? AND dette = ? GROUP BY id_article', (el[0],1)).fetchone()
                    dette = 0 if dette == None else int(dette[0])

                    final = tot_en - vente - dette
                    

                    nb = [el[0],el[1],int(el[2]),int(app),tot_en,vente,dette,final,int(el[3])]
                    ret.append(nb)

            return ret
    
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def benefice_brut(self,m_t:str):
        try:
            conn = sqlite3.connect(self.cheminBD)
            ret = []
            with conn:
                curseur = conn.cursor()
                ven = curseur.execute('SELECT stock_initial.libelle, sum(ventes.qte),sum(ventes.qte*ventes.pu),sum(ventes.qte*ventes.intrant),stock_initial.pu FROM ventes INNER JOIN stock_initial ON stock_initial.id = ventes.id_article WHERE ventes.mois_annee = ? GROUP BY id_article', (m_t,)).fetchall()
                for el in ven:
                    qte_ven = 0 if ven == None else el[1]
                    tot_ven = 0 if ven == None else el[2]
                    tot_int = 0 if ven == None else el[3]
                    
                    tot_achat = int(qte_ven)*int(el[4])

                    cr = int(tot_int) + int(tot_achat)

                    bb = int(tot_ven) - int(cr)



                    nb = [el[0],int(qte_ven),tot_ven,cr,bb]
                    ret.append(nb)

            return ret
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def chiffres(self, m_t:str):
        try:
            conn = sqlite3.connect(self.cheminBD)
            ret = []
            with conn:
                curseur = conn.cursor()
                app = curseur.execute('SELECT SUM(qte*pu) from approvisionement WHERE mois_annee = ?', (m_t,)).fetchone()
                app = 0 if app[0] == None else app[0]

                ven = curseur.execute('SELECT SUM(qte*pu) from ventes WHERE mois_annee = ?', (m_t,)).fetchone()
                ven = 0 if ven[0] == None else ven[0]

                renou_mat = curseur.execute('SELECT SUM((ventes.qte*ventes.intrant)+(ventes.qte*stock_initial.pu)) from ventes INNER JOIN stock_initial ON stock_initial.id = ventes.id_article WHERE ventes.mois_annee = ?', (m_t,)).fetchone()
                renou_mat = 0 if renou_mat[0] == None else renou_mat[0]

                bb = ven - renou_mat
                
                caisse = curseur.execute('SELECT caisse_debut from mois WHERE mois_annee = ?', (m_t,)).fetchone()
                caisse = 0 if caisse == None else caisse[0]

                ajout = curseur.execute('SELECT SUM(montant) from mouvement_mois WHERE mois_annee = ? AND type_mouvement = ?', (m_t,"Ajout")).fetchone()
                ajout = 0 if ajout[0] == None else ajout[0]

                retrait = curseur.execute('SELECT SUM(montant) from mouvement_mois WHERE mois_annee = ? AND type_mouvement = ?', (m_t,"Retrait")).fetchone()
                retrait = 0 if retrait[0] == None else retrait[0]

                caisse = caisse + ajout - retrait

                reste_caisse = caisse - app + ven - bb

                caisse = "{:,}".format(int(caisse)).replace(",", " ")
                app = "{:,}".format(int(app)).replace(",", " ")
                ven = "{:,}".format(int(ven)).replace(",", " ")
                renou_mat = "{:,}".format(int(renou_mat)).replace(",", " ")
                bb = "{:,}".format(int(bb)).replace(",", " ")
                reste_caisse = "{:,}".format(int(reste_caisse)).replace(",", " ")
                
                ret = [caisse,app,ven,renou_mat,bb,reste_caisse]
                return ret
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()

    def data_diagramme(self):
        try:
            conn = sqlite3.connect(self.cheminBD)
            ret = []
            with conn:
                curseur = conn.cursor()
                mois = curseur.execute('SELECT * FROM mois ORDER BY rowid DESC LIMIT 12').fetchall()
                for m in mois:
                    ven = curseur.execute('SELECT SUM(qte*pu) from ventes WHERE mois_annee = ?', (m[0],)).fetchone()
                    ven = 0 if ven[0] == None else ven[0]

                    az = [m[0], ven]
                    ret.append(az)

                ret.reverse()
                return ret
        except sqlite3.Error as e:
            print(f"l'erreur est : {e}")
        finally:
            conn.close()
