$(document).ready(function() {
    // Inicializar dropdowns e tabs
    $('.ui.dropdown').dropdown();
    $('.menu .item').tab();
    
    // Carregar lista de estufas
    loadGreenhouses();
    
    // Carregar lista de cultivos
    loadFlowers(1);
    
    // Configurar eventos
    $('#btn-filter').on('click', function() {
        loadFlowers(1);
    });
    
    $('#flower-form').on('submit', function(e) {
        e.preventDefault();
        saveFlower();
    });
    
    $('#btn-save-harvest').on('click', function() {
        saveHarvest();
    });
    
    $('#btn-save-treatment').on('click', function() {
        saveTreatment();
    });
    
    $('#btn-add-harvest').on('click', function() {
        const flowerId = $(this).data('flower-id');
        $('#harvest-flower-id').val(flowerId);
        $('#harvest-modal').modal('show');
    });
    
    $('#btn-add-treatment').on('click', function() {
        const flowerId = $(this).data('flower-id');
        $('#treatment-flower-id').val(flowerId);
        $('#treatment-modal').modal('show');
    });
});

// Função para carregar lista de estufas
function loadGreenhouses() {
    $.ajax({
        url: '/api/floriculture/greenhouse',
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            const select = $('#greenhouse-select');
            select.empty();
            select.append('<option value="">Selecione uma estufa</option>');
            
            response.items.forEach(function(greenhouse) {
                select.append(`<option value="${greenhouse.id}">${greenhouse.name}</option>`);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar estufas:', error);
            showMessage('Erro ao carregar estufas', 'error');
            
            // Dados mockados em caso de erro
            const mockData = [
                { id: 1, name: "Estufa Principal" },
                { id: 2, name: "Estufa Secundária" },
                { id: 3, name: "Estufa Experimental" }
            ];
            
            const select = $('#greenhouse-select');
            select.empty();
            select.append('<option value="">Selecione uma estufa</option>');
            
            mockData.forEach(function(greenhouse) {
                select.append(`<option value="${greenhouse.id}">${greenhouse.name}</option>`);
            });
        }
    });
}

// Função para carregar lista de cultivos
function loadFlowers(page) {
    const species = $('#filter-species').val();
    const status = $('#filter-status').val();
    
    $.ajax({
        url: '/api/floriculture/cultivation',
        method: 'GET',
        data: {
            page: page,
            page_size: 10,
            species: species,
            status: status
        },
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            renderFlowersTable(response.items);
            renderPagination(response.page, response.total_pages);
        },
        error: function(error) {
            console.error('Erro ao carregar cultivos:', error);
            showMessage('Erro ao carregar cultivos', 'error');
            
            // Dados mockados em caso de erro
            const mockData = {
                items: [
                    {
                        id: 1,
                        species: "Rosa",
                        variety: "Híbrida de Chá",
                        planting_date: "2024-03-15",
                        quantity: 500,
                        area_m2: 100.0,
                        greenhouse_id: 1,
                        greenhouse_name: "Estufa Principal",
                        expected_harvest_date: "2024-06-15",
                        status: "Em Cultivo",
                        notes: "Crescimento saudável"
                    },
                    {
                        id: 2,
                        species: "Tulipa",
                        variety: "Darwin Híbrida",
                        planting_date: "2024-02-10",
                        quantity: 1000,
                        area_m2: 150.0,
                        greenhouse_id: 2,
                        greenhouse_name: "Estufa Secundária",
                        expected_harvest_date: "2024-05-10",
                        status: "Em Cultivo",
                        notes: "Irrigação diária necessária"
                    }
                ],
                page: 1,
                total_pages: 1
            };
            
            renderFlowersTable(mockData.items);
            renderPagination(mockData.page, mockData.total_pages);
        }
    });
}

