import sys
import random
import time
import paramiko
import getpass
import socket
import platform
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser(description='Example command-line arguments')
parser.add_argument('--user', type=str, help='give target user')
parser.add_argument('--ip', type=str, help='give target ip')
args = parser.parse_args()
Tuser = args.user
Tip = args.ip
banners = ["""\033[92m          ,+'/.'+,    ___\n        \/\_/\_/\_/\,+' * \\\n\033[94m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m""",
           """\033[32m _ \033[0m\033[32;2m .----.\033[0m\n\033[0m\033[32m(_\\\033[0m\033[32;2m/      \\\033[0m\033[32m_,\n  \033[0m\033[32;2m'\033[0m\033[32muu\033[0m\033[32;2m----\033[0m\033[32muu\033[0m\033[32;2m~'\033[0m"""]
print(banners[0])
print(f'user:\033[31m{Tuser}\033[0m')
print(f'ip:\033[31m{Tip}\033[0m')
print("\033[33m------------------------------\033[0m")

system = platform.system()
Lip = None
Luser = None
if system == "Windows":
    try:
        # Use socket to get the local Lip address on Windows
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Lip = s.getsockname()[0]
        s.close()
    except socket.error:
        pass
elif system == "Linux":
    try:
        command = "ip route get 1 | awk '{print $NF;exit}'"
        Lip = subprocess.check_output(command, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        pass
elif system == "Android":
    try:
        command = "ip -4 route show scope global | grep wlan0 | awk '{print $9}'"
        Lip = subprocess.check_output(command, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        pass

if system == "Windows":
    try:
        username = getpass.getuser()
    except Exception as e:
        pass
elif system == "Linux" or system == "Android":
    try:
        # Use subprocess to get the username on Linux and Termux (Android)
        command = "whoami"
        username = subprocess.check_output(command, shell=True).decode().strip()
    except Exception as e:
        pass

if username:
    print(f"Username: {username}")
else:
    print("Failed to retrieve the username.")
if Lip:
    print(f"Local_ip:\033[32m{Lip}\033[0m")
else:
    print("Failed to retrieve the local Lip address.")

def get_ssh_password():
    # Get the SSH password securely
    try:
        Lpass = getpass.getpass(prompt="Enter SSH password: ")
        return Lpass
    except KeyboardInterrupt:
        sys.exit("\nPassword entry aborted. Exiting...")

def start_ssh_server():
    # Initialize SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    Lpass = get_ssh_password()

    try:
        # Connect to the target machine
        client.connect(Tip, username=Tuser, password=Lpass, port=22)

        # Start the SSH server on the target machine
        stdin, stdout, stderr = client.exec_command("sshd")

        # Wait for a few seconds to allow the server to start
        time.sleep(3)

        print("\033[32mOpenSSH server started\033[32m")
    except paramiko.AuthenticationException:
        print("Authentication failed. Check your SSH credentials.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_ssh_server()