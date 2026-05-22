// Placeholder for future JavaScript code

document.addEventListener("DOMContentLoaded", function() {
    const jsonResponseEl = document.getElementById("json-response");
    const accessTokenField = document.getElementById("access_token_field");
    const clientIdField = document.getElementById("client_id_field");

    // Logic to save access_token to localStorage after a successful ObterToken call
    if (jsonResponseEl && accessTokenField && window.location.pathname.includes("/module/mot/access-token")) {
        const jsonText = jsonResponseEl.value;
        if (jsonText) {
            try {
                const responseData = JSON.parse(jsonText);
                if (responseData && responseData.access_token) {
                    localStorage.setItem("token-mot", responseData.access_token);
                    console.log("Token MoT guardado no localStorage com sucesso.");
                }
            } catch (e) {
                console.error("Erro ao fazer parse da resposta JSON para extrair o token.", e);
            }
        }
    }

    // Logic to load access_token from localStorage for MoT API calls
    if (accessTokenField && window.location.pathname.includes("/module/mot/")) {
        const storedToken = localStorage.getItem("token-mot");
        if (storedToken) {
            accessTokenField.value = storedToken;
            console.log("Token MoT carregado do localStorage para o campo oculto.");
        } else {
            console.warn("Nenhum token MoT encontrado no localStorage.");
        }
    }

    // client_id is passed from Flask backend, so no need to fetch from localStorage
    // Ensure client_id is correctly set in the hidden field for all MoT methods
    if (clientIdField && window.location.pathname.includes("/module/mot/")) {
        // The value is already set by Flask template, just logging for clarity
        console.log("Client ID da MoT definido no campo oculto.", clientIdField.value);
    }

});


