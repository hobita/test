import subprocess

# Ask the user to enter a command
user_input = input("💻 Enter a command to run: ")
command = user_input.strip().split()

try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("📤 Command Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ Error:")
    print(e.stderr)
except FileNotFoundError:
    print("🚫 Command not found.")
