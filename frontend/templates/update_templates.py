import os
import re

# Diretórios a serem processados
directories = [
    'dashboards',
    'properties',
    'activities_inputs',
    'finance',
    'operations'
]

# Função para extrair o título da página
def extract_title(content):
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        return title_match.group(1)
    return "Kognia Agro"

# Função para extrair o conteúdo principal
def extract_content(content):
    # Procura pelo conteúdo principal
    content_match = re.search(r'<div class="ui (bottom attached )?segment">(.*?)</div>\s*</div>\s*(</body>|<script)', content, re.DOTALL)
    if content_match:
        return content_match.group(2).strip()
    return ""

# Função para extratar scripts extras
def extract_extra_js(content):
    # Procura por scripts extras
    js_match = re.search(r'<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>(.*?)</body>', content, re.DOTALL)
    if js_match:
        return js_match.group(1).strip()
    return ""

# Função para criar o novo conteúdo do template
def create_template_content(filename, directory, title, content, extra_js):
    menu_name = directory
    submenu_name = os.path.splitext(filename)[0]
    
    template = f'''{% extends "base.html" %}

{{% set active_menu = "{menu_name}" %}}
{{% set active_submenu = "{submenu_name}" %}}

{{% block title %}}{title}{{% endblock %}}

{{% block extra_css %}}
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/dash_agro.css') }}}}">
{{% endblock %}}

{{% block content %}}
<div class="ui segment">
{content}
</div>
{{% endblock %}}

{{% block extra_js %}}
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
{extra_js}
{{% endblock %}}'''
    
    return template

# Processar cada diretório
for directory in directories:
    dir_path = os.path.join(os.path.dirname(__file__), directory)
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.html') and filename != 'dash_general.html':  # Já atualizamos este
                file_path = os.path.join(dir_path, filename)
                
                # Ler o conteúdo atual
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extrair informações
                title = extract_title(content)
                main_content = extract_content(content)
                extra_js = extract_extra_js(content)
                
                # Criar novo conteúdo
                new_content = create_template_content(filename, directory, title, main_content, extra_js)
                
                # Salvar o novo conteúdo
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Atualizado: {file_path}")

print("Todas as páginas foram atualizadas para usar o template base.")