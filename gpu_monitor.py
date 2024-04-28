from flask import Flask, jsonify, render_template
import paramiko
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace these with your server's details
servers = [
    {'host': '192.168.1.50', 'username': 'username1, 'password': 'password123'},
    {'host': '192.168.1.51', 'username': 'username2, 'password': 'password123'},
    {'host': '192.168.1.52', 'username': 'username3, 'password': 'password123'},
    {'host': '192.168.1.53', 'username': 'username4, 'password': 'password123'},
    {'host': '192.168.1.54', 'username': 'username5, 'password': 'password123'},
    {'host': '192.168.1.55', 'username': 'username6, 'password': 'password123'}
]

def get_gpu_stats(server):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server['host'], username=server['username'], password=server['password'], port=22)
    
    command = 'nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,temperature.gpu --format=csv,noheader'
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    client.close()

    gpu_stats = []
    for line in output.strip().split('\n'):
        index, name, gpu_util, mem_util, temp = line.split(', ')
        gpu_stats.append({
            'index': index,
            'name': name,
            'gpu_load': gpu_util,
            'memory_usage': mem_util,
            'temperature': temp
        })
    return gpu_stats

@app.route('/gpu_stats')
def index_gpu_stats():
    all_gpu_stats = {}
    for server in servers:
        stats = get_gpu_stats(server)
        all_gpu_stats[server['host']] = stats
    print("Data fetched:", all_gpu_stats)  # Log the data being sent to the frontend
    return jsonify(all_gpu_stats)

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
