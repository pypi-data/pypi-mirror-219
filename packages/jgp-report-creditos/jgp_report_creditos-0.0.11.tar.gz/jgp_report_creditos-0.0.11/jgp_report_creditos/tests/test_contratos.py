import json
import requests
from jgp_report_creditos.report import makeContato

#API PARA EL TRABAJO
parametros ="301212412871"    
datos_json = requests.get("http://192.168.100.5:8000/api/v1/contratos/"+parametros).text
datos_json_ = json.loads(datos_json)

# Nos creamos en la memoria
def write_bytesio_to_file(filename, bytesio):    
      with open(filename, "wb") as outfile:
            outfile.write(bytesio.getbuffer())
      bytesio.close()
      
# *********************************************************************************
#debe de aceptar cuando no envia nada o NOMBRE DEL LECTOR POR EJEMPLO (jtriguero)
# si no envia el parametro de usuario_x por defecto imprimira vacio
# *********************************************************************************
usuario_x="jtriguero"
# Llamada de funcion
buffer= makeContato(datos_json_, usuario_x)  
write_bytesio_to_file("contrato.pdf", buffer)
