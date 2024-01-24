import socket
import ipaddress
import subprocess


def get_local_ips():
    local_ips = []

    try:
        host_name = socket.gethostname()

        host_ip = socket.gethostbyname(host_name)
        print(f"My IP address is: {host_ip}")

        network = ipaddress.IPv4Network(f"{host_ip}/24", strict=False)

        for ip in network.hosts():
            local_ips.append(str(ip))

        return local_ips[:4]

    except Exception as e:
        print(f"Erro ao obter endereços IP: {str(e)}")

    return local_ips


def ping_host(ip):
    try:
        subprocess.run(["ping", "-c", "1", ip], check=True)
        print(f"Ping para {ip} foi bem-sucedido.")
    except subprocess.CalledProcessError:
        print(f"Ping para {ip} falhou.")


ip_addresses = get_local_ips()
print(f"IP addresses of the first four hosts in the local network: {ip_addresses}")

for ip in ip_addresses:
    if ip != socket.gethostbyname(socket.gethostname()):
        ping_host(ip)
