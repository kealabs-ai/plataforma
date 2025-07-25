const API_URL = "http://localhost:8000";

// Função para calcular o subtotal de uma linha e o total geral
function calculateQuoteTotal() {
    let grandTotal = 0;
    $('#tableBody tr').each(function() {
        const $row = $(this);
        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
        const price = parseFloat($row.find('.price-input').val()) || 0;
        const subtotal = (quantity * price).toFixed(2); // Arredonda para 2 casas decimais

        $row.find('.subtotal-input').val(subtotal);
        grandTotal += parseFloat(subtotal);
    });
    $('#grandTotal').val(grandTotal.toFixed(2)); // Atualiza o total geral
    $('#quote-total-value').val(grandTotal.toFixed(2)); // Atualiza o campo de valor total do orçamento
}

// Função para calcular o subtotal de uma linha
function calculateRowSubtotal($row) {
    const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
    const price = parseFloat($row.find('.price-input').val()) || 0;
    const subtotal = quantity * price;
    $row.find('.subtotal-input').val(subtotal.toFixed(2));
    return subtotal;
}

// Inicializar os dropdowns e configurar eventos
function setupQuoteItemEvents() {
    // Inicializar os dropdowns
    $('.service-select').dropdown({
        onChange: function(value, text, $selectedItem) {
            const $dropdown = $(this);
            const $row = $dropdown.closest('tr');
            const priceInput = $row.find('.price-input');
            
            // Obter o preço do serviço selecionado
            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
            priceInput.val(selectedPrice.toFixed(2));
            
            // Calcular subtotal
            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
            
            // Recalcular total
            calculateQuoteTotal();
        }
    });
    
    // Configurar eventos para inputs de quantidade e preço
    $('#tableBody').on('input', '.quantity-input, .price-input', function() {
        const $row = $(this).closest('tr');
        const quantity = parseFloat($row.find('.quantity-input').val()) || 0;
        const price = parseFloat($row.find('.price-input').val()) || 0;
        $row.find('.subtotal-input').val((quantity * price).toFixed(2));
        calculateQuoteTotal();
    });
    
    // Configurar evento para remover linha
    $('#tableBody').on('click', '.remove-item', function() {
        if ($('#tableBody tr').length > 1) {
            $(this).closest('tr').remove();
            calculateQuoteTotal();
        }
    });
}

// Calcular total do orçamento
function calculateQuoteTotal() {
    let total = 0;
    $('.subtotal-input').each(function() {
        total += parseFloat($(this).val()) || 0;
    });
    
    const discount = parseFloat($('[name="discount"]').val()) || 0;
    total = total * (1 - discount / 100);
    
    $('#quote-total-value').val(total.toFixed(2));
}

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar os dropdowns do Semantic UI
    $('.ui.dropdown').dropdown();
    
    // Inicializar as tabs
    $('.menu .item').tab();
    
    // Configurar modais
    $('#add-project-btn').on('click', function() {
        $('#add-project-modal').modal('show');
    });
    
    $('#add-contact-btn').on('click', function() {
        $('#add-contact-modal').modal('show');
    });
    
    $('#add-maintenance-btn').on('click', function() {
        $('#add-maintenance-modal').modal('show');
    });
    
    $('#add-service-btn').on('click', function() {
        $('#add-service-modal').modal('show');
    });
    
    $('#add-quote-btn').on('click', function() {
        $('#add-quote-modal').modal('show');
    });
    
    // Configurar evento de desconto
    $('[name="discount"]').on('input', calculateQuoteTotal);
    
    // Carregar dados da API, com fallback para dados mockados
    loadLandscapingDataFromAPI().catch(error => {
        console.error('Erro ao carregar dados da API, usando dados mockados:', error);
    });
    
    // Configurar eventos iniciais
    setupQuoteItemEvents();
});

// Dados de exemplo para serviços
const mockServices = [
    {
        id: 1,
        service_name: 'Projeto Paisagístico Completo',
        category: 'Projeto',
        description: 'Elaboração de projeto paisagístico completo incluindo plantas, especificações e orçamento.',
        base_price: 2500.00,
        average_duration: 40,
        status: 'Ativo',
        image_url: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
    },
    {
        id: 2,
        service_name: 'Instalação de Jardim',
        category: 'Instalação',
        description: 'Serviço completo de instalação de jardim conforme projeto, incluindo preparação do solo, plantio e acabamento.',
        base_price: 3500.00,
        average_duration: 24,
        status: 'Ativo',
        image_url: 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
    },
    {
        id: 3,
        service_name: 'Manutenção Mensal',
        category: 'Manutenção',
        description: 'Serviço mensal de manutenção de jardins incluindo poda, adubação, controle de pragas e limpeza.',
        base_price: 450.00,
        average_duration: 4,
        status: 'Ativo',
        image_url: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
    }
];

