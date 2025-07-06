// URL base para as chamadas de API
// Usar o caminho relativo para evitar problemas de CORS e conexão
const API_URL = "http://localhost:8000"; // Ajuste conforme necessário para o ambiente de produção

// Funções para carregar dados
function loadDashboardData() {
    $.ajax({
        url: API_URL + '/api/beef_cattle/dashboard/summary',
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(data) {
            updateDashboard(data);
        },
        error: function(error) {
            console.error('Erro ao carregar dados do dashboard:', error);
            // Usar dados mockados em caso de erro
            const mockData = {
                "total_cattle": 5,
                "cattle_by_status": [
                    {"status": "Em Engorda", "count": 4},
                    {"status": "Vendido", "count": 1}
                ],
                "average_weight": 460.0,
                "monthly_sales": 11700.00
            };
            updateDashboard(mockData);
        }
    });
}

function updateDashboard(data) {
    $('#total-cattle').text(data.total_cattle || 0);
    
    // Find "Em Engorda" status count
    const activeCount = data.cattle_by_status.find(item => item.status === 'Em Engorda');
    $('#active-cattle').text(activeCount ? activeCount.count : 0);
    
    $('#avg-weight').text(data.average_weight ? data.average_weight.toFixed(0) : 0);
    $('#monthly-sales').text('R$ ' + (data.monthly_sales ? data.monthly_sales.toFixed(2) : '0.00'));
}

function loadCattleList(filters = {}, page = 1, pageSize = 10) {
    let url = API_URL + '/api/beef_cattle/';
    const queryParams = [];
    
    // Adicionar parâmetros de paginação
    queryParams.push(`page=${page}`);
    queryParams.push(`page_size=${pageSize}`);
    
    // Adicionar filtros como query params
    if (filters.status) queryParams.push(`status=${filters.status}`);
    if (filters.breed) queryParams.push(`breed=${filters.breed}`);
    if (filters.min_weight) queryParams.push(`min_weight=${filters.min_weight}`);
    if (filters.max_weight) queryParams.push(`max_weight=${filters.max_weight}`);
    
    if (queryParams.length > 0) {
        url += '?' + queryParams.join('&');
    }
    
    $.ajax({
        url: url,
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(response) {
            // Verificar se a resposta tem a estrutura esperada
            if (response && response.items) {
                renderCattleList(response.items);
                renderPagination(response, 'cattle-pagination', loadCattleList, filters);
            } else {
                // Se a resposta não tem a estrutura esperada, tratar como array direto
                console.warn('Resposta não tem a estrutura esperada:', response);
                renderCattleList(Array.isArray(response) ? response : []);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar lista de bovinos:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "official_id": "BG001",
                    "name": "Sultão",
                    "birth_date": "2023-01-15",
                    "breed": "Nelore",
                    "gender": "M",
                    "entry_date": "2024-01-10",
                    "entry_weight": 380.5,
                    "current_weight": 450.2,
                    "target_weight": 550.0,
                    "status": "Em Engorda",
                    "expected_finish_date": "2024-12-15",
                    "notes": "Animal saudável, boa conversão alimentar"
                },
                {
                    "id": 2,
                    "official_id": "BG002",
                    "name": "Trovão",
                    "birth_date": "2023-02-20",
                    "breed": "Angus",
                    "gender": "M",
                    "entry_date": "2024-01-15",
                    "entry_weight": 410.0,
                    "current_weight": 470.5,
                    "target_weight": 580.0,
                    "status": "Em Engorda",
                    "expected_finish_date": "2024-11-20",
                    "notes": "Cruzamento industrial, alto ganho diário"
                }
            ];
            
            // Aplicar filtros aos dados mockados
            let filteredData = mockData;
            if (filters.status) {
                filteredData = filteredData.filter(cattle => cattle.status === filters.status);
            }
            if (filters.breed) {
                filteredData = filteredData.filter(cattle => cattle.breed === filters.breed);
            }
            if (filters.min_weight) {
                filteredData = filteredData.filter(cattle => cattle.current_weight >= parseFloat(filters.min_weight));
            }
            if (filters.max_weight) {
                filteredData = filteredData.filter(cattle => cattle.current_weight <= parseFloat(filters.max_weight));
            }
            
            // Criar resposta paginada mockada
            const mockResponse = {
                items: filteredData,
                page: page,
                page_size: pageSize,
                total_items: filteredData.length,
                total_pages: Math.ceil(filteredData.length / pageSize)
            };
            
            renderCattleList(mockResponse.items);
            renderPagination(mockResponse, 'cattle-pagination', loadCattleList, filters);
        }
    });
}

