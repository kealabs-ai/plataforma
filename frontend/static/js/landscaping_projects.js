// Carregar dados dos projetos quando a aba de projetos for selecionada
$('.menu .item[data-tab="projects"]').on('click', function() {
    loadProjects();
});

// Função para carregar os projetos
function loadProjects() {
    $.ajax({
        url: `${API_URL}/api/landscaping/project`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            $('#planning-column-project').empty();
            $('#in-progress-column-project').empty();
            $('#review-column-project').empty();
            $('#completed-column-project').empty();
            
            const tbody = $('#projects-table-body');
            tbody.empty();
            
            if (response && response.items && response.items.length > 0) {
                response.items.forEach(function(project) {
                    const projectCard = `
                        <div class="ui card kanban-card-project" data-id="${project.id}">
                            <div class="content">
                                <div class="header">${project.name}</div>
                                <div class="meta">${project.client_name}</div>
                                <div class="description">
                                    ${project.description ? project.description.substring(0, 100) + (project.description.length > 100 ? '...' : '') : 'Sem descrição'}
                                </div>
                            </div>
                            <div class="extra content">
                                <div class="ui mini fluid selection dropdown status-dropdown-project">
                                    <input type="hidden" name="status" value="${project.status}">
                                    <i class="dropdown icon"></i>
                                    <div class="text">${project.status || 'Alterar status'}</div>
                                    <div class="menu">
                                        <div class="item" data-value="Planejamento">Planejamento</div>
                                        <div class="item" data-value="Em Andamento">Em Andamento</div>
                                        <div class="item" data-value="Revisão">Revisão</div>
                                        <div class="item" data-value="Concluído">Concluído</div>
                                    </div>
                                </div>
                            </div>
                            <div class="extra content">
                                <span>
                                    <i class="calendar icon"></i>
                                    ${formatDate(project.start_date)}
                                </span>
                                <span class="right floated">
                                    <i class="dollar sign icon"></i>
                                    ${project.budget ? 'R$ ' + parseFloat(project.budget).toFixed(2) : 'Sem orçamento'}
                                </span>
                            </div>
                        </div>
                    `;
                    
                    if (project.status === 'Planejamento' || project.status === 'planejamento') {
                        $('#planning-column-project').append(projectCard);
                    } else if (project.status === 'Em Andamento' || project.status === 'em_andamento') {
                        $('#in-progress-column-project').append(projectCard);
                    } else if (project.status === 'Revisão' || project.status === 'revisao') {
                        $('#review-column-project').append(projectCard);
                    } else if (project.status === 'Concluído' || project.status === 'concluido') {
                        $('#completed-column-project').append(projectCard);
                    }
                    
                    let statusClass = '';
                    if (project.status === 'Concluído' || project.status === 'concluido') {
                        statusClass = 'positive';
                    } else if (project.status === 'Cancelado' || project.status === 'cancelado') {
                        statusClass = 'negative';
                    } else if (project.status === 'Em Andamento' || project.status === 'em_andamento') {
                        statusClass = 'warning';
                    }
                    
                    tbody.append(`
                        <tr class="${statusClass}">
                            <td>${project.id}</td>
                            <td>${project.name}</td>
                            <td>${project.client_name}</td>
                            <td>${formatDate(project.start_date)}</td>
                            <td>${project.end_date ? formatDate(project.end_date) : '-'}</td>
                            <td>${project.area_m2}</td>
                            <td>${project.status}</td>
                            <td>R$ ${project.budget ? parseFloat(project.budget).toFixed(2) : '0.00'}</td>
                            <td>
                                <div class="ui mini buttons">
                                    <button class="ui blue button" onclick="viewProject(${project.id})"><i class="eye icon"></i></button>
                                    <button class="ui green button" onclick="editProject(${project.id})"><i class="edit icon"></i></button>
                                    <button class="ui red button" onclick="deleteProject(${project.id})"><i class="trash icon"></i></button>
                                </div>
                            </td>
                        </tr>
                    `);
                });
                
                renderPagination(response.page, response.total_pages, 'projects-pagination', 'loadProjectsPage');
                
                $('.status-dropdown-project').dropdown({
                    onChange: function(value, text, $selectedItem) {
                        const cardId = $(this).closest('.kanban-card-project').data('id');
                        if (cardId) {
                            updateProjectStatus(cardId, value);
                        }
                    }
                });
            } else {
                tbody.append('<tr><td colspan="9" class="center aligned">Nenhum projeto encontrado</td></tr>');
            }
        },
        error: function(error) {
            console.error('Erro ao carregar projetos:', error);
            $('#projects-table-body').html('<tr><td colspan="9" class="center aligned error">Erro ao carregar projetos</td></tr>');
        }
    });
}

