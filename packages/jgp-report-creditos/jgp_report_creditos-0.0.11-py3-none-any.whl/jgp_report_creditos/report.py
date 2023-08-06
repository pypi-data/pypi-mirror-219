#!/usr/bin/env python3
from .core.contrato.v1.contratos import ContratoPersonal, ContratoConvenio, ContratoConvenioCustodiaInmueble, ContratoConvenioCustodiaVehiculo, ContratoCustosiaInmueblePampahasi, ContratoDocumentoCustodiaVehiculo, ContratoOtroDocumentoCustodiaPatente, ContratoPersonalDocumentosCustodiaVehiculo, ContratoQuirografariaOficinaElCarmen, ContratoSolidario, ContratoConvenioGarantiaPersonal, ContratoPrendariayPersonal, ContratoErrorBase
# MACKE DEPOSITO
from .core.deposito import DetalleDepositoReporte, DepositoAplicados, FichaDeDatos
# Nuevos cambio creo deposito
from .core.deposito import NumberedCanvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF4
from reportlab.lib.units import inch, mm,cm
import json

import PyPDF4
#
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

#Importaciones para la tabla requerida
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from functools import partial

# import utils
from jgp_utils.date_time import formato_fecha

def makeContato(object_json, usuario=""):
        #CONVIERTO EL JSON EN LIBRERIA
        contrato = object_json
        #SACO EL NOMBRE DEL DOCUMENTO---(descriptión)

        tipo_garantia_=contrato["tipo_garantia"]
        print()
        description=tipo_garantia_["descripcion"]
        print(description)
        print("=================== \n")
        print("DDDDDDDDDDDDDDDDDDDDDDDDdd", contrato,usuario)
        
        #GENERO LOS PDF
        if description == "Personal":
            contrato_personal = ContratoPersonal(contrato, usuario)    
            return contrato_personal.generar1()

        elif description == "Solidario":
            contrato_solidario = ContratoSolidario(contrato,usuario)    
            return contrato_solidario.generar1()

        elif description == "Quirografaria":
            contrato_quirografaria_carmen = ContratoQuirografariaOficinaElCarmen(contrato,usuario)    
            return contrato_quirografaria_carmen.generar1()

        elif description == "Convenio":
            contrato_convenio = ContratoConvenio(contrato,usuario)  
            x = contrato_convenio.generar1()
            return x
            
        elif description == "Personal y Doc. custodia Vehiculo":
                contrato_personal_documento_custodia_vehiculo = ContratoPersonalDocumentosCustodiaVehiculo(contrato,usuario)    
                return contrato_personal_documento_custodia_vehiculo.generar1()
        
        elif description == "Doc. Custodia de Inmueble":
            contrato_custodia_inmueble_pampahasi = ContratoCustosiaInmueblePampahasi(contrato,usuario)    
            return contrato_custodia_inmueble_pampahasi.generar1()
            
        elif description == "Doc. Custodia de Vehiculo":
            contrato_documento_custodia_vehiculo = ContratoDocumentoCustodiaVehiculo(contrato,usuario)    
            return contrato_documento_custodia_vehiculo.generar1()

        elif description == "Otros Doc. En Custodia":
            contrato_otros_documentos_custodia_patente = ContratoOtroDocumentoCustodiaPatente(contrato,usuario)    
            return contrato_otros_documentos_custodia_patente.generar1()

        elif description == "Convenio y Doc. Custodia Inmueble":
            contrato_convenio_doc_custodia_inmueble = ContratoConvenioCustodiaInmueble(contrato,usuario)    
            return contrato_convenio_doc_custodia_inmueble.generar1()
            
        elif description == "Convenio y Doc. Custodia Vehiculo":
                contrato_convenio_doc_custodia_vehiculo = ContratoConvenioCustodiaVehiculo(contrato,usuario)    
                return contrato_convenio_doc_custodia_vehiculo.generar1()

        # 11 CONVENIO Y GARANTIA PERSONAL
        elif description == "Convenio y Garantia personal":
                contrato_convenio_garantia_personal = ContratoConvenioGarantiaPersonal(contrato,usuario)    
                return contrato_convenio_garantia_personal.generar1()
        
        # 12 PRENDARIA Y PERSONAL
        elif description == "Prendaria y Personal":
                contrato_garante_depositario = ContratoPrendariayPersonal(contrato,usuario)    
                return contrato_garante_depositario.generar1()            

        else:
            print("ªªªªªªªªª No se encontro el tipo de garantia ªªªªªªªªªªªªªªªªªª")
            contrato_error_base = ContratoErrorBase(contrato,usuario)    
            return contrato_error_base.generar1() 