function renderCattleList(data) {
    const tableBody = $('#cattle-table-body');
    tableBody.empty();
    
    // Verificar se data é um array
    if (!Array.isArray(data)) {
        console.error('Dados recebidos não são um array:', data);
        tableBody.append('<tr><td colspan="9" class="center aligned">Erro ao carregar dados</td></tr>');
        return;
    }
    
    data.forEach(cattle => {
        // Garantir que os valores numéricos sejam números
        const entryWeight = parseFloat(cattle.entry_weight) || 0;
        const currentWeight = parseFloat(cattle.current_weight) || 0;
        const weightGain = currentWeight - entryWeight;
        const weightGainClass = weightGain >= 0 ? 'weight-gain-positive' : 'weight-gain-negative';
        
        tableBody.append(`
            <tr>
                <td>${cattle.official_id}</td>
                <td>${cattle.name || '-'}</td>
                <td>${cattle.breed || '-'}</td>
                <td>${formatDate(cattle.entry_date)}</td>
                <td>${entryWeight.toFixed(1)}</td>
                <td>${currentWeight.toFixed(1)}</td>
                <td class="${weightGainClass}">${weightGain.toFixed(1)}</td>
                <td>${cattle.status}</td>
                <td>
                    <button class="ui mini icon button" onclick="viewCattle(${cattle.id})">
                        <i class="eye icon"></i>
                    </button>
                    <button class="ui mini icon button" onclick="editCattle(${cattle.id})">
                        <i class="edit icon"></i>
                    </button>
                    <button class="ui mini icon red button" onclick="deleteCattle(${cattle.id})">
                        <i class="trash icon"></i>
                    </button>
                </td>
            </tr>
        `);
    });
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="9" class="center aligned">Nenhum registro encontrado</td></tr>');
    }
}

function loadCattleForSelect(selectId) {
    $.ajax({
        url: API_URL + '/api/beef_cattle/?status=Em Engorda',
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(response) {
            // Verificar se a resposta tem a estrutura esperada
            if (response && response.items) {
                populateCattleSelect(selectId, response.items);
            } else {
                // Se a resposta não tem a estrutura esperada, tratar como array direto
                console.warn('Resposta não tem a estrutura esperada:', response);
                populateCattleSelect(selectId, Array.isArray(response) ? response : []);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar bovinos para select:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "official_id": "BG001",
                    "name": "Sultão",
                    "status": "Em Engorda"
                },
                {
                    "id": 2,
                    "official_id": "BG002",
                    "name": "Trovão",
                    "status": "Em Engorda"
                }
            ];
            populateCattleSelect(selectId, mockData);
        }
    });
}

function populateCattleSelect(selectId, data) {
    const select = $(selectId);
    select.empty();
    select.append('<option value="">Selecione um bovino</option>');
    
    // Verificar se data é um array
    if (!Array.isArray(data)) {
        // Se não for um array, verificar se é um objeto com propriedade items
        if (data && Array.isArray(data.items)) {
            data = data.items;
        } else {
            console.error('Dados recebidos não são um array:', data);
            select.dropdown('refresh');
            return;
        }
    }
    
    data.forEach(cattle => {
        select.append(`<option value="${cattle.id}">${cattle.official_id} - ${cattle.name || 'Sem nome'}</option>`);
    });
    
    select.dropdown('refresh');
}

function loadActiveCattleForSale() {
    $.ajax({
        url: API_URL + '/api/beef_cattle/?status=Em Engorda',
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(response) {
            // Verificar se a resposta tem a estrutura esperada
            if (response && response.items) {
                populateSaleCattleSelect(response.items);
            } else {
                // Se a resposta não tem a estrutura esperada, tratar como array direto
                console.warn('Resposta não tem a estrutura esperada:', response);
                populateSaleCattleSelect(Array.isArray(response) ? response : []);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar bovinos para venda:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "official_id": "BG001",
                    "name": "Sultão",
                    "current_weight": 450.2,
                    "status": "Em Engorda"
                },
                {
                    "id": 2,
                    "official_id": "BG002",
                    "name": "Trovão",
                    "current_weight": 470.5,
                    "status": "Em Engorda"
                }
            ];
            populateSaleCattleSelect(mockData);
        }
    });
}

function populateSaleCattleSelect(data) {
    const select = $('#sale-cattle-select');
    select.empty();
    select.append('<option value="">Selecione um bovino</option>');
    
    // Verificar se data é um array
    if (!Array.isArray(data)) {
        // Se não for um array, verificar se é um objeto com propriedade items
        if (data && Array.isArray(data.items)) {
            data = data.items;
        } else {
            console.error('Dados recebidos não são um array:', data);
            select.dropdown('refresh');
            return;
        }
    }
    
    data.forEach(cattle => {
        // Garantir que current_weight seja um número
        const currentWeight = parseFloat(cattle.current_weight) || 0;
        select.append(`<option value="${cattle.id}" data-weight="${currentWeight}">${cattle.official_id} - ${cattle.name || 'Sem nome'} (${currentWeight.toFixed(1)} kg)</option>`);
    });
    
    select.dropdown('refresh');
    
    // Set current weight when selecting a cattle
    select.change(function() {
        const selectedOption = $(this).find('option:selected');
        const weight = selectedOption.data('weight');
        if (weight) {
            $('input[name="final_weight"]').val(parseFloat(weight).toFixed(1));
            // Trigger calculation if price is set
            if ($('input[name="price_per_kg"]').val()) {
                $('input[name="price_per_kg"]').trigger('input');
            }
        }
    });
}

