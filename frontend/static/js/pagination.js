// Função para renderizar a paginação
function renderPagination(response, containerId, loadFunction, filters = {}) {
    const container = $(`#${containerId}`);
    container.empty();
    
    if (!response || !response.total_pages || response.total_pages <= 1) {
        return;
    }
    
    const pagination = $('<div class="ui pagination menu"></div>');
    
    // Botão anterior
    const prevButton = $(`<a class="item ${response.page <= 1 ? 'disabled' : ''}" data-page="${response.page - 1}"><i class="angle left icon"></i></a>`);
    if (response.page > 1) {
        prevButton.click(function() {
            loadFunction(filters, response.page - 1, response.page_size);
        });
    }
    pagination.append(prevButton);
    
    // Páginas
    const maxPages = 5;
    let startPage = Math.max(1, response.page - Math.floor(maxPages / 2));
    let endPage = Math.min(response.total_pages, startPage + maxPages - 1);
    
    if (endPage - startPage + 1 < maxPages) {
        startPage = Math.max(1, endPage - maxPages + 1);
    }
    
    // Primeira página
    if (startPage > 1) {
        const firstPage = $(`<a class="item" data-page="1">1</a>`);
        firstPage.click(function() {
            loadFunction(filters, 1, response.page_size);
        });
        pagination.append(firstPage);
        
        if (startPage > 2) {
            pagination.append($('<a class="disabled item">...</a>'));
        }
    }
    
    // Páginas numeradas
    for (let i = startPage; i <= endPage; i++) {
        const pageItem = $(`<a class="item ${i === response.page ? 'active' : ''}" data-page="${i}">${i}</a>`);
        if (i !== response.page) {
            pageItem.click(function() {
                loadFunction(filters, i, response.page_size);
            });
        }
        pagination.append(pageItem);
    }
    
    // Última página
    if (endPage < response.total_pages) {
        if (endPage < response.total_pages - 1) {
            pagination.append($('<a class="disabled item">...</a>'));
        }
        
        const lastPage = $(`<a class="item" data-page="${response.total_pages}">${response.total_pages}</a>`);
        lastPage.click(function() {
            loadFunction(filters, response.total_pages, response.page_size);
        });
        pagination.append(lastPage);
    }
    
    // Botão próximo
    const nextButton = $(`<a class="item ${response.page >= response.total_pages ? 'disabled' : ''}" data-page="${response.page + 1}"><i class="angle right icon"></i></a>`);
    if (response.page < response.total_pages) {
        nextButton.click(function() {
            loadFunction(filters, response.page + 1, response.page_size);
        });
    }
    pagination.append(nextButton);
    
    container.append(pagination);
    
    // Adicionar informações sobre os itens exibidos
    if (response.total_items !== undefined) {
        // Garantir que os valores sejam números inteiros
        const page = parseInt(response.page) || 1;
        const pageSize = parseInt(response.page_size) || 10;
        const totalItems = parseInt(response.total_items) || 0;
        
        const startItem = (page - 1) * pageSize + 1;
        const endItem = Math.min(startItem + pageSize - 1, totalItems);
        
        // Verificar se os valores são válidos antes de exibir
        if (!isNaN(startItem) && !isNaN(endItem) && !isNaN(totalItems) && totalItems > 0) {
            const infoText = $(`
                <div class="ui small text" style="margin-top: 10px; text-align: center;">
                    Mostrando ${startItem} a ${endItem} de ${totalItems} registros
                </div>
            `);
            
            container.append(infoText);
        }
    }
}