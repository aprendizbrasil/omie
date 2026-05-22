# Api's MoT(AllManager)
Integração da API MoT
Vamos implementar em Python alguns endpoins da Api MoT(AllManager).

## Design
### Estilos
Seguir os mesmos estilos já usados

### Menu da página layout.html
Vamos criar mais um módulo ("MoT - All.com") a ser exibido no menu da  página layout.html e especificar os métodos para o módulo:

{
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

### Logo da API
Inserir mais uma logo na tela layout.html, ao lado das demais:
omie\src\static\img\all-com.png

## Estrutura das pasta e arquivos
Vamos criar uma pasta específica para os arquivos responsáveis por cada endpointessa inegração:

### Pasta:
src/api-mot

### Arquivos:
ObterToken.py 
ListarDispositivos.py
QuantidadeDispositivos.py
ExibirConsumo.py
BuscarAlertas.py
BuscarEventos.py


## Credenciais e Acesso
### Credenciais e URL Base, que deverão ser incluídas no arquivo settings.json
{
  "api-mot": {
    "base_url": "apicorp.algartelecom.com.br",
    "client_Id": "2768affa-f5f2-4d66-9d27-69a41e62e385",
    "client_secret": "216e52a2-6836-431e-bfd7-64e91e0541b7",
    "username": "api_volp_ia",
    "password": "Dwith@2019",
    "realm": "0d5a3954",
    "grant_type": "client_credentials"
  }
}

### Header dos request aos endpoints
Para consumir os endpoints da API MoT(AllManager), é preciso enviar um token e client_id no header:
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>' \



## Endpoints 

### Obter Token
Executa a criação de um token de acesso.

POST /oauth-portal/access-token
ObterToken.py 

#### Headers
  --url https://apicorp.algartelecom.com.br/oauth-portal/access-token \
  --header 'Authorization: <authorization>' \
  --header 'Content-Type: application/json' \
  --header 'password: <password>' \
  --header 'realm: 0d5a3954' \
  --header 'username: <username>' \

##### Authorization
Como montar a Authorization: concatenar e codificar em Base64
  auth_string = f"{client_id}:{client_secret}"
  encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

Exemplo de Authorization:
  "Basic MzQ4OSozNDMyLTMOMzItMTIz"

Ao gerar o token, ele deve ser guardado para ser usado nas próximas requisições.

#### Body da requisição
  {
  "client_id": "<string>",
  "client_secret": "<string>"
  }

#### Exemplo de retorno da API
  {
    "access_token": "7f378120-e96f-4782-a8da-f86a46087a8b",
    "token_type": "access_token",
    "expires_in": 3600
  }

O tempo de expiração é retornado em segundos. Não precisa controlar o tempo de expiração por enquanto.




---
### Listar Dispositivos do Cliente
Retornar a lista de dispositivos de um cliente MoT. A lista em questão está pginada com filtros.

  GET /broker/devices
  ListarDispositivos.py

#### Headers
curl --request GET \
  --url https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/broker/devices \
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>'


#### Query Parameters
  page - integer required  - default 1
  linesPerPage - integer required​ - default 2
  showContracted - boolean optional - default true

#### Retorno da API
Um JSON com vário atributos.


---
### Listar Dispositivos do Cliente
Retornar a lista de dispositivos de um cliente MoT. A lista em questão está pginada com filtros.

  GET /broker/devices/quantity
  QuantidadeDispositivos.py

#### Headers
curl --request GET \
  --url https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/broker/devices \
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>'


#### Query Parameters
  status - enum required - valores: ACTIVE, CANCELED, SUSPENDED, TRADE_IN - default ACTIVE
  operator - string required​ - default ""
  connectedOperator - string required​ - default ""
  activationDateFrom - string optional - default "2020-01-01"
  activationDateTo - string optional - default <data de hoje>
  showContracted - boolean optional - default true

#### Retorno da API (exemplo)
Um JSON
  {
    "quantity": 100
  }



---
### Exibir Consumo do Dispositivo
Faz uma busca pelo consumo total (franquia).

  GET broker/{deviceId}/consumption/{virtualAccountId}
  ExibirConsumo.py

#### Headers
curl --request GET \
  --url https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/broker/{deviceId}/consumption/{virtualAccountId} \
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>'


#### Path Parameters
  deviceId - string required​ - default ""
  virtualAccountId - string required​ - default ""


#### Retorno da API (exemplo)
Um JSON
  {
    "valueInBytes": 1235
  }



---
### Buscar alertas do cliente
Faz a busca de alertas de um cliente

  GET /broker/alert
  BuscarAlertas.py

#### Headers
curl --request GET \
  --url https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/broker/alert  \
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>'


#### Query Parameters
  page - integer required  - default 1
  pageSize - integer required​ - default 2
  msisdn - string optional - default ""
  status - enum <string> optional - valores: 0, 1, 99, 98, 97 - default Null
  cratedBy - string optional - default ""
  startDate - string optional - default "2020-01-01"
  endDate - string optional - default ""
  customerId - number optional - default Null

#### Retorno da API (exemplo)
Um JSON
{
  "id": 308,
  "customerId": 10000,
  "terminalId": null,
  "contractId": null,
  "msisdn": null,
  "eventType": "CONSUMPTION",
  "field": "consumptionCurrentDay",
  "operator": ">",
  "thresholdValue": 31457280,
  "name": "Teste",
  "active": true,
  "createdAt": "2025-01-02T19:10:16.354",
  "createdBy": "vanilson_etica",
  "updatedAt": null,
  "updatedBy": null
}


---
### Buscar eventos do cliente
Faz a busca por eventos

  GET /broker/alert-events
  BuscarEventos.py

#### Headers
curl --request GET \
  --url https://apicorp.algartelecom.com.br/telecom/product-Inventory-management/management/v1/broker/alert-events \
  --header 'Content-Type: application/json' \
  --header 'access_token: <access_token>' \
  --header 'client_id: <client_id>'


#### Query Parameters
  showContracted - boolean required - default true 
  page - integer required  - default 1
  pageSize - integer required​ - default 2
  msisdn - string optional - default ""
  contractId - number optional - default Null
  dateFrom - string optional - default "2026-05-01T00:00:00.000Z"
  dateto - string optional - default <data atual>
  eventType - enum <string> optional - valores: CONSUMPTION (Consumo de simcards), CONTRACT_CONSUMPTION (Consumo de contrato) - default CONSUMPTION
  field - enum <string> optional - valores: consumptionCurrentDay, consumptionTotal, consumptionPercent, consumptionCurrentDayAnomaly, consumptionTotalAnomaly


#### Retorno da API (exemplo)
Um JSON
{
  "id": 29255,
  "alertId": 168,
  "customerId": 58987,
  "terminalId": 654556,
  "contractId": 45447,
  "msisdn": "5516998784563",
  "eventType": "CONTRACT_CONSUMPTION",
  "field": "consumptionPercent",
  "operator": ">",
  "thresholdValue": 150,
  "eventValue": 166.66666666666666,
  "name": "teste",
  "createdAt": "2025-01-30T16:10:04"
}