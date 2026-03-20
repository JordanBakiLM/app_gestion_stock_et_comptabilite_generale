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

                # # ----------- mois
                # curseur.execute('CREATE TABLE mois(mois_annee TEXT PRIMARY KEY, caisse TEXT)')

                # # ----------- dettes
                # curseur.execute('CREATE TABLE dette(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, montant TEXT)')
                
                # # ----------- Sorties
                # curseur.execute('CREATE TABLE sortie(id INTEGER PRIMARY KEY AUTOINCREMENT, libele TEXT, montant TEXT, mois_annee TEXT)')
                
                # # ----------- C. speciale
                # curseur.execute('CREATE TABLE commandes_speciales(id INTEGER PRIMARY KEY AUTOINCREMENT, libele TEXT, montant TEXT, intrant Text, mois_annee TEXT)')

                # # ----------- Classique
                # curseur.execute('CREATE TABLE classique(id INTEGER PRIMARY KEY AUTOINCREMENT, libele TEXT, qte TEXT, total TEXT, total_intrant TEXT, mois_annee TEXT)')

                # # ----------- Vente
                # curseur.execute('CREATE TABLE ventes(id INTEGER PRIMARY KEY AUTOINCREMENT, libele TEXT, qte TEXT, total TEXT, mois_annee TEXT)')
                

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

    
    # # --------------------------- gestion mois
    # def CRU_mois(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 0:
    #                 curseur.execute('INSERT INTO mois (mois_annee,caisse) VALUES (?,?)', data)
    #                 return 1
    #             elif state == 1:
    #                 mois_travail = curseur.execute('SELECT * FROM mois').fetchall()
    #                 return mois_travail
    #             elif state == 2:
    #                 curseur.execute('UPDATE mois SET caisse = ? WHERE mois_annee = ?', data)
    #                 return 1
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()

    # def get_dernier_mois(self):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             dernier_mois = curseur.execute('SELECT * FROM mois').fetchall()
    #             dernier_mois.reverse()
    #             if len(dernier_mois) == 0:
    #                 return -1
    #             else:
    #                 return dernier_mois[0][0]
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()
    
    # def get_tous_les_mois(self):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             dernier_mois = curseur.execute('SELECT * FROM mois').fetchall()
    #             dernier_mois.reverse()

    #             tous_les_mois = []
    #             for dm in dernier_mois:
    #                 tous_les_mois.append(dm[0])
                
    #             return tous_les_mois
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()
    
    # # --------------------------- gestion dette
    # def CRUD_dette(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 0:
    #                 curseur.execute('INSERT INTO dette (nom,montant) VALUES (?,?)', data)
    #                 return curseur.lastrowid
    #             elif state == 1:
    #                 dettes = curseur.execute('SELECT * FROM dette').fetchall()
    #                 return dettes
    #             elif state == 2:
    #                 curseur.execute('UPDATE dette SET nom = ?, montant = ? WHERE id = ?', data)
    #                 return 1
    #             elif state == 3:
    #                 curseur.execute('DELETE FROM dette WHERE id = ?', data)
    #                 return 1
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()

    # # --------------------------- gestion dette
    # def CRUD_sortie(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 0:
    #                 curseur.execute('INSERT INTO sortie (libele,montant,mois_annee) VALUES (?,?,?)', data)
    #                 return curseur.lastrowid
    #             elif state == 1:
    #                 sorties = curseur.execute('SELECT id,libele,montant FROM sortie WHERE mois_annee = ?', data).fetchall()
    #                 return sorties
    #             elif state == 2:
    #                 curseur.execute('UPDATE sortie SET libele = ?, montant = ?, mois_annee = ? WHERE id = ?', data)
    #                 return 1
    #             elif state == 3:
    #                 curseur.execute('DELETE FROM sortie WHERE id = ?', data)
    #                 return 1
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()


    # # --------------------------- gestion C. speciales
    # def CRUD_commandes_speciales(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 0:
    #                 curseur.execute('INSERT INTO commandes_speciales (libele,montant,intrant,mois_annee) VALUES (?,?,?,?)', data)
    #                 return curseur.lastrowid
    #             elif state == 1:
    #                 sorties = curseur.execute('SELECT id,libele,montant,intrant FROM commandes_speciales WHERE mois_annee = ?', data).fetchall()
    #                 return sorties
    #             elif state == 2:
    #                 curseur.execute('UPDATE commandes_speciales SET libele = ?, montant = ?, intrant = ?, mois_annee = ? WHERE id = ?', data)
    #                 return 1
    #             elif state == 3:
    #                 curseur.execute('DELETE FROM commandes_speciales WHERE id = ?', data)
    #                 return 1
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()


    # # --------------------------- gestion Classique

    # def initialisation_classique_mois(self,mt:str):
    #     liste_libele = [
    #         "Impréssion couleur",
    #         "Impréssion N/B",
    #         "Photocopie couleur",
    #         "Photocopie N/B",
    #         "Plastification",
    #         "Saisi et traitment de texte",
    #     ]
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             for l in liste_libele:
    #                 data = (l,"0","0","0",mt)
    #                 curseur = conn.cursor()
    #                 curseur.execute('INSERT INTO classique (libele,qte,total,total_intrant,mois_annee) VALUES (?,?,?,?,?)', data)
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()

    # def CRUD_commandes_classiques(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 1:
    #                 elements = curseur.execute('SELECT id,libele,qte FROM classique WHERE mois_annee = ?', data).fetchall()
    #                 return elements
    #             elif state == 2:
    #                 curseur.execute('UPDATE classique SET qte = ?, total = ?, total_intrant = ? WHERE id = ?', data)
    #                 return 1
                
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()


    # # --------------------------- ventes

    # def initialisation_vente_mois(self,mt:str):
    #     liste_libele = [
    #         "Chemises",
    #         "Sous-Chemises",
    #         "Reliure complete",
    #         "Element reliure",
    #         "Stylo",
    #         "Rame de format",
    #     ]
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             for l in liste_libele:
    #                 data = (l,"0","0",mt)
    #                 curseur = conn.cursor()
    #                 curseur.execute('INSERT INTO ventes (libele,qte,total,mois_annee) VALUES (?,?,?,?)', data)
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()

    # def CRUD_vente(self,state,data=()):
    #     try:
    #         conn = sqlite3.connect(self.cheminBD)
    #         with conn:
    #             curseur = conn.cursor()
    #             if state == 1:
    #                 elements = curseur.execute('SELECT id,libele,qte FROM ventes WHERE mois_annee = ?', data).fetchall()
    #                 return elements
    #             elif state == 2:
    #                 curseur.execute('UPDATE ventes SET qte = ?, total = ? WHERE id = ?', data)
    #                 return 1
                
    #     except sqlite3.Error as e:
    #         print(f"l'erreur est : {e}")
    #     finally:
    #         conn.close()
