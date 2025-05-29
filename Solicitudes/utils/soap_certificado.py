import zeep
from datetime import datetime

def obtener_certificado_soap(user_id, username):
    """
    Consume el servicio SOAP de calculadora y simula la obtención de un certificado.
    """
    try:
        wsdl = 'http://www.dneonline.com/calculator.asmx?wsdl'
        client = zeep.Client(wsdl=wsdl)
        resultado = client.service.Add(intA=user_id, intB=10)
    except Exception as e:
        resultado = f"Error SOAP: {e}"
    return {
        'certificado_id': f'CERT-{user_id}',
        'nombre': username,
        'fecha_emision': datetime.now().strftime('%Y-%m-%d'),
        'estado': 'Válido',
        'detalle': 'Certificado académico simulado para pruebas de integración.',
        'resultado_soap': resultado
    }
