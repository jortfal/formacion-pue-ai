from openai import AzureOpenAI

# Crear el cliente de AzureOpenAI
client = AzureOpenAI(
    azure_endpoint="<endpoint>",
    api_key="<key>",
    api_version="2024-08-01-preview")

messages = [{"role": "system",
             "content": "Es un asistente de inteligencia artificial diseñado para ayudar a buscar información."}]
end = False

while (end == False):
    question = input("Envia un mensaje a ChatGPT: ")

    if (question == "end"):
        end = True

    messages.append({"role": "user", "content": question})

    completion = client.chat.completions.create(
        model="gpt-35-turbo-16k",
        messages=messages,
        stream=False)

    print(completion.choices[0].message.content + "\n\n")

    messages.append(
        {"role": "assistant", "content": completion.choices[0].message.content})
