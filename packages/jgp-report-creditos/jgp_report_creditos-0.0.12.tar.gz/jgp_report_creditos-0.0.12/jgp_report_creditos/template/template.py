# -*- coding:utf-8 -*
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# Tambien podemos usar otras medidas
#from report_detalle_deposito import report_detalle_deposito1

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#Cambiar la hrientacion de la pagina

from reportlab.lib.pagesizes import landscape, letter


class HojaCanvas():
    def __init__(self, filename):
        self.filename = filename

    def create_canvas(self):
        # hoja normal vertical: pagesize=letter ; hoja horizontal: pagesize=landscape(letter)
        return canvas.Canvas(self.filename, pagesize=letter)

    
    


