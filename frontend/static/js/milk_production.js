// Configuração da API
const API_URL = 'http://localhost:8000/api';

// Variáveis globais
let currentPage = 1;
const pageSize = 5;
let totalPages = 1;
let animalsList = [];
let currentMilkPrice = 2.50; // Preço padrão do leite
let loadingAnimals = false; // Flag para evitar chamadas múltiplas

// Inicialização quando o documento estiver pronto
$(document).ready(function() {
    // Inicializa os componentes do Semantic UI
    $('.ui.dropdown').dropdown();
    
    // Carrega os dados iniciais
    loadDashboardData();
    loadAnimals();
    loadProductionEntries(currentPage);
    
    // Configura os eventos
    setupEventListeners();
    setupDateFilters();
});

// Carrega os dados do dashboard
function loadDashboardData(startDate = null, endDate = null, animalId = null) {
    let url = `${API_URL}/milk/dashboard`;
    let params = [];
    
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    if (animalId) params.push(`animal_id=${animalId}`);
    
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    // Preparar dados para enviar ao endpoint
    const requestData = {
        start_date: startDate || null,
        end_date: endDate || null,
        user_id: null, // Todos os usuários
        animal_id: animalId || null
    };
    
    // Chamada para obter o total de litros e atualizar indicadores
    $.ajax({
        url: `${API_URL}/milk/total-production`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function(totalData) {
            if (totalData && totalData.total_liters !== undefined) {
                // Atualiza o card de litros
                $('#total-liters').text(totalData.total_liters.toLocaleString('pt-BR', {
                    minimumFractionDigits: 1,
                    maximumFractionDigits: 1
                }));
                
                // Calcula e atualiza o valor total
                const totalValue = totalData.total_liters * currentMilkPrice;
                $('#total-value').text(formatCurrency(totalValue));
            }
        },
        error: function(error) {
            console.error('Erro ao obter total de produção:', error);
        }
    });
    
    // Carrega os dados do dashboard para os gráficos
    $.ajax({
        url: url,
        method: 'GET',
        success: function(data) {
            if (data && data.daily_production && data.animal_production) {
                renderDailyProductionChart(data.daily_production);
                renderAnimalProductionChart(data.animal_production);
                
                // Atualiza os cards de estatísticas
                if (data.statistics) {
                    // Armazena o preço do leite para uso em outros cálculos
                    if (data.statistics.milk_price) {
                        currentMilkPrice = data.statistics.milk_price;
                    }
                    updateStatisticsCards(data.statistics);
                } else {
                    // Carrega contagem de animais separadamente
                    loadAnimalCount();
                }
            } else {
                showMessage('warning', 'Dados incompletos', 'Os dados do dashboard estão incompletos ou em formato incorreto.');
            }
        },
        error: function(error) {
            showMessage('error', 'Erro ao carregar dados do dashboard', 'Verifique sua conexão e tente novamente.');
            console.error('Erro ao carregar dados do dashboard:', error);
        }
    });
}

// Carrega a contagem de animais do endpoint específico
function loadAnimalCount() {
    $.ajax({
        url: `${API_URL}/animals/total_count`,
        method: 'GET',
        success: function(data) {
            if (data && data.total_animals !== undefined) {
                $('#total-animals').text(data.total_animals.toLocaleString('pt-BR'));
            }
        },
        error: function(error) {
            console.error('Erro ao carregar contagem de animais:', error);
        }
    });
}

// Carrega a lista de animais
function loadAnimals() {
    if (loadingAnimals) return;
    
    loadingAnimals = true;
    $.ajax({
        url: `${API_URL}/milk/animals`,
        method: 'GET',
        success: function(data) {
            animalsList = data;
            populateAnimalDropdown(data);
            populateFilterAnimalDropdown(); // Popula o dropdown de filtro também
            loadingAnimals = false;
        },
        error: function(error) {
            showMessage('error', 'Erro ao carregar animais', 'Verifique sua conexão e tente novamente.');
            console.error('Erro ao carregar animais:', error);
            loadingAnimals = false;
        }
    });
}

