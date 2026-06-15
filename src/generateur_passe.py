import secrets
import string
import os

class Generateur_MDP:
    dossier_utilisateur = os.path.expanduser("~")
    chemin_fichier_txt = os.path.join(dossier_utilisateur, "DocumentsSa", "suiviStock_CG")
    chemin_fichier_txt = os.path.join(chemin_fichier_txt, "mot_de_passe.txt")
    
    @classmethod
    def set_mot_de_passe(cls):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        mot_de_passe = ''.join(secrets.choice(alphabet) for i in range (20))
        mot_de_passe = "    "
        try:
            with open(cls.chemin_fichier_txt, "w", encoding="utf-8") as f:
                f.write(mot_de_passe)
        except IOError as e:
            print(f"Erreur lors de l'écriture : {e}")


    @classmethod
    def comparer_mot_de_passe(cls, passe_saisi):
        try:
            with open(cls.chemin_fichier_txt, "r", encoding="utf-8") as f:
                passe = f.read()
                if passe == passe_saisi:
                    return True
                else:
                    return False
        except IOError as e:
            print(f"Erreur lors de l'écriture : {e}")


