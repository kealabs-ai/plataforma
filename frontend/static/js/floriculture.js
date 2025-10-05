const API_URL = "http://localhost:8000";  

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar os dropdowns do Semantic UI
    $('.ui.dropdown').dropdown();
    
    // Inicializar as tabs
    $('.menu .item').tab();
    
    // Configurar alternância entre visualização em grade e lista
    $('#grid-view-btn').on('click', function() {
        $('#grid-view').show();
        $('#list-view').hide();
        $('#grid-view-btn').addClass('active');
        $('#list-view-btn').removeClass('active');
    });
    
    $('#list-view-btn').on('click', function() {
        $('#grid-view').hide();
        $('#list-view').show();
        $('#list-view-btn').addClass('active');
        $('#grid-view-btn').removeClass('active');
    });
    
    // Configurar modais
    $('#add-plant-btn').on('click', function() {
        $('#add-plant-modal').modal('show');
    });
    
    $('#add-supplier-btn').on('click', function() {
        $('#add-supplier-modal').modal('show');
    });
    
    $('#add-cultivation-btn').on('click', function() {
        $('#add-cultivation-modal').modal('show');
    });
    
    $('#add-sale-btn').on('click', function() {
        $('#add-sale-modal').modal('show');
    });
    
    // Calcular valor total na venda
    $('#unit-price, [name="quantity"]').on('input', function() {
        const unitPrice = parseFloat($('#unit-price').val()) || 0;
        const quantity = parseInt($('[name="quantity"]').val()) || 1;
        $('#total-value').val((unitPrice * quantity).toFixed(2));
    });
    
    // Configurar evento de salvamento de planta
    $('#save-plant-btn').on('click', function() {
        savePlant();
    });
    
    // Configurar evento de salvamento de fornecedor
    $('#save-supplier-btn').on('click', function() {
        saveSupplier();
    });
    
    // Configurar evento de salvamento de cultivo
    $('#save-cultivation-btn').on('click', function() {
        saveCultivation();
    });
    
    // Configurar evento de salvamento de venda
    $('#save-sale-btn').on('click', function() {
        saveSale();
    });
    
    // Carregar dados reais da API, com fallback para dados mockados
    loadDataFromAPI().catch(error => {
        console.error('Erro ao carregar dados da API, usando dados mockados:', error);
        loadMockData();
    });
    
    // Inicializar gráficos
    initCharts();
});

