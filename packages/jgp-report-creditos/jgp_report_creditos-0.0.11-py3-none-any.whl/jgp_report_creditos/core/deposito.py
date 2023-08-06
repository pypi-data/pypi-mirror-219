import json
#from template.componets.componets import Componets
from jgp_report_creditos.template.components import Componets
from jgp_report_creditos.template.template import HojaCanvas

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


class NumberedCanvas(canvas.Canvas):
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
        """Encabezado"""
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
        """ ********************************* line ********************************************"""
        self.setFont('Helvetica',8)
        ancho, alto = letter
        self.setLineWidth(1.9)# grosor de la linea
        self.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.line(1.4*cm, 25.95*cm, ancho-1.4*cm, 25.95*cm)      
        self.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        print("ªªªªªªªªªªªªªªªªªªªªªªªªª:")    
        x,y= letter
        page = " %s / %s" % (self._pageNumber, page_count)       
        self.saveState()
        """ PIE DE PAGINA """
        # Agregar footer en cada página
        self.drawString(x/2, 1*cm, page)
        self.restoreState()
        #cabecera
        estilos = getSampleStyleSheet()
        font_size=8
        leading_interlineado=10
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=font_size, leading=leading_interlineado,fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        estilos.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
        table=[]
        # Agregar la cabecera de la tabla   
        header = [Paragraph("<b>ID</b>", estilos["center"]),
                Paragraph("<b>Operacion</b>", estilos["center"]), 
                Paragraph("<b>Nombre de cliente</b>", estilos["left"]), 
                Paragraph("<b>Banco</b>", estilos["left"]), 
                Paragraph("<b>Fecha depósito</b>", estilos["left"]), 
                Paragraph("<b>Forma aplicacion</b>", estilos["left"]), 
                Paragraph("<b>Monto</b>", estilos["right"])
                ]
        table.append(header)
        # Definir el tamaño de cada columna
        col_widths = [1.2*cm, 2.2*cm, 4.5*cm, 4*cm, 1.8*cm, 3.5*cm, 1.6*cm]
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
        table.drawOn(self, 1.395*cm, 24.6*cm)

# DepositDetailReport
class  DetalleDepositoReporte:
    def __init__(self, filename, data, titulo, usuario):
        # Crear el lienzo
        canvas_creator = HojaCanvas(filename)
        canvas = canvas_creator.create_canvas()
        #DIVERTIDO ---------------------------------------
        # Crear instancia de Shapes y llamar a las funciones para dibujar figuras
        shapes = Componets(canvas)
        # Encabezado
        y=shapes.encabezado(titulo,usuario)
        print("***********************************************")
        print(data["codigo_operacion"])

        # 1 filas (label, texto x, y, width, tamaño label)             
        y1=shapes.DrawRectanguleBorder("Operación:", data["codigo_operacion"],2, y-0.3, 6.7,1.7)
        shapes.DrawRectanguleBorder("Nombre Cliente:", data["nombre_completo"],7.4+2, y-0.3, 11.1, 2.2,)
        # 2 fila
        concepto_depositos = {"R": "Recuperación de cartera","I": "Ingreso de pagos parciales"}
        y2=shapes.DrawRectanguleBorder("Asesor:", data["asesor"],2, y1, 6.7, 1.7,)
        shapes.DrawRectanguleBorder("Concepto:", concepto_depositos[data["tipo_transaccion"]],7.4+2, y1, 8, 2.2)
        shapes.DrawRectanguleBorder("ID:", data["numero_documento"], 16.3+2, y1, 2.2, 0.65)
        #3 fila 
        bancos =   {"1": "BNB - 1502360716",
                    "2": "Bisa - 7773424017",
                    "3": "Economico - 2051563479",
                    "4": "Union - 10000030927541",
                    "5": "Mercantil Santa Cruz - 4068641015 ",
                    "6": "Solidario 1 - 311780-000-001",
                    "7": "Solidario 2 - 311780-000-002",
                    "8": "Solidario 3 - 311780-000-003",
                    "9": "Solidario 5 - 311780-000-005"}

        estados = { "E": "En proceso",
                    "V":"Verificado",
                    "R":"Registrado en caja",
                    "N":"No Encontrado"}
        y3=shapes.DrawRectanguleBorder("Banco:", bancos[data["banco"]], 2, y2, 6, 1.7,)
        shapes.DrawRectanguleBorder("Fecha:", data["fecha_deposito"], 6.5+2, y2, 2.8, 1)
        shapes.DrawRectanguleBorder("Estado:", estados[data["estado"]], 10.1+2, y2, 4.6, 1.1)
        shapes.DrawRectanguleBorder("Importe:", data["monto_depositado"],15.5+2, y2, 3, 1.3)
        #4 fila 
        y4=shapes.DrawRectanguleBorder("Notas:", data["observaciones"],2, y3, 18.5, 1.7)
        
        #linea  draw_line_gruesa_subtitulo(self, y, subtitulo)
        y5=shapes.draw_line_gruesa_subtitulo(y4,"")
        # y6 = shapes.cuadrado_box(3.5, y5,15.5,13.1) MAL NO RECONOCE EJE X
        #5 fila  generar_imagen(self, imagen_path, ancho, alto, posicion, y_estado)
        image_url = "https://app.jesusgranpoder.com.bo/uploads/depositos/a69824a0a13ffa66a7202a9b6d292c39.jpg"
        imagen_vertical = "https://app.jesusgranpoder.com.bo/uploads/depositos/fa67f78505b1c3ad489f679dcf41e44b.jpg"
        #y7 = shapes.generar_imagen(imagen_vertical,15.5, 13.1,"center",y5) EXCELENTE PERO NO REBAJA POR ESCALA 
        # imagen_scala(self,image_path, width, height):
        #y7 = shapes.resize_image(imagen_vertical, 15.5, 13.1)  MAL REVISAR
        
        canvas.save()
