// Carregar dados dos orçamentos quando a aba de orçamentos for selecionada
$('.menu .item[data-tab="quotes"]').on('click', function() {
    loadQuotes();
    loadClientsForQuotes();
});

// Configurar evento para mudança de quantidade por página de orçamentos
$(document).on('change', '#quotes-page-size', function() {
    loadQuotes(1, $(this).val());
});

// Função para carregar os orçamentos
function loadQuotes(page = 1, pageSize = null) {
    const currentPageSize = pageSize || $('#quotes-page-size').val() || 10;
    
    $.ajax({
        url: `${API_URL}/api/landscaping/quote?page=${page}&page_size=${currentPageSize}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            const tbody = $('#quotes-table-body');
            tbody.empty();
            
            if (response && response.items && response.items.length > 0) {
                const promises = response.items.map(async function(quote) {
                    let clientName = '-';
                    
                    // Buscar nome do cliente via API
                    if (quote.client_id) {
                        try {
                            const clientResponse = await fetch(`${API_URL}/api/landscaping/client/${quote.client_id}`, {
                                headers: {
                                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                                }
                            });
                            if (clientResponse.ok) {
                                const client = await clientResponse.json();
                                clientName = client.client_name || '-';
                            }
                        } catch (error) {
                            console.error('Erro ao buscar cliente:', error);
                        }
                    }
                    
                    let statusClass = '';
                    let statusBadge = '';
                    
                    if (quote.status === 'Pendente') {
                        statusClass = 'warning';
                        statusBadge = 'status-pending';
                    } else if (quote.status === 'Aprovado') {
                        statusClass = 'positive';
                        statusBadge = 'status-approved';
                    } else if (quote.status === 'Rejeitado') {
                        statusClass = 'negative';
                        statusBadge = 'status-rejected';
                    } else if (quote.status === 'Inativo') {
                        statusClass = 'disabled';
                    }  else if (quote.status === 'Em Revisão') {
                        statusClass = 'review';
                        statusBadge = 'status-review';
                    } else if (quote.status === 'Concluído') {
                        statusClass = 'completed';
                        statusBadge = 'status-completed';
                    } else if (quote.status === 'Cancelado') {
                        statusClass = 'canceled';
                        statusBadge = 'status-canceled';
                    }
                    
                    const createdDate = quote.created_at ? formatDate(quote.created_at) : (quote.created_date ? formatDate(quote.created_date) : '-');
                    const validUntil = quote.valid_until ? formatDate(quote.valid_until) : '-';
                    
                    return `
                        <tr class="${statusClass}">
                            <td>${quote.id}</td>
                            <td>${clientName}</td>
                            <td>${quote.description.substring(0, 50)}${quote.description.length > 50 ? '...' : ''}</td>
                            <td>${createdDate}</td>
                            <td>${validUntil}</td>
                            <td>${formatCurrency(quote.total_value)}</td>
                            <td><span class="status-badge ${statusBadge}">${quote.status}</span></td>
                            <td>
                                <div class="ui mini buttons">
                                    <button class="ui blue button" onclick="viewQuote(${quote.id})"><i class="eye icon"></i></button>
                                    <button class="ui green button" onclick="editQuote(${quote.id})"><i class="edit icon"></i></button>
                                    <button class="ui red button" onclick="inactivateQuote(${quote.id})"><i class="trash icon"></i></button>
                                </div>
                            </td>
                        </tr>
                    `;
                });
                
                Promise.all(promises).then(rows => {
                    tbody.append(rows.join(''));
                });
                
                renderQuotesPagination(response.page, response.total_pages, response.total_items, currentPageSize);
            } else {
                tbody.append('<tr><td colspan="8" class="center aligned">Nenhum orçamento encontrado</td></tr>');
                $('#quotes-pagination').empty();
            }
        },
        error: function(error) {
            console.error('Erro ao carregar orçamentos:', error);
            $('#quotes-table-body').html('<tr><td colspan="8" class="center aligned error">Erro ao carregar orçamentos</td></tr>');
        }
    });
}

function loadQuotesPage(page) {
    loadQuotes(page);
}

function renderQuotesPagination(currentPage, totalPages, totalItems, pageSize) {
    const pagination = $('#quotes-pagination');
    pagination.empty();
    
    if (totalPages <= 1) {
        return;
    }
    
    const prevDisabled = currentPage === 1 ? 'disabled' : '';
    pagination.append(`
        <a class="item ${prevDisabled}" onclick="${currentPage > 1 ? 'loadQuotesPage(' + (currentPage - 1) + ')' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        pagination.append('<a class="item" onclick="loadQuotesPage(1)">1</a>');
        if (startPage > 2) {
            pagination.append('<div class="disabled item">...</div>');
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        pagination.append(`
            <a class="item ${activeClass}" onclick="loadQuotesPage(${i})">
                ${i}
            </a>
        `);
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagination.append('<div class="disabled item">...</div>');
        }
        pagination.append(`<a class="item" onclick="loadQuotesPage(${totalPages})">${totalPages}</a>`);
    }
    
    const nextDisabled = currentPage === totalPages ? 'disabled' : '';
    pagination.append(`
        <a class="item ${nextDisabled}" onclick="${currentPage < totalPages ? 'loadQuotesPage(' + (currentPage + 1) + ')' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
    
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = Math.min(currentPage * pageSize, totalItems);
    $('#quotes-pagination-info').html(`
        Mostrando ${startItem} a ${endItem} de ${totalItems} orçamentos
    `);
}

function viewQuote(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/quote/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: async function(quote) {
            let clientName = quote.client || '-';
            
            // Buscar nome do cliente via API
            if (quote.client_id) {
                try {
                    const clientResponse = await fetch(`${API_URL}/api/landscaping/client/${quote.client_id}`, {
                        headers: {
                            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                        }
                    });
                    if (clientResponse.ok) {
                        const client = await clientResponse.json();
                        clientName = client.client_name || clientName;
                    }
                } catch (error) {
                    console.error('Erro ao buscar cliente:', error);
                }
            }
            
            let itemsHtml = '';
            if (quote.items && quote.items.length > 0) {
                itemsHtml = '<table class="ui celled table"><thead><tr><th>Serviço</th><th>Quantidade</th><th>Preço Unitário</th><th>Subtotal</th></tr></thead><tbody>';
                
                // Buscar nomes dos serviços
                const servicePromises = quote.items.map(async item => {
                    let serviceName = item.service_name || 'Serviço';
                    
                    if (item.service_id) {
                        try {
                            const serviceResponse = await fetch(`${API_URL}/api/landscaping/service/${item.service_id}`, {
                                headers: {
                                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                                }
                            });
                            if (serviceResponse.ok) {
                                const service = await serviceResponse.json();
                                serviceName = service.service_name || serviceName;
                            }
                        } catch (error) {
                            console.error('Erro ao buscar serviço:', error);
                        }
                    }
                    
                    const subtotal = item.quantity * item.unit_price;
                    return `
                        <tr>
                            <td>${serviceName}</td>
                            <td>${item.quantity}</td>
                            <td>${formatCurrency(item.unit_price)}</td>
                            <td>${formatCurrency(subtotal)}</td>
                        </tr>
                    `;
                });
                
                const itemRows = await Promise.all(servicePromises);
                itemsHtml += itemRows.join('') + '</tbody></table>';
            } else {
                itemsHtml = '<p>Nenhum item no orçamento</p>';
            }
            
            // Remover modal existente se houver
            $('#view-quote-modal').remove();
            
            $('body').append(`
                <div class="ui modal" id="view-quote-modal">
                    <i class="close icon"></i>
                    <div class="header">Orçamento #${quote.id}</div>
                    <div class="content">
                        <div class="ui form">
                            <div class="two fields">
                                <div class="field">
                                    <label>Cliente</label>
                                    <p>${clientName}</p>
                                </div>
                                <div class="field">
                                    <label>Status</label>
                                    <p>${quote.status}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Data de Criação</label>
                                    <p>${formatDate(quote.created_at || quote.created_date)}</p>
                                </div>
                                <div class="field">
                                    <label>Validade</label>
                                    <p>${formatDate(quote.valid_until)}</p>
                                </div>
                            </div>
                            <div class="field">
                                <label>Descrição</label>
                                <p>${quote.description}</p>
                            </div>
                            <div class="field">
                                <label>Itens do Orçamento</label>
                                ${itemsHtml}
                            </div>
                            <div class="field">
                                <label>Valor Total</label>
                                <p><strong>${formatCurrency(quote.total_value)}</strong></p>
                            </div>
                        </div>
                    </div>
                    <div class="actions">
                        <div class="ui primary button" onclick="generateQuotePDF(${quote.id})"><i class="file pdf icon"></i> Gerar PDF</div>
                        <div class="ui green button" onclick="sendQuotePDFWhatsApp(${quote.id})"><i class="whatsapp icon"></i> Enviar WhatsApp</div>
                        <div class="ui button" onclick="$('#view-quote-modal').modal('hide'); $('#view-quote-modal').remove();">Fechar</div>
                    </div>
                </div>
            `);
            $('#view-quote-modal').modal({
                onHidden: function() {
                    $('#view-quote-modal').remove();
                }
            }).modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do orçamento:', error);
            alert('Erro ao obter detalhes do orçamento');
        }
    });
}

function editQuote(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/quote/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(quote) {
            $('#add-quote-form')[0].reset();
            $('#tableBody').empty();
            
            // Cliente será selecionado após carregar a lista
            $('#add-quote-form input[name="valid_until"]').val(formatDateForInput(quote.valid_until));
            $('#add-quote-form textarea[name="description"]').val(quote.description);
            $('#add-quote-form textarea[name="notes"]').val(quote.notes || '');
            $('#add-quote-form select[name="status"]').dropdown('set selected', quote.status);
            $('#add-quote-form input[name="discount"]').val(0);
            
            $.ajax({
                url: `${API_URL}/api/landscaping/service`,
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                },
                success: function(servicesResponse) {
                    const services = servicesResponse.items || [];
                    $('#grandTotal').val('0.00');
                    $('#quote-total-value').val('0.00');
                    
                    if (quote.items && quote.items.length > 0) {
                        quote.items.forEach(function(item) {
                            const rowHtml = `
                                <tr>
                                    <td>
                                        <div class="ui selection dropdown service-select">
                                            <input type="hidden" name="service_id">
                                            <i class="dropdown icon"></i>
                                            <div class="default text">Selecione</div>
                                            <div class="menu"></div>
                                        </div>
                                    </td>
                                    <td><div class="ui input"><input type="number" class="quantity-input" value="${item.quantity}" min="1"></div></td>
                                    <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="${parseFloat(item.unit_price).toFixed(2)}"></div></td>
                                    <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="${(item.quantity * item.unit_price).toFixed(2)}"></div></td>
                                    <td class="center aligned"><button type="button" class="ui icon red mini button remove-item"><i class="trash icon"></i></button></td>
                                </tr>
                            `;
                            
                            $('#tableBody').append(rowHtml);
                            const $row = $('#tableBody tr').last();
                            
                            services.forEach(function(service) {
                                const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                                $row.find('.service-select .menu').append(option);
                            });
                            
                            $row.find('.service-select').dropdown({
                                onChange: function(value, text, $selectedItem) {
                                    const $dropdown = $(this);
                                    const $row = $dropdown.closest('tr');
                                    const priceInput = $row.find('.price-input');
                                    const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
                                    priceInput.val(selectedPrice.toFixed(2));
                                    const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
                                    $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
                                    calculateQuoteTotal();
                                }
                            });
                            
                            // Configurar eventos para inputs de quantidade e preço
                            $row.find('.quantity-input, .price-input').on('input', function() {
                                const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
                                const price = parseFloat($row.find('.price-input').val()) || 0;
                                $row.find('.subtotal-input').val((quantity * price).toFixed(2));
                                calculateQuoteTotal();
                            });
                            
                            // Configurar evento para remover linha
                            $row.find('.remove-item').on('click', function() {
                                if ($('#tableBody tr').length > 1) {
                                    $(this).closest('tr').remove();
                                    calculateQuoteTotal();
                                }
                            });
                            
                            $row.find('.service-select').dropdown('set selected', item.service_id);
                        });
                        calculateQuoteTotal();
                    }
                    
                    // Configurar eventos globais para a tabela
                    $('#tableBody').off('input', '.quantity-input, .price-input').on('input', '.quantity-input, .price-input', function() {
                        const $row = $(this).closest('tr');
                        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
                        const price = parseFloat($row.find('.price-input').val()) || 0;
                        $row.find('.subtotal-input').val((quantity * price).toFixed(2));
                        calculateQuoteTotal();
                    });
                    
                    $('#tableBody').off('click', '.remove-item').on('click', '.remove-item', function() {
                        if ($('#tableBody tr').length > 1) {
                            $(this).closest('tr').remove();
                            calculateQuoteTotal();
                        }
                    });
                    
                    setupQuoteItemEvents();
                    $('#add-quote-modal .header').text('Editar Orçamento');
                    
                    // Configurar busca rápida de clientes
                    setupClientSearch(quote.client_id);
                    
                    // Configurar botão de adicionar item no modal de edição
                    $('#add-quote-item').off('click').on('click', function(e) {
                        e.preventDefault();
                        addQuoteItemRow(services);
                        return false;
                    });
                    
                    $('#save-quote-btn').off('click').on('click', function() {
                        updateQuote(id);
                    });
                    
                    $('#add-quote-modal').modal({
                        closable: false
                    }).modal('show');
                },
                error: function(error) {
                    console.error('Erro ao carregar serviços:', error);
                    alert('Erro ao carregar serviços para edição do orçamento');
                }
            });
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do orçamento:', error);
            alert('Erro ao obter detalhes do orçamento');
        }
    });
}

function updateQuote(id) {
    // Limpar mensagens anteriores
    $('#add-quote-modal .ui.message').remove();
    
    const clientId = $('#add-quote-form select[name="client_id"]').val();
    const validUntil = $('#add-quote-form input[name="valid_until"]').val();
    const description = $('#add-quote-form textarea[name="description"]').val();
    const notes = $('#add-quote-form textarea[name="notes"]').val() || '';
    const status = $('#add-quote-form select[name="status"]').val() || 'Pendente';
    const totalValue = parseFloat($('#quote-total-value').val()) || 0;
    
    if (!clientId || !validUntil || !description || totalValue <= 0) {
        $('#add-quote-modal .content').prepend(`
            <div class="ui negative message">
                <i class="close icon"></i>
                <div class="header">Campos obrigatórios</div>
                <p>Por favor, preencha todos os campos obrigatórios e adicione pelo menos um item ao orçamento.</p>
            </div>
        `);
        $('.ui.message .close').on('click', function() {
            $(this).closest('.message').transition('fade');
        });
        return;
    }
    
    const items = [];
    $('#tableBody tr').each(function() {
        const serviceId = $(this).find('.service-select').dropdown('get value');
        const quantity = parseFloat($(this).find('.quantity-input').val()) || 0;
        const unitPrice = parseFloat($(this).find('.price-input').val()) || 0;
        const subtotal = quantity * unitPrice;
        
        if (serviceId && quantity > 0 && unitPrice > 0) {
            items.push({
                service_id: parseInt(serviceId),
                quantity: quantity,
                unit_price: unitPrice,
                subtotal: subtotal,
                description: ''
            });
        }
    });
    
    const quoteData = {
        client_id: parseInt(clientId),
        description: description,
        valid_until: validUntil,
        total_value: totalValue,
        notes: notes,
        status: status,
        items: items
    };
    
    $.ajax({
        url: `${API_URL}/api/landscaping/quote/${id}?user_id=1`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(quoteData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            $('#add-quote-modal .content').prepend(`
                <div class="ui positive message">
                    <i class="close icon"></i>
                    <div class="header">Sucesso!</div>
                    <p>Orçamento atualizado com sucesso!</p>
                </div>
            `);
            $('.ui.message .close').on('click', function() {
                $(this).closest('.message').transition('fade');
            });
            
            setTimeout(function() {
                $('#add-quote-modal').modal('hide');
                $('#add-quote-form')[0].reset();
                $('#tableBody').empty();
                $('#add-quote-modal .header').text('Novo Orçamento');
                $('#save-quote-btn').off('click');
                loadQuotes();
            }, 2000);
        },
        error: function(xhr, status, error) {
            console.error('Erro ao atualizar orçamento:', error);
            $('#add-quote-modal .content').prepend(`
                <div class="ui negative message">
                    <i class="close icon"></i>
                    <div class="header">Erro ao atualizar</div>
                    <p>${xhr.responseText || error}</p>
                </div>
            `);
            $('.ui.message .close').on('click', function() {
                $(this).closest('.message').transition('fade');
            });
        }
    });
}

function formatDateForInput(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
        if (typeof dateString === 'string' && dateString.includes('-')) {
            return dateString.split('T')[0];
        }
        return '';
    }
    return date.toISOString().split('T')[0];
}

function inactivateQuote(id) {
    if (confirm('Tem certeza que deseja inativar este orçamento?')) {
        $.ajax({
            url: `${API_URL}/api/landscaping/quote/${id}?user_id=1`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                alert('Orçamento inativado com sucesso!');
                loadQuotes();
            },
            error: function(error) {
                console.error('Erro ao inativar orçamento:', error);
                alert('Erro ao inativar orçamento');
            }
        });
    }
}

// Função para calcular o subtotal de uma linha e o total geral
function calculateQuoteTotal() {
    let grandTotal = 0;
    $('#tableBody tr').each(function() {
        const $row = $(this);
        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
        const price = parseFloat($row.find('.price-input').val()) || 0;
        const subtotal = (quantity * price).toFixed(2);

        $row.find('.subtotal-input').val(subtotal);
        grandTotal += parseFloat(subtotal);
    });
    $('#grandTotal').val(grandTotal.toFixed(2));
    $('#quote-total-value').val(grandTotal.toFixed(2));
}

// Inicializar os dropdowns e configurar eventos
function setupQuoteItemEvents() {
    $('.service-select').dropdown({
        onChange: function(value, text, $selectedItem) {
            const $dropdown = $(this);
            const $row = $dropdown.closest('tr');
            const priceInput = $row.find('.price-input');
            
            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
            priceInput.val(selectedPrice.toFixed(2));
            
            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
            
            calculateQuoteTotal();
        }
    });
    
    $('#tableBody').on('input', '.quantity-input, .price-input', function() {
        const $row = $(this).closest('tr');
        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
        const price = parseFloat($row.find('.price-input').val()) || 0;
        $row.find('.subtotal-input').val((quantity * price).toFixed(2));
        calculateQuoteTotal();
    });
    
    $('#tableBody').on('click', '.remove-item', function() {
        if ($('#tableBody tr').length > 1) {
            $(this).closest('tr').remove();
            calculateQuoteTotal();
        }
    });
}

// Adicionar item ao orçamento
$('#add-quote-item').on('click', function() {
    const newItem = $('.quote-item').first().clone();
    newItem.find('input').val('');
    newItem.find('select').val('');
    $('#quote-items').append(newItem);
    $('.ui.dropdown').dropdown('refresh');
    setupQuoteItemEvents();
});

// Configurar evento de desconto
$('[name="discount"]').on('input', calculateQuoteTotal);



// Função para adicionar nova linha de item no orçamento
function addQuoteItemRow(services) {
    const newRowHtml = `
        <tr>
            <td>
                <div class="ui selection dropdown service-select">
                    <input type="hidden" name="service_id">
                    <i class="dropdown icon"></i>
                    <div class="default text">Selecione</div>
                    <div class="menu"></div>
                </div>
            </td>
            <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00"></div></td>
            <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
            <td class="center aligned"><button type="button" class="ui icon red mini button remove-item"><i class="trash icon"></i></button></td>
        </tr>
    `;
    
    $('#tableBody').append(newRowHtml);
    const $newRow = $('#tableBody tr').last();
    
    services.forEach(function(service) {
        const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
        $newRow.find('.service-select .menu').append(option);
    });
    
    $newRow.find('.service-select').dropdown({
        onChange: function(value, text, $selectedItem) {
            const $dropdown = $(this);
            const $row = $dropdown.closest('tr');
            const priceInput = $row.find('.price-input');
            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
            priceInput.val(selectedPrice.toFixed(2));
            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
            calculateQuoteTotal();
        }
    });
    
    $newRow.find('.quantity-input, .price-input').on('input', function() {
        const quantity = parseFloat($newRow.find('.quantity-input').val()) || 0;
        const price = parseFloat($newRow.find('.price-input').val()) || 0;
        $newRow.find('.subtotal-input').val((quantity * price).toFixed(2));
        calculateQuoteTotal();
    });
    
    $newRow.find('.remove-item').on('click', function() {
        if ($('#tableBody tr').length > 1) {
            $newRow.remove();
            calculateQuoteTotal();
        }
    });
    
    calculateQuoteTotal();
}

// Função para enviar orçamento via WhatsApp
function sendQuoteWhatsApp(quoteId, clientId) {
    // Primeiro, buscar dados do cliente
    $.ajax({
        url: `${API_URL}/api/landscaping/client/${clientId}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(client) {
            if (!client.phone_number) {
                alert('Cliente não possui telefone cadastrado.');
                return;
            }
            
            // Gerar PDF do orçamento
            fetch(`${API_URL}/api/landscaping/quote/${quoteId}/pdf`, {
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                }
            })
            .then(response => response.blob())
            .then(blob => {
                // Criar FormData para envio
                const formData = new FormData();
                formData.append('phone_number', client.phone_number);
                formData.append('file', blob, `Orcamento_${quoteId}.pdf`);
                formData.append('filename', `Orçamento #${quoteId}.pdf`);
                
                // Enviar via WhatsApp
                return fetch(`${API_URL}/api/whatsapp/sendFile`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                    }
                });
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Orçamento enviado via WhatsApp com sucesso!');
                } else {
                    alert(`Erro ao enviar: ${result.message}`);
                }
            })
            .catch(error => {
                console.error('Erro ao enviar orçamento:', error);
                alert('Erro ao enviar orçamento via WhatsApp.');
            });
        },
        error: function() {
            alert('Erro ao obter dados do cliente.');
        }
    });
}

