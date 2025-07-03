// Funcionalidade para o menu lateral (sidebar)
$(document).ready(function() {
    // Garante que o menu esteja visível inicialmente em telas grandes
    if (window.innerWidth > 768) {
        $('.sidebar').removeClass('sidebar-hidden');
    } else {
        $('.main-content').addClass('main-content-full');
    }
    
    // Toggle do sidebar
    $('.toggle-sidebar').click(function() {
        $('.sidebar').toggleClass('sidebar-hidden');
        $('.main-content').toggleClass('main-content-full');
    });
    
    // Inicializa os dropdowns do menu
    $('.ui.dropdown').dropdown();
    
    // Inicializa os itens do menu
    $('.ui.vertical.menu .item').tab();
});