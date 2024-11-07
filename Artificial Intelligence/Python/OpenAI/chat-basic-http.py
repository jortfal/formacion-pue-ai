import json
import requests

endpoint = "<endpoint>"
apy_key = "<key>"

headers = {
    "Content-Type" : "application/json",
    "api-key" : apy_key
}

message = input("Envia un mensaje a ChatGPT: ")

data = {
    "messages": [{"role": "user", "content": message }]
}

try:
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()

    print(response.json()["choices"][0]["message"]["content"])
except Exception as err:
    print(f"Error: {err}")