function loadProjectsPage(page) {
    $.ajax({
        url: `${API_URL}/api/landscaping/project?page=${page}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            loadProjects();
        },
        error: function(error) {
            console.error('Erro ao carregar projetos:', error);
        }
    });
}

function viewProject(id) {
    $.ajax({
        url: `${API_URL}/api/landscaping/project/${id}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(project) {
            if (project.start_date && typeof project.start_date === 'string') {
                project.start_date = project.start_date;
            }
            if (project.end_date && typeof project.end_date === 'string') {
                project.end_date = project.end_date;
            }
            
            $('body').append(`
                <div class="ui modal" id="view-project-modal">
                    <i class="close icon"></i>
                    <div class="header">${project.name}</div>
                    <div class="content">
                        <div class="ui form">
                            <div class="two fields">
                                <div class="field">
                                    <label>Cliente</label>
                                    <p>${project.client_name}</p>
                                </div>
                                <div class="field">
                                    <label>Status</label>
                                    <p>${project.status}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Data de Início</label>
                                    <p>${formatDate(project.start_date)}</p>
                                </div>
                                <div class="field">
                                    <label>Data de Término</label>
                                    <p>${project.end_date ? formatDate(project.end_date) : '-'}</p>
                                </div>
                            </div>
                            <div class="two fields">
                                <div class="field">
                                    <label>Área (m²)</label>
                                    <p>${project.area_m2}</p>
                                </div>
                                <div class="field">
                                    <label>Orçamento</label>
                                    <p>R$ ${project.budget ? parseFloat(project.budget).toFixed(2) : '0.00'}</p>
                                </div>
                            </div>
                            <div class="field">
                                <label>Localização</label>
                                <p>${project.location}</p>
                            </div>
                            <div class="field">
                                <label>Descrição</label>
                                <p>${project.description || 'Sem descrição'}</p>
                            </div>
                        </div>
                    </div>
                    <div class="actions">
                        <div class="ui button" onclick="$('#view-project-modal').modal('hide')">Fechar</div>
                    </div>
                </div>
            `);
            $('#view-project-modal').modal('show');
        },
        error: function(error) {
            console.error('Erro ao obter detalhes do projeto:', error);
            alert('Erro ao obter detalhes do projeto');
        }
    });
}

function editProject(id) {
    alert('Editar projeto ' + id + ' (implementação pendente)');
}

function deleteProject(id) {
    if (confirm('Tem certeza que deseja excluir este projeto?')) {
        $.ajax({
            url: `${API_URL}/api/landscaping/project/${id}?user_id=1`,
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                alert('Projeto excluído com sucesso!');
                loadProjects();
            },
            error: function(error) {
                console.error('Erro ao excluir projeto:', error);
                alert('Erro ao excluir projeto');
            }
        });
    }
}

function updateProjectStatus(projectId, newStatus) {
    $.ajax({
        url: `${API_URL}/api/landscaping/project/${projectId}/status?user_id=1&status=${encodeURIComponent(newStatus)}`,
        method: 'PATCH',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            const card = $(`.kanban-card-project[data-id="${projectId}"]`);
            
            let targetColumn;
            if (newStatus === 'Planejamento' || newStatus === 'planejamento') {
                targetColumn = $('#planning-column-project');
            } else if (newStatus === 'Em Andamento' || newStatus === 'em_andamento') {
                targetColumn = $('#in-progress-column-project');
            } else if (newStatus === 'Revisão' || newStatus === 'revisao') {
                targetColumn = $('#review-column-project');
            } else if (newStatus === 'Concluído' || newStatus === 'concluido') {
                targetColumn = $('#completed-column-project');
            }
            
            if (card.length && targetColumn) {
                const cardContent = card.html();
                card.addClass('transition');
                card.detach();
                targetColumn.append(card);
                
                card.find('input[name="status"]').val(newStatus);
                card.find('.text').text(newStatus);
                
                card.find('.status-dropdown-project').dropdown({
                    onChange: function(value, text, $selectedItem) {
                        const cardId = $(this).closest('.kanban-card-project').data('id');
                        if (cardId) {
                            updateProjectStatus(cardId, value);
                        }
                    }
                });
                
                card.transition('pulse');
                
                const tableRow = $(`#projects-table-body tr td:contains(${projectId})`).parent();
                if (tableRow.length) {
                    tableRow.find('td:nth-child(7)').text(newStatus);
                    tableRow.removeClass('positive negative warning');
                    if (newStatus === 'Concluído' || newStatus === 'concluido') {
                        tableRow.addClass('positive');
                    } else if (newStatus === 'Cancelado' || newStatus === 'cancelado') {
                        tableRow.addClass('negative');
                    } else if (newStatus === 'Em Andamento' || newStatus === 'em_andamento') {
                        tableRow.addClass('warning');
                    }
                }
            } else {
                loadProjects();
            }
        },
        error: function(error) {
            console.error('Erro ao atualizar status:', error);
            alert('Erro ao atualizar status');
        }
    });
}

function renderPagination(currentPage, totalPages, elementId, callbackName) {
    const pagination = $(`#${elementId}`);
    pagination.empty();
    
    if (totalPages <= 1) {
        return;
    }
    
    pagination.append(`
        <a class="item ${currentPage === 1 ? 'disabled' : ''}" 
           onclick="${currentPage > 1 ? callbackName + '(' + (currentPage - 1) + ')' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    for (let i = 1; i <= totalPages; i++) {
        pagination.append(`
            <a class="item ${i === currentPage ? 'active' : ''}" 
               onclick="${callbackName}(${i})">
                ${i}
            </a>
        `);
    }
    
    pagination.append(`
        <a class="item ${currentPage === totalPages ? 'disabled' : ''}" 
           onclick="${currentPage < totalPages ? callbackName + '(' + (currentPage + 1) + ')' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
        return dateString;
    }
    return date.toLocaleDateString('pt-BR');
}