function loadWeightRecords(cattleId, page = 1, pageSize = 10) {
    $.ajax({
        url: API_URL + `/api/beef_cattle/weights/${cattleId}?page=${page}&page_size=${pageSize}`,
        method: 'GET',
        success: function(response) {
            renderWeightRecords(response.items);
            renderPagination(response, 'weight-pagination', function(filters, p, ps) {
                loadWeightRecords(cattleId, p, ps);
            });
            
            // Create weight chart with all data (not just the current page)
            if (response.items.length > 0) {
                createWeightChart(response.items);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar registros de peso:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "cattle_id": cattleId,
                    "weight_date": "2024-01-10",
                    "weight": 380.5,
                    "notes": "Peso de entrada"
                },
                {
                    "id": 2,
                    "cattle_id": cattleId,
                    "weight_date": "2024-02-10",
                    "weight": 400.0,
                    "notes": "Primeiro mês"
                }
            ];
            
            // Criar resposta paginada mockada
            const mockResponse = {
                items: mockData,
                page: page,
                page_size: pageSize,
                total_items: mockData.length,
                total_pages: Math.ceil(mockData.length / pageSize)
            };
            
            renderWeightRecords(mockResponse.items);
            renderPagination(mockResponse, 'weight-pagination', function(filters, p, ps) {
                loadWeightRecords(cattleId, p, ps);
            });
            
            // Create weight chart
            createWeightChart(mockData);
        }
    });
}

function renderWeightRecords(data) {
    const tableBody = $('#weight-table-body');
    tableBody.empty();
    
    let prevWeight = null;
    
    data.forEach((record, index) => {
        // Garantir que weight seja um número
        const weight = parseFloat(record.weight) || 0;
        const diff = prevWeight !== null ? weight - prevWeight : 0;
        const diffClass = diff >= 0 ? 'weight-gain-positive' : 'weight-gain-negative';
        const diffText = index > 0 ? `${diff > 0 ? '+' : ''}${diff.toFixed(1)}` : '-';
        
        tableBody.append(`
            <tr>
                <td>${formatDate(record.weight_date)}</td>
                <td>${weight.toFixed(2)}</td>
                <td class="${diffClass}">${diffText}</td>
                <td>${record.notes || '-'}</td>
                <td>
                    <button class="ui mini icon button" onclick="editWeightRecord(${record.id})">
                        <i class="edit icon"></i>
                    </button>
                    <button class="ui mini icon red button" onclick="deleteWeightRecord(${record.id})">
                        <i class="trash icon"></i>
                    </button>
                </td>
            </tr>
        `);
        
        prevWeight = weight;
    });
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="5" class="center aligned">Nenhum registro de peso encontrado</td></tr>');
    }
}

function loadFeedingRecords(cattleId, page = 1, pageSize = 10) {
    $.ajax({
        url: API_URL + `/api/beef_cattle/feeding/${cattleId}?page=${page}&page_size=${pageSize}`,
        method: 'GET',
        success: function(response) {
            renderFeedingRecords(response.items);
            renderPagination(response, 'feeding-pagination', function(filters, p, ps) {
                loadFeedingRecords(cattleId, p, ps);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar registros de alimentação:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "cattle_id": cattleId,
                    "feeding_date": "2024-01-15",
                    "feed_type": "Ração",
                    "quantity": 8.0,
                    "unit": "kg",
                    "notes": "Ração de crescimento"
                },
                {
                    "id": 2,
                    "cattle_id": cattleId,
                    "feeding_date": "2024-02-15",
                    "feed_type": "Ração",
                    "quantity": 10.0,
                    "unit": "kg",
                    "notes": "Aumento de ração"
                }
            ];
            
            // Criar resposta paginada mockada
            const mockResponse = {
                items: mockData,
                page: page,
                page_size: pageSize,
                total_items: mockData.length,
                total_pages: Math.ceil(mockData.length / pageSize)
            };
            
            renderFeedingRecords(mockResponse.items);
            renderPagination(mockResponse, 'feeding-pagination', function(filters, p, ps) {
                loadFeedingRecords(cattleId, p, ps);
            });
        }
    });
}

