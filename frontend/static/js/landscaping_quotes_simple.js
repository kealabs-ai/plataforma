// Versão simplificada do modal de orçamentos

// Função principal para inicializar o modal
function initializeQuoteModal() {
    // Limpar formulário
    $('#add-quote-form')[0].reset();
    $('#tableBody').empty();
    $('#grandTotal').val('0.00');
    $('#quote-total-value').val('0.00');
    $('#add-quote-modal .header').text('Novo Orçamento');
    
    // Carregar dados básicos
    loadBasicData();
    
    // Configurar dropdown de clientes
    setupClientDropdown();
    
    // Adicionar primeira linha
    addQuoteRow();
    
    // Configurar eventos
    setupEvents();
    
    // Mostrar modal
    $('#add-quote-modal').modal('show');
}

// Carregar dados básicos
function loadBasicData() {
    // Configurar dropdown de clientes
    setupClientDropdown();
    
    // Carregar serviços
    $.ajax({
        url: `${API_URL}/api/landscaping/service`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            window.services = response && response.items ? response.items : [];
        },
        error: function() {
            window.services = [];
            console.log('Erro ao carregar serviços');
        }
    });
}

// Adicionar linha de item
function addQuoteRow() {
    const services = window.services || [];
    const options = services.map(s => 
        `<div class="item" data-value="${s.id}" data-price="${s.base_price || 0}">${s.service_name}</div>`
    ).join('');
    
    const row = `
        <tr>
            <td>
                <div class="ui selection dropdown service-select">
                    <input type="hidden" name="service_id">
                    <i class="dropdown icon"></i>
                    <div class="default text">Selecione</div>
                    <div class="menu">${options}</div>
                </div>
            </td>
            <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
            <td><button type="button" class="ui red mini button remove-item"><i class="trash icon"></i></button></td>
        </tr>
    `;
    
    $('#tableBody').append(row);
    
    // Configurar dropdown da nova linha
    const $row = $('#tableBody tr').last();
    $row.find('.service-select').dropdown({
        onChange: function(value, text, $item) {
            const price = parseFloat($item.data('price')) || 0;
            $row.find('.price-input').val(price.toFixed(2));
            calculateRow($row);
        }
    });
    
    // Eventos de input
    $row.find('.quantity-input, .price-input').on('input', () => calculateRow($row));
    
    // Evento de remoção
    $row.find('.remove-item').on('click', function() {
        if ($('#tableBody tr').length > 1) {
            $row.remove();
            calculateTotal();
        }
    });
}

// Calcular subtotal de uma linha
function calculateRow($row) {
    const qty = parseFloat($row.find('.quantity-input').val()) || 0;
    const price = parseFloat($row.find('.price-input').val()) || 0;
    const subtotal = qty * price;
    $row.find('.subtotal-input').val(subtotal.toFixed(2));
    calculateTotal();
}

// Calcular total geral
function calculateTotal() {
    let total = 0;
    $('#tableBody .subtotal-input').each(function() {
        total += parseFloat($(this).val()) || 0;
    });
    
    const discount = parseFloat($('[name="discount"]').val()) || 0;
    const finalTotal = total * (1 - discount / 100);
    
    $('#grandTotal').val(total.toFixed(2));
    $('#quote-total-value').val(finalTotal.toFixed(2));
}

// Configurar eventos principais
function setupEvents() {
    // Botão adicionar item
    $('#add-quote-item').off('click').on('click', function(e) {
        e.preventDefault();
        addQuoteRow();
    });
    
    // Desconto
    $('[name="discount"]').off('input').on('input', calculateTotal);
    
    // Salvar
    $('#save-quote-btn').off('click').on('click', saveQuote);
}

// Salvar orçamento
function saveQuote() {
    // Limpar mensagens anteriores
    $('#add-quote-modal .ui.message').remove();
    
    const clientId = $('#add-quote-form select[name="client_id"]').val();
    const validUntil = $('#add-quote-form input[name="valid_until"]').val();
    const description = $('#add-quote-form textarea[name="description"]').val();
    const totalValue = parseFloat($('#quote-total-value').val()) || 0;
    
    // Debug - mostrar valores
    console.log('Valores do formulário:', {
        clientId, validUntil, description, totalValue
    });
    
    // Validação detalhada
    let errors = [];
    if (!clientId) errors.push('Cliente');
    if (!validUntil) errors.push('Data de Validade');
    if (!description) errors.push('Descrição');
    if (totalValue <= 0) errors.push('Valor Total (adicione itens)');
    
    if (errors.length > 0) {
        showMessage('error', 'Campos obrigatórios', 'Preencha: ' + errors.join(', '));
        return;
    }
    
    const items = [];
    $('#tableBody tr').each(function() {
        const serviceId = $(this).find('.service-select').dropdown('get value');
        const quantity = parseFloat($(this).find('.quantity-input').val()) || 0;
        const unitPrice = parseFloat($(this).find('.price-input').val()) || 0;
        
        if (serviceId && quantity > 0 && unitPrice > 0) {
            items.push({
                service_id: parseInt(serviceId),
                quantity: quantity,
                unit_price: unitPrice,
                subtotal: quantity * unitPrice
            });
        }
    });
    
    if (items.length === 0) {
        showMessage('error', 'Itens inválidos', 'Adicione pelo menos um item válido ao orçamento');
        return;
    }
    
    const data = {
        user_id: 1,
        client_id: parseInt(clientId),
        description: description,
        valid_until: validUntil,
        total_value: totalValue,
        notes: $('[name="notes"]').val() || '',
        status: $('[name="status"]').val() || 'Pendente',
        items: items
    };
    
    $.ajax({
        url: `${API_URL}/api/landscaping/quote`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function() {
            showMessage('success', 'Sucesso!', 'Orçamento salvo com sucesso!');
            setTimeout(() => {
                $('#add-quote-modal').modal('hide');
                if (typeof loadQuotes === 'function') loadQuotes();
            }, 2000);
        },
        error: function(xhr) {
            showMessage('error', 'Erro ao salvar', xhr.responseText || 'Erro desconhecido');
        }
    });
}

// Função para mostrar mensagens no modal
function showMessage(type, title, message) {
    const messageClass = type === 'success' ? 'positive' : 'negative';
    const messageHtml = `
        <div class="ui ${messageClass} message">
            <i class="close icon"></i>
            <div class="header">${title}</div>
            <p>${message}</p>
        </div>
    `;
    
    $('#add-quote-modal .content').prepend(messageHtml);
    
    $('.ui.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
}