// Função para renderizar tabela de cultivos
function renderFlowersTable(flowers) {
    const tbody = $('#flowers-table-body');
    tbody.empty();
    
    if (flowers.length === 0) {
        tbody.append('<tr><td colspan="9" class="center aligned">Nenhum cultivo encontrado</td></tr>');
        return;
    }
    
    flowers.forEach(function(flower) {
        const row = `
            <tr>
                <td>${flower.id}</td>
                <td>${flower.species}</td>
                <td>${flower.variety}</td>
                <td>${formatDate(flower.planting_date)}</td>
                <td>${flower.quantity}</td>
                <td>${flower.area_m2}</td>
                <td>${flower.greenhouse_name || '-'}</td>
                <td>${flower.status}</td>
                <td>
                    <button class="ui mini icon button" onclick="viewFlower(${flower.id})"><i class="eye icon"></i></button>
                    <button class="ui mini icon primary button" onclick="editFlower(${flower.id})"><i class="edit icon"></i></button>
                    <button class="ui mini icon negative button" onclick="deleteFlower(${flower.id})"><i class="trash icon"></i></button>
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// Função para renderizar paginação
function renderPagination(currentPage, totalPages) {
    const pagination = $('#pagination');
    pagination.empty();
    
    if (totalPages <= 1) {
        return;
    }
    
    // Botão anterior
    pagination.append(`
        <a class="item ${currentPage === 1 ? 'disabled' : ''}" 
           onclick="${currentPage > 1 ? 'loadFlowers(' + (currentPage - 1) + ')' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    // Páginas
    for (let i = 1; i <= totalPages; i++) {
        pagination.append(`
            <a class="item ${i === currentPage ? 'active' : ''}" 
               onclick="loadFlowers(${i})">
                ${i}
            </a>
        `);
    }
    
    // Botão próximo
    pagination.append(`
        <a class="item ${currentPage === totalPages ? 'disabled' : ''}" 
           onclick="${currentPage < totalPages ? 'loadFlowers(' + (currentPage + 1) + ')' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
}

// Função para visualizar detalhes de um cultivo
function viewFlower(id) {
    $.ajax({
        url: `/api/floriculture/cultivation/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(flower) {
            // Preencher detalhes do cultivo
            $('#detail-species').val(flower.species);
            $('#detail-variety').val(flower.variety);
            $('#detail-planting-date').val(formatDate(flower.planting_date));
            $('#detail-quantity').val(flower.quantity);
            $('#detail-area').val(flower.area_m2);
            $('#detail-greenhouse').val(flower.greenhouse_name || '-');
            $('#detail-harvest-date').val(flower.expected_harvest_date ? formatDate(flower.expected_harvest_date) : '-');
            $('#detail-status').val(flower.status);
            $('#detail-notes').val(flower.notes || '');
            
            // Configurar IDs para os botões
            $('#btn-edit-flower').data('flower-id', id);
            $('#btn-add-harvest').data('flower-id', id);
            $('#btn-add-treatment').data('flower-id', id);
            
            // Carregar registros de colheita
            loadHarvestRecords(id);
            
            // Carregar registros de tratamento
            loadTreatmentRecords(id);
            
            // Exibir modal
            $('#flower-detail-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao carregar detalhes do cultivo:', error);
            showMessage('Erro ao carregar detalhes do cultivo', 'error');
        }
    });
}

// Função para carregar registros de colheita
function loadHarvestRecords(flowerId) {
    $.ajax({
        url: `/api/floriculture/endpoints/harvest/${flowerId}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            const tbody = $('#harvest-records-body');
            tbody.empty();
            
            if (response.items.length === 0) {
                tbody.append('<tr><td colspan="4" class="center aligned">Nenhum registro de colheita encontrado</td></tr>');
                return;
            }
            
            response.items.forEach(function(record) {
                const row = `
                    <tr>
                        <td>${formatDate(record.harvest_date)}</td>
                        <td>${record.quantity}</td>
                        <td>${record.quality_grade}</td>
                        <td>${record.notes || '-'}</td>
                    </tr>
                `;
                tbody.append(row);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar registros de colheita:', error);
            $('#harvest-records-body').html('<tr><td colspan="4" class="center aligned">Erro ao carregar registros</td></tr>');
        }
    });
}

// Função para carregar registros de tratamento
function loadTreatmentRecords(flowerId) {
    $.ajax({
        url: `/api/floriculture/endpoints/treatment/${flowerId}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            const tbody = $('#treatment-records-body');
            tbody.empty();
            
            if (response.items.length === 0) {
                tbody.append('<tr><td colspan="5" class="center aligned">Nenhum registro de tratamento encontrado</td></tr>');
                return;
            }
            
            response.items.forEach(function(record) {
                const row = `
                    <tr>
                        <td>${formatDate(record.treatment_date)}</td>
                        <td>${record.treatment_type}</td>
                        <td>${record.product_used}</td>
                        <td>${record.quantity} ${record.unit}</td>
                        <td>${record.notes || '-'}</td>
                    </tr>
                `;
                tbody.append(row);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar registros de tratamento:', error);
            $('#treatment-records-body').html('<tr><td colspan="5" class="center aligned">Erro ao carregar registros</td></tr>');
        }
    });
}

// Função para salvar cultivo
function saveFlower() {
    const formData = {};
    $('#flower-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.quantity = parseInt(formData.quantity);
    formData.area_m2 = parseFloat(formData.area_m2);
    if (formData.greenhouse_id === '') {
        formData.greenhouse_id = null;
    } else {
        formData.greenhouse_id = parseInt(formData.greenhouse_id);
    }
    
    $.ajax({
        url: '/api/floriculture/endpoints/flowers',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            showMessage('Cultivo salvo com sucesso', 'success');
            $('#flower-form')[0].reset();
            $('.menu .item[data-tab="list"]').tab('change tab', 'list');
            loadFlowers(1);
        },
        error: function(error) {
            console.error('Erro ao salvar cultivo:', error);
            showMessage('Erro ao salvar cultivo', 'error');
        }
    });
}

// Função para editar cultivo
function editFlower(id) {
    $.ajax({
        url: `/api/floriculture/endpoints/flowers/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(flower) {
            // Preencher formulário
            $('#flower-form')[0].reset();
            $('#flower-form [name="species"]').val(flower.species);
            $('#flower-form [name="variety"]').val(flower.variety);
            $('#flower-form [name="planting_date"]').val(formatDateForInput(flower.planting_date));
            $('#flower-form [name="quantity"]').val(flower.quantity);
            $('#flower-form [name="area_m2"]').val(flower.area_m2);
            $('#flower-form [name="greenhouse_id"]').val(flower.greenhouse_id).trigger('change');
            if (flower.expected_harvest_date) {
                $('#flower-form [name="expected_harvest_date"]').val(formatDateForInput(flower.expected_harvest_date));
            }
            $('#flower-form [name="status"]').val(flower.status).trigger('change');
            $('#flower-form [name="notes"]').val(flower.notes || '');
            
            // Mudar para a aba de edição
            $('.menu .item[data-tab="new"]').tab('change tab', 'new');
            
            // Configurar formulário para edição
            $('#flower-form').data('edit-id', id);
            $('#flower-form').off('submit').on('submit', function(e) {
                e.preventDefault();
                updateFlower(id);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar cultivo para edição:', error);
            showMessage('Erro ao carregar cultivo para edição', 'error');
        }
    });
}

// Função para atualizar cultivo
function updateFlower(id) {
    const formData = {};
    $('#flower-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.quantity = parseInt(formData.quantity);
    formData.area_m2 = parseFloat(formData.area_m2);
    if (formData.greenhouse_id === '') {
        formData.greenhouse_id = null;
    } else {
        formData.greenhouse_id = parseInt(formData.greenhouse_id);
    }
    
    $.ajax({
        url: `/api/floriculture/endpoints/flowers/${id}`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            showMessage('Cultivo atualizado com sucesso', 'success');
            $('#flower-form')[0].reset();
            $('#flower-form').removeData('edit-id');
            $('#flower-form').off('submit').on('submit', function(e) {
                e.preventDefault();
                saveFlower();
            });
            $('.menu .item[data-tab="list"]').tab('change tab', 'list');
            loadFlowers(1);
        },
        error: function(error) {
            console.error('Erro ao atualizar cultivo:', error);
            showMessage('Erro ao atualizar cultivo', 'error');
        }
    });
}

// Função para excluir cultivo
function deleteFlower(id) {
    if (confirm('Tem certeza que deseja excluir este cultivo?')) {
        $.ajax({
            url: `/api/floriculture/endpoints/flowers/${id}`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            success: function(response) {
                showMessage('Cultivo excluído com sucesso', 'success');
                loadFlowers(1);
            },
            error: function(error) {
                console.error('Erro ao excluir cultivo:', error);
                showMessage('Erro ao excluir cultivo', 'error');
            }
        });
    }
}

// Função para salvar registro de colheita
function saveHarvest() {
    const formData = {};
    $('#harvest-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.flower_id = parseInt(formData.flower_id);
    formData.quantity = parseInt(formData.quantity);
    
    $.ajax({
        url: '/api/floriculture/endpoints/harvest',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            showMessage('Colheita registrada com sucesso', 'success');
            $('#harvest-modal').modal('hide');
            $('#harvest-form')[0].reset();
            
            // Recarregar registros de colheita
            loadHarvestRecords(formData.flower_id);
        },
        error: function(error) {
            console.error('Erro ao registrar colheita:', error);
            showMessage('Erro ao registrar colheita', 'error');
        }
    });
}

// Função para salvar registro de tratamento
function saveTreatment() {
    const formData = {};
    $('#treatment-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.flower_id = parseInt(formData.flower_id);
    formData.quantity = parseFloat(formData.quantity);
    
    $.ajax({
        url: '/api/floriculture/endpoints/treatment',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        success: function(response) {
            showMessage('Tratamento registrado com sucesso', 'success');
            $('#treatment-modal').modal('hide');
            $('#treatment-form')[0].reset();
            
            // Recarregar registros de tratamento
            loadTreatmentRecords(formData.flower_id);
        },
        error: function(error) {
            console.error('Erro ao registrar tratamento:', error);
            showMessage('Erro ao registrar tratamento', 'error');
        }
    });
}

// Função para formatar data
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para formatar data para input
function formatDateForInput(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// Função para obter token de autenticação
function getToken() {
    // Em um ambiente real, você obteria o token do localStorage ou sessionStorage
    return localStorage.getItem('token') || 'dummy_token_for_development';
}

// Função para exibir mensagem
function showMessage(message, type) {
    const color = type === 'success' ? 'green' : 'red';
    const icon = type === 'success' ? 'check circle' : 'exclamation triangle';
    
    $('body').append(`
        <div class="ui ${color} message" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
            <i class="${icon} icon"></i>
            <div class="content">
                <div class="header">${message}</div>
            </div>
        </div>
    `);
    
    setTimeout(function() {
        $('.ui.message').fadeOut(function() {
            $(this).remove();
        });
    }, 3000);
}