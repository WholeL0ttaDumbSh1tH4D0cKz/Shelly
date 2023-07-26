#H4D0cKz:SSH server starter
import sys
import os
import random
import time
import paramiko
import getpass
import socket
import platform
import subprocess
from argparse import ArgumentParser
from configparser import ConfigParser
from datetime import datetime

def get_arguments():
    parser = ArgumentParser(description='Start SSH server on a target machine')
    parser.add_argument('--user', type=str, required=True, help='Target user')
    parser.add_argument('--ip', type=str, required=True, help='Target IP address')
    return parser.parse_args()

def print_random_banner():
    banners = [
        "\033[92m          ,+'/.'+,    ___\n        \/\_/\_/\_/\,+' * \\\n\033[94m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m",
        "\033[32m _ \033[0m\033[32;2m .----.\033[0m\n\033[0m\033[32m(_\\\033[0m\033[32;2m/      \\\033[0m\033[32m_,\n  \033[0m\033[32;2m'\033[0m\033[32muu\033[0m\033[32;2m----\033[0m\033[32muu\033[0m\033[32;2m~'\033[0m"
    ]
    print(banners[0])

def get_local_ip():
    system = platform.system()
    if system == "Windows":
        try:
            # Use socket to get the local IP address on Windows
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except socket.error:
            pass
    elif system == "Linux":
        try:
            command = "ip route get 1 | awk '{print $NF;exit}'"
            local_ip = subprocess.check_output(command, shell=True).decode().strip()
            return local_ip
        except subprocess.CalledProcessError:
            pass
    elif system == "Android":
        try:
            command = "ip -4 route show scope global | grep wlan0 | awk '{print $9}'"
            local_ip = subprocess.check_output(command, shell=True).decode().strip()
            return local_ip
        except subprocess.CalledProcessError:
            pass

    return None

def get_local_user():
    system = platform.system()
    if system == "Windows":
        try:
            local_user = getpass.getuser()
            return local_user
        except Exception:
            pass
    elif system == "Linux" or system == "Android":
        try:
            # Use subprocess to get the username on Linux and Termux (Android)
            command = "whoami"
            local_user = subprocess.check_output(command, shell=True).decode().strip()
            return local_user
        except Exception:
            pass

    return None

def get_ssh_password():
    # Get the SSH password securely
    try:
        ssh_password = getpass.getpass(prompt="Enter SSH password: ")
        return ssh_password
    except KeyboardInterrupt:
        sys.exit("\nPassword entry aborted. Exiting...")

def generate_ssh_key_pair(save_folder):
    try:
        os.makedirs(save_folder, exist_ok=True)  # Create the 'saves' folder if it doesn't exist
        date_folder = os.path.join(save_folder, datetime.now().strftime("%m-%d-%Y"))
        os.makedirs(date_folder, exist_ok=True)  # Create a subfolder with the current date

        # Generate the SSH key pair
        key = paramiko.RSAKey.generate(2048)

        # Save the private key
        private_key_file = os.path.join(date_folder, 'id_rsa')
        with open(private_key_file, 'w') as f:
            key.write_private_key(f)

        # Save the public key
        public_key_file = os.path.join(date_folder, 'id_rsa.pub')
        with open(public_key_file, 'w') as f:
            f.write(f'{key.get_name()} {key.get_base64()}')

        print(f"SSH key pair generated and saved to \"{date_folder}\"")
        return private_key_file  # Return the path of the generated private key
    except Exception as e:
        sys.exit(f"Error generating and saving SSH key pair: {e}")

def read_config():
    # Create a ConfigParser instance and read the config file
    config = ConfigParser()
    config.read('config.ini')

    # Get the SSH configuration from the 'SSH' section of the config file
    ssh_config = config['SSH']
    port = ssh_config.getint('port', fallback=22)  # Default port is 22 if not specified

    return port

def start_ssh_server(private_key_file):
    # Initialize SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Use the generated private key for authentication
        key = paramiko.RSAKey.from_private_key_file(private_key_file)
        client.connect(Tip, username=Tuser, pkey=key, port=read_config())

        # Start the SSH server on the target machine
        stdin, stdout, stderr = client.exec_command("sshd")

        # Wait for a few seconds to allow the server to start
        time.sleep(3)

        print("\033[32mOpenSSH server started\033[32m")
    except paramiko.AuthenticationException:
        print(f"\033[31mFailed to connect. Invalid SSH credentials for user '{Tuser}' on IP '{Tip}'.\033[0m")
    except paramiko.SSHException as e:
        print(f"\033[31mSSH connection failed\033[0m: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def start_ssh_server_with_retry(private_key_file, max_retries=3, retry_delay=5):
    for attempt in range(1, max_retries + 1):
        print(f"Attempting SSH connection - Attempt {attempt}")
        try:
            start_ssh_server(private_key_file)
            return  # If the connection is successful, exit the retry loop.
        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(retry_delay)

    print("\033[31mFailed to start SSH server after multiple attempts.\033[0m\nExiting...")
def save_public_key_to_network(public_key, network_path):
    try:
        with open(network_path, 'w') as f:
            f.write(public_key)
        print(f"Public key saved to {network_path}")
    except Exception as e:
        sys.exit(f"Error saving public key to {network_path}: {e}")

def wait_for_public_key_download(network_path, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(network_path):
            print("Public key downloaded successfully.")
            return True
        time.sleep(2)
    print("Timed out waiting for the public key download.")
    return False
def save_public_key_to_target(public_key, target_ip, target_user):
    try:
        # Initialize SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the target machine using SSH
        client.connect(target_ip, username=target_user)

        # Save the public key to the target machine
        target_path = f'/home/{target_user}/id_rsa.pub'  # Change this to the desired location on the target machine
        stdin, stdout, stderr = client.exec_command(f"echo '{public_key}' > {target_path}")
        client.close()

        print(f"Public key saved to {target_path} on the target machine.")
    except paramiko.AuthenticationException:
        print("Authentication failed. Check your SSH credentials.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    args = get_arguments()
    Tuser = args.user
    Tip = args.ip

    def get_public_key():
        # Load the public key from the generated SSH key pair
        public_key_file = os.path.join(save_folder, datetime.now().strftime("%m-%d-%Y"), 'id_rsa.pub')
        with open(public_key_file, 'r') as f:
            return f.read()

    print_random_banner()
    print(f'user:\033[31m{Tuser}\033[0m')
    print(f'ip:\033[31m{Tip}\033[0m')
    print("\033[33m------------------------------\033[0m")

    # Get local IP and user
    Lip = get_local_ip()
    Luser = get_local_user()

    if Luser:
        None
    else:
        print("\033[31mFailed to retrieve the username.\033[0m")

    if Lip:
        None
    else:
        print("\033[31mFailed to retrieve the local IP address.\033[0m")

    # Generate and save the SSH key pair
    save_folder = 'saves'
    private_key_file = generate_ssh_key_pair(save_folder)

    # Save the public key to a network-accessible location
    public_key = get_public_key()
    network_path = f'saves\{datetime.now().strftime("%m-%d-%Y")}\id_rsa.pub'
    save_public_key_to_target(public_key, Tip, Tuser)

    # Wait for the public key to be downloaded (if needed) on the target machine
    print("Waiting for the public key to be downloaded on the target machine...")
    if wait_for_public_key_download(network_path):
        try:
            start_ssh_server(private_key_file)
        except:
            start_ssh_server_with_retry(private_key_file)