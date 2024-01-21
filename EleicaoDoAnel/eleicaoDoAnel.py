import time
import threading

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

# Simulação do processo de eleição
def simulacao_eleicao():
    for _ in range(3):  # Simula três rodadas de eleições
        realizar_eleicao()

# Inicia a simulação do processo de eleição
simulacao_eleicao()
