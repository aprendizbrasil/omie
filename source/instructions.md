# ESPECIFICAÇÕES DA API OMIE:
Este documento detalha os métodos da API da OMIE.
Credenciais de acesso e a BASEURL se encontram no arquivo config/settings.json 
Referências: https://developer.omie.com.br/service-list/

# Geral
Métodos do módulo GERAL.

## Clientes, Fornecedores, Transportadoras, etc	
    Cria/edita/consulta o cadastro de clientes, fornecedores, transportadoras, etc

### ListarClientes
- Lista os clientes cadastrados

- Parâmetros:
 	clientes_list_request	Lista os clientes cadastrados

- Retorno clientes_listfull_response: 
    Lista de clientes cadastrados no omie.

- Endpoint
https://app.omie.com.br/api/v1/geral/clientes/

- Requisição cURL:
curl -s BASEURL/geral/clientes/ \
 -H 'Content-type: application/json' \
 -d '{"call":"ListarClientes","param":[{"pagina":1,"registros_por_pagina":50,"apenas_importado_api":"N"}],"app_key":"#APP_KEY#","app_secret":"#APP_SECRET#"}'

- Retorno:
{
  "pagina": 1,
  "total_de_paginas": 1,
  "registros": 9,
  "total_de_registros": 9,
  "clientes_cadastro": [
    {
      "bairro": "Jardim Olinda",
      "bloquear_faturamento": "N",
      "cep": "",
      "cidade": "",
      "cidade_ibge": "",
      "cnpj_cpf": "",
      "codigo_cliente_integracao": "000.000.000-00",
      "codigo_cliente_omie": 11118224339,
      "codigo_pais": "2496",
      "complemento": "",
      "contato": "Paulo",
      "dadosBancarios": {
        "agencia": "",
        "cChavePix": "",
        "codigo_banco": "",
        "conta_corrente": "",
        "doc_titular": "",
        "nome_titular": "",
        "transf_padrao": "N"
      },
      "email": "seuemail@empresa.com.br",
      "endereco": "Rua Tomás de Aquino",
      "enderecoEntrega": {},
      "endereco_numero": "506",
      "enviar_anexos": "N",
      "estado": "EX",
      "exterior": "S",
      "inativo": "N",
      "info": {
        "cImpAPI": "N",
        "dAlt": "23/02/2026",
        "dInc": "23/02/2026",
        "hAlt": "13:16:38",
        "hInc": "13:16:38",
        "uAlt": "P001309697",
        "uInc": "P001309697"
      },
      "inscricao_estadual": "",
      "inscricao_municipal": "",
      "nome_fantasia": "EquiServ Informática",
      "pessoa_fisica": "N",
      "razao_social": "Equipamentos e Serviços em Informática Ltda",
      "recomendacoes": {
        "gerar_boletos": "N"
      },
      "tags": [
        {
          "tag": "Cliente"
        }
      ],
      "telefone1_ddd": "11",
      "telefone1_numero": "3775.7888"
    },
    {
        ...
    }
    ],
  "cDesStatus": " Elapsed time: 0.07"
}

---------------------------

### Consutar Cliente
- Consulta os dados de um cliente

- Parâmetros:
 	clientes_cadastro_chave	Chave para pesquisa do cadastro de clientes.

- Retorno clientes_listfull_response: 
    Retorna os dados de um clinte.

- Endpoint
https://app.omie.com.br/api/v1/geral/clientes/

- Requisição cURL:
curl -s https://app.omie.com.br/api/v1/geral/clientes/ \
 -H 'Content-type: application/json' \
 -d '{"call":"ConsultarCliente","param":[{"codigo_cliente_omie":11118224336,"codigo_cliente_integracao":""}],"app_key":"#APP_KEY#","app_secret":"#APP_SECRET#"}'

 - Retorno:
 {
  "codigo_cliente_omie": 11118224336,
  "codigo_cliente_integracao": "57.351.558/0001-39",
  "razao_social": "Papelaria e Livraria Rápida Ltda",
  "cnpj_cpf": "57.351.558/0001-39",
  "nome_fantasia": "Papelaria e Livraria Rápida",
  "telefone1_ddd": "11",
  "telefone1_numero": "3775-7888",
  "contato": "Roger",
  "endereco": "",
  "endereco_numero": "1",
  "bairro": "",
  "complemento": "",
  "estado": "SP",
  "cidade": "CAMPINAS (SP)",
  "cep": "13400000",
  "codigo_pais": "1058",
  "separar_endereco": "",
  "pesquisar_cep": "",
  "telefone2_ddd": "",
  "telefone2_numero": "",
  "fax_ddd": "",
  "fax_numero": "",
  "email": "",
  "homepage": "",
  "inscricao_estadual": "",
  "inscricao_municipal": "",
  "inscricao_suframa": "",
  "optante_simples_nacional": "",
  "tipo_atividade": "",
  "cnae": "",
  "produtor_rural": "",
  "contribuinte": "",
  "observacao": "",
  "obs_detalhadas": "",
  "recomendacao_atraso": "",
  "tags": [
    {
      "tag": "Cliente"
    },
    {
      "tag": "Fornecedor"
    }
  ],
  "pessoa_fisica": "N",
  "exterior": "N",
  "logradouro": "",
  "importado_api": "",
  "bloqueado": "",
  "cidade_ibge": "3509502",
  "valor_limite_credito": 0,
  "bloquear_faturamento": "N",
  "recomendacoes": {
    "gerar_boletos": "N"
  },
  "enderecoEntrega": {},
  "nif": "",
  "documento_exterior": "",
  "inativo": "N",
  "dadosBancarios": {
    "agencia": "",
    "cChavePix": "",
    "codigo_banco": "",
    "conta_corrente": "",
    "doc_titular": "",
    "nome_titular": "",
    "transf_padrao": "N"
  },
  "caracteristicas": [],
  "enviar_anexos": "N",
  "info": {
    "cImpAPI": "N",
    "dAlt": "23/02/2026",
    "dInc": "23/02/2026",
    "hAlt": "13:16:38",
    "hInc": "13:16:38",
    "uAlt": "P001309697",
    "uInc": "P001309697"
  },
  "bloquear_exclusao": ""
}



