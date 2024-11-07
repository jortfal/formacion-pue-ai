import json
from openai import AzureOpenAI
from pymongo import MongoClient


def get_CustomerID(customer):
    client = MongoClient('mongodb://localhost:27017')
    db = client['northwind']
    collection = db['customers']

    result = collection.find_one({'$text': {'$search': customer }}, {'CustomerID': 1})

    if(result != None):
        return json.dumps({'customer': customer, 'customerid': result['CustomerID']})
    else:
        return json.dumps({'customer': customer, 'customerid': "unknown"})


def main():
    client = AzureOpenAI(
        azure_endpoint="<endpoint>",
        api_key="<key>",
        api_version="2024-08-01-preview")

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_CustomerID",
                "description": "Retorna el código o identificador de un cliente.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer": {
                            "type": "string",
                            "description": "Nombre completo del cliente o nombre de su empresa"
                        }
                    },
                    "required": ["customer"]
                }
            }
        },
    ]

    messages = [
        {"role": "system", "content": "Erese un asistente virtual que informa sobre clientes"},
        {"role": "user", "content": input('Consulta: ')}]

    response = client.chat.completions.create(
        model = "gpt-35-turbo-16k",
        messages =  messages,
        tools = tools,
        tool_choice = "auto"
    )

    if (response.choices[0].message.tool_calls == None):
        print(response.choices[0].message.content)
    else:
        messages.append(response.choices[0].message)

        for tool in response.choices[0].message.tool_calls:
            if (tool.function.name == 'get_CustomerID'):                
                args = json.loads(tool.function.arguments)
                #print(f"Argumentos capturos por el modelo: {args}")

                id = get_CustomerID(customer=args.get('customer'))
                #print(f"Identificador retornado por la función: {id}")

                messages.append({
                    "tool_call_id": tool.id,
                    "role": "tool",
                    "name": "get_CustomerID",
                    "content": id
                })

        response2 = client.chat.completions.create(
            model="gpt-35-turbo-16k",
            messages=messages
        )

        print(response2.choices[0].message.content)


main()