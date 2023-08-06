#clase 
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import  Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
#Importaciones para la tabla requerida
from reportlab.platypus import (Paragraph, Table)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
import datetime
import os
from reportlab.pdfgen import canvas


class NumberedCanvasPasajes(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)
    def draw_page_number(self, page_count):
        # Dibuja el encabezado personalizado en cada página
        # ******************************* Encabezado ***************************************
        self.setFont('Helvetica',8)
        #obtengo la fecha actual
        x= datetime.datetime.now()
        #setting model of date
        ancho, alto = letter
        formatoFecha= x.strftime("%d/%m/%Y")
        self.drawString(ancho-3.8*cm, 27.1*cm, 'Fecha: '+formatoFecha)
        """ imagen """
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../resources/img/logo_jgp.png')
        # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
        self.drawImage(img, 1.4 * cm, 26.25 * cm, 5.5*cm, 1.2*cm, mask=None)  
        # ********************************* line ********************************************
        self.setFont('Helvetica',8)
        ancho, alto = letter
        self.setLineWidth(1.9)# grosor de la linea
        self.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.line(1.4*cm, 25.95*cm, ancho-1.4*cm, 25.95*cm)      
        self.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección 
        # ***************************** Información Asesor *********************************
        # Fila Labels
        estilos = getSampleStyleSheet()
        font_size=8
        leading_interlineado=9
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=font_size, leading=leading_interlineado,fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        table_info=[]
        # Agregar la cabecera de la tabla   
        header = [Paragraph("<b>Asesor Comercial:</b>", estilos["left"]),
                Paragraph("<b>Sucursal:</b>", estilos["left"]), 
                Paragraph("<b>Periodo:</b>", estilos["left"])
                ]
        table_info.append(header)
        
        # Crear una nueva fila con la suma total
        info_row = [Paragraph("Carla A. Condori", estilos["left"]),
                Paragraph("El Carmen", estilos["left"]),
                Paragraph("01/06/2023 al 31/07/2023", estilos["left"]),
                ]
        table_info.append(info_row)
                
        # Definir el tamaño de cada columna
        col_widths = [6.3*cm, 6.2*cm, 6.1*cm]
        # Definir el estilo de la tabla
        style = TableStyle([           
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),# interlineado Puede ser TOP, MIDDLE o BOTTOM
            ('TOPPADDING', (0,0),(-1,-1), 1),
            ('BOTTOMPADDING', (0,0),(-1,-1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
            ('RIGHTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
            #('GRID', (0, 0), (-1, -1), 0.5, colors.gray),#color de la tabla
        ])
        # Crear la tabla
        table_info = Table(table_info, colWidths=col_widths, rowHeights=None)
        # Aplicar el estilo a la tabla
        table_info.setStyle(style)
        # Dibujar la tabla en el lienzo
        table_info.wrapOn(self, -10, 0)
        # Posición de la tabla "lienzo" (x,y)
        table_info.drawOn(self, 1.395*cm, 24.8*cm)

        #************************************ PIE DE PAGINA *********************************
        # Agregar footer en cada página
        self.setFont('Helvetica',8)
        x,y= letter
        page = " %s / %s" % (self._pageNumber, page_count)       
        self.saveState()
        self.drawString(x/2, 1*cm, page)
        self.restoreState()







        #cabecera
        
        table=[]
        # Agregar la cabecera de la tabla   
        header = [Paragraph("<b>Fecha</b>", estilos["center"]),
                Paragraph("<b>Cliente</b>", estilos["center"]), 
                Paragraph("<b>Dirección - Ubicación</b>", estilos["left"]), 
                Paragraph("<b>Asunto</b>", estilos["left"]), 
                Paragraph("<b>Detalle</b>", estilos["left"]), 
                Paragraph("<b>Monto</b>", estilos["left"])
                ]
        table.append(header)
        # Definir el tamaño de cada columna
        col_widths = [3.3*cm, 3.4*cm, 4.9*cm, 2.2*cm, 3.6*cm, 1.4*cm]
        # Definir el estilo de la tabla
        style = TableStyle([           
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),# interlineado Puede ser TOP, MIDDLE o BOTTOM
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),#color de la tabla(lineas)
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=(221.0/255), green=(221.0/255), blue=(221.0/255))),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),# color del subtitulo
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ])
        # Crear la tabla
        table = Table(table, colWidths=col_widths, rowHeights=None)
        # Aplicar el estilo a la tabla
        table.setStyle(style)
        # Dibujar la tabla en el lienzo
        table.wrapOn(self, -10, 0)
        # Posición de la tabla "lienzo" (x,y)
        table.drawOn(self, 1.395*cm, 23.9*cm)


