function sendQuotePDFWhatsApp(quoteId) {
    const token = localStorage.getItem('token') || 'dummy_token';
    
    $.ajax({
        url: `${API_URL}/api/landscaping/quote/${quoteId}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        },
        success: function(quote) {
            $.ajax({
                url: `${API_URL}/api/landscaping/client/${quote.client_id}`,
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token
                },
                success: function(client) {
                    console.log('Cliente carregado:', client);
                    
                    if (!client.id_whatsapp || client.id_whatsapp.trim() === '') {
                        alert('Cliente não possui ID do WhatsApp cadastrado');
                        return;
                    }
                    
                    console.log('Enviando PDF para WhatsApp ID:', client.id_whatsapp);
                    
                    sendQuoteViaWhatsApp(quoteId, client.id_whatsapp);
                },
                error: function() {
                    alert('Erro ao buscar dados do cliente');
                }
            });
        },
        error: function() {
            alert('Erro ao buscar dados do orçamento');
        }
    });
}

function sendQuoteViaWhatsApp(quoteId, whatsappId) {
    const formData = new FormData();
    formData.append('quote_id', quoteId);
    formData.append('id_whatsapp', whatsappId);

    $.ajax({
        url: `${API_URL}/api/whatsapp/send-quote-pdf`,
        method: 'POST', 
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                alert('Orçamento enviado via WhatsApp com sucesso!');
            } else {
                alert('Falha ao enviar orçamento via WhatsApp: ' + response.message);
            }
        },
        error: function(xhr) {
            alert('Erro ao enviar orçamento via WhatsApp.');
        }
    });
}