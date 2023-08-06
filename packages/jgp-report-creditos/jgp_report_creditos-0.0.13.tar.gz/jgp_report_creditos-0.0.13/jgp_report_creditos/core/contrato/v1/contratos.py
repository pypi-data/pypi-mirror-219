from reportlab.pdfgen import canvas
from jgp_report_creditos.core.exception.exception import ContratoError

from .base import BaseContrato

class ContratoPersonal (BaseContrato):
    
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía Personal')
            self._partes_contratantes('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza('CUARTA')
            self._intereses('QUINTA')
            self._plazo('SEXTA')
            self._lugar('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias('DÉCIMA')
            self._supervision('DÉCIMA PRIMERA')
            self._cesion_obligacion('DÉCIMA SEGUNDA')
            self._autorizacion('DÉCIMA TERCERA')
            self._titulo_ejecutivo('DÉCIMA CUARTA')
            self._gastos('DÉCIMA QUINTA')
            self._derechos_deudor('DÉCIMA SEXTA')
            self._domicilio_especial('DÉCIMA SÉPTIMA')
            self._aceptacion('DÉCIMA OCTAVA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))  
        finally:
            print("TERMINADO")

#11 CONVENIO Y GARANTIA PERSONAL
class ContratoConvenioGarantiaPersonal (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Derecho de Línea y garantía Personal')
            self._partes_contratantes('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza('CUARTA')
            self._intereses_pyv('QUINTA')#garantes
            self._plazo('SEXTA')
            self._lugar('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias_cygp('DÉCIMA')
            #diferente 
            self._prohibiciones('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))  
        finally:
            print("TERMINADO")

# 12 GARANTE DEPOSITARIO
class ContratoPrendariayPersonal(BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía Prendaria y Personal')
            self._partes_contratantes3('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza3('CUARTA')
            self._intereses3('QUINTA')
            self._plazo('SEXTA')
            self._lugar_pyp('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias_pyp('DÉCIMA')
            #diferente 
            self._prohibiciones_pyp('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion4('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion3('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))   
        finally:
            print("TERMINADO")
# CONVENIO
class ContratoConvenio (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Derecho de Línea')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias2('DÉCIMA')
            #diferente 
            self._prohibiciones('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))  
        finally:
            print("TERMINADO")

# CONVENIO Y DOC. CUSTODIA DE INMUEBLE   -------------------------REVISADO 1-1
class ContratoConvenioCustodiaInmueble (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Derecho de Línea y Garantía de Documentos en Custodia de Inmueble')        
            self._partes_contratantes2('PRIMERA')       
            self._objeto_del_contrato('SEGUNDA')       
            self._desembolso('TERCERA')       
            self._gestion_cobranza2('CUARTA')        
            self._intereses2('QUINTA')        
            self._plazo('SEXTA')        
            self._lugar2('SÉPTIMA')        
            self._mora_ejecucion('OCTAVA')       
            self._caducidad_y_derecho_de_aceleracion('NOVENA')        
            self._garantias3('DÉCIMA')
            #diferente 
            self._prohibiciones_con_inmueble('DÉCIMA PRIMERA')       
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))   
        finally:
            print("TERMINADO")

# CONVENIO Y DOC. CUSTODIA DE VEHÍCULO   
class ContratoConvenioCustodiaVehiculo (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Derecho de Línea y Garantía de Documentos en Custodia de Vehículo')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')  
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias3V('DÉCIMA')
            #diferente 
            self._prohibiciones2('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e)) 
        finally:
            print("TERMINADO")

# DOC. CUSTODIA DE INMUEBLE DE PAMPAHASI M
class ContratoCustosiaInmueblePampahasi (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Documentos en Custodia de Inmueble')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias_pampahasi('DÉCIMA')
            #diferente 
            self._prohibiciones_pampahasi('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))    
        finally:
            print("TERMINADO")

# Documentos en Custodia de Vehículo M  ------EN REV
class ContratoDocumentoCustodiaVehiculo (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Documentos en Custodia de vehículo')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias8dcv('DÉCIMA')
            #diferente 
            self._prohibiciones3('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))    
        finally:
            print("TERMINADO")

# Otros Documentos en Custodia (patente) M
class ContratoOtroDocumentoCustodiaPatente (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía de Otros Documentos en Custodia')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias_otrosdc('DÉCIMA')
            #diferente 
            self._prohibiciones_otroscyv('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))    
        finally:
            print("TERMINADO")
# Personal y Documentos en Custodia de Vehículo M
class ContratoPersonalDocumentosCustodiaVehiculo (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía Personal y Documentos en Custodia de vehículo')
            self._partes_contratantes('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza('CUARTA')
            self._intereses_pyv('QUINTA')
            self._plazo('SEXTA')
            self._lugar_pyv('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias_pyv('DÉCIMA')
            #diferente 
            self._prohibiciones3('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion3('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))    
        finally:
            print("TERMINADO")
# Quirografaria OFICINA EL CARMEN
class ContratoQuirografariaOficinaElCarmen (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía Quirografaria')
            self._partes_contratantes2('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias6Q('DÉCIMA')
            #diferente 
            self._prohibiciones4('DÉCIMA PRIMERA')
            self._supervision('DÉCIMA SEGUNDA')
            self._cesion_obligacion('DÉCIMA TERCERA')
            self._autorizacion2('DÉCIMA CUARTA')
            self._titulo_ejecutivo('DÉCIMA QUINTA')
            self._gastos('DÉCIMA SEXTA')
            self._derechos_deudor('DÉCIMA SÉPTIMA')
            self._domicilio_especial('DÉCIMA OCTAVA')
            self._aceptacion2('DÉCIMA NOVENA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))   
        finally:
            print("TERMINADO")
            
# Solidario
class ContratoSolidario (BaseContrato):
    def __init__(self, json_enviado, usuario):
        try:
            super().__init__(json_enviado, usuario)
            self._tipo_contrato('PRESTAMO DE DINERO o MUTUO bajo garantía Solidaria')
            self._partes_contratantes2Soli('PRIMERA')
            self._objeto_del_contrato('SEGUNDA')
            self._desembolso('TERCERA')
            self._gestion_cobranza2('CUARTA')
            self._intereses2('QUINTA')
            self._plazo('SEXTA')
            self._lugar2('SÉPTIMA')
            self._mora_ejecucion('OCTAVA')
            self._caducidad_y_derecho_de_aceleracion('NOVENA')
            self._garantias4('DÉCIMA')
            #diferente 
            self._supervision('DÉCIMA PRIMERA')
            self._cesion_obligacion('DÉCIMA SEGUNDA')
            self._autorizacion2('DÉCIMA TERCERA')
            self._titulo_ejecutivo('DÉCIMA CUARTA')
            self._gastos_solidario('DÉCIMA QUINTA')
            self._derechos_deudor('DÉCIMA SEXTA')
            self._domicilio_especial('DÉCIMA SÉPTIMA')
            self._aceptacion2('DÉCIMA OCTAVA')
            self._firmas()
        except ContratoError as ex:
            p1, p2 = ex.args
            print("°°°°°°°°°°° ERROR PERSONALIZADO: °°°°°°°°°°")
            self._error_mensaje(p1,p2)
        except Exception as e:
            print("ERROR INESPERADO!!!!!") 
            self._error_mensaje("Error inesperado",repr(e))    
        finally:
            print("TERMINADO")
# CONTRATO ERROR BASE
class ContratoErrorBase(BaseContrato):
    def __init__(self, json_enviado, usuario):
        super().__init__(json_enviado, usuario)
        self._error_mensaje("Error en el contrato","Tipo de garantia desconocido")