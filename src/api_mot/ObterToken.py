import requests
import json
import base64

def execute_web(base_url, client_id, client_secret, username, password, realm):
    # base_url is expected to be "https://apicorp.algartelecom.com.br"
    endpoint = f"{base_url}/oauth-portal/access-token"
    
    # Montar Authorization base64
    auth_string = f"{client_id}:{client_secret}"
    encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    authorization_header = f"Basic {encoded_auth}"

    headers = {
        "Authorization": authorization_header,
        "Content-Type": "application/json",
        "password": password,
        "realm": realm,
        "username": username
    }

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    # Helper function to mask keys in the cURL command
    def mask_key(key):
        if len(key) > 6:
            return f"{key[:3]}..***..{key[-3:]}"
        return key

    masked_client_id = mask_key(client_id)
    masked_client_secret = mask_key(client_secret)
    masked_password = mask_key(password)
    masked_username = mask_key(username)
    
    masked_auth_string = f"{masked_client_id}:{masked_client_secret}"
    masked_encoded_auth = base64.b64encode(masked_auth_string.encode("utf-8")).decode("utf-8")
    masked_authorization_header = f"Basic {masked_encoded_auth}"

    payload_dict_masked = {
        "client_id": masked_client_id,
        "client_secret": masked_client_secret,
        "grant_type": "client_credentials"
    }
    payload_json_masked = json.dumps(payload_dict_masked)

    curl_command = (f"curl -s -X POST {endpoint} "
                    f"-H 'Authorization: {masked_authorization_header}' "
                    f"-H 'Content-Type: application/json' "
                    f"-H 'password: {masked_password}' "
                    f"-H 'realm: {realm}' "
                    f"-H 'username: {masked_username}' "
                    f"-d '{payload_json_masked}'")

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json(), curl_command
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP no endpoint {endpoint}: {e.response.status_code} - {e.response.text}")
        try:
            error_json = e.response.json()
            return {"error": f"HTTP Error {e.response.status_code}", "details": error_json}, curl_command
        except json.JSONDecodeError:
            return {"error": f"HTTP Error {e.response.status_code}", "details": e.response.text}, curl_command
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição no endpoint {endpoint}: {e}")
        return {"error": str(e)}, curl_command
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON no endpoint {endpoint}: {response.text if 'response' in locals() else ''}")
        return {"error": "Erro ao decodificar JSON", "details": response.text if 'response' in locals() else ""}, curl_command
    except Exception as e:
        print(f"Ocorreu um erro inesperado no endpoint {endpoint}: {e}")
        return {"error": str(e)}, curl_command
