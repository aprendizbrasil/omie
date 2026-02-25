import requests
import json

def execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina):
    endpoint = f"{base_url}crm/contatos/"
    
    headers = {
        "Content-type": "application/json"
    }

    payload = {
        "call": "ListarContatos",
        "param": [
            {
                "pagina": pagina,
                "registros_por_pagina": registros_por_pagina
            }
        ],
        "app_key": app_key,
        "app_secret": app_secret
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            error_json = e.response.json()
            if "faultstring" in error_json:
                return {"error": error_json["faultstring"], "code": error_json["faultcode"], "status_code": e.response.status_code}
            else:
                return {"error": f"HTTP Error {e.response.status_code}", "details": e.response.text}
        except json.JSONDecodeError:
            return {"error": f"HTTP Error {e.response.status_code}", "details": e.response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar JSON", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

def execute(app_key, app_secret, base_url, pagina, registros_por_pagina):
    response = execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina)
    print(json.dumps(response, indent=2, ensure_ascii=False))
