from flask import Flask, request, jsonify
from ssh_remote import ssh_connect, ssh_run_script_from_url
from slack_sdk import WebClient

app = Flask(__name__)  # create app instance

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


# Slack Bot OAuth token (keep secret!)
slack_token = "xoxb-9286285858423-9317413199649-ibEDsdDNegwmLG3MuWMTE9f1"
client = WebClient(token=slack_token)

def send_message(channel, text):
    response = client.chat_postMessage(channel=channel, text=text)
    return response

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    # Handle Slack URL verification challenge
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})

    # Handle Slack events
    if 'event' in data:
        event = data['event']
        text = event.get('text', '').strip()
        channel = event['channel']

        # SSH command
        if text.lower().startswith("!ssh"):
            try:
                parts = text.split()
                _, host, user, password, *cmd_parts = parts
                command = " ".join(cmd_parts)

                output, error = ssh_connect(host, user, password, command)

                if error:
                    response = f"❗Error:\n```{error}```"
                else:
                    response = f"✅ Output:\n```{output}```"

                send_message(channel, response)

            except Exception as e:
                send_message(channel, f"❌ Failed to run command: {e}")

        # Run remote script command
        elif text.lower().startswith("!runscript"):
            try:
                parts = text.split()
                # Minimum 5 parts: !runscript host user password script_url
                if len(parts) < 5:
                    send_message(channel, "❗ Usage: !runscript <host> <user> <password> <script_url>")
                else:
                    _, host, user, password, script_url = parts[:5]

                    output, error = ssh_run_script_from_url(host, user, password, script_url)

                    if error:
                        response = f"❗Error:\n```{error}```"
                    else:
                        response = f"✅ Output:\n```{output}```"

                    send_message(channel, response)

            except Exception as e:
                send_message(channel, f"❌ Failed to run script: {e}")

    return '', 200


# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