# RegisteredDepositsReport
class  DepositoAplicados:
    def __init__(self, filename, json_datos): 
    #def Depositos_en_banco(self):
        canvas_creator = HojaCanvas(filename)
        canvas = canvas_creator.create_canvas()
        #DIVERTIDO ---------------------------------------
        # Crear instancia de Shapes y llamar a las funciones para dibujar figuras
        shapes = Componets(canvas)
        #Trabajo con el json
        print(json_datos)
        id_json=json_datos["id"]
        imagen_json=json_datos["img"]
        # Encabezado
        titulo="DEPOSITOS APLICADOS"
        y=shapes.encabezado(titulo)
        print("ºººººººººººººººººººººººººººº ENTRA A DEPOSITOS APLICADOS ººººººººººººººººººº")
        print(y)
        y_valor = y-20
        y1 =shapes.generar_tabla_desde_json(25)
        print("------------- ",y1)
        #el json personalizado
        json_file = """
        [
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        }
        ,
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        }
        ,
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        }
        ,
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        },
        {
            "id": 1520,
            "operacion": "501211101538",
            "nombre_cliente": "Velasquez Mendoza Dante Josue",
            "banco": "BNB - 1502360716",
            "fecha_deposito": "2023-05-20",
            "forma_aplicacion": "Recueperacion de cartera",
            "monto": "80.00"
        }

        ]
        """
        datos_json = json.loads(json_file)
        y2= shapes.generate_pdf_from_json(y1,datos_json)
        print(y1)
        # 1 filas (label, texto x, y, width, tamaño label)
        canvas.save()

