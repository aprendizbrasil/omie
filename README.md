# Integração com a API OMIE

Este projeto demonstra a integração com a API da OMIE, fornecendo tanto uma interface de linha de comando quanto uma interface web para interagir com os métodos de clientes e contatos.

## Funcionalidades Implementadas

### Módulo Geral
*   **Listar Clientes:** Lista os clientes cadastrados na Omie.
*   **Consultar Cliente:** Consulta os detalhes de um cliente específico por código Omie ou código de integração.

### Módulo CRM
*   **Listar Contatos:** Lista os contatos cadastrados no CRM da Omie.
*   **Consultar Contato:** Consulta os detalhes de um contato específico por código de contato (`nCod`) ou código de integração (`cCodInt`).

### Interface Web
*   Uma interface web desenvolvida com Flask que atua como um "cardápio" da API, permitindo interagir com os métodos implementados através de formulários HTML.
*   Exibição formatada das respostas JSON da API.
*   Geração dinâmica de comandos cURL equivalentes para cada chamada à API, com `app_key` e `app_secret` mascarados para segurança.
*   Design minimalista e profissional, com logo personalizáveis.

## Estrutura do Projeto

```
omie/
├── config/
│   └── settings.json             # Configurações da API (APPKEY, APPSECRET, BASEURL)
├── src/
│   ├── api/                    # Módulos Python para cada método da API
│   │   ├── ConsultarCliente.py
│   │   ├── ConsultarContato.py
│   │   ├── ListarClientes.py
│   │   └── ListarContatos.py
│   ├── static/                 # Arquivos estáticos (CSS, JS, Imagens)
│   │   ├── css/style.css
│   │   ├── img/dwith01.webp
│   │   ├── img/logo-omie.png
│   │   ├── img/Zapio_01.png
│   │   └── js/script.js
│   ├── templates/              # Templates HTML (Jinja2)
│   │   ├── layout.html
│   │   ├── method.html
│   │   └── module.html
│   ├── app.py                  # Aplicação de linha de comando
│   └── web_app.py              # Aplicação web (Flask)
├── .venv/                      # Ambiente virtual Python
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## Como Configurar e Executar

### Pré-requisitos
*   Python 3.x
*   `pip` (gerenciador de pacotes do Python)

### 1. Clonar o Repositório (se aplicável)

```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd omie
```

### 2. Configurar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv .venv
```

### 3. Ativar o Ambiente Virtual

*   **No Windows (CMD ou PowerShell):**

    ```bash
    .\.venv\Scripts\activate
    ```

*   **No Linux/macOS (ou Git Bash no Windows):**

    ```bash
    source .venv/bin/activate
    ```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 5. Configurar Credenciais da API OMIE

Edite o arquivo `config/settings.json` e preencha com suas credenciais da API Omie:

```json
{
    "APPKEY": "SUA_APP_KEY_AQUI",
    "APPSECRET": "SUA_APP_SECRET_AQUI",
    "BASEURL": "https://app.omie.com.br/api/v1/"
}
```

### 6. Executar a Aplicação (Terminal)

Com o ambiente virtual ativado:

```bash
python src/app.py
```

Siga as instruções do menu no terminal para listar ou consultar clientes/contatos.

### 7. Executar a Aplicação (Web)

Com o ambiente virtual ativado:

```bash
python src/web_app.py
```

Abra seu navegador e acesse: `http://127.0.0.1:7100/`

Você poderá navegar pela interface, testar os métodos da API e observar as respostas JSON e os comandos cURL gerados. 