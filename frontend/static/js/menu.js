// Inicializa o menu quando o documento estiver pronto
$(document).ready(function() {
    // Inicializa todos os dropdowns com configuração especial
    $('.ui.dropdown').dropdown({
        // Configuração para manter o menu aberto quando hover
        on: 'hover'
    });
    
    // Obtém o menu ativo da página atual
    var activeMenu = $('body').data('active-menu');
    
    // Se houver um menu ativo, força a abertura do dropdown
    if (activeMenu && activeMenu !== 'dashboard') {
        // Adiciona classes para forçar a exibição do dropdown
        var $activeDropdown = $('.ui.dropdown.' + activeMenu);
        $activeDropdown.addClass('active visible');
        $activeDropdown.find('.menu').addClass('visible');
    }
});