# CRM
Métodos do módulo CRM.

## Contatos, Oportunidades e Tarefas etc.
    Cria/edita/consulta Contatos, Oportunidades e Tarefas

### Listar Contatos
- Lista os contatos do CRM

- Parâmetros:
 	contatoListarRequest	Solicitação da listagem de contatos.

- Retorno contatoListarResponse: 
    Lista de contatos cadastrados no omie.

- Endpoint
https://app.omie.com.br/api/v1/crm/contatos/

- Requisição cURL:
curl -s https://app.omie.com.br/api/v1/crm/contatos/ \
 -H 'Content-type: application/json' \
 -d '{"call":"ListarContatos","param":[{"pagina":1,"registros_por_pagina":1}],"app_key":"#APP_KEY#","app_secret":"#APP_SECRET#"}'

- Retorno:
{
  "pagina": 1,
  "total_de_paginas": 1,
  "registros": 1,
  "total_de_registros": 4,
  "cadastros": [
    {
      "cObs": "",
      "endereco": {
        "cBairro": "",
        "cCEP": "",
        "cCidade": "",
        "cCompl": "",
        "cEndereco": "",
        "cPais": "",
        "cUF": ""
      },
      "identificacao": {
        "cCargo": "Gerente de Alianças",
        "cCodInt": "",
        "cNome": "Paulo",
        "cSobrenome": "Mendonça",
        "dDtNasc": "01/01/1982",
        "nCod": 11118224256,
        "nCodConta": 11118224251,
        "nCodVend": 11118224252
      },
      "telefone_email": {
        "cDDDCel1": "011",
        "cDDDCel2": "",
        "cDDDFax": "",
        "cDDDTel": "",
        "cEmail": "plauto.diniz@newage-software.com.br",
        "cNumCel1": "7777-9999",
        "cNumCel2": "",
        "cNumFax": "",
        "cNumTel": "",
        "cWebsite": ""
      }
    }
  ]
}
---------------------------

### Consutar Contato
- Consulta os dados de um Contato

- Parâmetros:
 	CRM_CONTATOS_PESQUISA	Pesquisa do Contato

- Retorno: 
    Retorno cadastros: Lista os cadastros encontrados.

- Endpoint
https://app.omie.com.br/api/v1/crm/contatos/

- Requisição cURL:
curl -s https://app.omie.com.br/api/v1/crm/contatos/ \
 -H 'Content-type: application/json' \
 -d '{"call":"ConsultarContato","param":[{"nCod":11118224260,"cCodInt":""}],"app_key":"#APP_KEY#","app_secret":"#APP_SECRET#"}'

 - Retorno:
{
  "identificacao": {
    "cCargo": "Gerente de TI",
    "cCodInt": "",
    "cNome": "Fernando",
    "cSobrenome": "Siqueira",
    "dDtNasc": "01/01/1965",
    "nCod": 11118224260,
    "nCodConta": 11118224255,
    "nCodVend": 11118224252
  },
  "endereco": {
    "cBairro": "",
    "cCEP": "",
    "cCidade": "",
    "cCompl": "",
    "cEndereco": "",
    "cPais": "",
    "cUF": ""
  },
  "telefone_email": {
    "cDDDCel1": "11",
    "cDDDCel2": "",
    "cDDDFax": "",
    "cDDDTel": "11",
    "cEmail": "fernado@ti.com.br",
    "cNumCel1": "98888-1234",
    "cNumCel2": "",
    "cNumFax": "",
    "cNumTel": "3775-7888",
    "cWebsite": ""
  },
  "cObs": ""
}

