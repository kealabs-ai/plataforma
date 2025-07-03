# Instruções para Atualizar as Páginas Restantes

Para atualizar as páginas restantes para usar o template base, siga o padrão abaixo:

1. Abra cada arquivo HTML nas pastas:
   - properties/area_and_crop.html
   - activities_inputs/agricultural_inputs.html
   - activities_inputs/field_operations.html
   - finance/expenses_vs_revenues.html
   - operations/milk_production.html

2. Substitua todo o conteúdo pelo seguinte modelo, ajustando conforme necessário:

```html
{% extends "base.html" %}

{% set active_menu = 'NOME_DA_PASTA' %}
{% set active_submenu = 'NOME_DO_ARQUIVO_SEM_EXTENSAO' %}

{% block title %}TÍTULO_DA_PÁGINA - Kognia{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/dash_agro.css') }}">
{% endblock %}

{% block content %}
<div class="ui segment">
    <div class="ui grid">
        <div class="twelve wide column">
            <h2 class="ui header">
                <i class="ICONE_APROPRIADO icon"></i>
                <div class="content">
                    TÍTULO_DA_PÁGINA
                    <div class="sub header">SUBTÍTULO_DA_PÁGINA</div>
                </div>
            </h2>
        </div>
        <div class="four wide column right aligned">
            <button id="refresh-data" class="ui green button">
                <i class="sync icon"></i>
                Atualizar Dados
            </button>
        </div>
    </div>
    
    <!-- Área para mensagens de status -->
    <div id="status-messages"></div>
    
    <!-- CONTEÚDO_ESPECÍFICO_DA_PÁGINA -->
    <!-- Copie o conteúdo específico da página original aqui -->
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<!-- Adicione outros scripts específicos da página aqui -->
{% endblock %}
```

3. Ajuste os valores conforme necessário:
   - `active_menu`: nome da pasta (dashboards, properties, activities_inputs, finance, operations)
   - `active_submenu`: nome do arquivo sem extensão (ex: area_and_crop)
   - `TÍTULO_DA_PÁGINA`: título que aparece na aba do navegador
   - `ICONE_APROPRIADO`: ícone do Semantic UI apropriado para a página
   - `SUBTÍTULO_DA_PÁGINA`: subtítulo descritivo da página
   - `CONTEÚDO_ESPECÍFICO_DA_PÁGINA`: conteúdo específico da página original

4. Mantenha os scripts específicos de cada página no bloco `extra_js`

Seguindo este padrão, todas as páginas terão um layout consistente com o menu superior.