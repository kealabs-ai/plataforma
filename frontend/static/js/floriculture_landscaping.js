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
    
    $('#add-project-btn').on('click', function() {
        $('#add-project-modal').modal('show');
    });
    
    $('#add-cultivation-btn').on('click', function() {
        $('#add-cultivation-modal').modal('show');
    });
    
    $('#add-sale-btn').on('click', function() {
        $('#add-sale-modal').modal('show');
    });
    
    // Alternar entre campos de planta e projeto no modal de vendas
    $('#sale-type-select').on('change', function() {
        const selectedType = $(this).val();
        if (selectedType === 'Planta') {
            $('#plant-select-field').show();
            $('#project-select-field').hide();
            $('#quantity-field').show();
        } else if (selectedType === 'Projeto') {
            $('#plant-select-field').hide();
            $('#project-select-field').show();
            $('#quantity-field').hide();
        }
    });
    
    // Calcular valor total na venda
    $('#unit-price, [name="quantity"]').on('input', function() {
        const unitPrice = parseFloat($('#unit-price').val()) || 0;
        const quantity = parseInt($('[name="quantity"]').val()) || 1;
        $('#total-value').val((unitPrice * quantity).toFixed(2));
    });
    
    // Carregar dados de exemplo para demonstração
    loadMockData();
    
    // Inicializar gráficos
    initCharts();
});