class  FichaDeDatos:
    def __init__(self, filename, json_datos, titulo, usuario): 
        # Crear el lienzo
        canvas_creator = HojaCanvas(filename)
        canvas = canvas_creator.create_canvas()
        #DIVERTIDO ---------------------------------------
        # Crear instancia de Shapes y llamar a las funciones para dibujar figuras
        shapes = Componets(canvas)
        #Trabajo con el json
        print(json_datos)
        id_json=json_datos["id"]
        imagen_json=json_datos["img"]
        # Encabezado
        y=shapes.encabezado(titulo,usuario)


        """ DESDE AQUI COMIENZA LOS CAMBIOS """
        
        # ========================= 1 line =========================== 
        y0=shapes.draw_line_gruesa_subtitulo(y+0.4,"DATOS PERSONALES")
        # 1 filas (label, texto x, y, width, tamaño label)             
        y1=shapes.DrawRectanguleBorder("Primer Nombre:", id_json,2, y0, 9.2,2.8)
        shapes.DrawRectanguleBorder("No. C.I.:", "texto",9.7+2, y0, 5.7, 3.3)
        shapes.DrawRectanguleBorder("-", "fbgf",15.5+2, y0, 1.1, 0.2)
        shapes.DrawRectanguleBorder("Ext.:", "LP",16.8+2, y0, 1.6, 0.7)
        # 2 fila
        y2=shapes.DrawRectanguleBorder("Segundo Nombre:", "Monica",2, y1, 9.2,2.8)
        shapes.DrawRectanguleBorder("Fecha de Nacimiento:", "texto",11.7, y1, 8.8, 3.3)
        #3 fila 
        y3=shapes.DrawRectanguleBorder("Primer Apellido:", "Monica",2, y2, 9.2,2.8)
        shapes.DrawRectanguleBorder("Lugar Nacimiento:", "texto",11.7, y2, 8.8, 3.3)
        #4 fila 
        y4=shapes.DrawRectanguleBorder("Segundo Apellido:", "Monica",2, y3, 9.2,2.8)
        shapes.DrawRectanguleBorder("Nacionalidad:", "texto",11.7, y3, 8.8, 3.3)
        #5 fila 
        y5=shapes.DrawRectanguleBorder("Apellido de Casada:", "Monica",2, y4, 9.2,2.8)
        shapes.DrawRectanguleBorder("Estado Civil (Ci):", "texto",11.7, y4, 8.8, 3.3)
        #6 fila 
        y6=shapes.DrawRectanguleBorder("Conocido por:", "Monica",2, y5, 9.2,2.8)
        shapes.DrawRectanguleBorder("Estado civil sugún Visita:", "texto",11.7, y5, 8.8, 3.3)
        #7 fila 
        y7=shapes.DrawPalabra("Género:", 2, y6)
        shapes.DrawCheckBox("Femenino", 4.8, y6, 1.8, 1.3, True)
        shapes.DrawCheckBox("Masculino",7.4, y6, 1.8, 1.3, False)
        shapes.DrawRectanguleBorder("Dependientes:", "1",11.7, y6, 8.8, 3.3)
        #8 fila 
        y8=shapes.DrawRectanguleBorder("Nro. Celular (WhatsApp):", "70107672",2, y7, 6.1, 3.3)
        shapes.DrawRectanguleBorder("", "",8.5, y7, 2.8, 0)
        shapes.DrawRectanguleBorder("Correo electrónico:", "mrojascarlo@gmail.com",11.7, y7, 8.8, 2.7)
        # ========================= 2 line =========================== 
        l2=shapes.draw_line_delgada_con_label(y8,"DATOS DEL CONYUGUE")
        # 9 fila
        y9=shapes.DrawRectanguleBorder("Primer Apellido:", "Choquehuanca",2, l2, 5.4, 2.3)
        shapes.DrawRectanguleBorder("Segundo Apellido:", "Choquehuanca",7.7, l2, 5.3, 2.4)
        shapes.DrawRectanguleBorder("Nombres:", "Reynaldo",13.3, l2, 7.2, 1.4)
        # 10 fila
        y10=shapes.DrawRectanguleBorder("Actividad Principal:", "Sn",2, y9, 12.8, 2.6)
        shapes.DrawRectanguleBorder("Nro Celular (WhatsApp):", "",15.2, y9, 5.3, 3.3)
        # 11 fila
        y11=shapes.DrawRectanguleBorder("Lugar de trabajo:", "Sn",2, y10, 11.5, 2.3)
        shapes.DrawRectanguleBorder("Nro. C.I.:", "00",13.8, y10, 3.6, 1.2)
        shapes.DrawRectanguleBorder("-", "",17.5, y10, 1.1, 0.2)
        shapes.DrawRectanguleBorder("Ext.:", "LP",18.8, y10, 1.7, 0.8)
        # ========================= 3 line =========================== 
        l3=shapes.draw_line_gruesa_subtitulo(y11,"DOMICILIO")
        # 12 fila
        y12=shapes.DrawRectanguleBorder("Dirección Domicilio:", "Sn",2, l3, 9.6, 2.6)
        shapes.DrawRectanguleBorder("Nro.Puerta:", "00000",12, l3, 2.7, 1.6)
        shapes.DrawRectanguleBorder("Zona:", "La Paz-Villa Nueva Potosi el texto sobre pasa el box",15, l3, 5.5, 0.85)
        # 13 fila
        y13=shapes.DrawPalabra("Tenencia Vivienda:", 2, y12)
        shapes.DrawCheckBox("Propio", 4.45, y12, 1.4, 0.9, True)
        shapes.DrawCheckBox("Alquiler", 6.1, y12, 1.5, 1, False)
        shapes.DrawCheckBox("Anticrético", 7.8, y12, 1.9, 1.4, False)
        shapes.DrawCheckBox("Prestado", 9.9, y12, 1.7, 1.2, False)
        shapes.DrawCheckBox("Familiar", 11.7, y12, 1.6, 1.1, False)
        shapes.DrawRectanguleBorder("Comentario:", "",13.7, y12, 6.8, 1.7)
        # 14 fila
        y14=shapes.DrawRectanguleBorder("Referencia:", "Sn",2, y13, 15, 1.6)
        shapes.DrawRectanguleBorder("Años Residencia:", "",17.3, y13, 3.2, 2.3)
        # ========================= 4 line =========================== 
        l4=shapes.draw_line_gruesa_subtitulo(y14,"ACTIVIDAD")
        # 15 fila
        y15=shapes.DrawRectanguleBorder("Actividad Principal:", "Estudiante",2, l4, 10.4, 2.6)
        shapes.DrawRectanguleBorder("Años en el Rubro:", "9",12.7, l4, 3.5, 2.4)
        shapes.DrawRectanguleBorder("Años en el Negocio:", "9",16.7, l4, 3.8, 2.7)
        # 16 fila
        y16=shapes.DrawRectanguleBorder("CAEDEC Act. Ppal:", "75140",2, y15, 5, 2.6)
        shapes.DrawRectanguleBorder("", "ACTIVIDADES DE SERVICIOS AUXILIARES PARA LA ADMINISTRACION PUBLICA EN GENERAL",7.1, y15, 13.4,0)
        # 17 fila
        y17=shapes.DrawRectanguleBorder("Dirección Domicilio:", "Sn",2, y16, 9.6, 2.6)
        shapes.DrawRectanguleBorder("Nro.Puerta:", "00000",12, y16, 2.7, 1.6)
        shapes.DrawRectanguleBorder("Zona:", "La Paz-Villa Nueva Potosi el texto sobre pasa el box",15, y16, 5.5, 0.85)
        # 18 fila
        y18=shapes.DrawRectanguleBorder("Referencia:", "Estudiante",2, y17, 14.3, 1.6)
        shapes.DrawRectanguleBorder("Teléfono:", "9",16.6, y17, 3.9, 1.3)
        # 19 fila
        y19=shapes.DrawPalabra("Días Laborales:", 2, y18)
        shapes.DrawCheckBox("LU", 4.2, y18, 0.9,0.4, True)
        shapes.DrawCheckBox("MA", 5.4, y18, 1, 0.5, True)
        shapes.DrawCheckBox("MI", 6.6, y18, 0.9, 0.4, True)
        shapes.DrawCheckBox("JU", 7.8, y18, 0.9, 0.4, True)
        shapes.DrawCheckBox("VI", 9, y18, 0.9, 0.4, True)
        shapes.DrawCheckBox("SA", 10.1, y18, 0.9, 0.4, True)
        shapes.DrawCheckBox("DO", 11.3, y18, 1, 0.5, False)
        shapes.DrawPalabra("Horario:", 14.7, y18)
        shapes.DrawRectanguleBorder("desde", "08:30",15.9, y18, 2.2, 0.9)
        shapes.DrawRectanguleBorder("hasta", "18:30",18.3, y18, 2.2, 0.8)
        # 20 fila
        y20=shapes.DrawPalabra("Tenencia Negocio:", 2, y19)
        shapes.DrawCheckBox("Propio", 4.45, y19, 1.4, 0.9, True)
        shapes.DrawCheckBox("Alquiler", 6.1, y19, 1.5, 1, False)
        shapes.DrawCheckBox("Anticrético", 7.8, y19, 1.9, 1.4, False)
        shapes.DrawCheckBox("Prestado", 9.9, y19, 1.7, 1.2, False)
        shapes.DrawCheckBox("Familiar", 11.7, y19, 1.6, 1.1, False)
        shapes.DrawCheckBox("Otros", 13.4, y19, 1.3, 0.8, False)
        shapes.DrawRectanguleBorder("Comentario:", "",15.1, y19, 5.4, 1.7)        
        # 21 fila
        y21=shapes.DrawPalabra("Tipo de Negocio:", 2, y20)
        shapes.DrawCheckBox("Fijo", 4.2, y20, 1, 0.5, True)
        shapes.DrawCheckBox("Ambulante", 5.5, y20, 1.9, 1.4, False)
        shapes.DrawPalabra("Tipo de Ingreso:", 7.8, y20)
        shapes.DrawCheckBox("Dependiente", 9.9, y20, 2.2, 1.7, True)
        shapes.DrawCheckBox("Independiente", 12.3, y20, 2.4, 1.9, False)
        shapes.DrawRectanguleBorder("Ingreso Mensual Aprox.:", "0.00",15.2, y20, 5.3, 3.2) 
        # ========================= 5 line =========================== 
        l5=shapes.draw_line_delgada(y21)
        # 22 fila
        y22=shapes.DrawRectanguleBorder("Actividad Sec.:", "",2, l5, 10.4, 2.6)
        shapes.DrawRectanguleBorder("Años en el Rubro:", "",12.7, l5, 3.5, 2.4)
        shapes.DrawRectanguleBorder("Años en el Negocio:", "",16.7, l5, 3.8, 2.7)
        # 23 fila
        y23=shapes.DrawRectanguleBorder("CAEDEC Act. Sec:", "",2, y22, 5, 2.6)
        shapes.DrawRectanguleBorder("", "",7.1, y22, 13.4,0)
        # 24 fila
        y24=shapes.DrawRectanguleBorder("Dirección Domicilio:", "Sn",2, y23, 9.6, 2.6)
        shapes.DrawRectanguleBorder("Nro.Puerta:", "00000",12, y23, 2.7, 1.6)
        shapes.DrawRectanguleBorder("Zona:", "La Paz-Villa Nueva Potosi el texto sobre pasa el box",15, y23, 5.5, 0.85)
        # 25 fila
        y25=shapes.DrawRectanguleBorder("Referencia:", "",2, y24, 14.3, 1.6)
        shapes.DrawRectanguleBorder("Teléfono:", "",16.6, y24, 3.9, 1.3)
        # 26 fila
        y26=shapes.DrawPalabra("Días Laborales:", 2, y25)
        shapes.DrawCheckBox("LU", 4.2, y25, 0.9,0.4, True)
        shapes.DrawCheckBox("MA", 5.4, y25, 1, 0.5, True)
        shapes.DrawCheckBox("MI", 6.6, y25, 0.9, 0.4, True)
        shapes.DrawCheckBox("JU", 7.8, y25, 0.9, 0.4, True)
        shapes.DrawCheckBox("VI", 9, y25, 0.9, 0.4, True)
        shapes.DrawCheckBox("SA", 10.1, y25, 0.9, 0.4, True)
        shapes.DrawCheckBox("DO", 11.3, y25, 1, 0.5, False)
        shapes.DrawPalabra("Horario:", 14.7, y25)
        shapes.DrawRectanguleBorder("desde", "08:30",15.9, y25, 2.2, 0.9)
        shapes.DrawRectanguleBorder("hasta", "18:30",18.3, y25, 2.2, 0.8)
        # 27 fila
        y27=shapes.DrawPalabra("Tenencia Negocio:", 2, y26)
        shapes.DrawCheckBox("Propio", 4.45, y26, 1.4, 0.9, True)
        shapes.DrawCheckBox("Alquiler", 6.1, y26, 1.5, 1, False)
        shapes.DrawCheckBox("Anticrético", 7.8, y26, 1.9, 1.4, False)
        shapes.DrawCheckBox("Prestado", 9.9, y26, 1.7, 1.2, False)
        shapes.DrawCheckBox("Familiar", 11.7, y26, 1.6, 1.1, False)
        shapes.DrawCheckBox("Otros", 13.4, y26, 1.3, 0.8, False)
        shapes.DrawRectanguleBorder("Comentario:", "",15.1, y26, 5.4, 1.7)        
        # 28 fila
        y28=shapes.DrawPalabra("Tipo de Negocio:", 2, y27)
        shapes.DrawCheckBox("Fijo", 4.2, y27, 1, 0.5, True)
        shapes.DrawCheckBox("Ambulante", 5.5, y27, 1.9, 1.4, False)
        shapes.DrawPalabra("Tipo de Ingreso:", 7.8, y27)
        shapes.DrawCheckBox("Dependiente", 9.9, y27, 2.2, 1.7, True)
        shapes.DrawCheckBox("Independiente", 12.3, y27, 2.4, 1.9, False)
        shapes.DrawRectanguleBorder("Ingreso Mensual Aprox.:", "",15.2, y27, 5.3, 3.2) 
        # ========================= 6 line =========================== 
        l6=shapes.draw_line_gruesa_subtitulo(y28,"REFERENCIAS")
        # 29 fila
        y29=shapes.DrawRectanguleBorder("Referencia Familiar:", "",2, l6, 10.3, 2.7)
        shapes.DrawRectanguleBorder("Celular:", "9",12.5, l6, 3.1, 1.1)
        shapes.DrawRectanguleBorder("Parentesco:", "",15.9, l6, 4.6, 1.7)
        # 30 fila
        y30=shapes.DrawRectanguleBorder("Dirección:", "Calle 4 De Mayo, Zona Alto San Pedro",2, y29, 18.5, 1.5)
        # ========================= 7 line =========================== 
        l7=shapes.draw_line_delgada(y30)
        # 31 fila
        y31=shapes.DrawRectanguleBorder("Referencia Personal:", "",2, l7, 10.3, 2.7)
        shapes.DrawRectanguleBorder("Celular:", "9",12.5, l7, 3.1, 1.1)
        shapes.DrawRectanguleBorder("Parentesco:", "",15.9, l7, 4.6, 1.7)
        # 32 fila
        y32=shapes.DrawRectanguleBorder("Dirección:", "Calle 4 De Mayo, Zona Alto San Pedro",2, y31, 18.5, 1.5)
        # 33 texto
        nombre_completo="Rojas Carlo Maria Monica"
        carnet_identidad="6129195LP"
        texto="Yo, "+nombre_completo+"  con C.I. "+carnet_identidad+" autorizo en forma expresa a GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A., a solicitar informacion sobre mis antecedentes crediticios y otras cuentas por pagar de carácter económico, financiero y comercial registrados en el BI y la CIC de la Autoridad de Supervisión del Sistema Financiero (ASFI), mientras dure mi relación contractual con el citado usuario. Asimismo, autorizó: a) Incorporar los datos crediticios y de otras cuentas por pagar de carácter económico, financiero y comercial derivados de la relación con GESTION Y SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A., en la(s) base(s) de datos de propiedad de los Burós de Información que cuenten con Licencia de Funcionamiento de ASFI y en la CIC. b) Al registro de mis datos crediticios en las bases de datos de INFOCENTER S.A, con licencia de funcionamiento del Organismo de Supervisión, ASFI maravillosa LA PAZ."
        print("y32: ", y32)
        y33 =  shapes.Paragraph(2, y32, texto,18.5, 1.5)
        # 34 firmas
        print("y33: ",y33)
        print(y33)

        y34=shapes.TableSign(2,y33)
        # Guardar y cerrar el lienzo
        canvas.save()
