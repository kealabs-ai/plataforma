// Carregar dados dos orçamentos quando a aba de orçamentos for selecionada
$('.menu .item[data-tab="quotes"]').on('click', function() {
    loadQuotes();
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
                response.items.forEach(function(quote) {
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
                    }
                    
                    const createdDate = quote.created_date ? formatDate(quote.created_date) : '-';
                    const validUntil = quote.valid_until ? formatDate(quote.valid_until) : '-';
                    
                    tbody.append(`
                        <tr class="${statusClass}">
                            <td>${quote.id}</td>
                            <td>${quote.client}</td>
                            <td>${quote.description.substring(0, 50)}${quote.description.length > 50 ? '...' : ''}</td>
                            <td>${createdDate}</td>
                            <td>${validUntil}</td>
                            <td>R$ ${parseFloat(quote.total_value).toFixed(2)}</td>
                            <td><span class="status-badge ${statusBadge}">${quote.status}</span></td>
                            <td>
                                <div class="ui mini buttons">
                                    <button class="ui blue button" onclick="viewQuote(${quote.id})"><i class="eye icon"></i></button>
                                    <button class="ui green button" onclick="editQuote(${quote.id})"><i class="edit icon"></i></button>
                                    <button class="ui red button" onclick="inactivateQuote(${quote.id})"><i class="trash icon"></i></button>
                                </div>
                            </td>
                        </tr>
                    `);
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
        success: function(quote) {
            let itemsHtml = '';
            if (quote.items && quote.items.length > 0) {
                itemsHtml = '<table class="ui celled table"><thead><tr><th>Serviço</th><th>Quantidade</th><th>Preço Unitário</th><th>Subtotal</th></tr></thead><tbody>';
                quote.items.forEach(item => {
                    const subtotal = item.quantity * item.unit_price;
                    itemsHtml += `
                        <tr>
                            <td>${item.service_name || 'Serviço'}</td>
                            <td>${item.quantity}</td>
                            <td>R$ ${parseFloat(item.unit_price).toFixed(2)}</td>
                            <td>R$ ${subtotal.toFixed(2)}</td>
                        </tr>
                    `;
                });
                itemsHtml += '</tbody></table>';
            } else {
                itemsHtml = '<p>Nenhum item no orçamento</p>';
            }
            
            $('body').append(`
                <div class="ui modal" id="view-quote-modal">
                    <i class="close icon"></i>
                    <div class="header">Orçamento #${quote.id}</div>
                    <div class="content">
                        <div class="ui form">
                            <div class="two fields">
                                <div class="field">
                                    <label>Cliente</label>
                                    <p>${quote.client}</p>
                                </div>
                                <div class="field">
                                    <label>Status</label>
                                    <p>${quote.status}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Data de Criação</label>
                                    <p>${formatDate(quote.created_date)}</p>
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
                                <p><strong>R$ ${parseFloat(quote.total_value).toFixed(2)}</strong></p>
                            </div>
                        </div>
                    </div>
                    <div class="actions">
                        <div class="ui button" onclick="$('#view-quote-modal').modal('hide')">Fechar</div>
                    </div>
                </div>
            `);
            $('#view-quote-modal').modal('show');
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
            
            $('#add-quote-form select[name="client_id"]').val(quote.client_id).trigger('change');
            $('#add-quote-form input[name="valid_until"]').val(formatDateForInput(quote.valid_until));
            $('#add-quote-form textarea[name="description"]').val(quote.description);
            $('#add-quote-form textarea[name="notes"]').val(quote.notes || '');
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
                            
                            $row.find('.service-select').dropdown('set selected', item.service_id);
                        });
                        calculateQuoteTotal();
                    }
                    
                    setupQuoteItemEvents();
                    $('#add-quote-modal .header').text('Editar Orçamento');
                    
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
    const clientId = $('#add-quote-form select[name="client_id"]').val();
    const validUntil = $('#add-quote-form input[name="valid_until"]').val();
    const description = $('#add-quote-form textarea[name="description"]').val();
    const notes = $('#add-quote-form textarea[name="notes"]').val() || '';
    const totalValue = parseFloat($('#quote-total-value').val()) || 0;
    
    if (!clientId || !validUntil || !description || totalValue <= 0) {
        alert('Por favor, preencha todos os campos obrigatórios e adicione pelo menos um item ao orçamento.');
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
        user_id: 1,
        client_id: parseInt(clientId),
        description: description,
        valid_until: validUntil,
        total_value: totalValue,
        notes: notes,
        status: 'Pendente',
        items: items
    };
    
    $.ajax({
        url: `${API_URL}/api/landscaping/quote/${id}?user_id=${quoteData.user_id}`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(quoteData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            alert('Orçamento atualizado com sucesso!');
            $('#add-quote-modal').modal('hide');
            $('#add-quote-form')[0].reset();
            $('#add-quote-modal .header').text('Novo Orçamento');
            $('#save-quote-btn').off('click');
            loadQuotes();
        },
        error: function(xhr, status, error) {
            console.error('Erro ao atualizar orçamento:', error);
            alert('Erro ao atualizar orçamento: ' + (xhr.responseText || error));
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