# makeDepositDetail (data, username)
def makeDepositDetail(data, usuario=""):
    titulo="TITULO DEPOSITOS EN BANCO"
    ruta_archivo_entrada="Depositos_en_banco.pdf"
    creator = DetalleDepositoReporte(ruta_archivo_entrada,data, titulo, usuario)
    nombre_del_pdf_salida="Depositos en Banco con footer oficial.pdf"
    ruta_salida =nombre_del_pdf_salida
    def agregar_pie_de_pagina(ruta_archivo):
        try:
            # Abrir archivo PDF existente
            with open(ruta_archivo, 'rb') as archivo_entrada:
                lector_pdf = PyPDF4.PdfFileReader(archivo_entrada)
                num_paginas = lector_pdf.getNumPages()
                # Crear nuevo archivo PDF con pie de página
                with open(ruta_salida, 'wb') as archivo_salida:
                    escritor_pdf = PyPDF4.PdfFileWriter()
                    for num_pagina in range(num_paginas):
                        pagina = lector_pdf.getPage(num_pagina)
                        # Crear un lienzo de ReportLab
                        lienzo = canvas.Canvas(ruta_salida, pagesize=letter)
                        lienzo.setFont('Helvetica',6)
                        lienzo.drawRightString(106 * mm, 10 * mm + (0.2 * inch),f"{num_pagina + 1} / {num_paginas}")
                        lienzo.showPage()
                        lienzo.save()
                        # Agregar el contenido del lienzo a la página existente
                        lienzo_pdf = PyPDF4.PdfFileReader(ruta_salida)
                        pagina.mergePage(lienzo_pdf.getPage(0))
                        # Agregar la página al nuevo archivo PDF
                        escritor_pdf.addPage(pagina)
                    # Guardar el archivo PDF final
                    escritor_pdf.write(archivo_salida)
            print("Pie de página agregado correctamente.")
        except FileNotFoundError:
            print("El archivo no existe.")
        except PyPDF4.utils.PdfReadError:
            print("No se pudo leer el archivo PDF.")
    # Llamada a la función para agregar el pie de página
    agregar_pie_de_pagina(ruta_archivo_entrada)

