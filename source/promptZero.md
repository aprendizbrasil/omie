Olá! Quero integrar alguns endpoints da API da OMIE, listadas na página: https://developer.omie.com.br/service-list/ 

Primeiro, quero que crie o código para src/app.py  que vai oferecer a opção de chamar 2 métodos da API:
1- Listar Clientes
2- Consultar Cliente.

Ao selecionar uma delas,  o app.py vai solicitar os parâmetros necessários e depois vai chamar o arquivo correspondente ao método. Por exemplo: se digitar 1, app.py vai solicitar os parâmetros e chamar o arquivo src/api/ListarClientes.py, que vai executar o request e imprimir no terminal o retorno em formato JSON.

As informações detalhadas necessárias para o desenvolvimento da chamata à API e autenticação encontram-se no arquivo source/instructions.md

Inicialmente, vamos desenvolver apenas o app.py e o ListarClientes.py

Sempre que necessário, atualise o arquivo requirements.txt com todas as bibliotecas necessárias.

Vamos fazer esse protótipo para rodar no terminal, mas, depois de  desenvolvermos e testarmos, vamos implementar uma interface web. Não é necessário implementar nada para web agora, mas deixar a estrutura e os códigos em condições de facilmente modificá-los para implementar a iterface web. 