// Carrega os registros de produção com paginação
function loadProductionEntries(page) {
    $.ajax({
        url: `${API_URL}/milk/production?page=${page}&page_size=${pageSize}`,
        method: 'GET',
        success: function(data) {
            renderProductionTable(data.items);
            updatePagination(data.page, data.total_pages);
            currentPage = data.page;
            totalPages = data.total_pages;
        },
        error: function(error) {
            showMessage('error', 'Erro ao carregar registros de produção', 'Verifique sua conexão e tente novamente.');
            console.error('Erro ao carregar registros de produção:', error);
        }
    });
}

// Popula o dropdown de animais
function populateAnimalDropdown(animals) {
    const $dropdown = $('select[name="animal"]');
    $dropdown.empty();
    $dropdown.append('<option value="">Selecione o animal</option>');
    
    animals.forEach(animal => {
        $dropdown.append(`<option value="${animal.animal_id}">${animal.official_id} - ${animal.name || 'Sem nome'}</option>`);
    });
    
    // Reinicializa o dropdown do Semantic UI
    $dropdown.dropdown('refresh');
}

// Renderiza a tabela de registros de produção
function renderProductionTable(entries) {
    const $tableBody = $('.ui.table tbody');
    $tableBody.empty();

    if (!entries || entries.length === 0) {
        $tableBody.append(`
            <tr>
                <td colspan="6" class="center aligned">Nenhum registro encontrado</td>
            </tr>
        `);
        return;
    }

    entries.forEach(entry => {
        // Data de Produção
        let formattedDate = '';
        try {
            formattedDate = entry.production_date
                ? new Date(entry.production_date).toLocaleDateString('pt-BR')
                : '';
        } catch (e) {
            formattedDate = entry.production_date || '';
        }

        // Animal (ID Oficial + Nome)
        const animalName = entry.official_id
            ? `${entry.official_id}${entry.name ? ` (${entry.name})` : ''}`
            : (entry.name || 'N/A');

        // Litros Produzidos
        const litersProduced = entry.liters_produced !== undefined 
            ? parseFloat(entry.liters_produced).toFixed(1) + ' L'
            : 'N/A';

        // Período
        const periodText = getPeriodText(entry.period);

        // Observações
        const notes = entry.notes || '-';

        $tableBody.append(`
            <tr data-id="${entry.id}">
                <td>${formattedDate}</td>
                <td>${animalName}</td>
                <td>${litersProduced}</td>
                <td>${periodText}</td>
                <td>${notes}</td>
                <td class="center aligned collapsing">
                    <button class="ui mini icon button blue edit-entry">
                        <i class="edit icon"></i>
                    </button>
                    <button class="ui mini icon button red delete-entry">
                        <i class="trash icon"></i>
                    </button>
                </td>
            </tr>
        `);
    });

    setupTableActions();
}

// Função para formatar números como moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Atualiza os cards de estatísticas
function updateStatisticsCards(statistics) {
    // Preço por litro
    currentMilkPrice = statistics.milk_price || 2.50; // Valor padrão se não for fornecido
    $('#milk-price').text(formatCurrency(currentMilkPrice));
    
    // Total de animais
    $('#total-animals').text(statistics.total_animals.toLocaleString('pt-BR'));
    
    // Nota: Total de litros e valor total são atualizados pela chamada ao endpoint total-production
}

