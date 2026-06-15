from datetime import datetime
import os
import subprocess
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, orientation, unit, format):
        super().__init__(orientation, unit, format)

        self.horodatage = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        dossier_utilisateur = os.path.expanduser("~")
        self.chemin_fichier = os.path.join(dossier_utilisateur, "DocumentsSa", "suiviStock_CG", "doc_pdf")
        os.makedirs(self.chemin_fichier, exist_ok=True)
        self.chemin_fichier = os.path.join(self.chemin_fichier, f"fichier_{self.horodatage}.pdf")

        self.add_font('ArrialNarrow', '', 'src/assets/police/ArialNarrow/arialnarrow.ttf', uni=True)
        self.add_font('ArrialNarrow', 'B', 'src/assets/police/ArialNarrow/arialnarrow_bold.ttf', uni=True)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')

        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f"Edité par salcom le {self.horodatage}", 0, 0, 'L')

    def ouvrir_fchier(self):
        self.output(self.chemin_fichier, "F")

        relative = self.chemin_fichier
        absolue = os.path.abspath(relative)
        subprocess.Popen(['start', '', absolue], shell=True)