function renderFeedingRecords(data) {
    const tableBody = $('#feeding-table-body');
    tableBody.empty();
    
    data.forEach(record => {
        // Garantir que quantity seja um número
        const quantity = parseFloat(record.quantity) || 0;
        
        tableBody.append(`
            <tr>
                <td>${formatDate(record.feeding_date)}</td>
                <td>${record.feed_type}</td>
                <td>${quantity.toFixed(2)}</td>
                <td>${record.unit}</td>
                <td>${record.notes || '-'}</td>
                <td>
                    <button class="ui mini icon button" onclick="editFeedingRecord(${record.id})">
                        <i class="edit icon"></i>
                    </button>
                    <button class="ui mini icon red button" onclick="deleteFeedingRecord(${record.id})">
                        <i class="trash icon"></i>
                    </button>
                </td>
            </tr>
        `);
    });
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="6" class="center aligned">Nenhum registro de alimentação encontrado</td></tr>');
    }
}

function loadHealthRecords(cattleId, page = 1, pageSize = 10) {
    $.ajax({
        url: API_URL + `/api/beef_cattle/health/${cattleId}?page=${page}&page_size=${pageSize}`,
        method: 'GET',
        success: function(response) {
            renderHealthRecords(response.items);
            renderPagination(response, 'health-pagination', function(filters, p, ps) {
                loadHealthRecords(cattleId, p, ps);
            });
        },
        error: function(error) {
            console.error('Erro ao carregar registros de saúde:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "cattle_id": cattleId,
                    "record_date": "2024-01-12",
                    "record_type": "Vacinação",
                    "description": "Vacina contra febre aftosa",
                    "medicine": "Aftovacin",
                    "dosage": "5ml",
                    "notes": "Aplicação subcutânea"
                },
                {
                    "id": 2,
                    "cattle_id": cattleId,
                    "record_date": "2024-02-15",
                    "record_type": "Medicação",
                    "description": "Vermífugo",
                    "medicine": "Ivermectina",
                    "dosage": "10ml",
                    "notes": "Aplicação subcutânea"
                }
            ];
            
            // Criar resposta paginada mockada
            const mockResponse = {
                items: mockData,
                page: page,
                page_size: pageSize,
                total_items: mockData.length,
                total_pages: Math.ceil(mockData.length / pageSize)
            };
            
            renderHealthRecords(mockResponse.items);
            renderPagination(mockResponse, 'health-pagination', function(filters, p, ps) {
                loadHealthRecords(cattleId, p, ps);
            });
        }
    });
}

function renderHealthRecords(data) {
    const tableBody = $('#health-table-body');
    tableBody.empty();
    
    data.forEach(record => {
        tableBody.append(`
            <tr>
                <td>${formatDate(record.record_date)}</td>
                <td>${record.record_type}</td>
                <td>${record.description}</td>
                <td>${record.medicine || '-'}</td>
                <td>${record.dosage || '-'}</td>
                <td>${record.notes || '-'}</td>
                <td>
                    <button class="ui mini icon button" onclick="editHealthRecord(${record.id})">
                        <i class="edit icon"></i>
                    </button>
                    <button class="ui mini icon red button" onclick="deleteHealthRecord(${record.id})">
                        <i class="trash icon"></i>
                    </button>
                </td>
            </tr>
        `);
    });
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="7" class="center aligned">Nenhum registro de saúde encontrado</td></tr>');
    }
}

