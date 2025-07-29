// Carregar dados dos clientes quando a aba de contatos for selecionada
$('.menu .item[data-tab="contacts"]').on('click', function() {
    loadClients();
});

// Configurar evento para mudança de quantidade por página
$(document).on('change', '#contacts-page-size', function() {
    loadClients(1, $(this).val());
});

// Função para carregar os clientes
function loadClients(page = 1, pageSize = null) {
    const currentPageSize = pageSize || $('#contacts-page-size').val() || 10;
    
    $.ajax({
        url: `${API_URL}/api/landscaping/client?page=${page}&page_size=${currentPageSize}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            const tbody = $('#contacts-table-body');
            tbody.empty();
            
            if (response && response.items && response.items.length > 0) {
                response.items.forEach(function(client) {
                    let statusClass = '';
                    if (client.status === 'Ativo') statusClass = 'positive';
                    else if (client.status === 'Inativo') statusClass = 'negative';
                    else if (client.status === 'Lead') statusClass = 'warning';
                    
                    const address = client.address || '';
                    const cityState = client.city && client.state ? `${client.city} - ${client.state}` : (client.city || client.state || '');
                    const lastContact = client.updated_at ? formatDate(client.updated_at) : '-';
                    
                    let avatarImg;
                    if (client.img_profile && client.img_profile.trim() !== '') {
                        avatarImg = `<img src="${client.img_profile}" class="contact-avatar" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(client.client_name)}&background=random'">`;
                    } else {
                        avatarImg = `<img src="https://ui-avatars.com/api/?name=${encodeURIComponent(client.client_name)}&background=random" class="contact-avatar">`;
                    }
                    
                    tbody.append(`
                        <tr class="${statusClass}">
                            <td>${avatarImg}</td>
                            <td>${client.client_name}</td>
                            <td>${client.industry || '-'}</td>
                            <td>${client.phone_number || '-'}</td>
                            <td>${address}</td>
                            <td>${cityState}</td>
                            <td>${client.status}</td>
                            <td>${lastContact}</td>
                            <td>
                                <div class="ui mini buttons">
                                    <button class="ui blue button" onclick="viewClient(${client.id})"><i class="eye icon"></i></button>
                                    <button class="ui green button" onclick="editClient(${client.id})"><i class="edit icon"></i></button>
                                    <button class="ui red button" onclick="deleteClient(${client.id})"><i class="trash icon"></i></button>
                                </div>
                            </td>
                        </tr>
                    `);
                });
                
                renderContactsPagination(response.page, response.total_pages, response.total_items, currentPageSize);
            } else {
                tbody.append('<tr><td colspan="10" class="center aligned">Nenhum cliente encontrado</td></tr>');
                $('#contacts-pagination').empty();
            }
        },
        error: function(error) {
            console.error('Erro ao carregar clientes:', error);
            $('#contacts-table-body').html('<tr><td colspan="10" class="center aligned error">Erro ao carregar clientes</td></tr>');
        }
    });
}

function loadClientsPage(page) {
    loadClients(page);
}

function renderContactsPagination(currentPage, totalPages, totalItems, pageSize) {
    const pagination = $('#contacts-pagination');
    pagination.empty();
    
    if (totalPages <= 1) {
        return;
    }
    
    const prevDisabled = currentPage === 1 ? 'disabled' : '';
    pagination.append(`
        <a class="item ${prevDisabled}" onclick="${currentPage > 1 ? 'loadClientsPage(' + (currentPage - 1) + ')' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        pagination.append('<a class="item" onclick="loadClientsPage(1)">1</a>');
        if (startPage > 2) {
            pagination.append('<div class="disabled item">...</div>');
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? 'active' : '';
        pagination.append(`
            <a class="item ${activeClass}" onclick="loadClientsPage(${i})">
                ${i}
            </a>
        `);
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            pagination.append('<div class="disabled item">...</div>');
        }
        pagination.append(`<a class="item" onclick="loadClientsPage(${totalPages})">${totalPages}</a>`);
    }
    
    const nextDisabled = currentPage === totalPages ? 'disabled' : '';
    pagination.append(`
        <a class="item ${nextDisabled}" onclick="${currentPage < totalPages ? 'loadClientsPage(' + (currentPage + 1) + ')' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
    
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = Math.min(currentPage * pageSize, totalItems);
    $('#contacts-pagination-info').html(`
        Mostrando ${startItem} a ${endItem} de ${totalItems} contatos
    `);
}

function viewClient(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/client/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(client) {
            $('body').append(`
                <div class="ui modal" id="view-client-modal">
                    <i class="close icon"></i>
                    <div class="header">${client.client_name}</div>
                    <div class="content">
                        <div class="ui form">
                            <div class="two fields">
                                <div class="field">
                                    <label>Nome</label>
                                    <p>${client.client_name}</p>
                                </div>
                                <div class="field">
                                    <label>Pessoa de Contato</label>
                                    <p>${client.contact_person || '-'}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Email</label>
                                    <p>${client.email || '-'}</p>
                                </div>
                                <div class="field">
                                    <label>Telefone</label>
                                    <p>${client.phone_number || '-'}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Endereço</label>
                                    <p>${client.address || '-'}</p>
                                </div>
                                <div class="field">
                                    <label>Cidade/Estado</label>
                                    <p>${client.city && client.state ? client.city + ' - ' + client.state : (client.city || client.state || '-')}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Tipo</label>
                                    <p>${client.client_type || '-'}</p>
                                </div>
                                <div class="field">
                                    <label>Setor</label>
                                    <p>${client.industry || '-'}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Status</label>
                                    <p>${client.status}</p>
                                </div>
                                <div class="field">
                                    <label>CEP</label>
                                    <p>${client.zip_code || '-'}</p>
                                </div>
                            </div>
                            <div class="field">
                                <label>Observações</label>
                                <p>${client.notes || '-'}</p>
                            </div>
                        </div>
                    </div>
                    <div class="actions">
                        <div class="ui button" onclick="$('#view-client-modal').modal('hide')">Fechar</div>
                    </div>
                </div>
            `);
            $('#view-client-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do cliente:', error);
            alert('Erro ao obter detalhes do cliente');
        }
    });
}

