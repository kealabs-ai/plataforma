// Arquivo de teste para verificar o funcionamento do modal de orçamentos

// Função para testar o modal
function testQuoteModal() {
    console.log('Testando modal de orçamentos...');
    
    // Verificar se as funções existem
    if (typeof initializeQuoteModal === 'function') {
        console.log('✓ initializeQuoteModal existe');
    } else {
        console.error('✗ initializeQuoteModal não encontrada');
    }
    
    if (typeof addQuoteRow === 'function') {
        console.log('✓ addQuoteRow existe');
    } else {
        console.error('✗ addQuoteRow não encontrada');
    }
    
    if (typeof calculateTotal === 'function') {
        console.log('✓ calculateTotal existe');
    } else {
        console.error('✗ calculateTotal não encontrada');
    }
    
    // Verificar se os elementos HTML existem
    if ($('#add-quote-modal').length > 0) {
        console.log('✓ Modal HTML existe');
    } else {
        console.error('✗ Modal HTML não encontrado');
    }
    
    if ($('#add-quote-btn').length > 0) {
        console.log('✓ Botão de novo orçamento existe');
    } else {
        console.error('✗ Botão de novo orçamento não encontrado');
    }
    
    if ($('#tableBody').length > 0) {
        console.log('✓ Tabela de itens existe');
    } else {
        console.error('✗ Tabela de itens não encontrada');
    }
    
    if ($('#add-quote-item').length > 0) {
        console.log('✓ Botão de adicionar item existe');
    } else {
        console.error('✗ Botão de adicionar item não encontrado');
    }
    
    console.log('Teste concluído!');
}

// Executar teste quando a página carregar
$(document).ready(function() {
    setTimeout(testQuoteModal, 1000); // Aguardar 1 segundo para garantir que tudo carregou
});