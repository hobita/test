import paramiko

def ssh_connect(host, user, password, command):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect
        client.connect(hostname=host, username=user, password=password)
        print(f"✅ Connected to {host}")

        # Execute command
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Clean up
        client.close()

        return output, error

    except Exception as e:
        return "", f"❌ Connection failed: {e}"

# User inputs
if __name__ == "__main__":
    host = input("🌐 SSH Host (e.g. 192.168.1.10): ")
    user = input("👤 Username: ")
    password = input("🔑 Password: ")
    command = input("💻 Command to run: ")

    out, err = ssh_connect(host, user, password, command)

    print("\n📤 Output:\n", out)
    if err:
        print("❗ Error:\n", err)
