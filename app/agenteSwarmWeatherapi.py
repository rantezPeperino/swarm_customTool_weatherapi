# agentes_con_api.py
from agency_swarm import Agent
from agency_swarm.util.oai import set_openai_key
from langchain.tools import tool
import requests

# Establecer la clave de OpenAI
set_openai_key("")

# Definir una herramienta que llame a una API
@tool
def obtener_clima(ciudad: str):
    """
    Esta herramienta obtiene el clima actual de una ciudad específica usando la API de WeatherAPI.
    
    Args:
        ciudad (str): El nombre de la ciudad para la cual se desea obtener el clima.
    
    Returns:
        str: Una cadena con la descripción del clima y la temperatura en grados Celsius.
    """
    api_key = ""  # Reemplaza con tu clave de la API
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={ciudad}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        clima = data['current']['condition']['text']
        temperatura = data['current']['temp_c']
        return f"El clima en {ciudad} es {clima} con una temperatura de {temperatura}°C."
    else:
        return "No se pudo obtener la información del clima."

# Crear agentes con agency_swarm
class AgenteSaludo(Agent):
    def process(self, message):
        return f"Procesando el prompt del clima"

class AgenteDespedida(Agent):
    def process(self, message):
        return f"Fin del reporte"

class AgenteClima(Agent):
    def process(self, message):
        ciudad = message.split()[-1]  # Asume que el mensaje contiene el nombre de la ciudad al final
        return obtener_clima(ciudad)

# Simular la interacción con los agentes
def interactuar_con_agentes(mensaje):
    agente_saludo = AgenteSaludo()
    agente_despedida = AgenteDespedida()
    agente_clima = AgenteClima()

    respuesta_saludo = agente_saludo.process(mensaje)
    respuesta_clima = agente_clima.process(mensaje)
    respuesta_despedida = agente_despedida.process(mensaje)
    
    return f"{respuesta_saludo}\n{respuesta_clima}\n{respuesta_despedida}"

# Interacción: El usuario solicita el clima
mensaje = "Quiero saber el clima en el pais de Uruguay, capital de Uruguay, la localidad de Montevideo"
respuesta = interactuar_con_agentes(mensaje)

print(respuesta)  # Aquí el agente de clima responderá con la información solicitada