# makeRegisteredDeposits
def makeRegistrados(data, nombre_del_pdf_salida,titulo, subtitulo_t="", usuario=""):
    def ajustar_fuente_para_wrap(texto, estilo, ancho_maximo):
        from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
        fuente = getFont(estilo.fontName)
        tamaño_inicial = estilo.fontSize
        ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        
        while ancho_texto > ancho_maximo and tamaño_inicial > 1:
            tamaño_inicial -= 1
            print("tamaño inicial: ",tamaño_inicial)
            ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        estilo.fontSize = tamaño_inicial
        
    @staticmethod
    def _header_footer(canvas, doc, custom_data, subtitulo,custom_data2):
        estilos = getSampleStyleSheet()
        font_size=14
        estilos.add(ParagraphStyle(name='titulo', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        estilos.add(ParagraphStyle(name='sub-titulo', alignment=TA_CENTER, fontSize=8, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        print(custom_data2)
        ancho, alto=letter
        canvas.setFont('Helvetica',8)
        canvas.drawString(ancho-3.8*cm, 26.7*cm, "Usuario: "+custom_data2)

        estilo_titulo = estilos["titulo"]
        ajustar_fuente_para_wrap(custom_data, estilo_titulo, 10.8 * cm)
        parrafo = Paragraph(custom_data, estilo_titulo)
        parrafo.wrapOn(canvas, 10.8 * cm, 6 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(canvas, 6.8 * cm, 27* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

        estilo_sub_titulo = estilos["sub-titulo"]
        ajustar_fuente_para_wrap(subtitulo, estilo_sub_titulo, 10.8 * cm)
        parrafo = Paragraph(subtitulo, estilo_sub_titulo)
        parrafo.wrapOn(canvas, 10.8 * cm, 6 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(canvas, 6.8 * cm, 26.3* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
    
    estilos = getSampleStyleSheet()
    font_size=8
    leading_interlineado=10
    estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=font_size,leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    table=[]
    # Agregar los datos de cada registro al table_data
    for record in data:
        row = [
            Paragraph(str(round(record["id"], 2)), estilos["center"]),
            Paragraph(record["operacion"], estilos["center"]),
            Paragraph(record["nombre_cliente"], estilos["left"]),
            Paragraph(record["banco"], estilos["left"]),
            Paragraph(formato_fecha(record["fecha_deposito"]), estilos["left"]),
            Paragraph(record["forma_aplicacion"], estilos["left"]),
            Paragraph(record["monto"], estilos["right"])
        ]
        table.append(row)
    # Obtener la suma de la última columna
    total_sum = 0
    for record in data:
        total_sum += float(record["monto"])
    # Crear una nueva fila con la suma total
    total_row = [Paragraph("Total", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]), 
            Paragraph(str("{:.2f}".format(total_sum)), estilos["right"])]
    table.append(total_row)
    # Definir el tamaño de cada columna
    col_widths = [1.2*cm, 2.2*cm, 4.5*cm, 4*cm, 1.8*cm, 3.5*cm, 1.6*cm]
    # Crear la tabla y establecer el estilo de la tabla
    table = Table(table, colWidths=col_widths, rowHeights=None)                                                                                                                                                           
    table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('SPAN',(0,-1),(-2,-1)),#ultima fila
                ('TOPPADDING', (0,0),(-1,-1), 3),
                ('BOTTOMPADDING', (0,0),(-1,-1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
                ('RIGHTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),#color de la tabla
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),# interlineado Puede ser TOP, MIDDLE o BOTTOM(lineas)
                #('BOTTOMPADDING', (0,-1),(-1,-1), 3),
                #('TOPPADDING', (0,0),(-1,-1), 10),
                #('BOTTOMPADDING', (0,0),(-1,-1), 10),
                
            ]))
    # Crear el documento y establecer el encabezado personalizado en cada página
    doc = SimpleDocTemplate(nombre_del_pdf_salida, pagesize=letter,rightMargin=1*cm, leftMargin=1*cm,
                                topMargin=3.125*cm, bottomMargin=1.7*cm)# MARGENES Y DONDE COMIENZA EL PARRAFO
    
    # Llamar a doc.build con el string enviado a add_header
    doc.build([table], onFirstPage=partial(_header_footer,custom_data=titulo,subtitulo=subtitulo_t,custom_data2=usuario), onLaterPages=partial(_header_footer,custom_data=titulo, subtitulo=subtitulo_t,custom_data2=usuario),
                    canvasmaker=NumberedCanvas)
"""
def makePasajes(data, nombre_del_pdf_salida,titulo, subtitulo_t="", usuario=""):
    def ajustar_fuente_para_wrap(texto, estilo, ancho_maximo):
        from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
        fuente = getFont(estilo.fontName)
        tamaño_inicial = estilo.fontSize
        ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        
        while ancho_texto > ancho_maximo and tamaño_inicial > 1:
            tamaño_inicial -= 1
            print("tamaño inicial: ",tamaño_inicial)
            ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        estilo.fontSize = tamaño_inicial
        
    @staticmethod
    def _header_footer(canvas, doc, custom_data, subtitulo,custom_data2):
        estilos = getSampleStyleSheet()
        font_size=14
        estilos.add(ParagraphStyle(name='titulo', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        estilos.add(ParagraphStyle(name='sub-titulo', alignment=TA_CENTER, fontSize=8, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        print(custom_data2)
        ancho, alto=letter
        canvas.setFont('Helvetica',8)
        canvas.drawString(ancho-3.8*cm, 26.7*cm, "Usuario: "+custom_data2)

        estilo_titulo = estilos["titulo"]
        ajustar_fuente_para_wrap(custom_data, estilo_titulo, 10.8 * cm)
        parrafo = Paragraph(custom_data, estilo_titulo)
        parrafo.wrapOn(canvas, 10.8 * cm, 6 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(canvas, 6.8 * cm, 27* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

        estilo_sub_titulo = estilos["sub-titulo"]
        ajustar_fuente_para_wrap(subtitulo, estilo_sub_titulo, 10.8 * cm)
        parrafo = Paragraph(subtitulo, estilo_sub_titulo)
        parrafo.wrapOn(canvas, 10.8 * cm, 6 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(canvas, 6.8 * cm, 26.3* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
    
    estilos = getSampleStyleSheet()
    font_size=8
    leading_interlineado=10
    estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=font_size,leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    estilos.add(ParagraphStyle(name='right', alignment=TA_RIGHT, fontSize=font_size, leading=leading_interlineado, fontName='Helvetica'))
    table=[]
    # Agregar los datos de cada registro al table_data
    for record in data:
        row = [
            Paragraph(str(round(record["id"], 2)), estilos["center"]),
            Paragraph(record["operacion"], estilos["center"]),
            Paragraph(record["nombre_cliente"], estilos["left"]),
            Paragraph(record["banco"], estilos["left"]),
            Paragraph(formato_fecha(record["fecha_deposito"]), estilos["left"]),
            Paragraph(record["forma_aplicacion"], estilos["left"]),
            Paragraph(record["monto"], estilos["right"])
        ]
        table.append(row)
    # Obtener la suma de la última columna
    total_sum = 0
    for record in data:
        total_sum += float(record["monto"])
    # Crear una nueva fila con la suma total
    total_row = [Paragraph("Total", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]),
            Paragraph("", estilos["center"]), 
            Paragraph(str("{:.2f}".format(total_sum)), estilos["right"])]
    table.append(total_row)
    # Definir el tamaño de cada columna
    col_widths = [1.2*cm, 2.2*cm, 4.5*cm, 4*cm, 1.8*cm, 3.5*cm, 1.6*cm]
    # Crear la tabla y establecer el estilo de la tabla
    table = Table(table, colWidths=col_widths, rowHeights=None)                                                                                                                                                           
    table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('SPAN',(0,-1),(-2,-1)),#ultima fila
                ('TOPPADDING', (0,0),(-1,-1), 3),
                ('BOTTOMPADDING', (0,0),(-1,-1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
                ('RIGHTPADDING', (0, 0), (-1, -1), 4), #pading de la izquierda
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),#color de la tabla
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),# interlineado Puede ser TOP, MIDDLE o BOTTOM(lineas)
            ]))
    # Crear el documento y establecer el encabezado personalizado en cada página
    doc = SimpleDocTemplate(nombre_del_pdf_salida, pagesize=letter,rightMargin=1*cm, leftMargin=1*cm,
                                topMargin=3.125*cm, bottomMargin=1.7*cm)# MARGENES Y DONDE COMIENZA EL PARRAFO
    
    # Llamar a doc.build con el string enviado a add_header
    doc.build([table], onFirstPage=partial(_header_footer,custom_data=titulo,subtitulo=subtitulo_t,custom_data2=usuario), onLaterPages=partial(_header_footer,custom_data=titulo, subtitulo=subtitulo_t,custom_data2=usuario),
                    canvasmaker=NumberedCanvas)
"""

def makeFichaDeDatos(object_json, nombre_del_pdf_salida, titulo, usuario=""):      
    # ************************** FICHA DE DATOS *************************
    ruta_archivo_entrada="Ficha de datos.pdf"
    # Ruta del archivo PDF de salida
    ruta_salida = "Ficha de datos_footer.pdf"
    json_d= """
                {
                    "id": "287",
                    "codigo_operacion": "101211123840",
                    "img" : "https://d7lju56vlbdri.cloudfront.net/var/ezwebin_site/storage/images/_aliases/img_1col/noticias/solar-orbiter-toma-imagenes-del-sol-como-nunca-antes/9437612-1-esl-MX/Solar-Orbiter-toma-imagenes-del-Sol-como-nunca-antes.jpg"
            }
            """
    datos_json = json.loads(json_d)

    creator = FichaDeDatos(ruta_archivo_entrada,datos_json, titulo, usuario)
    # ========================= Cambiar de funcion ====================
    

    #Añadir pie de pagina
    def agregar_pie_de_pagina(ruta_archivo):
        try:
            # Abrir archivo PDF existente
            with open(ruta_archivo, 'rb') as archivo_entrada:
                lector_pdf = PyPDF4.PdfFileReader(archivo_entrada)
                num_paginas = lector_pdf.getNumPages()
                # Crear nuevo archivo PDF con pie de página
                with open(ruta_salida, 'wb') as archivo_salida:
                    escritor_pdf = PyPDF4.PdfFileWriter()
                    for num_pagina in range(num_paginas):
                        pagina = lector_pdf.getPage(num_pagina)
                        # Crear un lienzo de ReportLab
                        lienzo = canvas.Canvas(ruta_salida, pagesize=letter)
                        x,y=letter
                        print("11111111111111111111111111111111111111111111")
                        print(x,y)
                        
                        
                        # print(((x/cm)/2) * cm)
                        # lienzo.setFont('Helvetica',6)
                        # lienzo.drawRightString((((x/cm)/2)+1) * cm, (1-0.2) * cm,f"{num_pagina + 1} / {num_paginas}")#-0.2 por el alto de la letra 1/1
                        
                        """ OTRA MENERA """
                        estilos = getSampleStyleSheet()
                        font_size=6
                        estilos.add(ParagraphStyle(name='cadena_vacia', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica',leading=8,textColor=colors.black))
                        estilo_titulo = estilos["cadena_vacia"]
                        text=f"{num_pagina + 1} / {num_paginas}"
                        parrafo = Paragraph(text, estilo_titulo)
                        parrafo.wrapOn(lienzo, 0.5 * cm, 0.5 * cm)  # Anchura y altura máxima del párrafo en puntos
                        parrafo.drawOn(lienzo, (((x/cm)/2)) * cm, (1-0.2) * cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo

                        
                        lienzo.showPage()
                        lienzo.save()
                        # Agregar el contenido del lienzo a la página existente
                        lienzo_pdf = PyPDF4.PdfFileReader(ruta_salida)
                        pagina.mergePage(lienzo_pdf.getPage(0))
                        # Agregar la página al nuevo archivo PDF
                        escritor_pdf.addPage(pagina)
                    # Guardar el archivo PDF final
                    escritor_pdf.write(archivo_salida)
            print("Pie de página agregado correctamente.")
        except FileNotFoundError:
            print("El archivo no existe.")
        except PyPDF4.utils.PdfReadError:
            print("No se pudo leer el archivo PDF.")
    # Llamada a la función para agregar el pie de página
    agregar_pie_de_pagina(ruta_archivo_entrada)