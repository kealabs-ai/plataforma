// Arquivo específico para gerenciar o modal de orçamentos

// Função para inicializar o modal de orçamento
function initializeQuoteModal() {
    // Limpar formulário e tabela
    $('#add-quote-form')[0].reset();
    $('#tableBody').empty();
    $('#grandTotal').val('0.00');
    $('#quote-total-value').val('0.00');
    
    // Restaurar título padrão
    $('#add-quote-modal .header').text('Novo Orçamento');
    
    // Carregar dados de forma mais simples
    loadServicesForQuotes().then(() => {
        setupClientDropdown();
        addInitialQuoteRow();
        setupQuoteModalEvents();
        
        $('#add-quote-modal').modal({
            closable: false
        }).modal('show');
    }).catch(() => {
        // Se falhar, mostrar modal mesmo assim
        setupClientDropdown();
        addInitialQuoteRow();
        setupQuoteModalEvents();
        $('#add-quote-modal').modal('show');
    });
}

// Função para carregar serviços para o modal de orçamentos
function loadServicesForQuotes() {
    return new Promise((resolve) => {
        $.ajax({
            url: `${API_URL}/api/landscaping/service`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                window.availableServices = response.items || [];
                resolve();
            },
            error: function(error) {
                console.error('Erro ao carregar serviços:', error);
                window.availableServices = [];
                resolve(); // Resolve mesmo com erro
            }
        });
    });
}

// Função para adicionar linha inicial ao orçamento
function addInitialQuoteRow() {
    const services = window.availableServices || [];
    
    const rowHtml = `
        <tr>
            <td>
                <div class="ui selection dropdown service-select">
                    <input type="hidden" name="service_id">
                    <i class="dropdown icon"></i>
                    <div class="default text">Selecione um serviço</div>
                    <div class="menu">
                        ${services.map(service => 
                            `<div class="item" data-value="${service.id}" data-price="${service.base_price || 0}">${service.service_name}</div>`
                        ).join('')}
                    </div>
                </div>
            </td>
            <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00" min="0"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
            <td class="center aligned">
                <button type="button" class="ui icon red mini button remove-item">
                    <i class="trash icon"></i>
                </button>
            </td>
        </tr>
    `;
    
    $('#tableBody').append(rowHtml);
    
    const $newRow = $('#tableBody tr').last();
    initializeServiceDropdown($newRow);
}

// Função para inicializar dropdown de serviços em uma linha
function initializeServiceDropdown($row) {
    $row.find('.service-select').dropdown({
        onChange: function(value, text, $selectedItem) {
            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
            const $priceInput = $row.find('.price-input');
            
            // Atualizar preço
            $priceInput.val(selectedPrice.toFixed(2));
            
            // Calcular subtotal
            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
            
            // Recalcular total geral
            calculateQuoteTotal();
        }
    });
    
    // Configurar eventos de input para quantidade e preço
    $row.find('.quantity-input, .price-input').on('input', function() {
        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
        const price = parseFloat($row.find('.price-input').val()) || 0;
        const subtotal = quantity * price;
        
        $row.find('.subtotal-input').val(subtotal.toFixed(2));
        calculateQuoteTotal();
    });
    
    // Configurar evento de remoção
    $row.find('.remove-item').on('click', function() {
        if ($('#tableBody tr').length > 1) {
            $row.remove();
            calculateQuoteTotal();
        } else {
            alert('Deve haver pelo menos um item no orçamento.');
        }
    });
}

// Função para configurar eventos do modal
function setupQuoteModalEvents() {
    // Remover eventos anteriores para evitar duplicação
    $('#add-quote-item').off('click.quoteModal');
    $('#save-quote-btn').off('click.quoteModal');
    $('[name=\"discount\"]').off('input.quoteModal');
    
    // Evento para adicionar novo item
    $('#add-quote-item').on('click.quoteModal', function(e) {
        e.preventDefault();
        addNewQuoteItem();
        return false;
    });
    
    // Evento para salvar orçamento
    $('#save-quote-btn').on('click.quoteModal', function() {
        saveNewQuote();
    });
    
    // Evento para desconto
    $('[name=\"discount\"]').on('input.quoteModal', function() {
        calculateQuoteTotal();
    });
}

// Função para adicionar novo item ao orçamento
function addNewQuoteItem() {
    const services = window.availableServices || [];
    
    const rowHtml = `
        <tr>
            <td>
                <div class="ui selection dropdown service-select">
                    <input type="hidden" name="service_id">
                    <i class="dropdown icon"></i>
                    <div class="default text">Selecione um serviço</div>
                    <div class="menu">
                        ${services.map(service => 
                            `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`
                        ).join('')}
                    </div>
                </div>
            </td>
            <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00" min="0"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
            <td class="center aligned">
                <button type="button" class="ui icon red mini button remove-item">
                    <i class="trash icon"></i>
                </button>
            </td>
        </tr>
    `;
    
    $('#tableBody').append(rowHtml);
    
    // Inicializar dropdown da nova linha
    const $newRow = $('#tableBody tr').last();
    initializeServiceDropdown($newRow);
    
    // Recalcular total
    calculateQuoteTotal();
}

// Função para calcular total do orçamento
function calculateQuoteTotal() {
    let grandTotal = 0;
    
    $('#tableBody tr').each(function() {
        const subtotal = parseFloat($(this).find('.subtotal-input').val()) || 0;
        grandTotal += subtotal;
    });
    
    // Aplicar desconto se houver
    const discount = parseFloat($('[name="discount"]').val()) || 0;
    const totalWithDiscount = grandTotal * (1 - discount / 100);
    
    // Atualizar campos
    $('#grandTotal').val(grandTotal.toFixed(2));
    $('#quote-total-value').val(totalWithDiscount.toFixed(2));
}

