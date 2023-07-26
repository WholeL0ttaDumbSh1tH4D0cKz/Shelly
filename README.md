# SHELLY

SHELLY (SSH Server Starter Script) is a Python script that facilitates starting an SSH server on a target machine. The script generates an SSH key pair, saves the public key to a network-accessible location, and then attempts to connect to the target machine to start the SSH server. If needed, the script waits for the public key to be downloaded on the target machine before starting the SSH server.

## Prerequisites

Before using SHELLY, ensure the following requirements are met on both the machine running the script (local machine) and the target machine:

1. Python 3.x installed on both machines.
2. The paramiko library must be installed. You can install it using pip:
`pip install -r requirements.txt`
---
![TURT](images/SHELL.png)
## How to Use
Download the shelly.py script and ensure the prerequisites are met on both the local and target machines.

Open a terminal or command prompt on the local machine and navigate to the directory containing the main.py script.

Run the script with the following command:
`python shelly.py --user <TARGET_USER> --ip <TARGET_IP>`
Replace <TARGET_USER> with the username of the target machine and <TARGET_IP> with the IP address of the target machine.
# NOTES
The script will make multiple attempts to start the SSH server if it fails initially due to authentication issues or SSH connection problems.

The config.ini file in the same directory as the script can be used to configure the SSH port (default: 22). You can create the file if it doesn't exist and specify the port:
--
[SSH]\
port = 22
--
The script may require elevated privileges to run, especially on Windows systems. Make sure you have the necessary permissions.

Ensure that the script has necessary firewall and network access to connect to the target machine via SSH.


# This script is for educational and testing purposes only. Do not use it for illegal activities or to harm others. The creators of this script are not responsible for any misuse or damage caused by it.
--