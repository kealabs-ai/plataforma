// Carregar os dados de manutenção quando a aba for selecionada
$('.menu .item[data-tab="maintenance"]').on('click', function() {
    loadMaintenanceKanban();
});

// Função para carregar os dados de manutenção e exibir no Kanban board
function loadMaintenanceKanban() {
    $('#planning-column').empty();
    $('#in-progress-column').empty();
    $('#review-column').empty();
    $('#completed-column').empty();
    
    $.ajax({
        url: `${API_URL}/api/landscaping/maintenance`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            if (response && response.items && response.items.length > 0) {
                response.items.forEach(function(item) {
                    const card = createMaintenanceCard(item);
                    
                    switch(item.status) {
                        case 'Em Planejamento':
                            $('#planning-column').append(card);
                            break;
                        case 'Em Andamento':
                            $('#in-progress-column').append(card);
                            break;
                        case 'Em Revisão':
                            $('#review-column').append(card);
                            break;
                        case 'Concluído':
                            $('#completed-column').append(card);
                            break;
                        default:
                            $('#planning-column').append(card);
                    }
                });
                
                $('.status-dropdown').dropdown({
                    onChange: function(value, text, $choice) {
                        const cardId = $(this).closest('.kanban-card').data('id');
                        updateMaintenanceStatus(cardId, value);
                    }
                });
            }
        },
        error: function(error) {
            console.error('Erro ao carregar dados de manutenção:', error);
        }
    });
}

function updateMaintenanceStatus(maintenanceId, newStatus) {
    $.ajax({
        url: `${API_URL}/api/landscaping/maintenance/${maintenanceId}`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(maintenanceData) {
            const oldStatus = maintenanceData.status;
            const cost = parseFloat(maintenanceData.cost || 0);
            
            $.ajax({
                url: `${API_URL}/api/landscaping/maintenance/${maintenanceId}`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    status: newStatus
                }),
                headers: {
                    'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                },
                success: function(response) {
                    showMessage('Status atualizado com sucesso', 'success');
                    updateMonthlyRevenue();
                    loadMaintenanceKanban();
                },
                error: function(error) {
                    console.error('Erro ao atualizar status:', error);
                    showMessage('Erro ao atualizar status', 'error');
                }
            });
        },
        error: function(error) {
            console.error('Erro ao obter detalhes da manutenção:', error);
            showMessage('Erro ao obter detalhes da manutenção', 'error');
        }
    });
}

function updateMonthlyRevenue() {
    $.ajax({
        url: `${API_URL}/api/landscaping/maintenance`,
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            let totalRevenue = 0;
            if (response && response.items && response.items.length > 0) {
                const completedItems = response.items.filter(item => item.status === 'Concluído');
                totalRevenue = completedItems.reduce((sum, item) => {
                    return sum + (parseFloat(item.cost) || 0);
                }, 0);
            }
            
            $('#monthly-revenue').text('R$ ' + totalRevenue.toFixed(2));
        },
        error: function(error) {
            console.error('Erro ao calcular receita mensal:', error);
            $('#monthly-revenue').text('R$ 0.00');
        }
    });
}

function createMaintenanceCard(item) {
    return `
        <div class="ui card kanban-card" data-id="${item.id}">
            <div class="content">
                <div class="header">${item.project_name || 'Sem projeto'}</div>
                <div class="meta">${formatDate(item.date)}</div>
                <div class="description">
                    ${item.description.substring(0, 100)}${item.description.length > 100 ? '...' : ''}
                </div>
            </div>
            <div class="extra content">
                <div class="ui mini fluid selection dropdown status-dropdown">
                    <input type="hidden" name="status" value="${item.status}">
                    <i class="dropdown icon"></i>
                    <div class="text">${item.status || 'Alterar status'}</div>
                    <div class="menu">
                        <div class="item" data-value="Em Planejamento">Em Planejamento</div>
                        <div class="item" data-value="Em Andamento">Em Andamento</div>
                        <div class="item" data-value="Em Revisão">Em Revisão</div>
                        <div class="item" data-value="Concluído">Concluído</div>
                    </div>
                </div>
            </div>
            <div class="extra content">
                <span>
                    <i class="calendar check icon"></i>
                    ${item.type}
                </span>
                <span class="right floated">
                    ${item.cost ? 'R$ ' + parseFloat(item.cost).toFixed(2) : 'Sem custo'}
                </span>
            </div>
        </div>
    `;
}

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

// Inicializar quando a página for carregada
$(document).ready(function() {
    updateMonthlyRevenue();
    
    if ($('.menu .item[data-tab="maintenance"]').hasClass('active')) {
        loadMaintenanceKanban();
    }
});