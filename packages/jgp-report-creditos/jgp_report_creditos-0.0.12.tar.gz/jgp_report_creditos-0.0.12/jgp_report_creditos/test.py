import requests
#from report import makeContato
from jgp_report_creditos import makeContato

if  __name__ == '__main__':     
    print(" ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª test ªªªªªªªªªªªªªªªªªªªªªªªªªª")
    parametros ="401211601714"
    #datos_json= json.load(requests.get("http://190.181.25.202:8003/api/v1/cre/contrato/"+parametros).text)
    #http://192.168.100.5:8000/api/v1/contratos/501211601894/
    datos_json = requests.get("http://192.168.100.5:8000/api/v1/contratos/"+parametros).text
    print("ddddddddddddddddddddddddddddddddddddddd")

    #ESTA LLAMADA CREA EL PDF
    print(datos_json)
    pdf= makeContato(datos_json); 
    print(pdf)