function loadSalesRecords(filters = {}, page = 1, pageSize = 10) {
    // Se não houver filtros, use o endpoint GET
    if (Object.keys(filters).length === 0) {
        $.ajax({
            url: API_URL + `/api/beef_cattle/sales?page=${page}&page_size=${pageSize}`,
            method: 'GET',
            timeout: 10000, // Aumentar o timeout para 10 segundos
            success: function(response) {
                if (response && response.items) {
                    renderSalesData(response.items);
                    renderPagination(response, 'sales-pagination', loadSalesRecords, filters);
                } else {
                    renderSalesData(Array.isArray(response) ? response : []);
                }
            },
            error: function(error) {
                console.error('Erro ao carregar registros de venda:', error);
                // Usar dados mockados em caso de erro
                const mockData = [
                    {
                        "id": 1,
                        "cattle_id": 5,
                        "official_id": "BG005",
                        "name": "Relâmpago",
                        "sale_date": "2024-03-20",
                        "final_weight": 520.0,
                        "price_per_kg": 22.50,
                        "total_value": 11700.00,
                        "buyer": "Frigorífico São José",
                        "notes": "Venda antecipada por bom desempenho"
                    }
                ];
                
                // Criar resposta paginada mockada
                const mockResponse = {
                    items: mockData,
                    page: page,
                    page_size: pageSize,
                    total_items: mockData.length,
                    total_pages: Math.ceil(mockData.length / pageSize)
                };
                
                renderSalesData(mockResponse.items);
                renderPagination(mockResponse, 'sales-pagination', loadSalesRecords, filters);
            }
        });
    } else {
        // Se houver filtros, use o endpoint POST com os filtros no body
        // Adicionar parâmetros de paginação aos filtros
        filters.page = page;
        filters.page_size = pageSize;
        
        $.ajax({
            url: API_URL + '/api/beef_cattle/sales/search',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(filters),
            timeout: 10000, // Aumentar o timeout para 10 segundos
            success: function(response) {
                if (response && response.items) {
                    renderSalesData(response.items);
                    renderPagination(response, 'sales-pagination', loadSalesRecords, filters);
                } else {
                    renderSalesData(Array.isArray(response) ? response : []);
                }
            },
            error: function(error) {
                console.error('Erro ao carregar registros de venda com filtros:', error);
                // Usar dados mockados em caso de erro
                const mockData = [
                    {
                        "id": 1,
                        "cattle_id": 5,
                        "official_id": "BG005",
                        "name": "Relâmpago",
                        "sale_date": "2024-03-20",
                        "final_weight": 520.0,
                        "price_per_kg": 22.50,
                        "total_value": 11700.00,
                        "buyer": "Frigorífico São José",
                        "notes": "Venda antecipada por bom desempenho"
                    }
                ];
                
                // Aplicar filtros aos dados mockados
                let filteredData = mockData;
                if (filters.start_date || filters.end_date) {
                    // Filtrar por data se houver filtros de data
                    filteredData = mockData.filter(sale => {
                        const saleDate = new Date(sale.sale_date);
                        if (filters.start_date && new Date(filters.start_date) > saleDate) return false;
                        if (filters.end_date && new Date(filters.end_date) < saleDate) return false;
                        return true;
                    });
                }
                
                // Criar resposta paginada mockada
                const mockResponse = {
                    items: filteredData,
                    page: page,
                    page_size: pageSize,
                    total_items: filteredData.length,
                    total_pages: Math.ceil(filteredData.length / pageSize)
                };
                
                renderSalesData(mockResponse.items);
                renderPagination(mockResponse, 'sales-pagination', loadSalesRecords, filters);
            }
        });
    }
}

function renderSalesData(data) {
    const tableBody = $('#sales-table-body');
    tableBody.empty();
    
    data.forEach(record => {
        let peso = '-';
        if (record.final_weight !== null && record.final_weight !== undefined && !isNaN(Number(record.final_weight))) {
            peso = Number(record.final_weight).toFixed(2);
        }
        
        // Garantir que price_per_kg e total_value sejam números
        const pricePerKg = parseFloat(record.price_per_kg) || 0;
        const totalValue = parseFloat(record.total_value) || 0;
        
        tableBody.append(`
            <tr>
                <td>${formatDate(record.sale_date)}</td>
                <td>${record.official_id}</td>
                <td>${record.name || '-'}</td>
                <td>${peso}</td>
                <td>R$ ${pricePerKg.toFixed(2)}</td>
                <td>R$ ${totalValue.toFixed(2)}</td>
                <td>${record.buyer || '-'}</td>
                <td>
                    <button class="ui mini icon button" onclick="viewSaleRecord(${record.id})">
                        <i class="eye icon"></i>
                    </button>
                </td>
            </tr>
        `);
    });
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="8" class="center aligned">Nenhum registro de venda encontrado</td></tr>');
    }
}

// Variável global para armazenar todos os dados de análise
let allAnalyticsData = [];

