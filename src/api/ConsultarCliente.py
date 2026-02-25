import requests
import json

def execute_web(app_key, app_secret, base_url, codigo_cliente_omie, codigo_cliente_integracao):
    endpoint = f"{base_url}geral/clientes/"
    
    headers = {
        "Content-type": "application/json"
    }

    param_payload = {}
    if not codigo_cliente_omie and not codigo_cliente_integracao:
        return {"error": "Erro: Pelo menos um identificador de cliente (Código Cliente Omie ou Código de Integração) deve ser fornecido para a consulta."}

    if codigo_cliente_omie:
        param_payload["codigo_cliente_omie"] = int(codigo_cliente_omie)
        param_payload["codigo_cliente_integracao"] = ""
    elif codigo_cliente_integracao:
        param_payload["codigo_cliente_integracao"] = codigo_cliente_integracao
        param_payload["codigo_cliente_omie"] = 0

    payload = {
        "call": "ConsultarCliente",
        "param": [param_payload],
        "app_key": app_key,
        "app_secret": app_secret
    }

    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            return {"error": "500 Internal Server Error", "details": f"O cliente pode não ter sido encontrado ou a API da Omie teve um problema interno. Detalhes: {e.response.text}"}
        else:
            return {"error": "Erro na requisição HTTP", "details": str(e)}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "Erro ao decodificar JSON", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

def execute(app_key, app_secret, base_url, codigo_cliente_omie, codigo_cliente_integracao):
    response = execute_web(app_key, app_secret, base_url, codigo_cliente_omie, codigo_cliente_integracao)
    print(json.dumps(response, indent=2, ensure_ascii=False))