// Função para carregar dados reais da API
async function loadDataFromAPI() {
    try {
        // Buscar plantas (cultivos de flores)
        const plantsResponse = await fetch(`${API_URL}/api/floriculture/cultivation?page=1&page_size=100`, {
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || ''),
                'Accept': 'application/json'
            }
        });
        
        if (!plantsResponse.ok) {
            throw new Error(`Erro ao buscar flores: ${plantsResponse.status}`);
        }
        
        const plantsData = await plantsResponse.json();
        const plants = plantsData.items || [];

        // Buscar fornecedores
        const suppliersResponse = await fetch(`${API_URL}/api/floriculture/supplier?page=1&page_size=100`, {
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
        $('#total-plants').text(plants.reduce((sum, plant) => sum + (plant.quantity || 0), 0));
        $('#flower-varieties').text(plants.length);
        $('#monthly-sales').text('R$ ' + (8500).toFixed(2));
        $('#area-cultivated').text('350 m²');

        // Preencher grid de plantas
        const plantsGrid = $('#plants-grid');
        plantsGrid.empty();
        plants.forEach(plant => {
            plantsGrid.append(`
                <div class="ui card plant-card">
                    <div class="image">
                        <img src="${plant.image_url || 'https://via.placeholder.com/150'}" alt="${plant.species}">
                    </div>
                    <div class="content">
                        <a class="header">${plant.species}</a>
                        <div class="meta">
                            <span class="date">${plant.variety || ''}</span>
                        </div>
                        <div class="description">
                            ${plant.notes || ''}
                        </div>
                    </div>
                    <div class="extra content">
                        <span>
                            <i class="leaf icon"></i>
                            ${plant.status}
                        </span>
                        <span class="right floated">
                            ${plant.area_m2 || ''} m²
                        </span>
                    </div>
                    <div class="ui bottom attached buttons">
                        <button class="ui primary button">Detalhes</button>
                        <button class="ui green button">Comprar</button>
                    </div>
                </div>
            `);
        });

        // Preencher tabela de plantas
        const plantsTable = $('#plants-table-body');
        plantsTable.empty();
        plants.forEach(plant => {
            plantsTable.append(`
                <tr>
                    <td><img src="${plant.image_url || 'https://via.placeholder.com/50'}" alt="${plant.species}" class="plant-image"></td>
                    <td>${plant.species}</td>
                    <td>${plant.variety || ''}</td>
                    <td>${plant.status}</td>
                    <td>${plant.area_m2 || ''}</td>
                    <td>${plant.greenhouse_id || ''}</td>
                    <td>${plant.quantity || ''}</td>
                    <td>
                        <div class="ui mini buttons">
                            <button class="ui blue button"><i class="edit icon"></i></button>
                            <button class="ui green button"><i class="shopping cart icon"></i></button>
                            <button class="ui red button"><i class="trash icon"></i></button>
                        </div>
                    </td>
                </tr>
            `);
        });

        // Preencher tabela de fornecedores
        const suppliersTable = $('#suppliers-table-body');
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
                    <td>${formatDate(supplier.last_purchase)}</td>
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

        // Preencher selects
        const plantSelect = $('#cultivation-plant-select');
        plantSelect.empty();
        plantSelect.append('<option value="">Selecione uma planta</option>');
        plants.forEach(plant => {
            plantSelect.append(`<option value="${plant.id}">${plant.species}</option>`);
        });

        const salePlantSelect = $('#sale-plant-select');
        salePlantSelect.empty();
        salePlantSelect.append('<option value="">Selecione uma planta</option>');
        plants.forEach(plant => {
            salePlantSelect.append(`<option value="${plant.id}">${plant.species}</option>`);
        });

        $('.ui.dropdown').dropdown('refresh');
        
        return { plants, suppliers };
    } catch (error) {
        console.error('Erro ao carregar dados da API:', error);
        throw error;
    }
}

