import time
import threading
import os
import random

# Lista de IPs das máquinas
ips = ["172.16.100.2", "172.16.100.3", "172.16.100.4", "172.16.100.5", "172.16.100.6"]

# Variável para identificar o Coordenador
coordenador_id = 0
coordenador_ip = ips[coordenador_id]

# Mutex para exclusão mútua
mutex = threading.Lock()

# Variável para identificar o líder atual
lider_id = None
lider_ip = None

# Função para acessar o recurso compartilhado
def acessar_recurso(id, hostname, timestamp):
    global coordenador_id
    global coordenador_ip

    with mutex:
        print(f"Máquina {id} ({hostname}) está acessando o recurso compartilhado...")
        
        # Simula o acesso ao recurso
        with open("recurso_compartilhado.txt", "a") as arquivo:
            arquivo.write(f"Máquina {id} ({hostname}) acessou o recurso em {timestamp}\n")
        
        print(f"Acesso do Máquina {id} ({hostname}) ao recurso compartilhado concluído.")

        # Simula dinamicamente a falha do coordenador após alguns acessos
        if random.random() < 0.2:  # Aproximadamente 20% de chance de falha após cada acesso
            falhar_coordenador(id, hostname)

# Função para falhar o coordenador e iniciar o processo de eleição
def falhar_coordenador(id, hostname):
    global coordenador_id
    global coordenador_ip

    with mutex:
        print(f"*** Falha detectada! Máquina {coordenador_id} ({coordenador_ip}) falhou. Iniciando eleição...")

        # Simula a eleição
        realizar_eleicao()

# Função para realizar a eleição
def realizar_eleicao():
    global lider_id
    global lider_ip

    with mutex:
        print("Iniciando processo de eleição...")

        # Encontrar o próximo candidato a líder
        if lider_id is None or lider_id == max(range(len(ips))):
            candidato_id = 0
        else:
            candidato_id = lider_id + 1

        # Notificar o próximo candidato a líder
        print(f"Máquina {candidato_id} iniciando eleição...")

        # Simular a comunicação entre as máquinas
        time.sleep(1)

        # Atualizar o líder
        lider_id = candidato_id
        lider_ip = ips[candidato_id]

        print(f"Máquina {lider_id} ({lider_ip}) é o novo líder.")

# Simulação de solicitações de acesso
def simulacao():
    for i, ip in enumerate(ips):
        id = i
        hostname = f"maquina_{i}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        solicitar_acesso(id, hostname)
        time.sleep(1)  # Aguarda um segundo antes da próxima solicitação
        acessar_recurso(id, hostname, timestamp)

# Função para solicitar acesso ao recurso
def solicitar_acesso(id, hostname):
    global coordenador_ip

    print(f"Máquina {id} ({hostname}) está solicitando acesso ao recurso...")

    # Envia solicitação para o Coordenador
    with mutex:
        print(f"Solicitação de Máquina {id} ({hostname}) enviada para o Coordenador {coordenador_ip}.")

# Inicia a simulação
simulacao()