function loadAnalyticsData(filters = {}, page = 1, pageSize = 10) {
    $.ajax({
        url: API_URL + `/api/beef_cattle/dashboard/weight-gain?page=${page}&page_size=${pageSize}`,
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(response) {
            // Verificar se a resposta tem a estrutura esperada
            if (response && response.items && response.page && response.total_items) {
                // Armazenar todos os dados para uso posterior
                if (page === 1) {
                    allAnalyticsData = response.items;
                } else {
                    allAnalyticsData = allAnalyticsData.concat(response.items);
                }
                
                renderAnalyticsData(response.items);
                renderPagination(response, 'performance-pagination', loadAnalyticsData, filters);
            } else {
                // Se a resposta não tem a estrutura esperada, tratar como array direto
                console.warn('Resposta não tem a estrutura esperada:', response);
                
                const items = Array.isArray(response) ? response : [];
                
                // Armazenar todos os dados para uso posterior
                if (page === 1) {
                    allAnalyticsData = items;
                } else {
                    allAnalyticsData = allAnalyticsData.concat(items);
                }
                
                // Criar resposta paginada mockada
                const mockResponse = {
                    items: items,
                    page: parseInt(page) || 1,
                    page_size: parseInt(pageSize) || 10,
                    total_items: items.length,
                    total_pages: Math.ceil(items.length / (parseInt(pageSize) || 10))
                };
                
                renderAnalyticsData(mockResponse.items);
                renderPagination(mockResponse, 'performance-pagination', loadAnalyticsData, filters);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar dados de análise:', error);
            // Usar dados mockados em caso de erro
            const mockData = [
                {
                    "id": 1,
                    "official_id": "BG001",
                    "name": "Sultão",
                    "first_date": "2024-01-10",
                    "last_date": "2024-04-10",
                    "initial_weight": 380.5,
                    "current_weight": 450.2,
                    "days": 90,
                    "weight_gain": 69.7,
                    "daily_gain": 0.77
                },
                {
                    "id": 2,
                    "official_id": "BG002",
                    "name": "Trovão",
                    "first_date": "2024-01-15",
                    "last_date": "2024-04-15",
                    "initial_weight": 410.0,
                    "current_weight": 470.5,
                    "days": 90,
                    "weight_gain": 60.5,
                    "daily_gain": 0.67
                }
            ];
            
            // Armazenar todos os dados para uso posterior
            if (page === 1) {
                allAnalyticsData = mockData;
            } else {
                allAnalyticsData = allAnalyticsData.concat(mockData);
            }
            
            // Criar resposta paginada mockada
            const mockResponse = {
                items: mockData,
                page: parseInt(page) || 1,
                page_size: parseInt(pageSize) || 10,
                total_items: mockData.length,
                total_pages: Math.ceil(mockData.length / (parseInt(pageSize) || 10))
            };
            
            renderAnalyticsData(mockResponse.items);
            renderPagination(mockResponse, 'performance-pagination', loadAnalyticsData, filters);
        }
    });
}

function renderAnalyticsData(data) {
    const tableBody = $('#performance-table-body');
    tableBody.empty();
    
    // Verificar se data é um array
    if (!Array.isArray(data)) {
        console.error('Dados recebidos não são um array:', data);
        tableBody.append('<tr><td colspan="7" class="center aligned">Erro ao carregar dados</td></tr>');
        return;
    }
    
    if (data.length === 0) {
        tableBody.append('<tr><td colspan="7" class="center aligned">Nenhum dado disponível</td></tr>');
        return;
    }
    
    data.forEach(record => {
        // Garantir que os valores numéricos sejam números
        const initialWeight = parseFloat(record.initial_weight) || 0;
        const currentWeight = parseFloat(record.current_weight) || 0;
        const weightGain = parseFloat(record.weight_gain) || 0;
        const dailyGain = parseFloat(record.daily_gain) || 0;
        
        tableBody.append(`
            <tr>
                <td>${record.official_id}</td>
                <td>${record.name || '-'}</td>
                <td>${initialWeight.toFixed(1)}</td>
                <td>${currentWeight.toFixed(1)}</td>
                <td>${weightGain.toFixed(1)}</td>
                <td>${record.days}</td>
                <td>${dailyGain.toFixed(2)}</td>
            </tr>
        `);
    });
    
    // Create analytics charts com os dados da página atual
    createAnalyticsCharts(data);
}

// Chart creation functions
function createWeightChart(data) {
    const ctx = document.getElementById('weight-chart').getContext('2d');
    
    // Destroy previous chart if exists
    if (window.weightChart) {
        window.weightChart.destroy();
    }
    
    if (data.length === 0) return;
    
    const labels = data.map(record => formatDate(record.weight_date));
    const weights = data.map(record => parseFloat(record.weight) || 0);
    
    window.weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Peso (kg)',
                data: weights,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Peso (kg)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Data'
                    }
                }
            }
        }
    });
}

function createAnalyticsCharts(data) {
    // Weight gain chart
    const weightGainCtx = document.getElementById('weight-gain-chart').getContext('2d');
    
    if (window.weightGainChart) {
        window.weightGainChart.destroy();
    }
    
    if (data.length === 0) return;
    
    // Limitar a 10 registros para melhor visualização
    const chartData = allAnalyticsData.length > 0 ? allAnalyticsData.slice(0, 10) : data.slice(0, 10);
    
    const labels = chartData.map(record => record.official_id + (record.name ? ` - ${record.name}` : ''));
    const dailyGains = chartData.map(record => parseFloat(record.daily_gain) || 0);
    
    window.weightGainChart = new Chart(weightGainCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ganho Diário (kg)',
                data: dailyGains,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Ganho Diário (kg)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Ganho Diário de Peso por Bovino'
                }
            }
        }
    });
    
    // Sales chart
    $.ajax({
        url: API_URL + '/api/beef_cattle/sales',
        method: 'GET',
        timeout: 10000, // Aumentar o timeout para 10 segundos
        success: function(salesData) {
            if (salesData && salesData.items) {
                createSalesChart(salesData.items);
            } else {
                createSalesChart(salesData);
            }
        },
        error: function(error) {
            console.error('Erro ao carregar dados de vendas para gráfico:', error);
            // Usar dados mockados em caso de erro
            const mockSalesData = [
                {
                    "id": 1,
                    "cattle_id": 5,
                    "sale_date": "2024-03-20",
                    "total_value": 11700.00
                }
            ];
            createSalesChart(mockSalesData);
        }
    });
}

