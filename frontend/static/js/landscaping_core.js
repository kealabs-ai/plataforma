// Usar API_URL global se já estiver definida
if (typeof API_URL === 'undefined') {
    var API_URL = "http://localhost:8000";
}

// Arquivo principal responsável por integrar e carregar os demais módulos
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
    
    // Carregar dados da API, com fallback para dados mockados
    loadLandscapingDataFromAPI().catch(error => {
        console.error('Erro ao carregar dados da API, usando dados mockados:', error);
    });
    
    // Inicializar projetos no carregamento da página
    if (typeof loadProjects === 'function') {
        loadProjects();
    }
});

// Função para carregar dados da API
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

// Configurar AJAX para lidar com CORS
$.ajaxSetup({
    xhrFields: {
        withCredentials: false
    },
    crossDomain: true
});

function formatCurrency(value) {
    if (!value) return 'R$ 0,00';
    return parseFloat(value).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}