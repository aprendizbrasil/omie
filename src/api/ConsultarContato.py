import requests
import json

def execute_web(app_key, app_secret, base_url, nCod, cCodInt):
    endpoint = f"{base_url}crm/contatos/"
    
    headers = {
        "Content-type": "application/json"
    }

    param_payload = {}
    if not nCod and not cCodInt:
        return {"error": "Erro: Pelo menos um identificador de contato (nCod ou cCodInt) deve ser fornecido para a consulta."}

    if nCod:
        param_payload["nCod"] = int(nCod)
        param_payload["cCodInt"] = ""
    elif cCodInt:
        param_payload["cCodInt"] = cCodInt
        param_payload["nCod"] = 0 # Omie API example shows 0 if cCodInt is provided

    payload = {
        "call": "ConsultarContato",
        "param": [param_payload],
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

def execute(app_key, app_secret, base_url, nCod, cCodInt):
    response = execute_web(app_key, app_secret, base_url, nCod, cCodInt)
    print(json.dumps(response, indent=2, ensure_ascii=False))
