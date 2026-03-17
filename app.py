from flask import Flask, render_template_string
import psutil

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            text-align: center;
            font-family: Arial;
            background: #f4f4f4;
        }
        .container {
            display: flex;
            justify-content: center;
            gap: 50px;
            margin-top: 50px;
        }
        .chart-box {
            width: 300px;
        }
    </style>
</head>
<body>

<h1>System Monitoring Dashboard</h1>

<div class="container">
    <div class="chart-box">
        <canvas id="cpuChart"></canvas>
    </div>
    <div class="chart-box">
        <canvas id="memChart"></canvas>
    </div>
</div>

<script>
let cpuChart, memChart;

function createGauge(ctx, value, label) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: ['#4CAF50', '#ddd'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: label + ": " + value + "%"
                }
            }
        }
    });
}

function loadData() {
    fetch('/metrics')
    .then(res => res.json())
    .then(data => {
        if (cpuChart) cpuChart.destroy();
        if (memChart) memChart.destroy();

        cpuChart = createGauge(document.getElementById('cpuChart'), data.cpu, "CPU");
        memChart = createGauge(document.getElementById('memChart'), data.memory, "Memory");
    });
}

setInterval(loadData, 2000);
loadData();
</script>

</body>
</html>
"""
 


@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/metrics')
def metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
import os

port = int(os.environ.get("PORT", 5000))

app.run(host="0.0.0.0", port=port)