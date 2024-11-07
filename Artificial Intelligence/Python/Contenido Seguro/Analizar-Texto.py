from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory, AnalyzeTextOptions
import requests
import json

url = "<endpoint>"
clave = "<key1 or key2>"

# Utilizar los servicios de Seguridad de contenido mediante SDK
def RunSDK(texto):
    cliente = ContentSafetyClient(url, AzureKeyCredential(clave))
    consulta = AnalyzeTextOptions(text=texto)

    try:
        resultado = cliente.analyze_text(consulta)

        for item in resultado.categories_analysis:
            print(f"{item.category}: {item.severity}")

    except HttpResponseError as e:
        print(f"Error {e.error.code}: {e.error.message}")

# Utilizar los servicios de Seguridad de contenido mediante API Rest
def RunREST(texto):
    headers = {
        "Ocp-Apim-Subscription-Key": clave,
        "Content-Type": "application/json"
    }

    playload = {
        "text": texto
    }

    response = requests.post(f"{url}/contentsafety/text:analyze?api-version=2023-10-01", 
                             headers=headers, data= json.dumps(playload))
    
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error {response.status_code}: ")

# Probar código
texto = "Eres un poco idiota ..."
RunREST(texto)
