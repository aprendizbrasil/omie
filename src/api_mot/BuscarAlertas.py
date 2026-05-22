import requests
import json
import shlex

def execute_web(base_url, access_token, client_id, page, page_size, msisdn, status, created_by, start_date, end_date, customer_id):
    endpoint = f"{base_url}broker/alert"
    
    headers = {
        "Content-Type": "application/json",
        "access_token": access_token,
        "client_id": client_id
    }

    params = {
        "page": page,
        "pageSize": page_size,
    }

    if msisdn: params["msisdn"] = msisdn
    if status: params["status"] = status
    if created_by: params["cratedBy"] = created_by # Note: "cratedBy" is from prompt, not "createdBy"
    if start_date: params["startDate"] = start_date
    if end_date: params["endDate"] = end_date
    if customer_id: params["customerId"] = customer_id

    # Helper function to mask keys in the cURL command
    def mask_key(key):
        if len(key) > 6:
            return f"{key[:3]}..***..{key[-3:]}"
        return key

    masked_access_token = mask_key(access_token)
    masked_client_id = mask_key(client_id)

    headers_masked = {
        "Content-Type": "application/json",
        "access_token": masked_access_token,
        "client_id": masked_client_id
    }

    params_str = '&'.join([f'{k}={v}' for k, v in params.items()])
    curl_command = f"curl -s -G {shlex.quote(f'{endpoint}?{params_str}')} "
    for key, value in headers_masked.items():
        curl_command += f"-H {shlex.quote(f'{key}: {value}')} "

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
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
    except Exception as e:
        print(f"Ocorreu um erro inesperado no endpoint {endpoint}: {e}")
        return {"error": str(e)}, curl_command

def execute(base_url, access_token, client_id, page, page_size, msisdn, status, created_by, start_date, end_date, customer_id):
    response, _ = execute_web(base_url, access_token, client_id, page, page_size, msisdn, status, created_by, start_date, end_date, customer_id)
    print(json.dumps(response, indent=2, ensure_ascii=False))