function createSalesChart(salesData) {
    const salesCtx = document.getElementById('sales-chart').getContext('2d');
    
    if (window.salesChart) {
        window.salesChart.destroy();
    }
    
    // Garantir que salesData seja um array
    if (!Array.isArray(salesData)) {
        if (salesData && Array.isArray(salesData.items)) {
            salesData = salesData.items;
        } else {
            salesData = [];
        }
    }
    
    if (salesData.length === 0) {
        // Adicionar dados mockados se não houver dados
        salesData = [
            { sale_date: "2024-01-15", total_value: 9800.00 },
            { sale_date: "2024-02-10", total_value: 10500.00 },
            { sale_date: "2024-03-20", total_value: 11700.00 }
        ];
    }
    
    // Group sales by month
    const salesByMonth = {};
    salesData.forEach(sale => {
        // Verificar se sale.sale_date existe e é válido
        if (!sale.sale_date) return;
        
        try {
            const date = new Date(sale.sale_date);
            if (isNaN(date.getTime())) return; // Pular se a data for inválida
            
            const monthYear = `${date.getMonth() + 1}/${date.getFullYear()}`;
            
            if (!salesByMonth[monthYear]) {
                salesByMonth[monthYear] = 0;
            }
            
            // Garantir que total_value seja um número
            const totalValue = parseFloat(sale.total_value) || 0;
            salesByMonth[monthYear] += totalValue;
        } catch (e) {
            console.error('Erro ao processar data de venda:', e);
        }
    });
    
    const monthLabels = Object.keys(salesByMonth).sort((a, b) => {
        const [monthA, yearA] = a.split('/').map(Number);
        const [monthB, yearB] = b.split('/').map(Number);
        
        if (yearA !== yearB) return yearA - yearB;
        return monthA - monthB;
    });
    
    const monthlySales = monthLabels.map(month => salesByMonth[month]);
    
    window.salesChart = new Chart(salesCtx, {
        type: 'bar',
        data: {
            labels: monthLabels,
            datasets: [{
                label: 'Vendas Mensais (R$)',
                data: monthlySales,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Valor (R$)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Vendas Mensais'
                }
            }
        }
    });
}

// CRUD operations
function viewCattle(id) {
    // Implement view cattle details
    alert('Visualizar detalhes do bovino ' + id);
}

function editCattle(id) {
    // Implement edit cattle
    alert('Editar bovino ' + id);
}

function deleteCattle(id) {
    if (confirm('Tem certeza que deseja excluir este bovino?')) {
        $.ajax({
            url: API_URL + `/api/beef_cattle/${id}`,
            method: 'DELETE',
            success: function() {
                loadCattleList();
                loadDashboardData();
            },
            error: function(error) {
                alert('Erro ao excluir: ' + error.responseJSON.detail);
            }
        });
    }
}

function editWeightRecord(id) {
    // Implement edit weight record
    alert('Editar registro de peso ' + id);
}

function deleteWeightRecord(id) {
    // Implement delete weight record
    alert('Excluir registro de peso ' + id);
}

function editFeedingRecord(id) {
    // Implement edit feeding record
    alert('Editar registro de alimentação ' + id);
}

function deleteFeedingRecord(id) {
    // Implement delete feeding record
    alert('Excluir registro de alimentação ' + id);
}

function editHealthRecord(id) {
    // Implement edit health record
    alert('Editar registro de saúde ' + id);
}

function deleteHealthRecord(id) {
    // Implement delete health record
    alert('Excluir registro de saúde ' + id);
}

function viewSaleRecord(id) {
    // Implement view sale record
    alert('Visualizar registro de venda ' + id);
}

