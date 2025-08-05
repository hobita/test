from flask import Flask, request, jsonify
from ssh_remote import ssh_connect, ssh_run_script_from_url
from slack_sdk import WebClient
app = Flask(__name__)  #create app instance

# Route pour exécuter une commande SSH
@app.route('/ssh', methods=['POST'])
def run_command():
    try:
        data = request.get_json()
        host = data['host']
        user = data['user']
        password = data['password']
        command = data['command']

        output, error = ssh_connect(host, user, password, command)

        return jsonify({
            "success": error == "",
            "output": output,
            "error": error
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# Route pour exécuter un script distant via SSH
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        data = request.get_json()
        host = data['host']
        user = data['user']
        password = data['password']
        script_url = data['script_url']

        output, error = ssh_run_script_from_url(host, user, password, script_url)

        success = True
        if (
            "command not found" in error
            or "No such file" in error
            or "Permission denied" in error
        ):
            success = False

        return jsonify({
            "success": success,
            "output": output,
            "error": error
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400




# $$$salck token$$$#

slack_token = "# $$$salck token$$$#"
client = WebClient(token=slack_token)

def send_message(channel, text):
    response = client.chat_postMessage(channel=channel, text=text)
    return response

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    # Pour la validation de l'URL Slack
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})

    # Répondre aux messages qui contiennent "hello"
    if 'event' in data:
        event = data['event']
        if event.get('type') == 'message' and 'hello' in event.get('text', '').lower():
            channel = event['channel']
            send_message(channel, "Hi! I am your DevOps bot 🤖")

    return '', 200


# 🚀 Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

