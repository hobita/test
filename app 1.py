from flask import Flask, request, jsonify
import ssh_remote  # imports your ssh_remote.py

app = Flask(__name__)

@app.route('/ssh', methods=['POST'])
def ssh():
    data = request.json
    host = data.get('host')
    user = data.get('user')
    password = data.get('password')
    command = data.get('command', 'echo "Test SSH"')

    if not all([host, user, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    output, error = ssh_remote.ssh_connect(host, user, password, command)
    if error and error.startswith("❌"):
        return jsonify({'success': False, 'error': error}), 500

    return jsonify({'success': True, 'output': output, 'error': error})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