async function loadLandscapingDataFromAPI() {
    try {
        // Buscar projetos de paisagismo
        const projectsResponse = await fetch(`${API_URL}/api/landscaping/project?page=1&page_size=100`, {
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || ''),
                'Accept': 'application/json'
            }
        });
        
        if (!projectsResponse.ok) {
            throw new Error(`Erro ao buscar projetos: ${projectsResponse.status}`);
        }
        
        const projectsData = await projectsResponse.json();
        const projects = projectsData.items || [];

        // Buscar fornecedores de paisagismo
        const suppliersResponse = await fetch(`${API_URL}/api/landscaping/supplier?page=1&page_size=100`, {
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || ''),
                'Accept': 'application/json'
            }
        });
        
        if (!suppliersResponse.ok) {
            throw new Error(`Erro ao buscar fornecedores: ${suppliersResponse.status}`);
        }
        
        const suppliersData = await suppliersResponse.json();
        const suppliers = suppliersData.items || [];

        // Atualizar estatísticas
        $('#total-projects').text(projects.length);
        $('#active-projects').text(projects.filter(p => p.status === 'Em Andamento' || p.status === 'Em Planejamento').length);

        // Preencher grid de projetos
        const projectsGrid = $('#projects-grid');
        projectsGrid.empty();
        projects.forEach(project => {
            const budgetValue = Number(project.budget) || 0;
            const budgetFormatted = budgetValue.toFixed(2);
            
            projectsGrid.append(`
                <div class="ui card project-card">
                    <div class="content">
                        <a class="header">${project.name}</a>
                        <div class="meta">
                            <span class="date">${project.start_date ? formatDate(project.start_date) : ''}</span>
                        </div>
                        <div class="description">
                            ${project.description || ''}
                        </div>
                    </div>
                    <div class="extra content">
                        <span>
                            <i class="leaf icon"></i>
                            ${project.status}
                        </span>
                        <span class="right floated">
                            ${project.area_m2 || ''} m²
                        </span>
                    </div>
                    <div class="ui bottom attached buttons">
                        <button class="ui primary button">Detalhes</button>
                        <button class="ui green button">Orçar</button>
                    </div>
                </div>
            `);
        });

        // Preencher tabela de fornecedores
        const suppliersTable = $('#landscaping-suppliers-table-body');
        suppliersTable.empty();
        suppliers.forEach(supplier => {
            let statusClass = supplier.status === 'Ativo' ? 'positive' : 'negative';
            suppliersTable.append(`
                <tr class="${statusClass}">
                    <td>${supplier.id}</td>
                    <td>${supplier.name}</td>
                    <td>${supplier.contact_person}</td>
                    <td>${supplier.phone}</td>
                    <td>${supplier.email}</td>
                    <td>${supplier.products}</td>
                    <td>${formatDate(supplier.last_contract)}</td>
                    <td>${supplier.status}</td>
                    <td>
                        <div class="ui mini buttons">
                            <button class="ui blue button"><i class="edit icon"></i></button>
                            <button class="ui green button"><i class="eye icon"></i></button>
                            <button class="ui red button"><i class="trash icon"></i></button>
                        </div>
                    </td>
                </tr>
            `);
        });
        
        return { projects, suppliers };
    } catch (error) {
        console.error('Erro ao carregar dados da API:', error);
        throw error;
    }
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Carregar dados dos clientes quando a aba de contatos for selecionada
$('.menu .item[data-tab="contacts"]').on('click', function() {
    loadClients();
});

// Carregar dados dos orçamentos quando a aba de orçamentos for selecionada
$('.menu .item[data-tab="quotes"]').on('click', function() {
    loadQuotes();
});

