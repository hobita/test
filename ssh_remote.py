import paramiko

#Run distant script Git 
def ssh_run_script_from_url(host, user, password, script_url):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password)

        script_name = script_url.split('/')[-1]  # Extraire le nom du fichier

        commands = [
            f"curl -O {script_url}",     # Télécharger le script
            f"chmod +x {script_name}",   # Le rendre exécutable
            f"./{script_name}"           # Lancer le script
        ]

        full_command = " && ".join(commands)
        stdin, stdout, stderr = client.exec_command(full_command)

        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()

        return output, error

    except Exception as e:
        return "", f" SSH Error: {e}"


# Run simple cmnd via SSH
def ssh_connect(host, user, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password)

        print(f" Connected to {host}")
        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()

        return output, error

    except Exception as e:
        return "", f" Connection failed: {e}"


# Manual Test Mode(No API needed)

if __name__ == "__main__":
    host = input(" SSH Host (e.g. 192.168.1.10): ")
    user = input(" Username: ")
    password = input(" Password: ")
    command = input(" Command to run: ")

    out, err = ssh_connect(host, user, password, command)

    print("\n Output:\n", out)
    if err:
        print(" Error:\n", err)

