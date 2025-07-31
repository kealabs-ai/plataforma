// Carregar dados dos serviços quando a aba de serviços for selecionada
$('.menu .item[data-tab="services"]').on('click', function() {
    loadServices();
});

// Configurar evento para mudança de quantidade por página de serviços
$(document).on('change', '#services-page-size', function() {
    loadServices(1, $(this).val());
});

// Função para carregar os serviços
function loadServices(page = 1, pageSize = null) {
    const currentPageSize = pageSize || $('#services-page-size').val() || 10;
    
    $.ajax({
        url: `${API_URL}/api/landscaping/service?page=${page}&page_size=${currentPageSize}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            const tbody = $('#services-table-body');
            tbody.empty();
            
            if (response && response.items && response.items.length > 0) {
                response.items.forEach(function(service) {
                    let statusClass = service.status === 'Ativo' ? 'positive' : 'negative';
                    tbody.append(`
                        <tr class="${statusClass}">
                            <td>${service.id}</td>
                            <td>${service.service_name}</td>
                            <td>${service.category}</td>
                            <td>${service.description.substring(0, 50)}${service.description.length > 50 ? '...' : ''}</td>
                            <td>${service.average_duration} horas</td>
                            <td>${formatCurrency(service.base_price)}</td>
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
                
                renderServicesPagination(response.page, response.total_pages, response.total_items, currentPageSize);
            } else {
                tbody.append('<tr><td colspan="8" class="center aligned">Nenhum serviço encontrado</td></tr>');
                $('#services-pagination').empty();
            }
        },
        error: function(error) {
            console.error('Erro ao carregar serviços:', error);
            $('#services-table-body').html('<tr><td colspan="8" class="center aligned error">Erro ao carregar serviços</td></tr>');
        }
    });
}

function loadServicesPage(page) {
    loadServices(page);
}

function renderServicesPagination(currentPage, totalPages, totalItems, pageSize) {
    const pagination = $('#services-pagination');
    pagination.empty();
    
    if (totalPages <= 1) {
        return;
    }
    
    const prevDisabled = currentPage === 1 ? 'disabled' : '';
    pagination.append(`
        <a class="item ${prevDisabled}" onclick="${currentPage > 1 ? 'loadServicesPage(' + (currentPage - 1) + ')' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        pagination.append('<a class="item" onclick="loadServicesPage(1)">1</a>');
        if (startPage > 2) {
            pagination.append('<div class="disabled item">...</div>');
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        pagination.append(`
            <a class="item ${activeClass}" onclick="loadServicesPage(${i})">
                ${i}
            </a>
        `);
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagination.append('<div class="disabled item">...</div>');
        }
        pagination.append(`<a class="item" onclick="loadServicesPage(${totalPages})">${totalPages}</a>`);
    }
    
    const nextDisabled = currentPage === totalPages ? 'disabled' : '';
    pagination.append(`
        <a class="item ${nextDisabled}" onclick="${currentPage < totalPages ? 'loadServicesPage(' + (currentPage + 1) + ')' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
    
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = Math.min(currentPage * pageSize, totalItems);
    $('#services-pagination-info').html(`
        Mostrando ${startItem} a ${endItem} de ${totalItems} serviços
    `);
}

function viewService(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/service/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(service) {
            $('body').append(`
                <div class="ui modal" id="view-service-modal">
                    <i class="close icon"></i>
                    <div class="header">${service.service_name}</div>
                    <div class="content">
                        <div class="ui form">
                            <div class="two fields">
                                <div class="field">
                                    <label>Categoria</label>
                                    <p>${service.category}</p>
                                </div>
                                <div class="field">
                                    <label>Status</label>
                                    <p>${service.status}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Duração Média</label>
                                    <p>${service.average_duration} horas</p>
                                </div>
                                <div class="field">
                                    <label>Preço Base</label>
                                    <p>${formatCurrency(service.base_price)}</p>
                                </div>
                            </div>
                            <div class="field">
                                <label>Descrição</label>
                                <p>${service.description}</p>
                            </div>
                        </div>
                    </div>
                    <div class="actions">
                        <div class="ui button" onclick="$('#view-service-modal').modal('hide')">Fechar</div>
                    </div>
                </div>
            `);
            $('#view-service-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do serviço:', error);
            alert('Erro ao obter detalhes do serviço');
        }
    });
}

function editService(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/service/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(service) {
            $('#add-service-form [name="service_name"]').val(service.service_name);
            $('#add-service-form [name="category"]').val(service.category);
            $('#add-service-form [name="description"]').val(service.description);
            $('#add-service-form [name="average_duration"]').val(service.average_duration);
            $('#add-service-form [name="base_price"]').val(service.base_price);
            $('#add-service-form [name="status"]').val(service.status);
            
            $('.ui.dropdown').dropdown('refresh');
            $('#add-service-modal .header').text('Editar Serviço');
            
            $('#save-service-btn').off('click').on('click', function() {
                updateService(id);
            });
            
            $('#add-service-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do serviço:', error);
            alert('Erro ao obter detalhes do serviço');
        }
    });
}

function updateService(id) {
    const formData = {};
    $('#add-service-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    $.ajax({
        url: `${API_URL}/api/landscaping/service/${id}?user_id=1`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            alert('Serviço atualizado com sucesso!');
            $('#add-service-modal').modal('hide');
            $('#add-service-form')[0].reset();
            $('#add-service-modal .header').text('Novo Serviço');
            $('#save-service-btn').off('click').on('click', function() {
                saveService();
            });
            loadServices();
        },
        error: function(error) {
            console.error('Erro ao atualizar serviço:', error);
            alert('Erro ao atualizar serviço');
        }
    });
}

function inactivateService(id) {
    if (confirm('Tem certeza que deseja inativar este serviço?')) {
        $.ajax({
            url: `${API_URL}/api/landscaping/service/${id}?user_id=1`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                alert('Serviço inativado com sucesso!');
                loadServices();
            },
            error: function(error) {
                console.error('Erro ao inativar serviço:', error);
                alert('Erro ao inativar serviço');
            }
        });
    }
}

function saveService() {
    const formData = {};
    $('#add-service-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    formData.user_id = 1;
    
    $.ajax({
        url: `${API_URL}/api/landscaping/service`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            alert('Serviço criado com sucesso!');
            $('#add-service-modal').modal('hide');
            $('#add-service-form')[0].reset();
            loadServices();
        },
        error: function(error) {
            console.error('Erro ao criar serviço:', error);
            alert('Erro ao criar serviço');
        }
    });
}

// Configurar o botão de salvar serviço
$('#save-service-btn').on('click', function() {
    saveService();
});