// Função para salvar novo orçamento
function saveNewQuote() {
    // Limpar mensagens anteriores
    $('#add-quote-modal .ui.message').remove();
    
    // Obter dados do formulário
    const clientId = $('#add-quote-form select[name="client_id"]').val();
    const validUntil = $('#add-quote-form input[name="valid_until"]').val();
    const description = $('#add-quote-form textarea[name="description"]').val();
    const notes = $('#add-quote-form textarea[name="notes"]').val() || '';
    const status = $('#add-quote-form select[name="status"]').val() || 'Pendente';
    const totalValue = parseFloat($('#quote-total-value').val()) || 0;
    
    // Validar campos obrigatórios
    if (!clientId || !validUntil || !description || totalValue <= 0) {
        showQuoteModalMessage('error', 'Campos obrigatórios', 'Por favor, preencha todos os campos obrigatórios e adicione pelo menos um item ao orçamento.');
        return;
    }
    
    // Coletar itens do orçamento
    const items = [];
    let hasValidItems = false;
    
    $('#tableBody tr').each(function() {
        const serviceId = $(this).find('.service-select').dropdown('get value');
        const quantity = parseFloat($(this).find('.quantity-input').val()) || 0;
        const unitPrice = parseFloat($(this).find('.price-input').val()) || 0;
        
        if (serviceId && quantity > 0 && unitPrice > 0) {
            hasValidItems = true;
            items.push({
                service_id: parseInt(serviceId),
                quantity: quantity,
                unit_price: unitPrice,
                subtotal: quantity * unitPrice,
                description: ''
            });
        }
    });
    
    if (!hasValidItems) {
        showQuoteModalMessage('error', 'Itens inválidos', 'Adicione pelo menos um item válido ao orçamento.');
        return;
    }
    
    // Preparar dados para envio
    const quoteData = {
        user_id: 1, // Usando user_id fixo para teste
        client_id: parseInt(clientId),
        description: description,
        created_at: new Date().toISOString().split('T')[0],
        valid_until: validUntil,
        total_value: totalValue,
        notes: notes,
        status: status,
        items: items
    };
    
    // Enviar dados para a API
    $.ajax({
        url: `${API_URL}/api/landscaping/quote`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(quoteData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            showQuoteModalMessage('success', 'Sucesso!', 'Orçamento criado com sucesso!');
            
            setTimeout(function() {
                $('#add-quote-modal').modal('hide');
                $('#add-quote-form')[0].reset();
                $('#tableBody').empty();
                
                // Recarregar lista de orçamentos se a função existir
                if (typeof loadQuotes === 'function') {
                    loadQuotes();
                }
            }, 2000);
        },
        error: function(xhr, status, error) {
            console.error('Erro ao criar orçamento:', error);
            showQuoteModalMessage('error', 'Erro ao criar', xhr.responseText || error);
        }
    });
}

// Função para configurar dropdown de clientes com busca
function setupClientDropdown() {
    const clientDropdown = $('#add-quote-form select[name="client_id"]');
    
    // Limpar e reconfigurar dropdown
    clientDropdown.dropdown('destroy');
    clientDropdown.find('option:not(:first)').remove();
    
    // Carregar primeiros 20 clientes
    loadInitialClients();
    
    // Configurar dropdown com busca local e busca remota customizada
    clientDropdown.dropdown({
        fullTextSearch: true,
        placeholder: 'Selecione ou busque um cliente',
        onSearch: function(query) {
            if (query.length >= 2) {
                searchClients(query, clientDropdown);
            }
        }
    });
}

// Função para buscar clientes
function searchClients(query, dropdown) {
    $.ajax({
        url: `${API_URL}/api/landscaping/client/search?q=${encodeURIComponent(query)}&limit=20`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            if (response && response.items) {
                // Limpar opções existentes exceto a primeira
                dropdown.find('option:not(:first)').remove();
                
                // Adicionar novos resultados
                response.items.forEach(client => {
                    dropdown.append(`<option value="${client.id}">${client.client_name}</option>`);
                });
                
                // Atualizar dropdown
                dropdown.dropdown('refresh');
            }
        },
        error: function(error) {
            console.error('Erro ao buscar clientes:', error);
        }
    });
}

// Carregar primeiros 20 clientes
function loadInitialClients() {
    const clientSelect = $('#add-quote-form select[name="client_id"]');
    
    $.ajax({
        url: `${API_URL}/api/landscaping/client?page=1&page_size=20`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            if (response && response.items) {
                response.items.forEach(function(client) {
                    clientSelect.append(`<option value="${client.id}">${client.client_name}</option>`);
                });
            }
        },
        error: function(error) {
            console.error('Erro ao carregar clientes:', error);
        }
    });
}

// Função para mostrar mensagens no modal
function showQuoteModalMessage(type, title, message) {
    const messageClass = type === 'success' ? 'positive' : 'negative';
    const messageHtml = `
        <div class="ui ${messageClass} message">
            <i class="close icon"></i>
            <div class="header">${title}</div>
            <p>${message}</p>
        </div>
    `;
    
    $('#add-quote-modal .content').prepend(messageHtml);
    
    // Configurar botão de fechar mensagem
    $('.ui.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
}