function updatePagination(currentPage, totalPages) {
    const $pagination = $('.pagination');
    $pagination.empty();
    
    // Botão anterior
    $pagination.append(`
        <a class="icon item ${currentPage <= 1 ? 'disabled' : ''}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    // Páginas
    for (let i = 1; i <= totalPages; i++) {
        $pagination.append(`
            <a class="item ${i === currentPage ? 'active' : ''}">${i}</a>
        `);
    }
    
    // Botão próximo
    $pagination.append(`
        <a class="icon item ${currentPage >= totalPages ? 'disabled' : ''}">
            <i class="right chevron icon"></i>
        </a>
    `);
    
    // Configura os eventos de paginação
    setupPaginationEvents();
}

// Configura os eventos de paginação
function setupPaginationEvents() {
    // Clique nos números de página
    $('.pagination .item:not(.icon)').on('click', function() {
        if (!$(this).hasClass('active') && !$(this).hasClass('disabled')) {
            const page = parseInt($(this).text());
            loadProductionEntries(page);
        }
    });
    
    // Clique nos botões de navegação
    $('.pagination .icon.item').on('click', function() {
        if (!$(this).hasClass('disabled')) {
            if ($(this).find('.left.chevron').length > 0) {
                // Botão anterior
                if (currentPage > 1) {
                    loadProductionEntries(currentPage - 1);
                }
            } else {
                // Botão próximo
                if (currentPage < totalPages) {
                    loadProductionEntries(currentPage + 1);
                }
            }
        }
    });
}

// Configura os eventos para os botões de ação da tabela
function setupTableActions() {
    // Botão de edição
    $('.edit-entry').on('click', function() {
        const entryId = $(this).closest('tr').data('id');
        openEditModal(entryId);
    });
    
    // Botão de exclusão
    $('.delete-entry').on('click', function() {
        const entryId = $(this).closest('tr').data('id');
        confirmDeleteEntry(entryId);
    });
}

// Abre o modal de edição de registro
function openEditModal(entryId) {
    $.ajax({
        url: `${API_URL}/milk/production/${entryId}`,
        method: 'GET',
        success: function(entry) {
            if (!entry || !entry.id) {
                showMessage('error', 'Dados inválidos', 'Os dados do registro estão incompletos ou em formato incorreto.');
                return;
            }
            
            // Determina qual campo usar para a quantidade (quantity ou liters_produced)
            const quantity = entry.quantity !== undefined ? entry.quantity : 
                           (entry.liters_produced !== undefined ? entry.liters_produced : 0);
            
            // Preenche o formulário de edição
            $('#edit-form').form('set values', {
                edit_id: entry.id,
                edit_animal: entry.animal_id,
                edit_date: entry.production_date,
                edit_quantity: parseFloat(entry.quantity !== undefined ? entry.quantity : (entry.liters_produced !== undefined ? entry.liters_produced : 0)) || 0,
                edit_period: entry.period || '',
                edit_notes: entry.notes || ''
            });
            
            // Formata as informações do animal para o dropdown
            const animalInfo = [];
            if (entry.official_id) animalInfo.push(entry.official_id);
            if (entry.name) animalInfo.push(entry.name);
            if (entry.breed) animalInfo.push(entry.breed);
            if (entry.status) animalInfo.push(entry.status);
            if (entry.age) animalInfo.push(`${entry.age} anos`);

            const animalText = animalInfo.length > 0 ? animalInfo.join(' - ') : 'Animal desconhecido';
            
            // Atualiza o texto do animal no dropdown (somente leitura)
            $('select[name="edit_animal"]').empty()
                .append(`<option value="${entry.animal_id}">${animalText}</option>`);
            
            // Exibe o modal
            $('#edit-modal').modal('show');
        },
        error: function(error) {
            let errorMsg = 'Verifique sua conexão e tente novamente.';
            if (error.responseJSON && error.responseJSON.detail) {
                errorMsg = error.responseJSON.detail;
            }
            showMessage('error', 'Erro ao carregar dados do registro', errorMsg);
            console.error('Erro ao carregar dados do registro:', error);
        }
    });
}

// Confirma a exclusão de um registro
function confirmDeleteEntry(entryId) {
    if (confirm('Tem certeza que deseja inativar este registro de produção?')) {
        $.ajax({
            url: `${API_URL}/milk/production/${entryId}`,
            method: 'DELETE',
            success: function(response) {
                showMessage('success', 'Registro inativado', 'O registro de produção foi inativado com sucesso.');
                // Recarrega os dados do dashboard e da tabela
                loadDashboardData();
                loadProductionEntries(currentPage);
            },
            error: function(error) {
                let errorMsg = 'Verifique sua conexão e tente novamente.';
                if (error.responseJSON && error.responseJSON.detail) {
                    errorMsg = error.responseJSON.detail;
                }
                showMessage('error', 'Erro ao inativar registro', errorMsg);
                console.error('Erro ao inativar registro:', error);
            }
        });
    }
}

// Configura os eventos de formulários e botões
function setupEventListeners() {
    // Formulário de registro de produção
    $('form.ui.form:not(#animal-form):not(#edit-form)').on('submit', function(e) {
        e.preventDefault();
        
        // Cria o objeto base de dados
        const formData = {
            animal_id: parseInt($('select[name="animal"]').val()),
            production_date: $('input[name="date"]').val(),
            period: $('select[name="period"]').val(),
            notes: ''
        };
        
        // Adiciona o campo de quantidade com o nome correto (quantity ou liters_produced)
        const quantityValue = parseFloat($('input[name="quantity"]').val());
        formData.quantity = quantityValue;
        formData.liters_produced = quantityValue; // Adiciona ambos os campos para compatibilidade
        
        // Validação básica
        if (!formData.animal_id || !formData.production_date || !(formData.quantity || formData.liters_produced) || !formData.period) {
            showMessage('warning', 'Campos obrigatórios', 'Preencha todos os campos obrigatórios.');
            return;
        }
        
        // Envia os dados para a API
        $.ajax({
            url: `${API_URL}/milk/production`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                showMessage('success', 'Produção registrada', 'O registro de produção foi salvo com sucesso.');
                
                // Limpa o formulário
                $('form.ui.form:not(#animal-form):not(#edit-form)')[0].reset();
                
                // Recarrega os dados
                loadDashboardData();
                loadProductionEntries(1);
            },
            error: function(error) {
                let errorMsg = 'Verifique sua conexão e tente novamente.';
                if (error.responseJSON && error.responseJSON.detail) {
                    errorMsg = error.responseJSON.detail;
                }
                showMessage('error', 'Erro ao registrar produção', errorMsg);
                console.error('Erro ao registrar produção:', error);
            }
        });
    });
    
    // Botão de atualizar dados
    $('#refresh-data').on('click', function() {
        loadDashboardData();
        loadProductionEntries(currentPage);
    });
    
    // Botão de adicionar animal
    $('#add-animal-button').on('click', function() {
        $('#animal-modal').modal('show');
    });
    
    // Formulário de cadastro de animal
    $('#animal-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            official_id: $('input[name="official_id"]').val(),
            name: $('input[name="name"]').val(),
            birth_date: $('input[name="birth_date"]').val(),
            breed: $('input[name="breed"]').val(),
            gender: $('select[name="gender"]').val(),
            status: $('select[name="status"]').val(),
            entry_date: $('input[name="entry_date"]').val() || new Date().toISOString().split('T')[0]
        };
        
        // Validação básica
        if (!formData.official_id || !formData.birth_date || !formData.gender) {
            showMessage('warning', 'Campos obrigatórios', 'Preencha todos os campos obrigatórios.');
            return;
        }
        
        // Envia os dados para a API
        $.ajax({
            url: `${API_URL}/animals`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(data) {
                showMessage('success', 'Animal cadastrado', 'O animal foi cadastrado com sucesso.');
                
                // Fecha o modal
                $('#animal-modal').modal('hide');
                
                // Limpa o formulário
                $('#animal-form')[0].reset();
                
                // Recarrega a lista de animais
                loadAnimals();
            },
            error: function(error) {
                let errorMsg = 'Verifique sua conexão e tente novamente.';
                if (error.responseJSON && error.responseJSON.detail) {
                    errorMsg = error.responseJSON.detail;
                }
                showMessage('error', 'Erro ao cadastrar animal', errorMsg);
                console.error('Erro ao cadastrar animal:', error);
            }
        });
    });
    
    // Botão de salvar edição
    $('#save-edit-button').on('click', function() {
        const entryId = $('#edit-form input[name="edit_id"]').val();
        
        const quantityValue = parseFloat($('#edit-form input[name="edit_quantity"]').val());
        const formData = {
            quantity: quantityValue,
            liters_produced: quantityValue, // Adiciona ambos os campos para compatibilidade
            period: $('#edit-form select[name="edit_period"]').val(),
            notes: $('#edit-form textarea[name="edit_notes"]').val()
        };
        
        // Validação básica
        if (!(formData.quantity || formData.liters_produced) || !formData.period) {
            showMessage('warning', 'Campos obrigatórios', 'Preencha todos os campos obrigatórios.');
            return;
        }
        
        // Envia os dados para a API
        $.ajax({
            url: `${API_URL}/milk/production/${entryId}`,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                showMessage('success', 'Registro atualizado', 'O registro de produção foi atualizado com sucesso.');
                
                // Fecha o modal
                $('#edit-modal').modal('hide');
                
                // Recarrega os dados
                loadDashboardData();
                loadProductionEntries(currentPage);
            },
            error: function(error) {
                let errorMsg = 'Verifique sua conexão e tente novamente.';
                if (error.responseJSON && error.responseJSON.detail) {
                    errorMsg = error.responseJSON.detail;
                }
                showMessage('error', 'Erro ao atualizar registro', errorMsg);
                console.error('Erro ao atualizar registro:', error);
            }
        });
    });
}

// Renderiza o gráfico de produção diária
function renderDailyProductionChart(data) {
    const chartDom = document.getElementById('daily-production-chart');
    if (!chartDom || !data || !Array.isArray(data)) return;
    
    const myChart = echarts.init(chartDom);
    
    const dates = data.map(item => item.date);
    const values = data.map(item => parseFloat(item.total_liters) || 0);
    
    const option = {
        tooltip: {
            trigger: 'axis',
            formatter: '{b}: {c} litros'
        },
        xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
                rotate: 45,
                formatter: function(value) {
                    return new Date(value).toLocaleDateString('pt-BR');
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Litros'
        },
        series: [
            {
                data: values,
                type: 'line',
                smooth: true,
                lineStyle: {
                    color: '#4285f4',
                    width: 3
                },
                areaStyle: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            {
                                offset: 0,
                                color: 'rgba(66, 133, 244, 0.5)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(66, 133, 244, 0.1)'
                            }
                        ]
                    }
                }
            }
        ]
    };
    
    myChart.setOption(option);
    
    // Redimensiona o gráfico quando a janela for redimensionada
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// Renderiza o gráfico de produção por animal
function renderAnimalProductionChart(data) {
    const chartDom = document.getElementById('animal-production-chart');
    if (!chartDom || !data || !Array.isArray(data)) return;
    
    const myChart = echarts.init(chartDom);
    
    const animals = data.map(item => item.animal_name || `${item.name || '?'}`);
    const values = data.map(item => parseFloat(item.total_liters) || 0);
    
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} litros ({d}%)'
        },
        legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            data: animals
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: animals.map((name, index) => ({
                    value: values[index],
                    name: name
                }))
            }
        ]
    };
    
    myChart.setOption(option);
    
    // Redimensiona o gráfico quando a janela for redimensionada
    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

// Exibe uma mensagem de status
function showMessage(type, title, message) {
    const $statusMessages = $('#status-messages');
    
    // Remove mensagens anteriores
    $statusMessages.empty();
    
    // Cria a nova mensagem
    const $message = $(`
        <div class="ui ${type} message">
            <i class="close icon"></i>
            <div class="header">${title}</div>
            <p>${message}</p>
        </div>
    `);
    
    // Adiciona a mensagem ao container
    $statusMessages.append($message);
    
    // Configura o botão de fechar
    $message.find('.close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    
    // Esconde a mensagem automaticamente após 5 segundos
    setTimeout(function() {
        $message.transition('fade');
    }, 5000);
}

// Converte o código do período para texto
function getPeriodText(period) {
    switch (period) {
        case 'morning':
            return 'Manhã';
        case 'afternoon':
            return 'Tarde';
        case 'night':
            return 'Noite';
        default:
            return period;
    }
}

// Configura os filtros de data
function setupDateFilters() {
    $('#apply-filters').on('click', function() {
        const startDate = $('#start-date').val();
        const endDate = $('#end-date').val();
        const animalId = $('#filter-animal').val();
        
        loadDashboardData(startDate, endDate, animalId);
    });
    
    $('#clear-filters').on('click', function() {
        $('#start-date').val('');
        $('#end-date').val('');
        $('#filter-animal').val('').trigger('change');
        loadDashboardData();
    });
}

// Popula o dropdown de animais para filtro
function populateFilterAnimalDropdown() {
    if (animalsList.length === 0) {
        return; // Não faz nada se a lista estiver vazia, será chamado novamente quando os animais forem carregados
    }
    
    const $dropdown = $('#filter-animal');
    $dropdown.empty(); // Limpa o dropdown antes de popular
    
    // Adiciona a opção "Todos os animais"
    $dropdown.append('<option value="">Todos os animais</option>');
    
    animalsList.forEach(animal => {
        $dropdown.append(`<option value="${animal.animal_id}">${animal.official_id} - ${animal.name || 'Sem nome'}</option>`);
    });
    
    // Reinicializa o dropdown do Semantic UI
    $dropdown.dropdown('refresh');
}