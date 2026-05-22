from flask import Flask, render_template, redirect, url_for, request
import os
import json
import sys
from datetime import datetime # Import datetime for 'dateto' default
import shlex # Import shlex for shell escaping

# Adiciona o diretório raiz do projeto ao sys.path para que as importações funcionem
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.api import ListarClientes, ConsultarCliente
from src.api import ListarContatos, ConsultarContato
from src.api_mot import ObterToken, ListarDispositivos, QuantidadeDispositivos, ExibirConsumo, BuscarAlertas, BuscarEventos

app = Flask(__name__, 
            static_folder=os.path.abspath("src/static"),
            template_folder=os.path.abspath("src/templates"))

# Define os módulos e métodos para o menu (ainda não totalmente implementado)
MODULES = {
    "geral": {
        "name": "Geral",
        "methods": {
            "listar-clientes": "Listar Clientes",
            "consultar-cliente": "Consultar Cliente",
        }
    },
    "crm": {
        "name": "CRM",
        "methods": {
            "listar-contatos": "Listar Contatos",
            "consultar-contato": "Consultar Contato",
        }
    },
    "mot": {
        "name": "MoT - All.com",
        "methods": {
            "access-token": "Autenticar na All.com",
            "devices_list": "Listar Dispositivos do Cliente",
            "devices_quantity": "Quantidade de Dispositivos do Clientes",
            "devices_consumption": "Exibir Consumo do Dispositivo",
            "busca-alertas": "Buscar alertas do cliente",
            "busca-eventos": "Buscar eventos"
        }
    }
}

def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

def mask_key(key):
    if len(key) > 6:
        return f"{key[:3]}..***..{key[-3:]}"
    return key

@app.route("/")
def index():
    return redirect(url_for("module_page", module_name="geral"))

@app.route("/module/<module_name>")
def module_page(module_name):
    if module_name not in MODULES:
        return "Módulo não encontrado", 404
    
    module_info = MODULES[module_name]
    return render_template("module.html", 
                           modules=MODULES,
                           current_module=module_name,
                           module_info=module_info)