// Função para carregar os serviços
function loadServices() {
    $.ajax({
        url: 'http://localhost:8000/api/landscaping/service',
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            // Limpar os cards e a tabela
            $('#services-cards').empty();
            const tbody = $('#services-table-body');
            tbody.empty();
            
            if (response && response.items && response.items.length > 0) {
                // Preencher os cards
                response.items.forEach(function(service) {
                    // Adicionar card
                    $('#services-cards').append(`
                        <div class="ui card">
                            <div class="content">
                                <div class="header">${service.service_name}</div>
                                <div class="meta">${service.category}</div>
                                <div class="description">
                                    ${service.description.substring(0, 100)}${service.description.length > 100 ? '...' : ''}
                                </div>
                            </div>
                            <div class="extra content">
                                <span class="left floated">
                                    <i class="clock outline icon"></i>
                                    ${service.average_duration} horas
                                </span>
                                <span class="right floated">
                                    R$ ${parseFloat(service.base_price).toFixed(2)}
                                </span>
                            </div>
                            <div class="ui bottom attached buttons">
                                <button class="ui blue button" onclick="viewService(${service.id})"><i class="eye icon"></i> Ver</button>
                                <button class="ui green button" onclick="editService(${service.id})"><i class="edit icon"></i> Editar</button>
                                <button class="ui red button" onclick="inactivateService(${service.id})"><i class="trash icon"></i> Inativar</button>
                            </div>
                        </div>
                    `);
                    
                    // Adicionar linha na tabela
                    let statusClass = service.status === 'Ativo' ? 'positive' : 'negative';
                    tbody.append(`
                        <tr class="${statusClass}">
                            <td>${service.id}</td>
                            <td>${service.service_name}</td>
                            <td>${service.category}</td>
                            <td>${service.description.substring(0, 50)}${service.description.length > 50 ? '...' : ''}</td>
                            <td>${service.average_duration} horas</td>
                            <td>R$ ${parseFloat(service.base_price).toFixed(2)}</td>
                            <td>${service.status}</td>
                            <td>
                                <div class="ui mini buttons">
                                    <button class="ui blue button" onclick="viewService(${service.id})"><i class="eye icon"></i></button>
                                    <button class="ui green button" onclick="editService(${service.id})"><i class="edit icon"></i></button>
                                    <button class="ui red button" onclick="inactivateService(${service.id})"><i class="trash icon"></i></button>
                                </div>
                            </td>
                        </tr>
                    `);
                });
            } else {
                tbody.append('<tr><td colspan="8" class="center aligned">Nenhum serviço encontrado</td></tr>');
            }
        },
        error: function(error) {
            console.error('Erro ao carregar serviços:', error);
            $('#services-table-body').html('<tr><td colspan="8" class="center aligned error">Erro ao carregar serviços</td></tr>');
        }
    });
}

// Carregar clientes para o dropdown de clientes
function loadClientsForQuotes() {
    $.ajax({
        url: `${API_URL}/api/landscaping/client`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            const clientSelect = $('#quote-client-filter, [name="client_id"]');
            clientSelect.empty();
            clientSelect.append('<option value="">Selecione</option>');
            
            if (response && response.items && response.items.length > 0) {
                response.items.forEach(function(client) {
                    clientSelect.append(`<option value="${client.id}">${client.client_name}</option>`);
                });
            }
            
            // Reinicializar dropdowns
            $('.ui.dropdown').dropdown('refresh');
        },
        error: function(error) {
            console.error('Erro ao carregar clientes:', error);
        }
    });
}