// Função para carregar dados de exemplo
function loadMockData() {
    // Dados de exemplo para plantas
    const mockPlants = [
        {
            id: 1,
            species: 'Rosa Vermelha',
            variety: 'Gallica',
            planting_date: '2023-10-15',
            area_m2: 25.5,
            greenhouse_id: 1,
            expected_harvest_date: '2024-01-15',
            status: 'active',
            notes: 'Rosa vermelha tradicional, perfeita para jardins e arranjos.',
            image_url: 'https://images.unsplash.com/photo-1559563362-c667ba5f5480'
        },
        {
            id: 2,
            species: 'Orquídea Phalaenopsis',
            variety: 'Branca',
            planting_date: '2023-09-20',
            area_m2: 10.0,
            greenhouse_id: 2,
            expected_harvest_date: '2024-02-20',
            status: 'active',
            notes: 'Orquídea elegante de fácil cultivo, ideal para ambientes internos.',
            image_url: 'https://images.unsplash.com/photo-1566550747935-a6f55a696122'
        },
        {
            id: 3,
            species: 'Lírio',
            variety: 'Asiático',
            planting_date: '2023-11-05',
            area_m2: 15.0,
            greenhouse_id: 1,
            expected_harvest_date: '2024-03-05',
            status: 'active',
            notes: 'Lírio perfumado, excelente para arranjos florais.',
            image_url: 'https://images.unsplash.com/photo-1588701107566-af76b932e2e8'
        }
    ];
    
    // Dados de exemplo para fornecedores
    const mockSuppliers = [
        {
            id: 1,
            name: 'Flores & Cia',
            contact_person: 'João Silva',
            phone: '(11) 98765-4321',
            email: 'contato@floresecia.com.br',
            products: 'Flores, Sementes, Mudas',
            last_purchase: '2023-08-15',
            status: 'Ativo'
        },
        {
            id: 2,
            name: 'Jardim Verde',
            contact_person: 'Maria Oliveira',
            phone: '(11) 91234-5678',
            email: 'vendas@jardimverde.com.br',
            products: 'Vasos, Substratos, Fertilizantes',
            last_purchase: '2023-09-02',
            status: 'Ativo'
        }
    ];
    
    // Atualizar estatísticas
    $('#total-plants').text(mockPlants.length);
    $('#flower-varieties').text(mockPlants.length);
    $('#monthly-sales').text('R$ ' + (8500).toFixed(2));
    $('#area-cultivated').text('350 m²');
    
    // Preencher grid de plantas
    const plantsGrid = $('#plants-grid');
    plantsGrid.empty();
    
    mockPlants.forEach(plant => {
        plantsGrid.append(`
            <div class="ui card plant-card">
                <div class="image">
                    <img src="${plant.image_url}" alt="${plant.species}">
                </div>
                <div class="content">
                    <a class="header">${plant.species}</a>
                    <div class="meta">
                        <span class="date">${plant.variety || ''}</span>
                    </div>
                    <div class="description">
                        ${plant.notes || ''}
                    </div>
                </div>
                <div class="extra content">
                    <span>
                        <i class="leaf icon"></i>
                        ${plant.status}
                    </span>
                    <span class="right floated">
                        ${plant.area_m2 || ''} m²
                    </span>
                </div>
                <div class="ui bottom attached buttons">
                    <button class="ui primary button">Detalhes</button>
                    <button class="ui green button">Comprar</button>
                </div>
            </div>
        `);
    });
    
    // Preencher tabela de plantas
    const plantsTable = $('#plants-table-body');
    plantsTable.empty();
    
    mockPlants.forEach(plant => {
        plantsTable.append(`
            <tr>
                <td><img src="${plant.image_url}" alt="${plant.species}" class="plant-image"></td>
                <td>${plant.species}</td>
                <td>${plant.variety || ''}</td>
                <td>${plant.status}</td>
                <td>${plant.area_m2 || ''}</td>
                <td>${plant.greenhouse_id || ''}</td>
                <td>${plant.quantity || ''}</td>
                <td>
                    <div class="ui mini buttons">
                        <button class="ui blue button"><i class="edit icon"></i></button>
                        <button class="ui green button"><i class="shopping cart icon"></i></button>
                        <button class="ui red button"><i class="trash icon"></i></button>
                    </div>
                </td>
            </tr>
        `);
    });
    
    // Preencher tabela de fornecedores
    const suppliersTable = $('#suppliers-table-body');
    suppliersTable.empty();
    
    mockSuppliers.forEach(supplier => {
        let statusClass = supplier.status === 'Ativo' ? 'positive' : 'negative';
        
        suppliersTable.append(`
            <tr class="${statusClass}">
                <td>${supplier.id}</td>
                <td>${supplier.name}</td>
                <td>${supplier.contact_person}</td>
                <td>${supplier.phone}</td>
                <td>${supplier.email}</td>
                <td>${supplier.products}</td>
                <td>${formatDate(supplier.last_purchase)}</td>
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
    
    // Preencher selects
    const plantSelect = $('#cultivation-plant-select');
    plantSelect.empty();
    plantSelect.append('<option value="">Selecione uma planta</option>');
    
    mockPlants.forEach(plant => {
        plantSelect.append(`<option value="${plant.id}">${plant.species}</option>`);
    });
    
    const salePlantSelect = $('#sale-plant-select');
    salePlantSelect.empty();
    salePlantSelect.append('<option value="">Selecione uma planta</option>');
    
    mockPlants.forEach(plant => {
        salePlantSelect.append(`<option value="${plant.id}">${plant.species}</option>`);
    });
    
    // Reinicializar dropdowns após preencher
    $('.ui.dropdown').dropdown('refresh');
}

// Função para inicializar gráficos
function initCharts() {
    // Gráfico de cultivo
    const cultivationCtx = document.getElementById('cultivation-chart')?.getContext('2d');
    if (cultivationCtx) {
        new Chart(cultivationCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Plantas Cultivadas',
                    data: [65, 59, 80, 81, 56, 55],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Função para salvar nova planta
function savePlant() {
    const formData = {};
    $('#add-plant-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.stock = parseInt(formData.stock) || 0;
    formData.price = parseFloat(formData.price) || 0;
    
    $.ajax({
        url: `${API_URL}/api/floriculture/plant`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            showMessage('Planta salva com sucesso!', 'success');
            $('#add-plant-modal').modal('hide');
            $('#add-plant-form')[0].reset();
            loadDataFromAPI().catch(() => loadMockData());
        },
        error: function(xhr, status, error) {
            console.error('Erro ao salvar planta:', error);
            showMessage('Erro ao salvar planta: ' + (xhr.responseText || error), 'error');
        }
    });
}

// Função para salvar fornecedor
function saveSupplier() {
    const formData = {};
    $('#add-supplier-form').serializeArray().forEach(function(item) {
        if (item.name === 'products') {
            if (!formData[item.name]) formData[item.name] = [];
            formData[item.name].push(item.value);
        } else {
            formData[item.name] = item.value;
        }
    });
    
    // Converter array de produtos em string
    if (Array.isArray(formData.products)) {
        formData.products = formData.products.join(', ');
    }
    
    $.ajax({
        url: `${API_URL}/api/floriculture/supplier`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            showMessage('Fornecedor salvo com sucesso!', 'success');
            $('#add-supplier-modal').modal('hide');
            $('#add-supplier-form')[0].reset();
            loadDataFromAPI().catch(() => loadMockData());
        },
        error: function(xhr, status, error) {
            console.error('Erro ao salvar fornecedor:', error);
            showMessage('Erro ao salvar fornecedor: ' + (xhr.responseText || error), 'error');
        }
    });
}

// Função para salvar cultivo
function saveCultivation() {
    const formData = {};
    $('#add-cultivation-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.plant_id = parseInt(formData.plant_id) || 0;
    formData.quantity = parseInt(formData.quantity) || 0;
    
    $.ajax({
        url: `${API_URL}/api/floriculture/cultivation`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            showMessage('Cultivo registrado com sucesso!', 'success');
            $('#add-cultivation-modal').modal('hide');
            $('#add-cultivation-form')[0].reset();
            loadDataFromAPI().catch(() => loadMockData());
        },
        error: function(xhr, status, error) {
            console.error('Erro ao registrar cultivo:', error);
            showMessage('Erro ao registrar cultivo: ' + (xhr.responseText || error), 'error');
        }
    });
}

// Função para salvar venda
function saveSale() {
    const formData = {};
    $('#add-sale-form').serializeArray().forEach(function(item) {
        formData[item.name] = item.value;
    });
    
    // Converter valores numéricos
    formData.plant_id = parseInt(formData.plant_id) || 0;
    formData.quantity = parseInt(formData.quantity) || 0;
    formData.unit_price = parseFloat(formData.unit_price) || 0;
    formData.total_value = parseFloat(formData.total_value) || 0;
    
    $.ajax({
        url: `${API_URL}/api/floriculture/sale`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        headers: {
            'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
        },
        success: function(response) {
            showMessage('Venda registrada com sucesso!', 'success');
            $('#add-sale-modal').modal('hide');
            $('#add-sale-form')[0].reset();
            loadDataFromAPI().catch(() => loadMockData());
        },
        error: function(xhr, status, error) {
            console.error('Erro ao registrar venda:', error);
            showMessage('Erro ao registrar venda: ' + (xhr.responseText || error), 'error');
        }
    });
}

// Função para exibir mensagens
function showMessage(message, type) {
    const messageClass = type === 'success' ? 'positive' : 'negative';
    const icon = type === 'success' ? 'check circle' : 'exclamation triangle';
    
    $('body').append(`
        <div class="ui ${messageClass} message" style="position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;">
            <i class="close icon"></i>
            <i class="${icon} icon"></i>
            <div class="content">
                <div class="header">${type === 'success' ? 'Sucesso' : 'Erro'}</div>
                <p>${message}</p>
            </div>
        </div>
    `);
    
    // Configurar botão de fechar
    $('.ui.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });
    
    // Auto-remover após 5 segundos
    setTimeout(function() {
        $('.ui.message').fadeOut(function() {
            $(this).remove();
        });
    }, 5000);
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}