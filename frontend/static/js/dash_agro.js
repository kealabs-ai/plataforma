$(document).ready(function() {
    // Dados simulados
    const simulatedData = {
        crop_production: [
            {crop: 'Soja', total_production: 118002},
            {crop: 'Milho', total_production: 0},
            {crop: 'Trigo', total_production: 0},
            {crop: 'Cana', total_production: 119228},
            {crop: 'Feijão', total_production: 51723}
        ],
        milk_production: [
            {month: '2025-01', total_liters: 5000},
            {month: '2025-02', total_liters: 5200},
            {month: '2025-03', total_liters: 4800},
            {month: '2025-04', total_liters: 5100},
            {month: '2025-05', total_liters: 5300},
            {month: '2025-06', total_liters: 5150}
        ],
        inputs_distribution: [
            {product: 'Adubo', total_cost: 12000}
        ],
        soil_ph: [
            {plot_name: 'Talhão 1', pH: 6.99},
            {plot_name: 'Talhão 2', pH: 6.96},
            {plot_name: 'Talhão 3', pH: 6.13},
            {plot_name: 'Talhão 4', pH: 7.23},
            {plot_name: 'Talhão 5', pH: 6.51},
            {plot_name: 'Talhão 6', pH: 5.92},
            {plot_name: 'Talhão 7', pH: 7.04},
            {plot_name: 'Talhão 8', pH: 6.46},
            {plot_name: 'Talhão 9', pH: 5.93},
            {plot_name: 'Talhão 10', pH: 5.80}
        ],
        financial_data: [
            {month: '2025-01', revenue: 25000, expense: 18000},
            {month: '2025-02', revenue: 28000, expense: 19000},
            {month: '2025-03', revenue: 22000, expense: 16000},
            {month: '2025-04', revenue: 26000, expense: 17500},
            {month: '2025-05', revenue: 29000, expense: 20000},
            {month: '2025-06', revenue: 27000, expense: 18500}
        ]
    };

    // Inicializa os gráficos
    try {
        // Gráfico de produção agrícola
        const cropChart = echarts.init(document.getElementById('crop-production-chart'));
        cropChart.setOption({
            title: {
                text: 'Produção por Cultura (kg)',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} kg ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [{
                name: 'Produção',
                type: 'pie',
                radius: '50%',
                data: simulatedData.crop_production.map(item => ({
                    value: item.total_production,
                    name: item.crop
                })),
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        });

        // Gráfico de produção leiteira
        const milkChart = echarts.init(document.getElementById('milk-production-chart'));
        milkChart.setOption({
            title: {
                text: 'Produção Leiteira Mensal (L)',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: simulatedData.milk_production.map(item => item.month)
            },
            yAxis: {
                type: 'value',
                name: 'Litros'
            },
            series: [{
                name: 'Produção de Leite',
                type: 'line',
                data: simulatedData.milk_production.map(item => item.total_liters),
                smooth: true,
                itemStyle: {
                    color: '#5470c6'
                },
                areaStyle: {
                    opacity: 0.3
                }
            }]
        });

        // Gráfico de insumos
        const inputsChart = echarts.init(document.getElementById('inputs-chart'));
        inputsChart.setOption({
            title: {
                text: 'Distribuição de Gastos com Insumos',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            xAxis: {
                type: 'value',
                name: 'Valor (R$)'
            },
            yAxis: {
                type: 'category',
                data: simulatedData.inputs_distribution.map(item => item.product)
            },
            series: [{
                name: 'Custo',
                type: 'bar',
                data: simulatedData.inputs_distribution.map(item => item.total_cost),
                itemStyle: {
                    color: '#91cc75'
                }
            }]
        });

        // Gráfico de pH do solo
        const soilChart = echarts.init(document.getElementById('soil-ph-chart'));
        soilChart.setOption({
            title: {
                text: 'pH do Solo por Talhão',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                data: simulatedData.soil_ph.map(item => item.plot_name),
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                name: 'pH',
                min: 5,
                max: 8
            },
            series: [{
                name: 'pH',
                type: 'bar',
                data: simulatedData.soil_ph.map(item => item.pH),
                itemStyle: {
                    color: function(params) {
                        const ph = params.value;
                        if (ph < 6.0) return '#ff6b6b'; // Ácido - vermelho
                        if (ph > 7.5) return '#4ecdc4'; // Alcalino - azul
                        return '#95de64'; // Neutro - verde
                    }
                },
                markLine: {
                    data: [
                        {yAxis: 6.0, name: 'pH Mínimo Ideal'},
                        {yAxis: 7.0, name: 'pH Máximo Ideal'}
                    ]
                }
            }]
        });

        // Gráfico financeiro
        const financialChart = echarts.init(document.getElementById('financial-chart'));
        financialChart.setOption({
            title: {
                text: 'Receita vs Despesa Mensal',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Receita', 'Despesa', 'Lucro'],
                bottom: 0
            },
            xAxis: {
                type: 'category',
                data: simulatedData.financial_data.map(item => item.month)
            },
            yAxis: {
                type: 'value',
                name: 'Valor (R$)'
            },
            series: [
                {
                    name: 'Receita',
                    type: 'bar',
                    data: simulatedData.financial_data.map(item => item.revenue),
                    itemStyle: {
                        color: '#52c41a'
                    }
                },
                {
                    name: 'Despesa',
                    type: 'bar',
                    data: simulatedData.financial_data.map(item => item.expense),
                    itemStyle: {
                        color: '#ff4d4f'
                    }
                },
                {
                    name: 'Lucro',
                    type: 'line',
                    data: simulatedData.financial_data.map(item => item.revenue - item.expense),
                    itemStyle: {
                        color: '#1890ff'
                    },
                    lineStyle: {
                        width: 3
                    }
                }
            ]
        });

        // Redimensiona gráficos quando a janela muda de tamanho
        window.addEventListener('resize', function() {
            cropChart.resize();
            milkChart.resize();
            inputsChart.resize();
            soilChart.resize();
            financialChart.resize();
        });

        // Exibe mensagem de sucesso
        $('#status-messages').html(
            `<div class="ui success message">
                <i class="close icon"></i>
                <div class="header">Dados carregados</div>
                <p>Os dados foram carregados com sucesso.</p>
            </div>`
        );

        // Configura botão de fechar nas mensagens
        $(document).on('click', '.message .close', function() {
            $(this).closest('.message').transition('fade');
        });

        // Configura botão de atualizar
        $('#refresh-data').on('click', function() {
            location.reload();
        });

    } catch (error) {
        console.error('Erro ao inicializar gráficos:', error);
        $('#status-messages').html(
            `<div class="ui negative message">
                <i class="close icon"></i>
                <div class="header">Erro na inicialização</div>
                <p>Não foi possível inicializar os gráficos: ${error.message}</p>
                <p>Verifique o console para mais detalhes.</p>
            </div>`
        );
    }
});