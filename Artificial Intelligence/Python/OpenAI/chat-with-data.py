from openai import AzureOpenAI

# Crear el cliente de AzureOpenAI
client = AzureOpenAI(
    azure_endpoint="<endpoint>",
    api_key="<key>",
    api_version="2024-08-01-preview")

message = input("Envía un mensaje a ChatGPT: ")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Es un asistente de inteligencia artificial que ayuda a los usuarios a encontrar información."},
        {"role": "system", "content": "Los datos del cliente se entrega en formato JSON, con los campos Empresa, Dirección y Teléfono"},
        {"role": "user", "content": [
            {
                "type": "text",
                "text": message
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://formacionestech.blob.core.windows.net/imagenes/Factura1.jpg"
                }
            }]
        }
    ])

print(completion.choices[0].message.content)
