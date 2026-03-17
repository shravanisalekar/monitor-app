from flask import Flask, render_template_string
import psutil

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h2 style="text-align:center;">CPU & Memory Usage</h2>
    <canvas id="chart" width="400" height="200"></canvas>

    <script>
        async function fetchData() {
            const response = await fetch('/metrics');
            return await response.json();
        }

        async function updateChart(chart) {
            const data = await fetchData();
            chart.data.datasets[0].data = [data.cpu, data.memory];
            chart.update();
        }

        const ctx = document.getElementById('chart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['CPU %', 'Memory %'],
                datasets: [{
                    label: 'Usage',
                    data: [0, 0]
                }]
            }
        });

        setInterval(() => updateChart(chart), 2000);
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