@app.route("/module/<module_name>/<method_name>", methods=["GET", "POST"])
def method_page(module_name, method_name):
    if module_name not in MODULES:
        return "Módulo não encontrado", 404
    
    if method_name not in MODULES[module_name]["methods"]:
        return "Método não encontrado", 404
    
    method_display_name = MODULES[module_name]["methods"][method_name]
    method_parameters = []
    json_response_data = "Aguardando resposta da API..."
    curl_command_data = "Aguardando chamada..."
    method_endpoint = ""

    settings = load_settings()
    app_key = settings["APPKEY"]
    app_secret = settings["APPSECRET"]
    omie_base_url = settings["BASEURL"]
    
    mot_settings = settings.get("api-mot", {})
    mot_base_url_full = mot_settings.get("base_url", "https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/") # Full base URL
    mot_base_url_token = "https://apicorp.algartelecom.com.br" # Specific base URL for token endpoint

    mot_client_id = mot_settings.get("client_Id", "") # Fixed client_Id for MoT endpoints

    # --- Define parameters and endpoint for GET requests ---
    if module_name == "geral":
        method_endpoint = f"{omie_base_url}geral/clientes/"
        if method_name == "listar-clientes":
            method_parameters = [
                {"name": "pagina", "default": 1, "type": "number"},
                {"name": "registros_por_pagina", "default": 5,"type": "number"},
                {"name": "apenas_importado_api", "default": "N", "type": "text"},
            ]
        elif method_name == "consultar-cliente":
            method_parameters = [
                {"name": "codigo_cliente_omie", "default": "", "type": "text"},
                {"name": "codigo_cliente_integracao", "default": "", "type": "text"},
            ]
    elif module_name == "crm":
        method_endpoint = f"{omie_base_url}crm/contatos/"
        if method_name == "listar-contatos":
            method_parameters = [
                {"name": "pagina", "default": 1, "type": "number"},
                {"name": "registros_por_pagina", "default": 1, "type": "number"},
            ]
        elif method_name == "consultar-contato":
            method_parameters = [
                {"name": "nCod", "default": "", "type": "text"},
                {"name": "cCodInt", "default": "", "type": "text"},
            ]
    elif module_name == "mot":
        if method_name == "access-token":
            method_endpoint = f"{mot_base_url_token}/oauth-portal/access-token"
            method_parameters = [
                {"name": "client_id", "default": mot_settings.get("client_Id", ""), "type": "text"},
                {"name": "client_secret", "default": mot_settings.get("client_secret", ""), "type": "text"},
            ]
        elif method_name == "devices_list":
            method_endpoint = f"{mot_base_url_full}broker/devices"
            method_parameters = [
                {"name": "page", "default": 1, "type": "number"},
                {"name": "linesPerPage", "default": 2, "type": "number"},
                {"name": "showContracted", "default": 1, "type": "number", "options": [1, 0]},
            ]
        elif method_name == "devices_quantity":
            method_endpoint = f"{mot_base_url_full}broker/devices/quantity"
            method_parameters = [
                {"name": "status", "default": "ACTIVE", "type": "text", "options": ["ACTIVE", "CANCELED", "SUSPENDED", "TRADE_IN"]},
                {"name": "operator", "default": "", "type": "text"},
                {"name": "connectedOperator", "default": "", "type": "text"},
                # # {"name": "activationDateFrom", "default": "2020-01-01", "type": "date"},
                # {"name": "activationDateTo", "default": datetime.now().strftime("%Y-%m-%d"), "type": "date"},
                # {"name": "activationDateFrom", "default": "", "type": "date"},
                # {"name": "activationDateTo", "default": "", "type": "date"},
                {"name": "showContracted", "default": 1, "type": "number", "options": [1, 0]},
            ]
        elif method_name == "devices_consumption":
            method_endpoint = f"{mot_base_url_full}broker/{{deviceId}}/consumption/{{virtualAccountId}}"
            method_parameters = [
                {"name": "deviceId", "default": "", "type": "text"},
                {"name": "virtualAccountId", "default": "", "type": "text"},
            ]
        elif method_name == "busca-alertas":
            method_endpoint = f"{mot_base_url_full}broker/alert"
            method_parameters = [
                {"name": "page", "default": 1, "type": "number"},
                {"name": "pageSize", "default": 2, "type": "number"},
                {"name": "msisdn", "default": "", "type": "text"},
                {"name": "status", "default": "", "type": "text", "options": ["", "0", "1", "99", "98", "97"]},
                {"name": "cratedBy", "default": "", "type": "text"},
                {"name": "startDate", "default": "2020-01-01", "type": "date"},
                {"name": "endDate", "default": "", "type": "date"},
                {"name": "customerId", "default": "", "type": "number"},
            ]
        elif method_name == "busca-eventos":
            method_endpoint = f"{mot_base_url_full}broker/alert-events"
            method_parameters = [
                {"name": "showContracted", "default": 1, "type": "number", "options": [1, 0]},
                {"name": "page", "default": 1, "type": "number"},
                {"name": "pageSize", "default": 2, "type": "number"},
                {"name": "msisdn", "default": "", "type": "text"},
                {"name": "contractId", "default": "", "type": "number"},
                {"name": "dateFrom", "default": "2026-05-01T00:00:00.000Z", "type": "text"},
                {"name": "dateto", "default": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "type": "text"},
                {"name": "eventType", "default": "CONSUMPTION", "type": "text", "options": ["CONSUMPTION", "CONTRACT_CONSUMPTION"]},
                {"name": "field", "default": "", "type": "text", "options": ["", "consumptionCurrentDay", "consumptionTotal", "consumptionPercent", "consumptionCurrentDayAnomaly", "consumptionTotalAnomaly"]},
            ]

    # --- Handle POST requests ---
    if request.method == "POST":
        form_data = request.form
        try:
            # Common masked keys for Omie API
            masked_app_key = mask_key(app_key)
            masked_app_secret = mask_key(app_secret)

            # Common masked client_id for MoT API
            masked_mot_client_id = mask_key(mot_client_id)

            if module_name == "geral":
                # ... (Omie API logic remains the same)
                if method_name == "listar-clientes":
                    pagina = int(form_data.get("pagina", 1))
                    registros_por_pagina = int(form_data.get("registros_por_pagina", 50))
                    apenas_importado_api = form_data.get("apenas_importado_api", "N")

                    payload_dict = {
                        "call": "ListarClientes",
                        "param": [
                            {
                                "pagina": pagina,
                                "registros_por_pagina": registros_por_pagina,
                                "apenas_importado_api": apenas_importado_api
                            }
                        ],
                        "app_key": masked_app_key,
                        "app_secret": masked_app_secret
                    }
                    payload_json = json.dumps(payload_dict)
                    curl_command_data = f"curl -s {shlex.quote(method_endpoint)} -H \"Content-type: application/json\" -d {shlex.quote(payload_json)}"
                    
                    response = ListarClientes.execute_web(app_key, app_secret, omie_base_url, pagina, registros_por_pagina, apenas_importado_api)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."

                elif method_name == "consultar-cliente":
                    codigo_cliente_omie = form_data.get("codigo_cliente_omie", "")
                    codigo_cliente_integracao = form_data.get("codigo_cliente_integracao", "")

                    param_payload_dict = {
                        "codigo_cliente_omie": int(codigo_cliente_omie) if codigo_cliente_omie else 0,
                        "codigo_cliente_integracao": codigo_cliente_integracao if codigo_cliente_integracao else ""
                    }

                    payload_dict = {
                        "call": "ConsultarCliente",
                        "param": [param_payload_dict],
                        "app_key": masked_app_key,
                        "app_secret": masked_app_secret
                    }
                    payload_json = json.dumps(payload_dict)
                    curl_command_data = f"curl -s {shlex.quote(method_endpoint)} -H \"Content-type: application/json\" -d {shlex.quote(payload_json)}"

                    response = ConsultarCliente.execute_web(app_key, app_secret, omie_base_url, codigo_cliente_omie, codigo_cliente_integracao)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
            
            elif module_name == "crm":
                # ... (CRM API logic remains the same)
                if method_name == "listar-contatos":
                    pagina = int(form_data.get("pagina", 1))
                    registros_por_pagina = int(form_data.get("registros_por_pagina", 1))

                    payload_dict = {
                        "call": "ListarContatos",
                        "param": [
                            {
                                "pagina": pagina,
                                "registros_por_pagina": registros_por_pagina
                            }
                        ],
                        "app_key": masked_app_key,
                        "app_secret": masked_app_secret
                    }
                    payload_json = json.dumps(payload_dict)
                    curl_command_data = f"curl -s {shlex.quote(method_endpoint)} -H \"Content-type: application/json\" -d {shlex.quote(payload_json)}"
                    
                    response = ListarContatos.execute_web(app_key, app_secret, omie_base_url, pagina, registros_por_pagina)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."

                elif method_name == "consultar-contato":
                    nCod = form_data.get("nCod", "")
                    cCodInt = form_data.get("cCodInt", "")

                    param_payload_dict = {}
                    if nCod:
                        param_payload_dict["nCod"] = int(nCod)
                        param_payload_dict["cCodInt"] = ""
                    elif cCodInt:
                        param_payload_dict["cCodInt"] = cCodInt
                        param_payload_dict["nCod"] = 0

                    payload_dict = {
                        "call": "ConsultarContato",
                        "param": [param_payload_dict],
                        "app_key": masked_app_key,
                        "app_secret": masked_app_secret
                    }
                    payload_json = json.dumps(payload_dict)
                    curl_command_data = f"curl -s {shlex.quote(method_endpoint)} -H \"Content-type: application/json\" -d {shlex.quote(payload_json)}"

                    response = ConsultarContato.execute_web(app_key, app_secret, omie_base_url, nCod, cCodInt)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
            
            elif module_name == "mot":
                access_token_header = form_data.get("access_token", "")
                # This client_id will be the fixed one from settings.json, passed via hidden field
                client_id_header = form_data.get("client_id", "")

                # For GET requests, query parameters need to be handled. For POST, payload is used.

                if method_name == "access-token":
                    client_id_form = form_data.get("client_id", "")
                    client_secret_form = form_data.get("client_secret", "")
                    
                    mot_username = mot_settings.get("username", "")
                    mot_password = mot_settings.get("password", "")
                    mot_realm = mot_settings.get("realm", "")

                    response, curl_command_data = ObterToken.execute_web(
                        mot_base_url_token, 
                        client_id_form, 
                        client_secret_form, 
                        mot_username, 
                        mot_password, 
                        mot_realm
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is already returned from ObterToken.execute_web

                elif method_name == "devices_list":
                    page = int(form_data.get("page", 1))
                    lines_per_page = int(form_data.get("linesPerPage", 2))
                    show_contracted = int(form_data.get("showContracted", 1)) # Expect 1 or 0

                    response, curl_command_data = ListarDispositivos.execute_web(
                        mot_base_url_full, # Use mot_base_url_full
                        access_token_header, 
                        client_id_header, 
                        page, 
                        lines_per_page, 
                        show_contracted
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is returned from ListarDispositivos.execute_web

                elif method_name == "devices_quantity":
                    status = form_data.get("status", "ACTIVE")
                    operator = form_data.get("operator", "")
                    connected_operator = form_data.get("connectedOperator", "")
                    activation_date_from = form_data.get("activationDateFrom", "2020-01-01")
                    activation_date_to = form_data.get("activationDateTo", datetime.now().strftime("%Y-%m-%d"))
                    show_contracted = int(form_data.get("showContracted", 1)) # Expect 1 or 0

                    response, curl_command_data = QuantidadeDispositivos.execute_web(
                        mot_base_url_full, 
                        access_token_header, 
                        client_id_header, 
                        status, 
                        operator, 
                        connected_operator, 
                        activation_date_from, 
                        activation_date_to, 
                        show_contracted
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is returned from QuantidadeDispositivos.execute_web

                elif method_name == "devices_consumption":
                    device_id = form_data.get("deviceId", "")
                    virtual_account_id = form_data.get("virtualAccountId", "")

                    response, curl_command_data = ExibirConsumo.execute_web(
                        mot_base_url_full, 
                        access_token_header, 
                        client_id_header, 
                        device_id, 
                        virtual_account_id
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is returned from ExibirConsumo.execute_web
                
                elif method_name == "busca-alertas":
                    page = int(form_data.get("page", 1))
                    page_size = int(form_data.get("pageSize", 2))
                    msisdn = form_data.get("msisdn", "")
                    status = form_data.get("status", "")
                    created_by = form_data.get("cratedBy", "") # Note the typo 'cratedBy' from prompt
                    start_date = form_data.get("startDate", "2020-01-01")
                    end_date = form_data.get("endDate", "")
                    customer_id = form_data.get("customerId", "")

                    response, curl_command_data = BuscarAlertas.execute_web(
                        mot_base_url_full, 
                        access_token_header, 
                        client_id_header, 
                        page, 
                        page_size, 
                        msisdn, 
                        status, 
                        created_by, 
                        start_date, 
                        end_date, 
                        customer_id
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is returned from BuscarAlertas.execute_web

                elif method_name == "busca-eventos":
                    show_contracted = int(form_data.get("showContracted", 1)) # Expect 1 or 0
                    page = int(form_data.get("page", 1))
                    page_size = int(form_data.get("pageSize", 2))
                    msisdn = form_data.get("msisdn", "")
                    contract_id = form_data.get("contractId", "")
                    date_from = form_data.get("dateFrom", "2026-05-01T00:00:00.000Z")
                    date_to = form_data.get("dateto", datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
                    event_type = form_data.get("eventType", "CONSUMPTION")
                    field = form_data.get("field", "")

                    response, curl_command_data = BuscarEventos.execute_web(
                        mot_base_url_full, 
                        access_token_header, 
                        client_id_header, 
                        show_contracted, 
                        page, 
                        page_size, 
                        msisdn, 
                        contract_id, 
                        date_from, 
                        date_to, 
                        event_type, 
                        field
                    )
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
                    # curl_command_data is returned from BuscarEventos.execute_web

        except Exception as e:
            json_response_data = f"Erro ao processar requisição: {e}"
            curl_command_data = "Erro na geração do comando cURL devido a falha no processamento."

    return render_template("method.html",
                           modules=MODULES,
                           current_module=module_name,
                           method_name=method_name,
                           method_display_name=method_display_name,
                           method_parameters=method_parameters,
                           json_response_data=json_response_data,
                           curl_command_data=curl_command_data,
                           request_form=request.form, # Pass request.form to retain input
                           mot_client_id=mot_client_id, # Pass mot_client_id to template for JS
                           method_endpoint=method_endpoint # Pass the dynamic endpoint
                           )

if __name__ == '__main__':
    app.run(debug=True, port=7100)