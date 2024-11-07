from openai import AzureOpenAI

# Crear el cliente de AzureOpenAI
client = AzureOpenAI(
    azure_endpoint="<endpoint>",
    api_key="<key>",
    api_version="2024-08-01-preview")

request = input("Envia un mensaje a ChatGPT: ")

completion = client.chat.completions.create(
    model="gpt-35-turbo-16k",
    messages=[
        {"role": "user", "content": request}],
    stream=False)

print(completion.choices[0].message.content)