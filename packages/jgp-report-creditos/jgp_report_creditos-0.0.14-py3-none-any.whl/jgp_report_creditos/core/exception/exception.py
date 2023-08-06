# Creamos nuestra propia excepción heredando
# de la clase Exception    
class ContratoError(Exception):
    """
    Errores de Formato, campos requeridos y Valroes no validos.
    """
    def __init__(self, parametro1, parametro2):
        self.tipo_error = parametro1
        self.message = parametro2
   