function editClient(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/client/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(client) {
            $('#add-contact-form [name="name"]').val(client.client_name);
            $('#add-contact-form [name="contact_person"]').val(client.contact_person || '');
            $('#add-contact-form [name="email"]').val(client.email || '');
            $('#add-contact-form [name="phone"]').val(client.phone_number || '');
            $('#add-contact-form [name="address"]').val(client.address || '');
            $('#add-contact-form [name="city"]').val(client.city || '');
            $('#add-contact-form [name="state"]').val(client.state || '');
            $('#add-contact-form [name="zip_code"]').val(client.zip_code || '');
            $('#add-contact-form [name="type"]').val(client.client_type || '').trigger('change');
            $('#add-contact-form [name="industry"]').val(client.industry || '');
            $('#add-contact-form [name="status"]').val(client.status).trigger('change');
            $('#add-contact-form [name="notes"]').val(client.notes || '');
            
            $('.ui.dropdown').dropdown('refresh');
            $('#add-contact-modal .header').text('Editar Contato');
            
            $('#save-contact-btn').off('click').on('click', function() {
                updateClient(id);
            });
            
            $('#add-contact-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do cliente:', error);
            alert('Erro ao obter detalhes do cliente');
        }
    });
}

function updateClient(id) {
    const formData = {};
    $('#add-contact-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    const clientData = {
        client_name: formData.name,
        contact_person: formData.contact_person,
        email: formData.email,
        phone_number: formData.phone,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        zip_code: formData.zip_code,
        client_type: formData.type,
        industry: formData.industry,
        status: formData.status,
        notes: formData.notes
    };
    
    $.ajax({
        url: `${API_URL}/api/landscaping/client/${id}?user_id=1`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(clientData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            alert('Cliente atualizado com sucesso!');
            $('#add-contact-modal').modal('hide');
            $('#add-contact-form')[0].reset();
            $('#add-contact-modal .header').text('Novo Contato');
            $('#save-contact-btn').off('click').on('click', function() {
                saveClient();
            });
            loadClients();
        },
        error: function(error) {
            console.error('Erro ao atualizar cliente:', error);
            alert('Erro ao atualizar cliente');
        }
    });
}

function deleteClient(id) {
    if (confirm('Tem certeza que deseja inativar este cliente?')) {
        $.ajax({
            url: `${API_URL}/api/landscaping/client/${id}?user_id=1`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                alert('Cliente inativado com sucesso!');
                loadClients();
            },
            error: function(error) {
                console.error('Erro ao inativar cliente:', error);
                alert('Erro ao inativar cliente');
            }
        });
    }
}

function saveClient() {
    const formData = {};
    $('#add-contact-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    const clientData = {
        user_id: 1,
        client_name: formData.name,
        contact_person: formData.contact_person,
        email: formData.email,
        phone_number: formData.phone,
        address: formData.address,
        city: formData.city,
        state: formData.state,
        zip_code: formData.zip_code,
        client_type: formData.type,
        industry: formData.industry,
        status: formData.status,
        notes: formData.notes
    };
    
    $.ajax({
        url: `${API_URL}/api/landscaping/client`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(clientData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            alert('Cliente criado com sucesso!');
            $('#add-contact-modal').modal('hide');
            $('#add-contact-form')[0].reset();
            loadClients();
        },
        error: function(error) {
            console.error('Erro ao criar cliente:', error);
            alert('Erro ao criar cliente');
        }
    });
}

// Configurar o botão de salvar contato
$('#save-contact-btn').on('click', function() {
    saveClient();
});