import json
from reportlab.platypus import (SimpleDocTemplate, Spacer, Paragraph, Table)

import datetime
import io
#from msilib import Table

import os
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

#preubas 2 round
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

#
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO
import os
# Importaciones para la tabla
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT

print("dsdsdd")

class Componets:
    index=1
    cont=1
    def __init__(self, canvas):
        self.canvas = canvas

    # ===================todo para tabla=======================
    
    def generate_pdf_from_json(self,y,json_file):
        # Estilos de parrafos
        #Add styles
        estilos = getSampleStyleSheet()
        #type of styles
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=9.1, fontName = 'Helvetica'))
        estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=9.1, fontName = 'Helvetica'))
        estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=9.1, fontName = 'Helvetica'))
        estilos.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontSize=9.1, fontName = 'Helvetica'))

        data=json_file
        print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
        print(data[1]["id"])

        # Crear un nuevo lienzo
        #c = canvas.Canvas(output_pdf, pagesize=letter)

        # Definir la posición de inicio de la tabla
        x = 50

        # Definir el tamaño de cada columna
        #datos 4 ahora---> 6
        col_widths = [0.8*cm, 2.5*cm, 4.5*cm, 4*cm, 2.7*cm, 3.1*cm, 1.5*cm]

        # Definir el estilo de la tabla
        style = TableStyle([#-1 ultimo -2 antipenultimo
            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('VALIGN',(0,0),(-1,0),'MIDDLE'),
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.gray),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255))),#color del fondo del encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),#color de la letra del encabezado
            #('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            #('BACKGROUND', (0, 1), (-1, -1), colors.beige),#pinta lo interno debajo del encabezado 
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Crear una lista para almacenar las filas de la tabla
        table_data = []

        # Agregar la cabecera de la tabla
        header = ["ID", "Operacion", "Nombre \n de \n cliente", "Banco", "Fecha \n depósito",  "Forma \n aplicacion", "Monto"]
        table_data.append(header)

        # Agregar los datos de cada registro al table_data
        for record in data:
            row = [
                Paragraph(str(round(record["id"],2))),
                Paragraph(record["operacion"]),
                Paragraph(record["nombre_cliente"]),
                Paragraph(record["banco"]),
                Paragraph(record["fecha_deposito"],estilos["left"]),
                Paragraph(record["forma_aplicacion"],estilos["right"]),
                Paragraph(record["monto"], estilos["center"])
            ]
        
            table_data.append(row)

        # Crear la tabla
        table = Table(table_data, colWidths=col_widths, rowHeights=None )

        # Aplicar el estilo a la tabla
        table.setStyle(style)

        # Dibujar la tabla en el lienzo
        table.wrapOn(self.canvas, 0, 0)
        # Posicion de la tabla (x,y)
        table.drawOn(self.canvas, x, y*cm)
    
    # =================== IMAGEN REBAJA POR PIXCELES =======================
    """def resize_image(self,image_path, width, height):
        image = Image.open(image_path)
        image.thumbnail((width, height))
        return image"""
    
    def imagen_scala(self, image_url, y ,width_x, height_y):
        # Descargar la imagen desde la URL
        response = requests.get(image_url)
        image_data = BytesIO(response.content)

        # Cargar y redimensionar la imagen (image_data, 100, 200)
        image = self.resize_image(image_data, width_x, height_y)

        # Obtener la extensión de la imagen original
        image_extension = response.headers.get("content-type").split("/")[-1]
        if not image_extension:
            image_extension = "jpg"  # Asignar una extensión predeterminada si no se puede obtener

        # Guardar la imagen redimensionada en un archivo temporal
        temp_file = f"temp_image.{image_extension}"
        image.save(temp_file)

        # Obtener las dimensiones de la imagen redimensionada
        image_width, image_height = image.size

        # Agregar la imagen al lienzo
        self.canvas.drawImage(temp_file, x=100, y=y*cm, width=image_width*cm, height=image_height*cm)

        # Eliminar el archivo temporal
    # =================== IMAGEN POSICION =======================
    def get_position(self,position, canvas_width, image_width):
        if position.lower() == 'left':
            return 2
        elif position.lower() == 'right':
            return canvas_width - image_width-1
        elif position.lower() == 'center':
            return (canvas_width - image_width) / 2
        else:
            raise ValueError('La posición debe ser "left", "right" o "center".')

    def generar_imagen(self, imagen_path, ancho, alto, posicion, y_estado):
        canvas_width, canvas_height = letter

        pulgadas=2.54
        canvas_width = (canvas_width/72)
        canvas_width = canvas_width*pulgadas

        image_width = ancho 
        image_height = alto 

        x = self.get_position(posicion, canvas_width, image_width)
        y = y_estado - alto
        self.canvas.drawImage(imagen_path, x*cm, y *cm, width=image_width *cm, height=image_height*cm )
        return y
    
    def image_draw(self,x, y, width, height, url):
        spacio=0.5
        y= y-height-spacio
        print("valor de y dado: ", y)
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo,self.index,self.cont)
            # Iniializo el valor de y ademas i++ para el cambio de pagina
            # arriba 25 inicio de pagina
            y=27.7- height
            print("cambio de pagina ini: ", y)
        self.canvas.drawImage(url,x * cm, y * cm, width *cm, height *cm, mask=None)
        return y

    def cuadrado_box(self, x, y, pwidth,pheight):
        # Dibujar el rectángulo rect(self, x, y, width, height, stroke=1, fill=0)
        #espacio=0.5
        y= y-pwidth
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            # Iniializo el valor de y ademas i++ para el cambio de pagina
            # arriba 25 inicio de pagina
            y=27.7- pwidth
            
        self.canvas.setLineWidth(0.4)# grosor de la linea
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.setFillColor(colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255)))
        self.canvas.rect((x)*cm, (y)*cm, (pwidth)*cm, (pheight)*cm, stroke = 1,fill=1)# borde
        
        print("posicion de lienzo despues de dibujar y: ",y)
        return y

    def DrawRectanguleBorder(self, text_label, text,x, y, pwidth, tamaño_label): 
        #tamaño_label
        pheight =0.5   # *cm estatico
        y= y-pheight
        if(y<2):
            print("=============================================")
            print("Debe de irse a otra pagina")
            print("pwidth: ",pwidth)
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            # Iniializo el valor de y ademas i++ para el cambio de pagina
            # arriba 25 inicio de pagina
            y=25.71- pheight
            
        #width  =7   *cm dado
        label_sm = tamaño_label     #*cm  tamaño: lable_smedio 2cm
        
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text_label)

        # Dibujar el rectángulo rect(self, x, y, width, height, stroke=1, fill=0)
        self.canvas.setLineWidth(0.4)# grosor de la linea
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.setFillColor(colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255)))
        self.canvas.rect((x+label_sm)*cm, y*cm, (pwidth-label_sm)*cm, (pheight-0.1)*cm, stroke = 1,fill=1)# borde

        # Agregar el texto dentro del rectángulo
        self.canvas.setFont("Helvetica", 8)
        self.canvas.setFillColor(colors.black)
        #pwidth-tamaño_label
        lineas = []
        print(text)
        if(text!="" and text!=None ):
            palabras = text.split() 
            linea_actual = palabras[0] 
            for palabra in palabras[1:]: 
                if self.canvas.stringWidth(linea_actual + " " + palabra, "Helvetica", 8) <= (pwidth-tamaño_label)*cm: 
                    linea_actual += " " + palabra 
                else: 
                    lineas.append(linea_actual) 
                    linea_actual = palabra 
            lineas.append(linea_actual) 
            text=lineas[0]

            estilos = getSampleStyleSheet()
            font_size=8
            estilos.add(ParagraphStyle(name='texto_into_box', alignment=TA_LEFT, fontSize=font_size, fontName='Helvetica',leading=8,textColor=colors.black))
            estilo_titulo = estilos["texto_into_box"]
            parrafo = Paragraph(text, estilo_titulo)
            parrafo.wrapOn(self.canvas, (pwidth-tamaño_label-0.2) * cm, 0.5 * cm)  # Anchura y altura máxima del párrafo en puntos
            parrafo.drawOn(self.canvas, (x+label_sm+0.2)*cm, (y + 0.1) * cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

        # en caso de que la cadena este vacia SALDRA -
        else:
            estilos = getSampleStyleSheet()
            font_size=8
            estilos.add(ParagraphStyle(name='cadena_vacia', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica',leading=8,textColor=colors.black))
            estilo_titulo = estilos["cadena_vacia"]
            text="-"
            parrafo = Paragraph(text, estilo_titulo)
            parrafo.wrapOn(self.canvas, (pwidth-tamaño_label) * cm, 0.5 * cm)  # Anchura y altura máxima del párrafo en puntos
            parrafo.drawOn(self.canvas, (x+label_sm)*cm, (y + 0.15) * cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo



        
        return y

    def DrawIntoBox(self, x, y,texto,width):
        self.canvas.setFillColor(colors.black)
        tamaño_letra_parrafo=8
        self.canvas.setFont("Helvetica", tamaño_letra_parrafo)  # Fuente: Helvetica, Tamaño: 12 puntos 
        # Divide el texto en líneas para que no exceda el ancho dado 
        lineas = [] 
        if(texto!=""):
            palabras = texto.split() 
            linea_actual = palabras[0] 
            for palabra in palabras[1:]: 
                if self.canvas.stringWidth(linea_actual + " " + palabra, "Helvetica", tamaño_letra_parrafo) <= width: 
                    linea_actual += " " + palabra 
                else: 
                    lineas.append(linea_actual) 
                    linea_actual = palabra 
            lineas.append(linea_actual) 
            # Verifica si alguna línea excede el ancho dado 
            if any(self.canvas.stringWidth(linea, "Helvetica", tamaño_letra_parrafo) > width for linea in lineas): 
                print("Error: Al menos una línea excede el ancho proporcionado.") 
                return 
            # Calcula la altura total del texto 
            altura_texto = len(lineas) * 14  # 14 puntos de altura para cada línea 
            # Calcula la posición de inicio en el eje y 
            y_inicio = y - altura_texto 
            # Dibuja el rectángulo del área de texto 
            self.canvas.rect(x, y_inicio, width, altura_texto) 
            # Dibuja cada línea de texto en sentido normal 
            for linea in lineas[0:1]: 
                self.canvas.drawString(2*cm, 15*cm + (altura_texto - 1*7), "prueba") 
                self.canvas.drawString(x, y*cm + (altura_texto - 1*7), linea) 
                
    def DrawPalabra(self, text,x, y):
        #tamaño_label
        pheight =0.5   # *cm estatico
        y= y-pheight
        if(y<2):
            print("=============================================")
            print("Debe de irse a otra pagina")
            
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            # Iniializo el valor de y ademas i++ para el cambio de pagina
            # arriba 25 inicio de pagina
            y=25.71- pheight        
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text)
        return y

    def draw_line_gruesa_subtitulo(self, y, subtitulo): 
        """ line """
        ancho, alto = letter
        pheight=0.4
        y= y-pheight
        if(y<2):
            print("=============================================")
            print("Debe de irse a otra pagina--------")
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo,self.index,40)
            # Iniializo el valor de y ademas i++ para el cambio de pagina: arriba 25 inicio de pagina
            y=25.71
        self.canvas.setLineWidth(2)# grosor de la linea
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, y*cm, ancho-30.9, y*cm)
        # Agregar el subtitulo
        self.canvas.setFillColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.setFont("Helvetica-Bold", 8)
        self.canvas.drawString(2 * cm, (y-0.4)* cm, subtitulo)
        return y-0.5

    def DrawCheckBox(self, text_label, x, y, pwidth, tamaño_label, sw):
        #tamaño_label
        pheight =0.5   # *cm estatico
        y= y-pheight
        if(y<2):
            print("=============================================")
            print("Debe de irse a otra pagina")
            print("pwidth: ",pwidth)
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            # Iniializo el valor de y ademas i++ para el cambio de pagina
            # arriba 25 inicio de pagina
            y=25.71- pheight
            
        #width  =7   *cm dado
        label_sm = tamaño_label     #*cm  tamaño: lable_smedio 2cm
        
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text_label)

        # Dibujar el rectángulo rect(self, x, y, width, height, stroke=1, fill=0)
        self.canvas.setLineWidth(0.4)# grosor de la linea
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.setFillColor(colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255)))
        self.canvas.rect((x+label_sm)*cm, y*cm, (pwidth-label_sm)*cm, (pheight-0.1)*cm, stroke = 1,fill=1)# borde

        if sw:
            # Agregar simbolo check si lo requiere
            pheight_check=0.45
            # Dibujar el símbolo de marca de verificación
            self.canvas.setFont("Helvetica", pheight_check*cm)
            self.canvas.setFillColor(colors.black)
            self.canvas.drawString((x+label_sm+0.1)*cm, (y + 0.05) * cm, u"\u2713")  # Código Unicode para el símbolo de marca de verificación
        return y

    def TableSign(self,x,y):
        # Agregar la cabecera de la tabla   
        table = [["", "", ""],
                ["FIRMA DEL CLIENTE", "FIRMA Y SELLO DE ASESOR COMERCIAL", "FIRMA Y SELO PLATAFORMA"]]
        
        # Definir el tamaño de cada columna
        col_widths = [6.2*cm, 6.2*cm, 6.2*cm]
        row_widths = [1.6*cm, 0.4*cm]
        # Definir el estilo de la tabla
        style = TableStyle([           
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),# interlineado Puede ser TOP, MIDDLE o BOTTOM
            ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))),#color de la tabla(lineas)
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))),# color del subtitulo
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN',(0, 0), (-1, -1),'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ])
        # Crear la tabla
        table = Table(table, colWidths=col_widths, rowHeights=row_widths)
        # Aplicar el estilo a la tabla
        table.setStyle(style)
        # Dibujar la tabla en el lienzo
        table.wrapOn(self.canvas, 20, 10)
        # Posición de la tabla "lienzo" (x,y)
        table.drawOn(self.canvas, x*cm, (y-2.5+0.35)*cm)# 2.5 ancho de la tabla
        print("sale TABLA")
        return y-2.5+0.3
    
    def Paragraph(self,x, y, texto, width, height):
        
        y=(y-0.3-height)
        print("Donde empieza a dibujar el parrafo: ",y)

        # x=x*cm
        # width=width*cm
        # height=height*cm
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='parrafo', alignment=TA_JUSTIFY, fontSize=6, fontName='Helvetica',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        estilo_titulo = estilos["parrafo"]
        parrafo = Paragraph(texto, estilo_titulo)
        parrafo.wrapOn(self.canvas, width*cm, height*cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(self.canvas, x * cm, y* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

        print("retorna el parrafo: ",y)
        return (y)
    
    def draw_line_delgada(self,y): 
        """ line """
        tobutton=0.2
        ancho, alto = letter
        self.canvas.setLineWidth(0.8)# grosor de la linea
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, (y-tobutton)*cm, ancho-30.9, (y-tobutton)*cm)
        return y-0.3

    def draw_line_delgada_con_label(self,y, subtitulo): 
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        """ line """
        ancho, alto = letter
        pheight=0.2
        y= y-pheight
        if(y<2):
            print("=============================================")
            print("Debe de irse a otra pagina--------")
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo,self.index,40)
            # Iniializo el valor de y ademas i++ para el cambio de pagina: arriba 25 inicio de pagina
            y=25.71
        self.canvas.setLineWidth(0.8)# grosor de la linea
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, y*cm, ancho-30.9, y*cm)
        # Agregar el subtitulo
        self.canvas.setFillColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.setFont("Helvetica-Bold", 8)
        self.canvas.drawString(2 * cm, (y-0.4)* cm, subtitulo)
        return y-0.5

    def ajustar_fuente_para_wrap(self,texto, estilo, ancho_maximo):
        from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
        fuente = getFont(estilo.fontName)
        tamaño_inicial = estilo.fontSize
        ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        
        while ancho_texto > ancho_maximo and tamaño_inicial > 1:
            tamaño_inicial -= 1
            print("tamaño inicial: ",tamaño_inicial)
            ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        estilo.fontSize = tamaño_inicial

    def encabezado(self,titulo, usuario):
        # Change the position of this to wherever you want the page number to be
        """Encabezado"""
        self.canvas.setFont('Helvetica',7)#corregido
        #obtengo la fecha actual
        x= datetime.datetime.now()
        #setting model of date
        ancho, alto = letter
        formatoFecha= x.strftime("%d/%m/%Y")
        self.canvas.drawString(ancho-90, 27*cm, 'Fecha: '+formatoFecha)
        self.canvas.drawString(ancho-90, 26.6*cm, usuario)

        """ Titulo """
        estilos = getSampleStyleSheet()
        font_size=14
        estilos.add(ParagraphStyle(name='titulo', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        ancho, alto=letter
        estilo_titulo = estilos["titulo"]
        self.ajustar_fuente_para_wrap(titulo, estilo_titulo, 10.8 * cm)
        parrafo = Paragraph(titulo, estilo_titulo)
        parrafo.wrapOn(self.canvas, 9.5 * cm, 1 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(self.canvas, 8 *cm, 27*cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

        #self.canvas.drawString(letter[1]-19.3 *cm, 26.5*cm, titulo)


        """ imagen """
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../resources/img/logo_jgp.png')
        # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
        self.canvas.drawImage(img, 2 * cm, 26.1 * cm, 160, 35, mask=None)  
        """ line """
        ancho, alto = letter
        self.canvas.setLineWidth(2)
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, 25.7*cm, ancho-30.9, 25.7*cm)
        print("ªªªªªªªªªªªªªªªªªªªªªªªªª:")
        return 25.7 #0.3 espacio de abajo