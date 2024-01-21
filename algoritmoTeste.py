import subprocess

# Lista de IPs das máquinas
ips = ["172.16.100.2", "172.16.100.3", "172.16.100.4", "172.16.100.5", "172.16.100.6"]

def testar_comunicacao(ip_origem, ip_destino):
    try:
        # Executa o comando de ping
        subprocess.run(["ping", "-c", "4", ip_destino], check=True)
        print(f"Comunicação de {ip_origem} para {ip_destino}: OK")
    except subprocess.CalledProcessError:
        print(f"Falha na comunicação de {ip_origem} para {ip_destino}")

# Testa a comunicação entre todas as máquinas
for i, ip_origem in enumerate(ips):
    for j, ip_destino in enumerate(ips):
        if i != j:  # Evita ping da máquina para ela mesma
            testar_comunicacao(f"maquina_{i}", ip_destino)
