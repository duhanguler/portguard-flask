fetch("/uptime").then(res => res.json()).then(data => {
    const ctx = document.getElementById('uptimeChart').getContext('2d');
    const labels = data.map(d => d.target);
    const values = data.map(d => d.uptime);
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Uptime %',
                data: values,
                backgroundColor: 'rgba(13, 110, 253, 0.7)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});