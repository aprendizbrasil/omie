import requests
import json

def execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina, apenas_importado_api):
    endpoint = f"{base_url}geral/clientes/"
    
    headers = {
        "Content-type": "application/json"
    }

    payload = {
        "call": "ListarClientes",
        "param": [
            {
                "pagina": pagina,
                "registros_por_pagina": registros_por_pagina,
                "apenas_importado_api": apenas_importado_api
            }
        ],
        "app_key": app_key,
        "app_secret": app_secret
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        # print(f"Erro na requisição: {e}") # Keep printing for terminal use if needed
        return {"error": str(e)}
    except json.JSONDecodeError:
        # print(f"Erro ao decodificar JSON: {response.text}") # Keep printing for terminal use if needed
        return {"error": "Erro ao decodificar JSON", "details": response.text}
    except Exception as e:
        # print(f"Ocorreu um erro inesperado: {e}") # Keep printing for terminal use if needed
        return {"error": str(e)}

def execute(app_key, app_secret, base_url, pagina, registros_por_pagina, apenas_importado_api):
    response = execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina, apenas_importado_api)
    print(json.dumps(response, indent=2, ensure_ascii=False))
