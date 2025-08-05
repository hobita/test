import subprocess

# Command to run (you can change it to 'uptime', 'df -h', etc.)
command = ["ls", "-l"]

try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("📤 Command Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ Error:")
    print(e.stderr)
