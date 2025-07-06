// Funções para gerenciamento do preço do leite
function loadCurrentMilkPrice() {
    $.ajax({
        url: `${API_URL}/milk/price/current`,
        method: 'GET',
        success: function(data) {
            if (data) {
                // Atualiza o preço do leite no card
                currentMilkPrice = data.milk_price || data.rural_producer_pair_price || 2.50;
                $('#milk-price').text(formatCurrency(currentMilkPrice));
                
                // Atualiza o valor total com base no novo preço
                const totalLiters = parseFloat($('#total-liters').text().replace(/\./g, '').replace(',', '.')) || 0;
                const totalValue = totalLiters * currentMilkPrice;
                $('#total-value').text(formatCurrency(totalValue));
            }
        },
        error: function(error) {
            console.error('Erro ao obter preço atual do leite:', error);
        }
    });
}

function setupMilkPriceModal() {
    // O evento de clique já está configurado em setupEventListeners
    
    // Botão para salvar as alterações
    $('#save-milk-price-button').on('click', function() {
        updateMilkPrice();
    });
    
    // Atualiza o valor final ao alterar o preço médio ou a margem
    $('#net-price-avg, #dairy-percentage').on('input', function() {
        calculateFinalPrice();
    });
}

function openMilkPriceModal() {
    // Carrega os dados atuais do preço do leite
    $.ajax({
        url: `${API_URL}/milk/price/current`,
        method: 'GET',
        success: function(data) {
            if (data) {
                // Formata o mês para exibição (YYYY-MM para MM/YYYY)
                let month = data.month || new Date().toISOString().substring(0, 7);
                const [year, monthNum] = month.split('-');
                const formattedMonth = `${monthNum}/${year}`;
                
                // Preenche os campos do formulário
                $('#current-month').val(formattedMonth);
                $('#net-price-avg').val(data.net_price_avg || 2.50);
                $('#dairy-percentage').val((data.dairy_percentage || 0.15) * 100); // Converte para porcentagem
                $('#milk-price-value').val(formatCurrency(data.milk_price || data.rural_producer_pair_price || 2.50));
                
                // Carrega o histórico de preços
                loadPriceHistory(1);
                
                // Abre o modal
                $('#milk-price-modal').modal('show');
            }
        },
        error: function(error) {
            console.error('Erro ao obter preço atual do leite:', error);
            showMessage('error', 'Erro', 'Não foi possível carregar os dados do preço do leite.');
        }
    });
}

function calculateFinalPrice() {
    const netPriceAvg = parseFloat($('#net-price-avg').val()) || 0;
    const dairyPercentage = parseFloat($('#dairy-percentage').val()) / 100 || 0;
    
    // Calcula o preço final
    const finalPrice = netPriceAvg * (1 - dairyPercentage);
    
    // Atualiza o campo de valor final
    $('#milk-price-value').val(formatCurrency(finalPrice));
}

function updateMilkPrice() {
    const netPriceAvg = parseFloat($('#net-price-avg').val()) || 0;
    const dairyPercentage = parseFloat($('#dairy-percentage').val()) / 100 || 0;
    
    // Validação básica
    if (netPriceAvg <= 0) {
        showMessage('warning', 'Validação', 'O valor do mês deve ser maior que zero.');
        return;
    }
    
    if (dairyPercentage < 0 || dairyPercentage > 1) {
        showMessage('warning', 'Validação', 'A margem aplicada deve estar entre 0% e 100%.');
        return;
    }
    
    // Envia os dados para a API
    $.ajax({
        url: `${API_URL}/milk/price/update`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            net_price_avg: netPriceAvg,
            dairy_percentage: dairyPercentage
        }),
        success: function(data) {
            if (data) {
                // Atualiza o preço do leite no card
                currentMilkPrice = data.milk_price || data.rural_producer_pair_price || 2.50;
                $('#milk-price').text(formatCurrency(currentMilkPrice));
                
                // Atualiza o valor total com base no novo preço
                const totalLiters = parseFloat($('#total-liters').text().replace(/\./g, '').replace(',', '.')) || 0;
                const totalValue = totalLiters * currentMilkPrice;
                $('#total-value').text(formatCurrency(totalValue));
                
                // Fecha o modal
                $('#milk-price-modal').modal('hide');
                
                // Exibe mensagem de sucesso
                showMessage('success', 'Sucesso', 'Preço do leite atualizado com sucesso.');
            }
        },
        error: function(error) {
            console.error('Erro ao atualizar preço do leite:', error);
            showMessage('error', 'Erro', 'Não foi possível atualizar o preço do leite.');
        }
    });
}

function loadPriceHistory(page) {
    priceHistoryPage = page;
    
    $.ajax({
        url: `${API_URL}/milk/price/history?page=${page}&page_size=${priceHistoryPageSize}`,
        method: 'GET',
        success: function(data) {
            if (data && data.items) {
                renderPriceHistoryTable(data.items);
                updatePriceHistoryPagination(data.page, data.total_pages);
            }
        },
        error: function(error) {
            console.error('Erro ao obter histórico de preços:', error);
        }
    });
}

function renderPriceHistoryTable(items) {
    const $tableBody = $('#price-history-table');
    $tableBody.empty();
    
    if (!items || items.length === 0) {
        $tableBody.append(`
            <tr>
                <td colspan="5" class="center aligned">Nenhum registro encontrado</td>
            </tr>
        `);
        return;
    }
    
    items.forEach(item => {
        // Formata o mês para exibição (YYYY-MM-DD para MM/YYYY)
        let recordDate = item.record_date || '';
        if (recordDate) {
            const date = new Date(recordDate);
            recordDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()}`;
        }
        
        // Formata os valores monetários
        const netPriceAvg = formatCurrency(item.net_price_avg || 0);
        const dairyPercentage = `${((item.dairy_percentage || 0) * 100).toFixed(1)}%`;
        const finalPrice = formatCurrency(item.rural_producer_pair_price || 0);
        
        $tableBody.append(`
            <tr>
                <td>${item.state || 'SP'}</td>
                <td>${recordDate}</td>
                <td>${netPriceAvg}</td>
                <td>${dairyPercentage}</td>
                <td>${finalPrice}</td>
            </tr>
        `);
    });
}

function updatePriceHistoryPagination(currentPage, totalPages) {
    const $pagination = $('#price-history-pagination');
    $pagination.empty();
    
    // Botão anterior
    $pagination.append(`
        <a class="icon item ${currentPage <= 1 ? 'disabled' : ''}" data-page="${currentPage - 1}">
            <i class="left chevron icon"></i>
        </a>
    `);
    
    // Páginas
    for (let i = 1; i <= totalPages; i++) {
        $pagination.append(`
            <a class="item ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</a>
        `);
    }
    
    // Botão próximo
    $pagination.append(`
        <a class="icon item ${currentPage >= totalPages ? 'disabled' : ''}" data-page="${currentPage + 1}">
            <i class="right chevron icon"></i>
        </a>
    `);
    
    // Configura os eventos de paginação
    $pagination.find('.item').on('click', function() {
        if (!$(this).hasClass('disabled') && !$(this).hasClass('active')) {
            const page = parseInt($(this).data('page'));
            loadPriceHistory(page);
        }
    });
}