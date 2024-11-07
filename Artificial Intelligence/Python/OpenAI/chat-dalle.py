import json, requests, os
from io import BytesIO
from openai import AzureOpenAI
from PIL import Image


# Crear el cliente de AzureOpenAI
client = AzureOpenAI(
    azure_endpoint="<endpoint>",
    api_key="<key>",
    api_version="2024-02-01")

request = input("Describe una imagen: ")

#request = request + "; la imagen debe ser en B/N"

response = client.images.generate(
    model="dall-e-3",
    prompt=request,
    n=1)

print(response.data[0].revised_prompt)
print(response.data[0].url)

responseImagen = requests.get(response.data[0].url)

# Modo 1
imageContent = Image.open(BytesIO(responseImagen.content))
imageContent.show()

# Modo 2
path = "Imágenes\\Imagen1.png"

with open(path, "wb") as imageFile:
    imageFile.write(responseImagen.content)

imageContent2 = Image.open(path)
imageContent2.show()