// Inicializar a página
$(document).ready(function() {
    // Carregar serviços e clientes quando o modal de orçamento for aberto
    $('#add-quote-btn').on('click', function() {
        // Limpar o formulário
        $('#add-quote-form')[0].reset();
        
        // Restaurar o título padrão do modal
        $('#add-quote-modal .header').text('Novo Orçamento');
        
        // Restaurar o comportamento padrão do botão de salvar
        $('#save-quote-btn').off('click').on('click', function() {
            // Obter dados do formulário
            const clientId = $('#add-quote-form select[name="client_id"]').val();
            const validUntil = $('#add-quote-form input[name="valid_until"]').val();
            const description = $('#add-quote-form textarea[name="description"]').val();
            const notes = $('#add-quote-form textarea[name="notes"]').val() || '';
            const totalValue = parseFloat($('#quote-total-value').val()) || 0;
            const discount = parseFloat($('#add-quote-form input[name="discount"]').val()) || 0;
            
            // Validar campos obrigatórios
            if (!clientId || !validUntil || !description || totalValue <= 0) {
                alert('Por favor, preencha todos os campos obrigatórios e adicione pelo menos um item ao orçamento.');
                return;
            }
            
            // Coletar itens do orçamento da tabela
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
            
            // Preparar dados para envio
            const quoteData = {
                user_id: 1, // Usando user_id fixo para teste
                client_id: parseInt(clientId), // Usar o ID do cliente
                description: description,
                created_at: new Date().toISOString().split('T')[0], // Usar created_at em vez de created_date
                valid_until: validUntil,
                total_value: totalValue,
                notes: notes,
                status: 'Pendente',
                items: items // Incluir os itens do orçamento
            };
            
            console.log('Enviando orçamento:', quoteData);
            
            $.ajax({
                url: `${API_URL}/api/landscaping/quote`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(quoteData),
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                },
                success: function(response) {
                    alert('Orçamento criado com sucesso!');
                    $('#add-quote-modal').modal('hide');
                    $('#add-quote-form')[0].reset();
                    loadQuotes();
                },
                error: function(xhr, status, error) {
                    console.error('Erro ao criar orçamento:', error);
                    console.error('Status:', status);
                    console.error('Resposta:', xhr.responseText);
                    alert('Erro ao criar orçamento: ' + (xhr.responseText || error));
                }
            });
        });
        
        // Carregar serviços e clientes
        loadServices();
        loadClientsForQuotes();
        
        // Limpar todas as linhas da tabela
        $('#tableBody').empty();
        
        // Resetar o total geral
        $('#grandTotal').val('0.00');
        $('#quote-total-value').val('0.00');
        
        // Adicionar uma linha inicial à tabela
        const initialRowHtml = `
            <tr>
                <td>
                    <div class="ui selection dropdown service-select">
                        <input type="hidden" name="service_id">
                        <i class="dropdown icon"></i>
                        <div class="default text">Selecione</div>
                        <div class="menu">
                            <!-- Opções serão adicionadas aqui -->
                        </div>
                    </div>
                </td>
                <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
                <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00"></div></td>
                <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
                <td class="center aligned"><button type="button" class="ui icon red mini button remove-item"><i class="trash icon"></i></button></td>
            </tr>
        `;
        
        // Adicionar a linha inicial à tabela
        $('#tableBody').append(initialRowHtml);
        
        // Obter a linha adicionada
        const $firstRow = $('#tableBody tr').first();
        
        // Carregar serviços para o primeiro item
        $.ajax({
            url: `${API_URL}/api/landscaping/service`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                if (response && response.items && response.items.length > 0) {
                    // Limpar o dropdown existente
                    $firstRow.find('.service-select .menu').empty();
                    
                    // Adicionar os serviços ao dropdown
                    response.items.forEach(function(service) {
                        const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                        $firstRow.find('.service-select .menu').append(option);
                    });
                    
                    // Inicializar o dropdown
                    $firstRow.find('.service-select').dropdown({
                        onChange: function(value, text, $selectedItem) {
                            const $dropdown = $(this);
                            const $row = $dropdown.closest('tr');
                            const priceInput = $row.find('.price-input');
                            
                            // Obter o preço do serviço selecionado
                            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
                            priceInput.val(selectedPrice.toFixed(2));
                            
                            // Calcular subtotal
                            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
                            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
                            
                            // Recalcular total
                            calculateQuoteTotal();
                        }
                    });
                }
            }
        });
    });
    
    // Adicionar item ao orçamento
    $('#add-quote-item').on('click', function() {
        // Criar uma nova linha para a tabela
        const newRowHtml = `
            <tr>
                <td>
                    <div class="ui selection dropdown service-select">
                        <input type="hidden" name="service_id">
                        <i class="dropdown icon"></i>
                        <div class="default text">Selecione</div>
                        <div class="menu">
                            <!-- Opções serão adicionadas aqui -->
                        </div>
                    </div>
                </td>
                <td><div class="ui input"><input type="number" class="quantity-input" value="1" min="1"></div></td>
                <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="0.00"></div></td>
                <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="0.00"></div></td>
                <td class="center aligned"><button type="button" class="ui icon red mini button remove-item"><i class="trash icon"></i></button></td>
            </tr>
        `;
        
        // Adicionar a nova linha à tabela
        $('#tableBody').append(newRowHtml);
        
        // Obter a nova linha adicionada
        const $newRow = $('#tableBody tr').last();
        
        // Adicionar os serviços ao dropdown da nova linha
        $.ajax({
            url: `${API_URL}/api/landscaping/service`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                if (response && response.items && response.items.length > 0) {
                    // Adicionar os serviços ao dropdown
                    response.items.forEach(function(service) {
                        const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                        $newRow.find('.service-select .menu').append(option);
                    });
                    
                    // Inicializar o dropdown
                    $newRow.find('.service-select').dropdown({
                        onChange: function(value, text, $selectedItem) {
                            const $dropdown = $(this);
                            const $row = $dropdown.closest('tr');
                            const priceInput = $row.find('.price-input');
                            
                            // Obter o preço do serviço selecionado
                            const selectedPrice = parseFloat($selectedItem.data('price')) || 0;
                            priceInput.val(selectedPrice.toFixed(2));
                            
                            // Calcular subtotal
                            const quantity = parseFloat($row.find('.quantity-input').val()) || 1;
                            $row.find('.subtotal-input').val((quantity * selectedPrice).toFixed(2));
                            
                            // Recalcular total
                            calculateQuoteTotal();
                        }
                    });
                    
                    // Recalcular totais
                    calculateQuoteTotal();
                }
            }
        });
    });
    
    // Carregar orçamentos se a aba estiver ativa inicialmente
    if ($('.menu .item[data-tab="quotes"]').hasClass('active')) {
        loadQuotes();
    }
});