// static/js/grafico_resumo.js

document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('graficoResumo').getContext('2d');

    // Valores injetados pelo Django no template
    const receitas = parseFloat(document.getElementById('graficoResumo').dataset.receitas);
    const despesas = parseFloat(document.getElementById('graficoResumo').dataset.despesas);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Receitas', 'Despesas'],
            datasets: [{
                label: 'Valores em R$',
                data: [receitas, despesas],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',   // Verde para receitas
                    'rgba(220, 53, 69, 0.8)'     // Vermelho para despesas
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'R$ ' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            }
        }
    });
});