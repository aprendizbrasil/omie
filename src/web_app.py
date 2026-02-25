from flask import Flask, render_template, redirect, url_for, request
import os
import json
import sys

# Adiciona o diretório raiz do projeto ao sys.path para que as importações funcionem
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.api import ListarClientes, ConsultarCliente
from src.api import ListarContatos, ConsultarContato

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

    settings = load_settings()
    app_key = settings["APPKEY"]
    app_secret = settings["APPSECRET"]
    base_url = settings["BASEURL"]

    if module_name == "geral":
        if method_name == "listar-clientes":
            method_parameters = [
                {"name": "pagina", "default": 1, "type": "number"},
                {"name": "registros_por_pagina", "default": 5, "type": "number"},
                {"name": "apenas_importado_api", "default": "N", "type": "text"},
            ]
        elif method_name == "consultar-cliente":
            method_parameters = [
                {"name": "codigo_cliente_omie", "default": "", "type": "text"},
                {"name": "codigo_cliente_integracao", "default": "", "type": "text"},
            ]
    elif module_name == "crm":
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

    if request.method == "POST":
        form_data = request.form
        try:
            masked_app_key = mask_key(app_key)
            masked_app_secret = mask_key(app_secret)

            if module_name == "geral":
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
                    curl_command_data = f"curl -s {base_url}geral/clientes/ -H \"Content-type: application/json\" -d \\\'{payload_json}\\\'"
                    
                    response = ListarClientes.execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina, apenas_importado_api)
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
                    curl_command_data = f"curl -s {base_url}geral/clientes/ -H \"Content-type: application/json\" -d \\\'{payload_json}\\\'"

                    response = ConsultarCliente.execute_web(app_key, app_secret, base_url, codigo_cliente_omie, codigo_cliente_integracao)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."
            
            elif module_name == "crm":
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
                    curl_command_data = f"curl -s {base_url}crm/contatos/ -H \"Content-type: application/json\" -d \\\'{payload_json}\\\'"
                    
                    response = ListarContatos.execute_web(app_key, app_secret, base_url, pagina, registros_por_pagina)
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
                    curl_command_data = f"curl -s {base_url}crm/contatos/ -H \"Content-type: application/json\" -d \\\'{payload_json}\\\'"

                    response = ConsultarContato.execute_web(app_key, app_secret, base_url, nCod, cCodInt)
                    json_response_data = json.dumps(response, indent=2, ensure_ascii=False) if response else "Erro ao obter dados."

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
                           request_form=request.form # Pass request.form to retain input
                           )

if __name__ == '__main__':
    app.run(debug=True, port=7100)