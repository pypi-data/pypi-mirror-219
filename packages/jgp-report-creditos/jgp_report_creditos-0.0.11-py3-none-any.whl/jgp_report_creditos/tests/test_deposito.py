
import json
# makePasajes
from jgp_report_creditos.report import makeDepositDetail, makeRegistrados, makeFichaDeDatos

json_d= """
                {
                        "id": "287",
                        "codigo_operacion": "101211123840",
                        "img" : "https://d7lju56vlbdri.cloudfront.net/var/ezwebin_site/storage/images/_aliases/img_1col/noticias/solar-orbiter-toma-imagenes-del-sol-como-nunca-antes/9437612-1-esl-MX/Solar-Orbiter-toma-imagenes-del-Sol-como-nunca-antes.jpg"
                }
                """

datos_json = json.loads(json_d)

# ******************* Llamamos a nuestra funcion ****************
json_d= """
                {
                    "pk":4,
                    "codigo_operacion":"302221302711",
                    "banco":"8",
                    "fecha_deposito":"2023-07-07",
                    "nombre_completo":"302221302711 - C-V - Bitre Lopez Juan Carlos",
                    "numero_documento":"12345678",
                    "monto_depositado":"12.00",
                    "tipo_transaccion":"I",
                    "observaciones":"",
                    "imagen_comprobante":"http://192.168.100.5:8000/media/depositos/comprobantes/20230704/Captura_desde_2023-06-28_09-53-43.png",
                    "fecha_verificacion":null,
                    "estado":"E",
                    "registro_caja":false,
                    "fecha_caja":null,
                    "creado_en":"2023-07-04 12:04:14Z",
                    "actualizado_en":"2023-07-04 12:04:14Z",
                    "eliminado_en":null,
                    "asesor":null,
                    "extracto_deposito":null,
                    "sucursal_creacion":301,
                    "usuario_actualizacion":22,
                    "usuario_caja":null,
                    "usuario_verificacion":null,
                    
                    "id": "287",
                    "codigo_operacion": "101211123840",
                    "img" : "https://d7lju56vlbdri.cloudfront.net/var/ezwebin_site/storage/images/_aliases/img_1col/noticias/solar-orbiter-toma-imagenes-del-sol-como-nunca-antes/9437612-1-esl-MX/Solar-Orbiter-toma-imagenes-del-Sol-como-nunca-antes.jpg"
                }
                """
usuario="jtriguero"
data = json.loads(json_d)

makeDepositDetail(data, usuario)

# ****************** Llamamos a nuestra funcion ************
data_json = """
            [
            {
                "id": 15201,
                "operacion": "5012111t0153",
                "nombre_cliente": "Vazquez Mendozaggggggg ggf Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-02-04",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 25202,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-02-30",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 35203,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 45204,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 5520,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 61121,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 7,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 8,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de jkjkj uicartera",
                "monto": "80.00"
            },
            {
                "id": 9,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 10,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 11,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 12,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 13,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 14,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 15,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            }
            ,
            {
                "id": 16,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            }
            ,
            {
                "id": 17,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            }
            ,
            {
                "id": 18,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 19,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 20,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 21,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 22,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 23,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 24,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 25,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 26,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 27,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 28,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 29,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 30,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 31,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 32,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 33,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 34,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 35,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 36,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },{
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },{
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },{
                "id": 37,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-05-20",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            }
        ]
        """
data = json.loads(data_json)   
nombre_del_pdf_salida="TABLA oficial.pdf"
usuario="jtriguero"
titulo="Depositos Registratos q w e r t u i o p a s d f g h j k l ñ"
subtitulo="Periodo: 2023/06/05 al 2023/06/06"
makeRegistrados(data, nombre_del_pdf_salida,titulo,subtitulo,usuario)

# ****************** Llamamos a nuestra funcion  PASAJES ************
data_json = """
            [
            {
                "id": 15201,
                "operacion": "5012111t0153",
                "nombre_cliente": "Vazquez Mendozaggggggg ggf Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-02-04",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            },
            {
                "id": 25202,
                "operacion": "501211101538",
                "nombre_cliente": "Vazquez Mendoza Dante Josue",
                "banco": "BNB - 1502360716",
                "fecha_deposito": "2023-02-30",
                "forma_aplicacion": "Recuperacion de cartera",
                "monto": "80.00"
            }
        ]
        """
data = json.loads(data_json)   
"""nombre_del_pdf_salida="TABLA PASAJES.pdf"
usuario="jtriguero"
titulo="Depositos De Pasajes"
subtitulo="Periodo: 2023/06/05 al 2023/06/06"
makePasajes(data, nombre_del_pdf_salida,titulo,subtitulo,usuario)"""

#revisar
# ******************* Llamamos a nuestra funcion ****************
json_d= """
                {
                        "id": "287",
                        "codigo_operacion": "101211123840",
                        "img" : "https://d7lju56vlbdri.cloudfront.net/var/ezwebin_site/storage/images/_aliases/img_1col/noticias/solar-orbiter-toma-imagenes-del-sol-como-nunca-antes/9437612-1-esl-MX/Solar-Orbiter-toma-imagenes-del-Sol-como-nunca-antes.jpg"
                }
                """

usuario="jtriguero"
titulo="TITULO FICHA DE DATOS"
data = json.loads(json_d)
nombre_del_pdf_salida="Ficha de datos.pdf"
makeFichaDeDatos(data, nombre_del_pdf_salida, titulo, usuario)

