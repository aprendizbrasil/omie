import sys
import os
import json

# Adiciona o diretório raiz do projeto ao sys.path para que as importações funcionem
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from src.api import ListarClientes
from src.api import ConsultarCliente

def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

def main():
    settings = load_settings()
    app_key = settings["APPKEY"]
    app_secret = settings["APPSECRET"]
    base_url = settings["BASEURL"]

    while True:
        print("\n--- Menu OMIE API ---")
        print("1. Listar Clientes")
        print("2. Consultar Cliente")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            print("\n--- Listar Clientes ---")
            pagina = 1
            registros_por_pagina = 50
            apenas_importado_api = "N"
            ListarClientes.execute(
                app_key,
                app_secret,
                base_url,
                pagina,
                registros_por_pagina,
                apenas_importado_api
            )
        elif choice == "2":
            print("\n--- Consultar Cliente ---")
            client_id_type = input("Consultar por (1) Código Cliente Omie ou (2) Código Cliente Integração? ")
            codigo_cliente_omie = ""
            codigo_cliente_integracao = ""

            if client_id_type == "1":
                codigo_cliente_omie = input("Digite o Código do Cliente Omie: ")
            elif client_id_type == "2":
                codigo_cliente_integracao = input("Digite o Código de Integração do Cliente: ")
            else:
                print("Opção inválida. Retornando ao menu principal.")
                continue

            ConsultarCliente.execute(
                app_key,
                app_secret,
                base_url,
                codigo_cliente_omie,
                codigo_cliente_integracao
            )
        elif choice == "3":
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()