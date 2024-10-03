# SSH Brute Force Script

This Python script is designed to perform brute-force attacks on SSH servers using provided username and password wordlists. The script uses multi-threading for faster password cracking and displays verbose output for debugging.

## Features:
- Brute-force SSH login using a single username or a username list.
- Multi-threaded to improve the speed of the brute-force attack.
- Verbose output to track the progress of the attack.
- Automatically stops after successful login is found.

## Usage:
python ssh_bruteforce.py -i <target IP> -u <username> -w <password wordlist>
Example Commands:
Brute-force using a single username:
python ssh_bruteforce.py -i 192.168.1.100 -u admin -w passwords.txt

Brute-force using a username list and password list:
python ssh_bruteforce.py -i 192.168.1.100 -ulist usernames.txt -w passwords.txt

## Arguments:
-i, --target: Target IP address (required)
-u, --username: Single username to use (optional if using a userlist)
-ulist, --userlist: File containing a list of usernames (optional if using a single username)
-w, --wordlist: File containing a list of passwords (required)
-p, --port: SSH port (default is 22)
-T, --threads: Number of threads (default is 5)
-v, --verbose: Enable verbose mode to see detailed logs

## Disclaimer:
This script is intended for educational and ethical purposes only. Do not use it to brute-force systems you do not own or have permission to access. Misuse of this tool may be illegal.
