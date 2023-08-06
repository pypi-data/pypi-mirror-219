import json
import requests
from jgp_report_creditos.report import makeContato

#API PARA EL TRABAJO
parametros ="401331801699"    
datos_json = requests.get("http://192.168.100.5:8000/api/v1/contratos/"+parametros).text
#Convenio y Garantia personal
datos_diccionario = json.loads(datos_json)

# Nos creamos en la memoria
def write_bytesio_to_file(filename, bytesio):    
      with open(filename, "wb") as outfile:
            outfile.write(bytesio.getbuffer())
      bytesio.close()

datos_diccionario = json.loads(datos_json)
# *********************************************************************************
#debe de aceptar cuando no envia nada o NOMBRE DEL LECTOR POR EJEMPLO (jtriguero)
# si no envia el parametro de usuario_x por defecto imprimira vacio
# *********************************************************************************
usuario_x=""
# Llamada de funcion
buffer= makeContato(datos_diccionario, usuario_x)  
write_bytesio_to_file("contrato.pdf", buffer)