// Helper functions
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Document ready function
$(document).ready(function() {
    // Initialize dropdowns
    $('.ui.dropdown').dropdown();
    
    // Initialize tabs
    $('.menu .item').tab();
    
    // Load dashboard data
    loadDashboardData();
    
    // Load cattle list
    loadCattleList();
    
    // Event listeners for buttons
    $('#add-cattle-btn').click(function() {
        $('#add-cattle-modal').modal('show');
    });
    
    $('#add-weight-btn').click(function() {
        const cattleId = $('#weight-cattle-select').val();
        if (!cattleId) {
            alert('Por favor, selecione um bovino primeiro.');
            return;
        }
        $('#weight-cattle-id').val(cattleId);
        $('#add-weight-modal').modal('show');
    });
    
    $('#add-feeding-btn').click(function() {
        const cattleId = $('#feeding-cattle-select').val();
        if (!cattleId) {
            alert('Por favor, selecione um bovino primeiro.');
            return;
        }
        $('#feeding-cattle-id').val(cattleId);
        $('#add-feeding-modal').modal('show');
    });
    
    $('#add-health-btn').click(function() {
        const cattleId = $('#health-cattle-select').val();
        if (!cattleId) {
            alert('Por favor, selecione um bovino primeiro.');
            return;
        }
        $('#health-cattle-id').val(cattleId);
        $('#add-health-modal').modal('show');
    });
    
    $('#add-sale-btn').click(function() {
        loadActiveCattleForSale();
        $('#add-sale-modal').modal('show');
    });
    
    // Form submissions
    $('#save-cattle-btn').click(function() {
        const form = $('#add-cattle-form');
        if (form[0].checkValidity()) {
            const formData = {};
            form.serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            
            $.ajax({
                url: API_URL + '/api/beef_cattle/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    $('#add-cattle-modal').modal('hide');
                    form[0].reset();
                    loadCattleList();
                    loadDashboardData();
                },
                error: function(error) {
                    alert('Erro ao salvar: ' + error.responseJSON.detail);
                }
            });
        } else {
            form[0].reportValidity();
        }
    });
    
    $('#save-weight-btn').click(function() {
        const form = $('#add-weight-form');
        if (form[0].checkValidity()) {
            const formData = {};
            form.serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            
            $.ajax({
                url: API_URL + '/api/beef_cattle/weights',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    $('#add-weight-modal').modal('hide');
                    form[0].reset();
                    loadWeightRecords($('#weight-cattle-select').val());
                    loadCattleList();
                },
                error: function(error) {
                    alert('Erro ao salvar: ' + error.responseJSON.detail);
                }
            });
        } else {
            form[0].reportValidity();
        }
    });
    
    $('#save-feeding-btn').click(function() {
        const form = $('#add-feeding-form');
        if (form[0].checkValidity()) {
            const formData = {};
            form.serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            
            $.ajax({
                url: API_URL + '/api/beef_cattle/feeding',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    $('#add-feeding-modal').modal('hide');
                    form[0].reset();
                    loadFeedingRecords($('#feeding-cattle-select').val());
                },
                error: function(error) {
                    alert('Erro ao salvar: ' + error.responseJSON.detail);
                }
            });
        } else {
            form[0].reportValidity();
        }
    });
    
    $('#save-health-btn').click(function() {
        const form = $('#add-health-form');
        if (form[0].checkValidity()) {
            const formData = {};
            form.serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            
            $.ajax({
                url: API_URL + '/api/beef_cattle/health',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    $('#add-health-modal').modal('hide');
                    form[0].reset();
                    loadHealthRecords($('#health-cattle-select').val());
                },
                error: function(error) {
                    alert('Erro ao salvar: ' + error.responseJSON.detail);
                }
            });
        } else {
            form[0].reportValidity();
        }
    });
    
    $('#save-sale-btn').click(function() {
        const form = $('#add-sale-form');
        if (form[0].checkValidity()) {
            const formData = {};
            form.serializeArray().forEach(item => {
                formData[item.name] = item.value;
            });
            
            $.ajax({
                url: API_URL + '/api/beef_cattle/sales',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(response) {
                    $('#add-sale-modal').modal('hide');
                    form[0].reset();
                    loadSalesRecords();
                    loadCattleList();
                    loadDashboardData();
                },
                error: function(error) {
                    alert('Erro ao salvar: ' + error.responseJSON.detail);
                }
            });
        } else {
            form[0].reportValidity();
        }
    });
    
    // Calculate total value in sale form
    $('input[name="final_weight"], input[name="price_per_kg"]').on('input', function() {
        const weight = parseFloat($('input[name="final_weight"]').val()) || 0;
        const price = parseFloat($('input[name="price_per_kg"]').val()) || 0;
        const total = weight * price;
        $('#total-value').val(total.toFixed(2));
    });
    
    // Tab change events
    $('.menu .item').on('click', function() {
        const tab = $(this).data('tab');
        
        if (tab === 'weight-records') {
            loadCattleForSelect('#weight-cattle-select');
        } else if (tab === 'feeding-records') {
            loadCattleForSelect('#feeding-cattle-select');
        } else if (tab === 'health-records') {
            loadCattleForSelect('#health-cattle-select');
        } else if (tab === 'sales-records') {
            loadSalesRecords();
        } else if (tab === 'analytics') {
            // Resetar os dados armazenados ao mudar para a aba de análise
            allAnalyticsData = [];
            loadAnalyticsData();
        }
    });
    
    // Filter events
    $('#apply-filters').click(function() {
        loadCattleList({
            status: $('#status-filter').val(),
            breed: $('#breed-filter').val(),
            min_weight: $('#min-weight-filter').val(),
            max_weight: $('#max-weight-filter').val()
        });
    });
    
    $('#clear-filters').click(function() {
        $('#status-filter').dropdown('clear');
        $('#breed-filter').dropdown('clear');
        $('#min-weight-filter').val('');
        $('#max-weight-filter').val('');
        loadCattleList();
    });
});