// Função para configurar busca rápida de clientes com search dropdown
function setupClientSearch(selectedClientId = null) {
    const clientDropdown = $('#add-quote-form select[name="client_id"]');
    
    // Limpar dropdown antes de reconfigurar
    clientDropdown.dropdown('destroy');
    
    // Configurar dropdown com busca
    clientDropdown.dropdown({
        fullTextSearch: true,
        filterRemoteData: false,
        saveRemoteData: false,
        minCharacters: 1,
        searchDelay: 300,
        placeholder: 'Selecione ou busque um cliente',
        message: {
            noResults: 'Nenhum cliente encontrado'
        }
    });
    
    // Carregar todos os clientes inicialmente
    loadClientsForQuotes();
    
    if (selectedClientId) {
        setTimeout(function() {
            clientDropdown.dropdown('set selected', selectedClientId);
        }, 500);
    }
}

// Função para carregar clientes para o dropdown de orçamentos
function loadClientsForQuotes() {
    const clientSelect = $('#quote-client-filter, [name="client_id"]');
    clientSelect.find('option:not(:first)').remove();
    
    function loadPage(page = 1, allClients = []) {
        $.ajax({
            url: `${API_URL}/api/landscaping/client?page=${page}&page_size=100`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                if (response && response.items) {
                    allClients = allClients.concat(response.items);
                    
                    // Se há mais páginas, carregar a próxima
                    if (page < response.total_pages) {
                        loadPage(page + 1, allClients);
                    } else {
                        // Todas as páginas carregadas, popular dropdown
                        allClients.forEach(function(client) {
                            clientSelect.append(`<option value="${client.id}">${client.client_name}</option>`);
                        });
                        $('.ui.dropdown').dropdown('refresh');
                    }
                }
            },
            error: function(error) {
                console.error('Erro ao carregar clientes:', error);
            }
        });
    }
    
    loadPage();
}

