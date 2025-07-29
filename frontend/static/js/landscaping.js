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
    
    // Adicionar item ao orçamento
    $('#add-quote-item').on('click', function() {
        // Adicionar um novo item normalmente
        const newItem = $('.quote-item').first().clone();
        newItem.find('input').val('');
        newItem.find('select').val('');
        $('#quote-items').append(newItem);
        $('.ui.dropdown').dropdown('refresh');
        setupQuoteItemEvents();
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

// Função para carregar dados de exemplo
function loadMockData() {
    // Dados de exemplo para projetos
    const mockProjects = [
        {
            id: 1,
            name: 'Jardim Residencial Vila Verde',
            client_name: 'Maria Silva',
            start_date: '2023-05-15',
            end_date: '2023-06-30',
            area_m2: 120,
            budget: 8500.00,
            status: 'concluído',
            location: 'Rua das Flores, 123',
            description: 'Projeto de jardim residencial com foco em plantas nativas e sustentabilidade.'
        },
        {
            id: 2,
            name: 'Praça Empresarial Tech Park',
            client_name: 'Tech Innovations LTDA',
            start_date: '2023-07-10',
            end_date: '2023-09-15',
            area_m2: 450,
            budget: 32000.00,
            status: 'em_andamento',
            location: 'Av. Tecnologia, 500',
            description: 'Revitalização da praça central do parque empresarial com conceito moderno e sustentável.'
        }
    ];
    
    // Dados de exemplo para fornecedores
    const mockSuppliers = [
        {
            id: 1,
            name: 'Pedras & Jardins',
            contact_person: 'Roberto Almeida',
            phone: '(11) 99876-5432',
            email: 'contato@pedrasejardins.com.br',
            products: 'Pedras decorativas, Cascalho, Areia',
            last_contract: '2023-10-15',
            status: 'Ativo',
            notes: 'Fornecedor de materiais para pavimentação'
        },
        {
            id: 2,
            name: 'Árvores Brasil',
            contact_person: 'Ana Ferreira',
            phone: '(11) 98765-1234',
            email: 'vendas@arvoresbrasil.com.br',
            products: 'Árvores, Arbustos, Palmeiras',
            last_contract: '2023-11-20',
            status: 'Ativo',
            notes: 'Fornecedor especializado em árvores nativas'
        }
    ];
    
    // Dados de exemplo para contatos
    const mockContacts = [
        {
            id: 1,
            name: 'Maria Silva',
            type: 'Cliente',
            email: 'maria.silva@email.com',
            phone: '(11) 98765-4321',
            address: 'Rua das Flores, 123',
            status: 'Ativo',
            company: 'Residencial',
            last_contact: '2023-08-15',
            avatar: 'https://randomuser.me/api/portraits/women/65.jpg'
        },
        {
            id: 2,
            name: 'Tech Innovations LTDA',
            type: 'Cliente',
            email: 'contato@techinnovations.com',
            phone: '(11) 3456-7890',
            address: 'Av. Tecnologia, 500',
            status: 'Ativo',
            company: 'Tech Innovations LTDA',
            last_contact: '2023-07-22',
            avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
        }
    ];
    
    // Atualizar estatísticas
    $('#total-projects').text(mockProjects.length);
    $('#active-projects').text(mockProjects.filter(p => p.status === 'em_andamento' || p.status === 'planejamento').length);
    $('#total-clients').text(mockContacts.filter(c => c.type === 'Cliente').length);
    $('#monthly-revenue').text('R$ ' + (32000).toFixed(2));
    
    // Preencher grid de projetos
    const projectsGrid = $('#projects-grid');
    projectsGrid.empty();
    mockProjects.forEach(project => {
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
    
    // Reinicializar dropdowns após preencher
    $('.ui.dropdown').dropdown('refresh');
}

// Função auxiliar para formatar datas
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}
    $(document).ready(function() {
        // Inicializar dropdowns e tabs
        $('.ui.dropdown').dropdown();
        $('.menu .item').tab();
        
        // Carregar lista de projetos
        loadProjectsFromLandscapingJS();
        
        // Carregar dashboard quando a aba for selecionada
        $('.menu .item[data-tab="dashboard"]').on('click', function() {
            loadDashboard();
        });
        
        // Configurar eventos
        $('#btn-filter').on('click', function() {
            loadProjectsFromLandscapingJS();
        });
        
        $('#project-form').on('submit', function(e) {
            e.preventDefault();
            saveProject();
        });

        // Carregar dados dos serviços quando a aba de serviços for selecionada
        $('.menu .item[data-tab="services"]').on('click', function() {
            loadServices();
        });
    });
    
    // Função para carregar lista de projetos do landscaping.js
    function loadProjectsFromLandscapingJS() {
        const projectType = $('#filter-project-type').val() || "";
        const status = $('#filter-status').val() || "";
        const clientName = $('#filter-client').val() || "";

        // Usar a função loadLandscapingDataFromAPI do landscaping.js
        loadLandscapingDataFromAPI()
            .then(data => {
                let projects = data.projects || [];
                
                // Aplicar filtros se necessário
                if (projectType) {
                    projects = projects.filter(p => p.project_type === projectType);
                }
                if (status) {
                    projects = projects.filter(p => p.status === status);
                }
                if (clientName) {
                    projects = projects.filter(p => p.client_name && p.client_name.toLowerCase().includes(clientName.toLowerCase()));
                }
                renderProjectsTable(projects);
                renderPagination(1, 1, 'pagination', 'loadProjectsFromLandscapingJS');
            })
            .catch(error => {
                console.error('Erro ao carregar projetos:', error);
                showMessage('Erro ao carregar projetos', 'error');
                
                // Usar dados mockados em caso de erro
                const mockProjects = window.mockProjects || [];
                renderProjectsTable(mockProjects);
                renderPagination(1, 1, 'pagination', 'loadProjectsFromLandscapingJS');
            });
    }
    
    // Função para renderizar tabela de projetos
    function renderProjectsTable(projects) {
        const tbody = $('#projects-table-body');
        tbody.empty();
        
        if (projects.length === 0) {
            tbody.append('<tr><td colspan="9" class="center aligned">Nenhum projeto encontrado</td></tr>');
            return;
        }
        
        projects.forEach(function(project) {
            const startDate = new Date(project.start_date); // Cria um objeto Date a partir da string
            const endDate = new Date(project.expected_end_date); // Cria outro objeto Date
            const diffTime = Math.abs(endDate.getTime() - startDate.getTime());
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            const row = `
                <tr>
                    <td>${project.id}</td>
                    <td>${project.name}</td>
                    <td>${project.client_name || '-'}</td>
                    <td>${formatDate(project.start_date)}</td>
                    <td>${diffDays + ' dias' || '-'}</td>
                    <td>${project.area_m2 || '-'}</td> 
                    <td>${project.status}</td>
                    <td>R$ ${(Number(project.budget) || 0).toFixed(2)}</td>
                    <td>
                        <button class="ui mini icon button" onclick="viewProject(${project.id})"><i class="eye icon"></i></button>
                        <button class="ui mini icon primary button" onclick="editProject(${project.id})"><i class="edit icon"></i></button>
                        <button class="ui mini icon negative button" onclick="deleteProject(${project.id})"><i class="trash icon"></i></button>
                    </td>
                </tr>
            `;
            tbody.append(row);
        });
        loadDashboard();
        loadMaintenanceKanban();
    }
    
    // Função para renderizar paginação
    function renderPagination(currentPage, totalPages, elementId, callbackName) {
        const pagination = $(`#${elementId}`);
        pagination.empty();
        
        if (totalPages <= 1) {
            return;
        }
        
        // Botão anterior
        pagination.append(`
            <a class="item ${currentPage === 1 ? 'disabled' : ''}" 
               onclick="${currentPage > 1 ? callbackName + '(' + (currentPage - 1) + ')' : ''}">
                <i class="left chevron icon"></i>
            </a>
        `);
        
        // Páginas
        for (let i = 1; i <= totalPages; i++) {
            pagination.append(`
                <a class="item ${i === currentPage ? 'active' : ''}" 
                   onclick="${callbackName}(${i})">
                    ${i}
                </a>
            `);
        }
        
        // Botão próximo
        pagination.append(`
            <a class="item ${currentPage === totalPages ? 'disabled' : ''}" 
               onclick="${currentPage < totalPages ? callbackName + '(' + (currentPage + 1) + ')' : ''}">
                <i class="right chevron icon"></i>
            </a>
        `);
    }
    
    // Função para carregar dashboard
    function loadDashboard() {
        $.ajax({
            url: `${API_URL}/api/landscaping/dashboard`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            success: function(data) {
                // Atualizar estatísticas
                $('#total-projects').text(data.projects_summary.total_projects);
                $('#active-projects').text(data.projects_summary.active_projects);
                $('#total-clients').text(data.quantity_clients || 0);
                $('#completed-projects').text(data.projects_summary.completed_projects);
                $('#budget-percentage').text(`${data.budget_summary.percentage.toFixed(0)}%`);
                
                // Verificar se estamos na aba de dashboard antes de tentar renderizar gráficos
                if ($('.menu .item[data-tab="dashboard"]').hasClass('active')) {
                    // Renderizar gráficos
                    renderProjectTypesChart(data.projects_by_type);
                    renderTaskStatusChart(data.tasks_by_status);
                    renderExpensesChart(data.materials_by_category);
                    renderMonthlyProgressChart(data.monthly_progress);
                }
            },
            error: function(error) {
                console.error('Erro ao carregar dados do dashboard:', error);
                showMessage('Erro ao carregar dados do dashboard', 'error');
                
                // Usar dados mockados em caso de erro
                const mockData = {
                    projects_summary: {
                        total_projects: 10,
                        active_projects: 6,
                        completed_projects: 3,
                        cancelled_projects: 1
                    },
                    projects_by_type: [
                        {type: "Residencial", count: 5},
                        {type: "Comercial", count: 3},
                        {type: "Público", count: 2}
                    ],
                    budget_summary: {
                        total_budget: 250000.0,
                        total_spent: 180000.0,
                        percentage: 72.0
                    },
                    tasks_by_status: [
                        {status: "Pendente", count: 15},
                        {status: "Em Andamento", count: 22},
                        {status: "Concluída", count: 48}
                    ],
                    materials_by_category: [
                        {category: "Plantas", total: 45000.0},
                        {category: "Materiais de Construção", total: 65000.0},
                        {category: "Ferramentas", total: 12000.0},
                        {category: "Outros", total: 8000.0}
                    ],
                    monthly_progress: [
                        {month: "2024-01", completed_tasks: 12},
                        {month: "2024-02", completed_tasks: 18},
                        {month: "2024-03", completed_tasks: 15},
                        {month: "2024-04", completed_tasks: 20}
                    ]
                };
                
                // Atualizar estatísticas com dados mockados
                $('#total-projects').text(mockData.projects_summary.total_projects);
                $('#active-projects').text(mockData.projects_summary.active_projects);
                $('#completed-projects').text(mockData.projects_summary.completed_projects);
                $('#budget-percentage').text(`${mockData.budget_summary.percentage.toFixed(0)}%`);
                
                // Renderizar gráficos com dados mockados
                renderProjectTypesChart(mockData.projects_by_type);
                renderTaskStatusChart(mockData.tasks_by_status);
                renderExpensesChart(mockData.materials_by_category);
                renderMonthlyProgressChart(mockData.monthly_progress);
            }
        });
    }
    
    // Função para renderizar gráfico de tipos de projetos
    function renderProjectTypesChart(data) {
        const chartElement = document.getElementById('chart-project-types');
        if (!chartElement) return; // Se o elemento não existir, sair da função
        
        const ctx = chartElement.getContext('2d');
        
        if (window.projectTypesChart) {
            window.projectTypesChart.destroy();
        }
        
        window.projectTypesChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(item => item.type),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Função para renderizar gráfico de status de tarefas
    function renderTaskStatusChart(data) {
        const chartElement = document.getElementById('chart-task-status');
        if (!chartElement) return; // Se o elemento não existir, sair da função
        
        const ctx = chartElement.getContext('2d');
        
        if (window.taskStatusChart) {
            window.taskStatusChart.destroy();
        }
        
        window.taskStatusChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.status),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(75, 192, 192, 0.6)'
                    ],
                    borderColor: [
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Função para renderizar gráfico de despesas
    function renderExpensesChart(data) {
        const chartElement = document.getElementById('chart-expenses');
        if (!chartElement) return; // Se o elemento não existir, sair da função
        
        const ctx = chartElement.getContext('2d');
        
        if (window.expensesChart) {
            window.expensesChart.destroy();
        }
        
        window.expensesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.category),
                datasets: [{
                    label: 'Valor (R$)',
                    data: data.map(item => item.total),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
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
    // Função para renderizar gráfico de progresso mensal
    function renderMonthlyProgressChart(data) {
        const chartElement = document.getElementById('chart-monthly-progress');
        if (!chartElement) return; // Se o elemento não existir, sair da função
        
        const ctx = chartElement.getContext('2d');
        
        if (window.monthlyProgressChart) {
            window.monthlyProgressChart.destroy();
        }
        
        window.monthlyProgressChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => formatMonth(item.month)),
                datasets: [{
                    label: 'Tarefas Concluídas',
                    data: data.map(item => item.completed_tasks),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    tension: 0.4
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
    
    // Função para salvar projeto
    function saveProject() {
        const formData = {};
        $('#project-form').serializeArray().forEach(function(item) {
            formData[item.name] = item.value;
        });
        
        // Converter valores numéricos
        formData.area_m2 = parseFloat(formData.area_m2);
        formData.budget = parseFloat(formData.budget);
        
        $.ajax({
            url: API_URL + '/api/landscaping/project',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            success: function(response) {
                showMessage('Projeto salvo com sucesso', 'success');
                $('#project-form')[0].reset();
                $('.menu .item[data-tab="list"]').tab('change tab', 'list');
                loadProjectsFromLandscapingJS();
            },
            error: function(error) {
                console.error('Erro ao salvar projeto:', error);
                showMessage('Erro ao salvar projeto', 'error');
            }
        });
    }
    
    // Função para visualizar projeto
    function viewProject(id) {
        // Redirecionar para a página de detalhes do projeto
        window.location.href = `/landscaping/project/${id}`;
    }
    
    // Função para editar projeto
    function editProject(id) {
        $.ajax({
            url: `${API_URL}/api/landscaping/project/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            success: function(project) {
                // Preencher formulário
                $('#project-form')[0].reset();
                $('#project-form [name="name"]').val(project.name);
                $('#project-form [name="client_name"]').val(project.client_name);
                $('#project-form [name="project_type"]').val(project.project_type).trigger('change');
                $('#project-form [name="area_m2"]').val(project.area_m2);
                $('#project-form [name="budget"]').val(project.budget);
                $('#project-form [name="start_date"]').val(formatDateForInput(project.start_date));
                if (project.expected_end_date) {
                    $('#project-form [name="expected_end_date"]').val(formatDateForInput(project.expected_end_date));
                }
                $('#project-form [name="status"]').val(project.status).trigger('change');
                $('#project-form [name="address"]').val(project.location || '');
                $('#project-form [name="description"]').val(project.description || '');
                
                // Mudar para a aba de edição
                $('.menu .item[data-tab="new"]').tab('change tab', 'new');
                
                // Configurar formulário para edição
                $('#project-form').data('edit-id', id);
                $('#project-form').off('submit').on('submit', function(e) {
                    e.preventDefault();
                    updateProject(id);
                });
            },
            error: function(error) {
                console.error('Erro ao carregar projeto para edição:', error);
                showMessage('Erro ao carregar projeto para edição', 'error');
            }
        });
    }
    
    // Função para atualizar projeto
    function updateProject(id) {
        const formData = {};
        $('#project-form').serializeArray().forEach(function(item) {
            formData[item.name] = item.value;
        });
        
        // Converter valores numéricos
        formData.area_m2 = parseFloat(formData.area_m2);
        formData.budget = parseFloat(formData.budget);
        
        // Adicionar user_id no corpo da requisição
        formData.user_id = 1; // Usando user_id fixo para teste
        
        $.ajax({
            url: `${API_URL}/api/landscaping/project/${id}`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            success: function(response) {
                showMessage('Projeto atualizado com sucesso', 'success');
                $('#project-form')[0].reset();
                $('#project-form').removeData('edit-id');
                $('#project-form').off('submit').on('submit', function(e) {
                    e.preventDefault();
                    saveProject();
                });
                $('.menu .item[data-tab="list"]').tab('change tab', 'list');
                loadProjectsFromLandscapingJS();
            },
            error: function(error) {
                console.error('Erro ao atualizar projeto:', error);
                showMessage('Erro ao atualizar projeto', 'error');
            }
        });
    }
    
    // Função para excluir projeto
    function deleteProject(id) {
        if (confirm('Tem certeza que deseja excluir este projeto?')) {
            $.ajax({
                url: `${API_URL}/api/landscaping/project/${id}`,
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + getToken()
                },
                success: function(response) {
                    showMessage('Projeto excluído com sucesso', 'success');
                    loadProjectsFromLandscapingJS();
                },
                error: function(error) {
                    console.error('Erro ao excluir projeto:', error);
                    showMessage('Erro ao excluir projeto', 'error');
                }
            });
        }
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
        if (isNaN(date.getTime())) {
            // Se a data não for válida, tentar formatar a string diretamente
            if (typeof dateString === 'string' && dateString.includes('-')) {
                return dateString.split('T')[0]; // Remove a parte de hora se existir
            }
            return '';
        }
        return date.toISOString().split('T')[0];
    }
    
    // Função para formatar mês
    function formatMonth(monthString) {
        if (!monthString) return '-';
        const [year, month] = monthString.split('-');
        const date = new Date(year, month - 1);
        return date.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
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
       // Função para carregar os dados de manutenção e exibir no Kanban board
    function loadMaintenanceKanban() {
        // Limpar as colunas do Kanban
        $('#planning-column').empty();
        $('#in-progress-column').empty();
        $('#review-column').empty();
        $('#completed-column').empty();
        
        // Fazer requisição Ajax para o endpoint /maintenance
        $.ajax({
            url: `${API_URL}/api/landscaping/maintenance`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                // Processar os itens retornados
                if (response && response.items && response.items.length > 0) {
                    response.items.forEach(function(item) {
                        // Criar o card
                        const card = createMaintenanceCard(item);
                        
                        // Posicionar o card na coluna correta com base no status
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
                                // Se o status não corresponder a nenhuma coluna específica,
                                // colocar na coluna de planejamento
                                $('#planning-column').append(card);
                        }
                    });
                    
                    // Inicializar os dropdowns após adicionar os cards
                    $('.status-dropdown').dropdown({
                        onChange: function(value, text, $choice) {
                            // Obter o ID do card
                            const cardId = $(this).closest('.kanban-card').data('id');
                            
                            // Atualizar o status via API
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
    
    // Função para atualizar o status de uma manutenção
    function updateMaintenanceStatus(maintenanceId, newStatus) {
        // Primeiro, obter os detalhes da manutenção para saber o status anterior e o custo
        $.ajax({
            url: `${API_URL}/api/landscaping/maintenance/${maintenanceId}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(maintenanceData) {
                const oldStatus = maintenanceData.status;
                const cost = parseFloat(maintenanceData.cost || 0);
                
                // Agora atualizar o status
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
                        
                        // Atualizar a receita mensal com base nas manutenções concluídas
                        updateMonthlyRevenue();
                        
                        // Recarregar o Kanban board para refletir a mudança
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
    
    // Função para atualizar a receita mensal
    function updateMonthlyRevenue() {
        // Buscar todas as manutenções
        $.ajax({
            url: `${API_URL}/api/landscaping/maintenance`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                // Calcular o somatório dos custos de todas as manutenções concluídas
                let totalRevenue = 0;
                if (response && response.items && response.items.length > 0) {
                    // Filtrar apenas as manutenções com status Concluído
                    const completedItems = response.items.filter(item => item.status === 'Concluído');
                    totalRevenue = completedItems.reduce((sum, item) => {
                        return sum + (parseFloat(item.cost) || 0);
                    }, 0);
                }
                
                // Atualizar o valor na tela
                $('#monthly-revenue').text('R$ ' + totalRevenue.toFixed(2));
            },
            error: function(error) {
                console.error('Erro ao calcular receita mensal:', error);
                // Em caso de erro, definir um valor padrão
                $('#monthly-revenue').text('R$ 0.00');
            }
        });
    }
    
    // Função para criar um card de manutenção
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
    
    // Função para formatar data
    function formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    }
    
    // Carregar os dados quando a aba de manutenção for selecionada
    $('.menu .item[data-tab="maintenance"]').on('click', function() {
        loadMaintenanceKanban();
    });
    
    // Também carregar os dados quando a página for carregada, se a aba de manutenção estiver ativa
    $(document).ready(function() {
        // Atualizar a receita mensal ao carregar a página
        updateMonthlyRevenue();
        
        if ($('.menu .item[data-tab="maintenance"]').hasClass('active')) {
            loadMaintenanceKanban();
        }
    });
        // Carregar dados dos clientes quando a aba de contatos for selecionada
    $('.menu .item[data-tab="contacts"]').on('click', function() {
        loadClients();
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
                        // Definir a classe CSS com base no status
                        let statusClass = '';
                        if (client.status === 'Ativo') statusClass = 'positive';
                        else if (client.status === 'Inativo') statusClass = 'negative';
                        else if (client.status === 'Lead') statusClass = 'warning';
                        
                        // Formatar o endereço completo
                        const address = client.address || '';
                        const cityState = client.city && client.state ? `${client.city} - ${client.state}` : (client.city || client.state || '');
                        
                        // Formatar a data do último contato
                        const lastContact = client.updated_at ? formatDate(client.updated_at) : '-';
                        
                        // Determinar qual imagem usar
                        let avatarImg;
                        if (client.img_profile && client.img_profile.trim() !== '') {
                            avatarImg = `<img src="${client.img_profile}" class="contact-avatar" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(client.client_name)}&background=random'">`;
                        } else {
                            avatarImg = `<img src="https://ui-avatars.com/api/?name=${encodeURIComponent(client.client_name)}&background=random" class="contact-avatar">`;
                        }
                        
                        // Adicionar a linha na tabela
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
                    
                    // Configurar paginação
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
    
    // Função para carregar uma página específica de clientes
    function loadClientsPage(page) {
        loadClients(page);
    }
    
    // Configurar evento para mudança de quantidade por página
    $(document).on('change', '#contacts-page-size', function() {
        loadClients(1, $(this).val());
    });
    
    // Função para renderizar paginação dos contatos
    function renderContactsPagination(currentPage, totalPages, totalItems, pageSize) {
        const pagination = $('#contacts-pagination');
        pagination.empty();
        
        if (totalPages <= 1) {
            return;
        }
        
        // Botão anterior
        const prevDisabled = currentPage === 1 ? 'disabled' : '';
        pagination.append(`
            <a class="item ${prevDisabled}" onclick="${currentPage > 1 ? 'loadClientsPage(' + (currentPage - 1) + ')' : ''}">
                <i class="left chevron icon"></i>
            </a>
        `);
        
        // Páginas
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
        
        // Botão próximo
        const nextDisabled = currentPage === totalPages ? 'disabled' : '';
        pagination.append(`
            <a class="item ${nextDisabled}" onclick="${currentPage < totalPages ? 'loadClientsPage(' + (currentPage + 1) + ')' : ''}">
                <i class="right chevron icon"></i>
            </a>
        `);
        
        // Informações de paginação
        const startItem = (currentPage - 1) * pageSize + 1;
        const endItem = Math.min(currentPage * pageSize, totalItems);
        $('#contacts-pagination-info').html(`
            Mostrando ${startItem} a ${endItem} de ${totalItems} contatos
        `);
    }
    
    // Funções para visualizar, editar e excluir clientes
    function viewClient(id) {
        $.ajax({
            url: `${API_URL}/api/landscaping/client/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(client) {
                // Criar modal de visualização
                $('body').append(`
                    <div class="ui modal" id="view-client-modal">
                        <i class="close icon"></i>
                        <div class="header">
                            ${client.client_name}
                        </div>
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
                            <div class="ui button" onclick="$('#view-client-modal').modal('hide')">
                                Fechar
                            </div>
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
                // Preencher o formulário com os dados do cliente
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
                
                // Atualizar os dropdowns
                $('.ui.dropdown').dropdown('refresh');
                
                // Alterar o título do modal
                $('#add-contact-modal .header').text('Editar Contato');
                
                // Alterar o comportamento do botão de salvar
                $('#save-contact-btn').off('click').on('click', function() {
                    updateClient(id);
                });
                
                // Mostrar o modal
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
        
        // Mapear campos do formulário para os campos da API
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
            url: `${API_URL}/api/landscaping/client/${id}?user_id=1`, // Usando user_id fixo para teste
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
                url: `${API_URL}/api/landscaping/client/${id}?user_id=1`, // Usando user_id fixo para teste
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
        
        // Mapear campos do formulário para os campos da API
        const clientData = {
            user_id: 1, // Usando user_id fixo para teste
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
     // Carregar dados dos orçamentos quando a aba de orçamentos for selecionada
    $('.menu .item[data-tab="quotes"]').on('click', function() {
        loadQuotes();
    });
    
    // Função para carregar os orçamentos
    function loadQuotes() {
        $.ajax({
            url: `${API_URL}/api/landscaping/quote`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                const tbody = $('#quotes-table-body');
                tbody.empty();
                
                if (response && response.items && response.items.length > 0) {
                    response.items.forEach(function(quote) {
                        // Definir a classe CSS com base no status
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
                        
                        // Formatar as datas
                        const createdDate = quote.created_date ? formatDate(quote.created_date) : '-';
                        const validUntil = quote.valid_until ? formatDate(quote.valid_until) : '-';
                        
                        // Adicionar a linha na tabela
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
                    
                    // Configurar paginação
                    renderPagination(response.page, response.total_pages, 'quotes-pagination', 'loadQuotesPage');
                } else {
                    tbody.append('<tr><td colspan="8" class="center aligned">Nenhum orçamento encontrado</td></tr>');
                }
            },
            error: function(error) {
                console.error('Erro ao carregar orçamentos:', error);
                $('#quotes-table-body').html('<tr><td colspan="8" class="center aligned error">Erro ao carregar orçamentos</td></tr>');
            }
        });
    }
    
    // Função para carregar uma página específica de orçamentos
    function loadQuotesPage(page) {
        $.ajax({
            url: `${API_URL}/api/landscaping/quote?page=${page}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                // Mesmo código da função loadQuotes
                // ...
            },
            error: function(error) {
                console.error('Erro ao carregar orçamentos:', error);
            }
        });
    }
    
    // Funções para visualizar, editar e inativar orçamentos
    function viewQuote(id) {
        $.ajax({
            url: `${API_URL}/api/landscaping/quote/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(quote) {
                // Criar modal de visualização
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
                
                // Criar e mostrar modal
                $('body').append(`
                    <div class="ui modal" id="view-quote-modal">
                        <i class="close icon"></i>
                        <div class="header">
                            Orçamento #${quote.id}
                        </div>
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
                            <div class="ui button" onclick="$('#view-quote-modal').modal('hide')">
                                Fechar
                            </div>
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
        // Buscar os dados do orçamento para edição
        $.ajax({
            url: `${API_URL}/api/landscaping/quote/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(quote) {
                // Limpar o formulário
                $('#add-quote-form')[0].reset();
                
                // Limpar todas as linhas da tabela
                $('#tableBody').empty();
                
                // Preencher os campos do formulário
                $('#add-quote-form select[name="client_id"]').val(quote.client_id).trigger('change');
                $('#add-quote-form input[name="valid_until"]').val(formatDateForInput(quote.valid_until));
                $('#add-quote-form textarea[name="description"]').val(quote.description);
                $('#add-quote-form textarea[name="notes"]').val(quote.notes || '');
                $('#add-quote-form input[name="discount"]').val(0); // Reset discount
                
                // Carregar serviços para os itens
                $.ajax({
                    url: `${API_URL}/api/landscaping/service`,
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
                    },
                    success: function(servicesResponse) {
                        const services = servicesResponse.items || [];
                        
                        // Resetar o total geral
                        $('#grandTotal').val('0.00');
                        $('#quote-total-value').val('0.00');
                        
                        // Adicionar os itens do orçamento à tabela
                        if (quote.items && quote.items.length > 0) {
                            quote.items.forEach(function(item) {
                                // Criar uma nova linha para a tabela
                                const rowHtml = `
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
                                        <td><div class="ui input"><input type="number" class="quantity-input" value="${item.quantity}" min="1"></div></td>
                                        <td><div class="ui input"><input type="number" step="0.01" class="price-input" value="${parseFloat(item.unit_price).toFixed(2)}"></div></td>
                                        <td><div class="ui input"><input type="number" step="0.01" class="subtotal-input" readonly value="${(item.quantity * item.unit_price).toFixed(2)}"></div></td>
                                        <td class="center aligned"><button type="button" class="ui icon red mini button remove-item"><i class="trash icon"></i></button></td>
                                    </tr>
                                `;
                                
                                // Adicionar a linha à tabela
                                $('#tableBody').append(rowHtml);
                                
                                // Obter a linha adicionada
                                const $row = $('#tableBody tr').last();
                                
                                // Preencher o dropdown de serviços
                                services.forEach(function(service) {
                                    const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                                    $row.find('.service-select .menu').append(option);
                                });
                                
                                // Inicializar o dropdown e selecionar o serviço
                                $row.find('.service-select').dropdown({
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
                                        
                                        // Se este não é a primeira linha e um serviço foi selecionado, consolidar os itens
                                        if (!$row.is($('#tableBody tr').first()) && value) {
                                            consolidateQuoteItems();
                                        }
                                    }
                                });
                                
                                // Selecionar o serviço correto
                                $row.find('.service-select').dropdown('set selected', item.service_id);
                            });
                            
                            // Calcular o total
                            calculateQuoteTotal();
                        } else {
                            // Se não há itens, adicionar uma linha vazia
                            const emptyRowHtml = `
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
                            
                            // Adicionar a linha vazia à tabela
                            $('#tableBody').append(emptyRowHtml);
                            
                            // Obter a linha adicionada
                            const $row = $('#tableBody tr').first();
                            
                            // Preencher o dropdown de serviços
                            services.forEach(function(service) {
                                const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                                $row.find('.service-select .menu').append(option);
                            });
                            
                            // Inicializar o dropdown
                            $row.find('.service-select').dropdown({
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
                        
                        // Configurar eventos para os itens da tabela
                        setupQuoteItemEvents();
                        
                        // Alterar o título do modal
                        $('#add-quote-modal .header').text('Editar Orçamento');
                        
                        // Alterar o comportamento do botão de salvar
                        $('#save-quote-btn').off('click').on('click', function() {
                            updateQuote(id);
                        });
                        
                        // Mostrar o modal e impedir que feche ao clicar fora
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
    
    function inactivateQuote(id) {
        if (confirm('Tem certeza que deseja inativar este orçamento?')) {
            $.ajax({
                url: `${API_URL}/api/landscaping/quote/${id}?user_id=1`, // Usando user_id fixo para teste
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
    
    // O botão de salvar orçamento é configurado no $(document).ready()
    
    // Carregar serviços para o dropdown de itens do orçamento
   
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
                    
                    // Configurar paginação
                    renderPagination(response.page, response.total_pages, 'services-pagination', 'loadServicesPage');
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
       // Função para carregar uma página específica de serviços
    function loadServicesPage(page) {
        $.ajax({
            url: `http://localhost:8000/api/landscaping/service?page=${page}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                loadServices();
            },
            error: function(error) {
                console.error('Erro ao carregar serviços:', error);
            }
        });
    }
   
     // Funções para visualizar, editar e inativar serviços
    function viewService(id) {
        $.ajax({
            url: `http://localhost:8000/api/landscaping/service/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(service) {
                // Criar modal de visualização
                $('body').append(`
                    <div class="ui modal" id="view-service-modal">
                        <i class="close icon"></i>
                        <div class="header">
                            ${service.service_name}
                        </div>
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
                                        <p>R$ ${parseFloat(service.base_price).toFixed(2)}</p>
                                    </div>
                                </div>
                                <div class="field">
                                    <label>Descrição</label>
                                    <p>${service.description}</p>
                                </div>
                            </div>
                        </div>
                        <div class="actions">
                            <div class="ui button" onclick="$('#view-service-modal').modal('hide')">
                                Fechar
                            </div>
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
            url: `http://localhost:8000/api/landscaping/service/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(service) {
                // Preencher o formulário com os dados do serviço
                $('#add-service-form [name="service_name"]').val(service.service_name);
                $('#add-service-form [name="category"]').val(service.category);
                $('#add-service-form [name="description"]').val(service.description);
                $('#add-service-form [name="average_duration"]').val(service.average_duration);
                $('#add-service-form [name="base_price"]').val(service.base_price);
                $('#add-service-form [name="status"]').val(service.status);
                
                // Atualizar os dropdowns
                $('.ui.dropdown').dropdown('refresh');
                
                // Alterar o título do modal
                $('#add-service-modal .header').text('Editar Serviço');
                
                // Alterar o comportamento do botão de salvar
                $('#save-service-btn').off('click').on('click', function() {
                    updateService(id);
                });
                
                // Mostrar o modal
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
            url: `http://localhost:8000/api/landscaping/service/${id}?user_id=1`, // Usando user_id fixo para teste
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
                url: `http://localhost:8000/api/landscaping/service/${id}?user_id=1`, // Usando user_id fixo para teste
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
    
    // Configurar o botão de salvar serviço
    $('#save-service-btn').on('click', function() {
        saveService();
    });
    
    function saveService() {
        const formData = {};
        $('#add-service-form').serializeArray().forEach(function(item) {
            formData[item.name] = item.value;
        });
        
        // Adicionar id_user fixo para teste (em vez de user_id)
        formData.user_id = 1; // Mantemos user_id no objeto JS, mas o backend vai usar como id_user
        
        $.ajax({
            url: 'http://localhost:8000/api/landscaping/service',
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
    
    // Função para atualizar orçamento
    function updateQuote(id) {
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
        
        // Obter o nome do cliente selecionado
        const clientName = $('#add-quote-form select[name="client_id"] option:selected').text();
        
        // Preparar dados para envio
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
        
        console.log('Atualizando orçamento:', quoteData);
        
        $.ajax({
            url: `${API_URL}/api/landscaping/quote/${id}?user_id=${quoteData.user_id}`,
            method: 'PUT', // Usando PUT conforme implementado na API
            contentType: 'application/json',
            data: JSON.stringify(quoteData),
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                alert('Orçamento atualizado com sucesso!');
                $('#add-quote-modal').modal('hide');
                $('#add-quote-form')[0].reset();
                
                // Restaurar o título e comportamento padrão do modal
                $('#add-quote-modal .header').text('Novo Orçamento');
                $('#save-quote-btn').off('click').on('click', function() {
                    $('#save-quote-btn').trigger('click');
                });
                
                // Recarregar lista de orçamentos
                loadQuotes();
            },
            error: function(xhr, status, error) {
                console.error('Erro ao atualizar orçamento:', error);
                console.error('Status:', status);
                console.error('Resposta:', xhr.responseText);
                alert('Erro ao atualizar orçamento: ' + (xhr.responseText || error));
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
        });
        
        // Carregar orçamentos se a aba estiver ativa inicialmente
        if ($('.menu .item[data-tab="quotes"]').hasClass('active')) {
            loadQuotes();
        }
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
                // Limpar as colunas do quadro Kanban
                $('#planning-column-project').empty();
                $('#in-progress-column-project').empty();
                $('#review-column-project').empty();
                $('#completed-column-project').empty();
                
                // Limpar a tabela
                const tbody = $('#projects-table-body');
                tbody.empty();
                
                if (response && response.items && response.items.length > 0) {
                    // Distribuir os projetos nas colunas do quadro Kanban
                    response.items.forEach(function(project) {
                        // Criar o card do projeto
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
                        
                        // Adicionar o card na coluna apropriada
                        if (project.status === 'Planejamento' || project.status === 'planejamento') {
                            $('#planning-column-project').append(projectCard);
                        } else if (project.status === 'Em Andamento' || project.status === 'em_andamento') {
                            $('#in-progress-column-project').append(projectCard);
                        } else if (project.status === 'Revisão' || project.status === 'revisao') {
                            $('#review-column-project').append(projectCard);
                        } else if (project.status === 'Concluído' || project.status === 'concluido') {
                            $('#completed-column-project').append(projectCard);
                        }
                        
                        // Adicionar linha na tabela
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
                    
                    // Configurar paginação
                    renderPagination(response.page, response.total_pages, 'projects-pagination', 'loadProjectsPage');
                    
                    // Inicializar os dropdowns de status
                    $('.status-dropdown-project').dropdown({
                        onChange: function(value, text, $selectedItem) {
                            // Obter o ID do card/projeto
                            const cardId = $(this).closest('.kanban-card-project').data('id');
                            if (cardId) {
                                // Atualizar o status via API
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
    
    // Função para carregar uma página específica de projetos
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
    
    // Funções para visualizar, editar e excluir projetos
    function viewProject(id) {
        $.ajax({
            url: `${API_URL}/api/landscaping/project/${id}`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(project) {
                // Garantir que os campos de data estejam no formato correto
                if (project.start_date && typeof project.start_date === 'string') {
                    project.start_date = project.start_date;
                }
                if (project.end_date && typeof project.end_date === 'string') {
                    project.end_date = project.end_date;
                }
                // Criar modal de visualização
                $('body').append(`
                    <div class="ui modal" id="view-project-modal">
                        <i class="close icon"></i>
                        <div class="header">
                            ${project.name}
                        </div>
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
                            <div class="ui button" onclick="$('#view-project-modal').modal('hide')">
                                Fechar
                            </div>
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
        // Implementação pendente
        alert('Editar projeto ' + id + ' (implementação pendente)');
    }
    
    function deleteProject(id) {
        if (confirm('Tem certeza que deseja excluir este projeto?')) {
            $.ajax({
                url: `${API_URL}/api/landscaping/project/${id}?user_id=1`, // Usando user_id fixo para teste
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
    
    // Função para atualizar o status de um projeto
    function updateProjectStatus(projectId, newStatus) {
        // Usar o endpoint otimizado para atualizar apenas o status
        $.ajax({
            url: `${API_URL}/api/landscaping/project/${projectId}/status?user_id=1&status=${encodeURIComponent(newStatus)}`, // Usando user_id fixo para teste
            method: 'PATCH',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                // Encontrar o card do projeto
                const card = $(`.kanban-card-project[data-id="${projectId}"]`);
                
                // Determinar a coluna de destino com base no novo status
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
                
                // Mover o card para a nova coluna com animação
                if (card.length && targetColumn) {
                    // Salvar o conteúdo do card antes de movê-lo
                    const cardContent = card.html();
                    
                    // Efeito de destaque antes de mover
                    card.addClass('transition');
                    
                    // Remover o card da coluna atual
                    card.detach();
                    
                    // Adicionar o card à nova coluna
                    targetColumn.append(card);
                    
                    // Atualizar o valor do status no dropdown
                    card.find('input[name="status"]').val(newStatus);
                    card.find('.text').text(newStatus);
                    
                    // Reinicializar o dropdown
                    card.find('.status-dropdown-project').dropdown({
                        onChange: function(value, text, $selectedItem) {
                            const cardId = $(this).closest('.kanban-card-project').data('id');
                            if (cardId) {
                                updateProjectStatus(cardId, value);
                            }
                        }
                    });
                    
                    // Aplicar efeito visual
                    card.transition('pulse');
                    
                    // Atualizar também a linha na tabela
                    const tableRow = $(`#projects-table-body tr td:contains(${projectId})`).parent();
                    if (tableRow.length) {
                        // Atualizar o texto da célula de status
                        tableRow.find('td:nth-child(7)').text(newStatus);
                        
                        // Atualizar a classe da linha com base no novo status
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
                    // Se não encontrou o card ou a coluna, recarrega tudo
                    loadProjects();
                }
            },
            error: function(error) {
                console.error('Erro ao atualizar status:', error);
                alert('Erro ao atualizar status');
            }
        });
    }
    
    // Função auxiliar para formatar datas
    function formatDate(dateString) {
        if (!dateString) return '-';
        
        // Verificar se a data é válida
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return dateString; // Retornar a string original se não for uma data válida
        }
        
        return date.toLocaleDateString('pt-BR');
    }
    
    // Configurar o botão de salvar contato
    $('#save-contact-btn').on('click', function() {
        saveClient();
    });
    
    // Inicializar a página
    $(document).ready(function() {
        // Carregar serviços se a aba estiver ativa inicialmente
        if ($('.menu .item[data-tab="services"]').hasClass('active')) {
            loadServices();
        }
        
        // Carregar projetos se a aba estiver ativa inicialmente
        if ($('.menu .item[data-tab="projects"]').hasClass('active')) {
            loadProjects();
        }
    });

    // Função para carregar os clientes nos dropdowns
    function loadClientsInDropdowns() {
        $.ajax({
            url: `${API_URL}/api/landscaping/client`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                if (response && response.items && response.items.length > 0) {
                    // Limpar os dropdowns existentes
                    $('#project-client-filter').find('option:not(:first)').remove();
                    $('#quote-client-filter').find('option:not(:first)').remove();
                    $('#maintenance-client-filter').find('option:not(:first)').remove();
                    $('select[name="client_id"]').find('option:not(:first)').remove();
                    
                    // Adicionar os clientes aos dropdowns
                    response.items.forEach(function(client) {
                        const option = `<option value="${client.id}">${client.client_name}</option>`;
                        
                        // Adicionar ao dropdown de filtro de projetos
                        $('#project-client-filter').append(option);
                        
                        // Adicionar ao dropdown de filtro de orçamentos
                        $('#quote-client-filter').append(option);
                        
                        // Adicionar ao dropdown de filtro de manutenção
                        $('#maintenance-client-filter').append(option);
                        
                        // Adicionar aos dropdowns de formulários
                        $('select[name="client_id"]').append(option);
                    });
                    
                    // Reinicializar os dropdowns
                    $('.ui.dropdown').dropdown('refresh');
                }
            },
            error: function(error) {
                console.error('Erro ao carregar clientes:', error);
            }
        });
    }
    
    // Função para carregar os serviços nos dropdowns
    function loadServicesInDropdowns() {
        console.log('Carregando serviços...');
        $.ajax({
            url: `${API_URL}/api/landscaping/service`,
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + (localStorage.getItem('token') || 'dummy_token')
            },
            success: function(response) {
                console.log('Serviços carregados:', response);
                if (response && response.items && response.items.length > 0) {
                    // Limpar os dropdowns existentes
                    $('.service-select .menu').empty();
                    
                    // Adicionar os serviços aos dropdowns
                    response.items.forEach(function(service) {
                        const option = `<div class="item" data-value="${service.id}" data-price="${service.base_price}">${service.service_name}</div>`;
                        
                        // Adicionar aos dropdowns de serviços
                        $('.service-select .menu').append(option);
                    });
                    
                    // Inicializar os dropdowns com as opções de serviço
                    $('.service-select').dropdown({
                        onChange: function(value, text, $choice) {
                            const price = $choice.data('price');
                            const row = $(this).closest('.quote-item');
                            
                            if (price) {
                                row.find('.price-input').val(parseFloat(price).toFixed(2));
                                
                                // Calcular subtotal
                                const quantity = parseFloat(row.find('.quantity-input').val()) || 1;
                                row.find('.subtotal-input').val((quantity * price).toFixed(2));
                                
                                // Recalcular total
                                calculateQuoteTotal();
                                
                                // Se este não é o primeiro item e um serviço foi selecionado, consolidar os itens
                                if (!row.is($('.quote-item').first()) && value) {
                                    consolidateQuoteItems();
                                }
                            }
                        }
                    });
                }
            },
            error: function(error) {
                console.error('Erro ao carregar serviços:', error);
            }
        });
    }
    
    // Função para consolidar itens do orçamento com o mesmo serviço
    function consolidateQuoteItems() {
        // Criar um mapa para armazenar os itens por serviço
        const serviceMap = {};
        
        // Percorrer todas as linhas da tabela
        $('#tableBody tr').each(function() {
            const $row = $(this);
            const serviceId = $row.find('.service-select').dropdown('get value');
            
            // Ignorar linhas sem serviço selecionado
            if (!serviceId) return;
            
            // Se o serviço já existe no mapa, consolidar
            if (serviceMap[serviceId]) {
                // Somar a quantidade
                const existingQuantity = parseFloat(serviceMap[serviceId].find('.quantity-input').val()) || 0;
                const currentQuantity = parseFloat($row.find('.quantity-input').val()) || 0;
                serviceMap[serviceId].find('.quantity-input').val(existingQuantity + currentQuantity);
                
                // Recalcular o subtotal da linha existente
                const price = parseFloat(serviceMap[serviceId].find('.price-input').val()) || 0;
                const newQuantity = existingQuantity + currentQuantity;
                serviceMap[serviceId].find('.subtotal-input').val((price * newQuantity).toFixed(2));
                
                // Remover a linha atual
                $row.remove();
            } else {
                // Adicionar ao mapa
                serviceMap[serviceId] = $row;
            }
        });
        
        // Recalcular o total geral
        calculateQuoteTotal();
    }
    
    // Função para calcular o total do orçamento
    function calculateQuoteTotal() {
        let total = 0;
        $('.subtotal-input').each(function() {
            total += parseFloat($(this).val()) || 0;
        });
        
        // Atualizar o total geral (sem desconto)
        $('#grandTotal').val(total.toFixed(2));
        
        const discount = parseFloat($('[name="discount"]').val()) || 0;
        total = total * (1 - discount / 100);
        
        $('#quote-total-value').val(total.toFixed(2));
    }
    
    // Configurar AJAX para lidar com CORS
    $.ajaxSetup({
        xhrFields: {
            withCredentials: false
        },
        crossDomain: true
    });
    
    // Carregar dados quando a página for carregada
    $(document).ready(function() {
        loadClientsInDropdowns();
        loadServicesInDropdowns();
        
        // Carregar dados quando os modais forem abertos
        $('#add-project-btn, #add-maintenance-btn').on('click', function() {
            loadClientsInDropdowns();
        });
        
        $('#add-quote-btn').on('click', function() {
            // Limpar todas as linhas da tabela
            $('#tableBody').empty();
            
            // Resetar o total geral
            $('#grandTotal').val('0.00');
            $('#quote-total-value').val('0.00');
            
            // Carregar clientes e serviços
            loadClientsInDropdowns();
            
            // Abrir o modal e impedir que feche ao clicar fora
            $('#add-quote-modal').modal({
                closable: false
            }).modal('show');
            
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
        
        // Carregar dados quando as abas forem selecionadas
        $('.menu .item').on('click', function() {
            loadClientsInDropdowns();
            if ($(this).data('tab') === 'quotes') {
                loadServicesInDropdowns();
            }
        });
        
        // Configurar eventos para itens de orçamento
        $(document).on('input', '.quantity-input', function() {
            const row = $(this).closest('tr');
            const quantity = parseFloat($(this).val()) || 0;
            const price = parseFloat(row.find('.price-input').val()) || 0;
            row.find('.subtotal-input').val((quantity * price).toFixed(2));
            calculateQuoteTotal();
        });
        
        $(document).on('input', '.price-input', function() {
            const row = $(this).closest('tr');
            const price = parseFloat($(this).val()) || 0;
            const quantity = parseFloat(row.find('.quantity-input').val()) || 0;
            row.find('.subtotal-input').val((quantity * price).toFixed(2));
            calculateQuoteTotal();
        });
        
        // Adicionar item ao orçamento
        $('#add-quote-item').on('click', function(e) {
            // Prevenir comportamento padrão do botão para evitar que o modal feche
            e.preventDefault();
            
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
                        
                        // Configurar eventos para inputs de quantidade e preço na nova linha
                        $newRow.find('.quantity-input, .price-input').on('input', function() {
                            const quantity = parseFloat($newRow.find('.quantity-input').val()) || 0;
                            const price = parseFloat($newRow.find('.price-input').val()) || 0;
                            $newRow.find('.subtotal-input').val((quantity * price).toFixed(2));
                            calculateQuoteTotal();
                        });
                        
                        // Configurar evento para remover linha
                        $newRow.find('.remove-item').on('click', function() {
                            if ($('#tableBody tr').length > 1) {
                                $newRow.remove();
                                calculateQuoteTotal();
                            }
                        });
                        
                        // Recalcular totais
                        calculateQuoteTotal();
                    }
                }
            });
            
            // Garantir que o modal permaneça aberto
            return false;
        });
        
        // Remover item do orçamento
        $(document).on('click', '.remove-item', function() {
            if ($('#tableBody tr').length > 1) {
                $(this).closest('tr').remove();
                calculateQuoteTotal();
            }
        });
        
        // Salvar orçamento
        $('#save-quote-btn').on('click', function() {
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
            
            // Verificar se há pelo menos um item válido
            let hasValidItems = false;
            
            $('.quote-item').each(function() {
                const serviceId = $(this).find('.service-select input[name="service"]').val();
                const quantity = parseFloat($(this).find('.quantity-input').val()) || 0;
                const unitPrice = parseFloat($(this).find('.price-input').val()) || 0;
                
                if (serviceId && quantity > 0 && unitPrice > 0) {
                    hasValidItems = true;
                    return false; // Sair do loop se encontrar pelo menos um item válido
                }
            });
            
            if (!hasValidItems) {
                alert('Adicione pelo menos um item válido ao orçamento.');
                return;
            }
            
            // Obter o nome do cliente selecionado
            const clientName = $('#add-quote-form select[name="client_id"] option:selected').text();
            
            // Coletar itens do orçamento
            const items = [];
            $('.quote-item').each(function() {
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
                user_id: 1,
                client_id: parseInt(clientId),
                description: description,
                created_date: new Date().toISOString().split('T')[0],
                valid_until: validUntil,
                total_value: totalValue,
                notes: notes,
                status: 'Pendente',
                items: items
            };
            
            console.log('Enviando orçamento:', quoteData);
            
            // Enviar dados para a API
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
    });