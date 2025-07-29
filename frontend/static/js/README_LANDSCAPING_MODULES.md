# Modularização do Sistema de Paisagismo

Este documento descreve a modularização do arquivo `landscaping.js` em módulos menores e mais organizados.

## Estrutura dos Módulos

### 1. landscaping_core.js
**Responsabilidade**: Arquivo principal responsável por integrar e carregar os demais módulos.

**Conteúdo**:
- Constante API_URL
- Inicialização da aplicação (DOMContentLoaded)
- Configuração de dropdowns e tabs do Semantic UI
- Configuração de modais
- Função `loadLandscapingDataFromAPI()` para carregar dados gerais
- Função auxiliar `formatDate()`
- Configuração AJAX para CORS

### 2. landscaping_contacts.js
**Responsabilidade**: Contém todas as funcionalidades relacionadas à aba de Contatos.

**Funcionalidades**:
- Carregamento de clientes/contatos
- Paginação de contatos
- Visualização de detalhes do cliente
- Edição de clientes
- Criação de novos clientes
- Exclusão/inativação de clientes
- Renderização da tabela de contatos

**Principais Funções**:
- `loadClients(page, pageSize)`
- `viewClient(id)`
- `editClient(id)`
- `updateClient(id)`
- `deleteClient(id)`
- `saveClient()`
- `renderContactsPagination()`

### 3. landscaping_projects.js
**Responsabilidade**: Responsável por todo o contexto relacionado à aba de Projetos.

**Funcionalidades**:
- Carregamento de projetos
- Quadro Kanban de projetos
- Visualização de detalhes do projeto
- Edição de projetos
- Exclusão de projetos
- Atualização de status de projetos
- Renderização da tabela de projetos

**Principais Funções**:
- `loadProjects()`
- `viewProject(id)`
- `editProject(id)`
- `deleteProject(id)`
- `updateProjectStatus(projectId, newStatus)`
- `renderPagination()`

### 4. landscaping_quotes.js
**Responsabilidade**: Contém o código referente à aba de Orçamentos.

**Funcionalidades**:
- Carregamento de orçamentos
- Visualização de orçamentos
- Edição de orçamentos
- Inativação de orçamentos
- Cálculo de totais de orçamentos
- Configuração de eventos para itens de orçamento

**Principais Funções**:
- `loadQuotes(page, pageSize)`
- `viewQuote(id)`
- `editQuote(id)`
- `inactivateQuote(id)`
- `calculateQuoteTotal()`
- `setupQuoteItemEvents()`
- `renderQuotesPagination()`

### 5. landscaping_services.js
**Responsabilidade**: Abrange todas as operações relacionadas à aba de Serviços.

**Funcionalidades**:
- Carregamento de serviços
- Visualização de detalhes do serviço
- Edição de serviços
- Criação de novos serviços
- Inativação de serviços
- Paginação de serviços

**Principais Funções**:
- `loadServices(page, pageSize)`
- `viewService(id)`
- `editService(id)`
- `updateService(id)`
- `inactivateService(id)`
- `saveService()`
- `renderServicesPagination()`

### 6. landscaping_maintenance.js
**Responsabilidade**: Responsável pela lógica da aba de Manutenção.

**Funcionalidades**:
- Carregamento de dados de manutenção
- Quadro Kanban de manutenção
- Atualização de status de manutenção
- Cálculo de receita mensal
- Criação de cards de manutenção

**Principais Funções**:
- `loadMaintenanceKanban()`
- `updateMaintenanceStatus(maintenanceId, newStatus)`
- `updateMonthlyRevenue()`
- `createMaintenanceCard(item)`
- `showMessage(message, type)`

## Como Usar

### Inclusão no HTML
Os módulos devem ser incluídos no HTML na seguinte ordem:

```html
<!-- Módulos do Landscaping -->
<script src="{{ url_for('static', filename='js/landscaping_core.js') }}"></script>
<script src="{{ url_for('static', filename='js/landscaping_contacts.js') }}"></script>
<script src="{{ url_for('static', filename='js/landscaping_projects.js') }}"></script>
<script src="{{ url_for('static', filename='js/landscaping_quotes.js') }}"></script>
<script src="{{ url_for('static', filename='js/landscaping_services.js') }}"></script>
<script src="{{ url_for('static', filename='js/landscaping_maintenance.js') }}"></script>
```

### Dependências
- jQuery
- Semantic UI
- Chart.js (para gráficos)

## Vantagens da Modularização

1. **Manutenibilidade**: Cada módulo contém apenas o código relacionado ao seu contexto específico
2. **Reutilização**: Módulos podem ser reutilizados em outras partes da aplicação
3. **Organização**: Código mais organizado e fácil de navegar
4. **Desenvolvimento em Equipe**: Diferentes desenvolvedores podem trabalhar em módulos diferentes
5. **Debugging**: Mais fácil identificar e corrigir problemas específicos
6. **Performance**: Possibilidade de carregar apenas os módulos necessários

## Observações Importantes

- O arquivo original `landscaping.js` **NÃO** deve ser modificado, servindo apenas como referência
- O `landscaping_core.js` deve ser sempre o primeiro a ser carregado
- Todas as funções mantêm a mesma assinatura e comportamento do arquivo original
- As variáveis globais (como `API_URL`) estão definidas no módulo core
- Cada módulo é independente e pode ser desenvolvido/mantido separadamente

## Estrutura de Arquivos

```
frontend/static/js/
├── landscaping.js (arquivo original - não modificar)
├── landscaping_core.js (módulo principal)
├── landscaping_contacts.js (módulo de contatos)
├── landscaping_projects.js (módulo de projetos)
├── landscaping_quotes.js (módulo de orçamentos)
├── landscaping_services.js (módulo de serviços)
├── landscaping_maintenance.js (módulo de manutenção)
└── README_LANDSCAPING_MODULES.md (este arquivo)
```