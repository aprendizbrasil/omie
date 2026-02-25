# INSTRUÇÕES PARA INTERFACE WEB

A interface servirá como um cardápio da API, exibindo os Métodos implementados para cada Módulo com link para susa respectivas páginas de Método, onde poderá ser realizado o request.

Pagina Principal 
├── Página do Módulo              o
│   ├── Página do Método 
│   ├── Página do Método 
│   ├── Página do Método 
├── Página do Módulo              o
│   ├── Página do Método 
│   ├── Página do Método 
├── ...             o
│   ├── ...


## Estrutura principal
Todas páginas exibirão sempre a imagem com o logo da empresa no topo da página e, logo abaixo, um menu horizontal. Abaixo do Menu, uma linha separadora.
Cada item do menu horizontal aponta para página de um Módulo, que lista os Métodos implementados. 

- Logo Empresa <img>
- Menu Horizontal: 'Geral', 'CRM', 'Finaças', 'Serviços'
- Linha separadora

### Estrutura da página de um Módulo
A página do Módulo vai exibir no topo a estrutura principal já descrita.
Abaixo dessa estrutura, vai exibir:

#### Lista dos Métodos e um link que direciona para página do respectivo Método
- Nome do Método - <H2>
- Endpoint - <H3>
- Parâmetros <Table> - A tabela terá duas colunas: uma para nome do parâmetro e outra para digitarmos o valor do mesmo <input>
- Botão de 'Enviar' <Btn>
- Linha separadora
- Caixa de Texto Longo, onde será exibido o JSON de resposta da chamada a API
- Caixa de Texto Longo com comando cURL equivalente da chamada
- Os valores dos parâmetros terão valores defaults  

### Observações sobre o Design
- A página deverá der um estilo, minimalista e profissional
- A página deverá ser o mais clean possível
- O design deveve seguir padrões de codificação que facilitem sua edição, manutenção e personalização futuramente.

### Observações sobre a estrutura
Criei a seguinte estrutura de pastas para arquivos estáticos e templates:
omie/
│
├── src/                # Código fonte principal da aplicação
│   ├── static/         # Arquivos lidos diretamente pelo navegador
│   │   ├── css/        # Estilos (.css)
│   │   ├── js/         # Scripts de frontend (.js)
│   │   └── img/        # Imagens e ícones
│   │
│   └── templates/      # Arquivos HTML (renderizados pelo Python)

### Os Métodos de cada módulo
- Abaixo, uma listagem dos Módulos e seus respectivos métodos. 
- Cada método vai chamar sua execução na pasta /src/api.
- Os arquivos HTML (templates) ficarão na pasta /src/static/templates.

#### Geral
- Listar Clientes
- Consultar Cliente
- Incluir Cliente
- Listar Clientes Resumido


#### CRM
- Listar Contatos
- Consultar Contato
- Incluir Contato
- Verificar Contato

#### Finaças
- Gerar Boleto
- Obter Boleto
- Cancelar Boleto
- GerarPix
- Gerar QrCode Pix
- Listar Pix
- Listar Status Pix
- Obter Pix
- Obter Status Pix
- Cancelar Pix

#### Serviços
- Listar Cadastro Servico
- Consultar CadastroS Servico


### Observação
Até o momento, foram implementados dois Métodos do Módulo 'Geral', apenas: 
- Listar Clientes e 
- Consultar Cliente