// Função para carregar dados de exemplo
function loadMockData() {
    // Dados de exemplo para plantas
    const mockPlants = [
        {
            id: 1,
            name: 'Rosa Vermelha',
            scientific_name: 'Rosa gallica',
            category: 'Flores',
            environment: 'Externo',
            sun_needs: 'Pleno Sol',
            watering: '2-3 dias',
            stock: 45,
            price: 15.90,
            image_url: 'https://images.unsplash.com/photo-1559563362-c667ba5f5480?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Rosa vermelha tradicional, perfeita para jardins e arranjos.'
        },
        {
            id: 2,
            name: 'Orquídea Phalaenopsis',
            scientific_name: 'Phalaenopsis sp.',
            category: 'Flores',
            environment: 'Interno',
            sun_needs: 'Meia Sombra',
            watering: 'Semanal',
            stock: 30,
            price: 45.00,
            image_url: 'https://images.unsplash.com/photo-1566550747935-a6f55a696122?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Orquídea elegante de fácil cultivo, ideal para ambientes internos.'
        },
        {
            id: 3,
            name: 'Palmeira Areca',
            scientific_name: 'Dypsis lutescens',
            category: 'Árvores',
            environment: 'Ambos',
            sun_needs: 'Meia Sombra',
            watering: '2-3 dias',
            stock: 15,
            price: 89.90,
            image_url: 'https://images.unsplash.com/photo-1598880940639-090b8d7ff378?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Palmeira elegante que purifica o ar, ideal para decoração interna e externa.'
        },
        {
            id: 4,
            name: 'Suculenta Echeveria',
            scientific_name: 'Echeveria elegans',
            category: 'Suculentas',
            environment: 'Ambos',
            sun_needs: 'Pleno Sol',
            watering: 'Quinzenal',
            stock: 60,
            price: 12.50,
            image_url: 'https://images.unsplash.com/photo-1509423350716-97f9360b4e09?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Suculenta de baixa manutenção, perfeita para iniciantes.'
        },
        {
            id: 5,
            name: 'Grama Esmeralda',
            scientific_name: 'Zoysia japonica',
            category: 'Gramados',
            environment: 'Externo',
            sun_needs: 'Pleno Sol',
            watering: '2-3 dias',
            stock: 100,
            price: 15.00,
            image_url: 'https://images.unsplash.com/photo-1520452112805-c6692c840af0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Grama resistente e de baixa manutenção, ideal para jardins residenciais.'
        },
        {
            id: 6,
            name: 'Buxinho',
            scientific_name: 'Buxus sempervirens',
            category: 'Arbustos',
            environment: 'Externo',
            sun_needs: 'Meia Sombra',
            watering: '2-3 dias',
            stock: 25,
            price: 35.00,
            image_url: 'https://images.unsplash.com/photo-1584478919944-e669c5124e8e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            description: 'Arbusto perfeito para topiaria e bordaduras em jardins formais.'
        }
    ];
    
    // Dados de exemplo para projetos
    const mockProjects = [
        {
            id: 1,
            project_name: 'Jardim Residencial Vila Verde',
            client: 'Maria Silva',
            start_date: '2023-05-15',
            deadline: '2023-06-30',
            area: 120,
            value: 8500.00,
            status: 'Concluído',
            address: 'Rua das Flores, 123',
            description: 'Projeto de jardim residencial com foco em plantas nativas e sustentabilidade.'
        },
        {
            id: 2,
            project_name: 'Praça Empresarial Tech Park',
            client: 'Tech Innovations LTDA',
            start_date: '2023-07-10',
            deadline: '2023-09-15',
            area: 450,
            value: 32000.00,
            status: 'Em Andamento',
            address: 'Av. Tecnologia, 500',
            description: 'Revitalização da praça central do parque empresarial com conceito moderno e sustentável.'
        },
        {
            id: 3,
            project_name: 'Jardim Vertical Edifício Aurora',
            client: 'Condomínio Edifício Aurora',
            start_date: '2023-08-05',
            deadline: '2023-10-10',
            area: 80,
            value: 15000.00,
            status: 'Planejamento',
            address: 'Rua do Sol, 789',
            description: 'Implementação de jardim vertical na fachada principal do edifício residencial.'
        }
    ];
    
    // Atualizar estatísticas
    $('#total-plants').text(mockPlants.reduce((sum, plant) => sum + plant.stock, 0));
    $('#active-projects').text(mockProjects.filter(p => p.status === 'Em Andamento').length);
    $('#monthly-sales').text('R$ ' + (12500).toFixed(2));
    $('#area-cultivated').text('650 m²');
    
    // Preencher grid de plantas
    const plantsGrid = $('#plants-grid');
    plantsGrid.empty();
    
    mockPlants.forEach(plant => {
        plantsGrid.append(`
            <div class="ui card plant-card">
                <div class="image">
                    <img src="${plant.image_url}" alt="${plant.name}">
                </div>
                <div class="content">
                    <a class="header">${plant.name}</a>
                    <div class="meta">
                        <span class="date">${plant.scientific_name}</span>
                    </div>
                    <div class="description">
                        ${plant.description}
                    </div>
                </div>
                <div class="extra content">
                    <span>
                        <i class="leaf icon"></i>
                        ${plant.category}
                    </span>
                    <span class="right floated">
                        R$ ${plant.price.toFixed(2)}
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
                <td><img src="${plant.image_url}" alt="${plant.name}" class="plant-image"></td>
                <td>${plant.name}</td>
                <td>${plant.scientific_name}</td>
                <td>${plant.category}</td>
                <td>${plant.environment}</td>
                <td>${plant.sun_needs}</td>
                <td>${plant.stock}</td>
                <td>R$ ${plant.price.toFixed(2)}</td>
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
    
    // Preencher cards de projetos
    const projectsCards = $('#projects-cards');
    projectsCards.empty();
    
    mockProjects.forEach(project => {
        let statusColor = '';
        switch(project.status) {
            case 'Concluído': statusColor = 'green'; break;
            case 'Em Andamento': statusColor = 'blue'; break;
            case 'Planejamento': statusColor = 'orange'; break;
            case 'Cancelado': statusColor = 'red'; break;
            default: statusColor = 'grey';
        }
        
        projectsCards.append(`
            <div class="ui card">
                <div class="content">
                    <div class="header">${project.project_name}</div>
                    <div class="meta">Cliente: ${project.client}</div>
                    <div class="description">
                        <p>${project.description}</p>
                        <div class="ui list">
                            <div class="item">
                                <i class="calendar icon"></i>
                                <div class="content">Início: ${formatDate(project.start_date)}</div>
                            </div>
                            <div class="item">
                                <i class="calendar check icon"></i>
                                <div class="content">Prazo: ${formatDate(project.deadline)}</div>
                            </div>
                            <div class="item">
                                <i class="expand icon"></i>
                                <div class="content">Área: ${project.area} m²</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="extra content">
                    <span class="left floated">
                        <i class="dollar sign icon"></i>
                        R$ ${project.value.toFixed(2)}
                    </span>
                    <span class="right floated">
                        <div class="ui ${statusColor} label">${project.status}</div>
                    </span>
                </div>
                <div class="ui bottom attached buttons">
                    <button class="ui primary button">Detalhes</button>
                    <button class="ui green button">Editar</button>
                </div>
            </div>
        `);
    });
    
    // Preencher tabela de projetos
    const projectsTable = $('#projects-table-body');
    projectsTable.empty();
    
    mockProjects.forEach(project => {
        let statusClass = '';
        switch(project.status) {
            case 'Concluído': statusClass = 'positive'; break;
            case 'Em Andamento': statusClass = 'warning'; break;
            case 'Planejamento': statusClass = ''; break;
            case 'Cancelado': statusClass = 'negative'; break;
            default: statusClass = '';
        }
        
        projectsTable.append(`
            <tr class="${statusClass}">
                <td>${project.id}</td>
                <td>${project.project_name}</td>
                <td>${project.client}</td>
                <td>${formatDate(project.start_date)}</td>
                <td>${formatDate(project.deadline)}</td>
                <td>${project.area} m²</td>
                <td>${project.status}</td>
                <td>R$ ${project.value.toFixed(2)}</td>
                <td>
                    <div class="ui mini buttons">
                        <button class="ui blue button"><i class="eye icon"></i></button>
                        <button class="ui green button"><i class="edit icon"></i></button>
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
        plantSelect.append(`<option value="${plant.id}">${plant.name}</option>`);
    });
    
    const salePlantSelect = $('#sale-plant-select');
    salePlantSelect.empty();
    salePlantSelect.append('<option value="">Selecione uma planta</option>');
    
    mockPlants.forEach(plant => {
        salePlantSelect.append(`<option value="${plant.id}">${plant.name} - R$ ${plant.price.toFixed(2)}</option>`);
    });
    
    const saleProjectSelect = $('#sale-project-select');
    saleProjectSelect.empty();
    saleProjectSelect.append('<option value="">Selecione um projeto</option>');
    
    mockProjects.forEach(project => {
        saleProjectSelect.append(`<option value="${project.id}">${project.project_name} - R$ ${project.value.toFixed(2)}</option>`);
    });
    
    // Reinicializar dropdowns após preencher
    $('.ui.dropdown').dropdown('refresh');
}

// Função para inicializar gráficos
function initCharts() {
    // Gráfico de cultivo
    const cultivationCtx = document.getElementById('cultivation-chart').getContext('2d');
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
    
    // Gráfico de crescimento
    const growthCtx = document.getElementById('growth-chart').getContext('2d');
    new Chart(growthCtx, {
        type: 'line',
        data: {
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5', 'Semana 6'],
            datasets: [{
                label: 'Taxa de Crescimento',
                data: [5, 10, 15, 25, 32, 40],
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });
    
    // Gráfico de vendas
    const salesCtx = document.getElementById('sales-chart').getContext('2d');
    new Chart(salesCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Vendas (R$)',
                data: [12500, 19000, 15000, 17500, 21000, 22500],
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
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
    
    // Gráfico de vendas por categoria
    const salesByCategoryCtx = document.getElementById('sales-by-category-chart').getContext('2d');
    new Chart(salesByCategoryCtx, {
        type: 'pie',
        data: {
            labels: ['Flores', 'Arbustos', 'Árvores', 'Gramados', 'Suculentas'],
            datasets: [{
                label: 'Vendas por Categoria',
                data: [35, 20, 15, 20, 10],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
    
    // Gráfico de receita
    const revenueCtx = document.getElementById('revenue-chart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Receita',
                data: [12500, 19000, 15000, 17500, 21000, 22500],
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Despesas',
                data: [8000, 12000, 9500, 11000, 13500, 14000],
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });
    
    // Gráfico de top vendedores
    const topSellersCtx = document.getElementById('top-sellers-chart').getContext('2d');
    new Chart(topSellersCtx, {
        type: 'horizontalBar',
        data: {
            labels: ['Rosa Vermelha', 'Orquídea', 'Palmeira Areca', 'Suculenta', 'Grama Esmeralda'],
            datasets: [{
                label: 'Unidades Vendidas',
                data: [120, 90, 45, 180, 95],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true
        }
    });
    
    // Gráfico de tendências sazonais
    const seasonalTrendsCtx = document.getElementById('seasonal-trends-chart').getContext('2d');
    new Chart(seasonalTrendsCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            datasets: [{
                label: 'Flores',
                data: [65, 70, 80, 95, 100, 90, 85, 80, 75, 70, 65, 60],
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Árvores',
                data: [40, 45, 50, 55, 60, 65, 70, 75, 80, 70, 60, 50],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });
    
    // Gráfico de desempenho de projetos
    const projectPerformanceCtx = document.getElementById('project-performance-chart').getContext('2d');
    new Chart(projectPerformanceCtx, {
        type: 'radar',
        data: {
            labels: ['Planejamento', 'Execução', 'Qualidade', 'Prazo', 'Custo', 'Satisfação'],
            datasets: [{
                label: 'Projeto 1',
                data: [85, 90, 95, 80, 75, 95],
                fill: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(255, 99, 132)'
            }, {
                label: 'Projeto 2',
                data: [90, 85, 80, 85, 90, 85],
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                pointBackgroundColor: 'rgb(54, 162, 235)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(54, 162, 235)'
            }]
        },
        options: {
            responsive: true,
            elements: {
                line: {
                    borderWidth: 3
                }
            }
        }
    });
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}