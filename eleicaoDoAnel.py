import threading
import time
import random

class EleicaoAnel:
    def __init__(self, num_dispositivos, recurso_arquivo):
        self.coordenador = None
        self.num_dispositivos = num_dispositivos
        self.mutex = threading.Lock()
        self.recurso_arquivo = recurso_arquivo

    def iniciar_eleicao(self, dispositivo_id):
        with self.mutex:
            if self.coordenador is None:
                self.coordenador = dispositivo_id
                print(f"Dispositivo {dispositivo_id} tornou-se o coordenador.")
            else:
                print(f"Dispositivo {dispositivo_id} iniciou eleição.")
                candidato = dispositivo_id
                proximo_vizinho = (dispositivo_id % self.num_dispositivos) + 1
                self.notificar_vizinho(proximo_vizinho, candidato)

    def notificar_vizinho(self, vizinho_id, candidato):
        print(f"Dispositivo {candidato} passou a eleição para dispositivo {vizinho_id}.")
        time.sleep(random.uniform(0.5, 2.0))  # Simula o tempo de comunicação
        self.iniciar_eleicao(vizinho_id)

    def escrever_arquivo(self, mensagem):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.recurso_arquivo, 'a') as arquivo:
            arquivo.write(f"{mensagem} - Timestamp: {timestamp}\n")

# Exemplo de uso
recurso_arquivo = "recurso_eleicao.txt"
eleicao_anel = EleicaoAnel(num_dispositivos=4, recurso_arquivo=recurso_arquivo)

# Simulação de início de eleição
for dispositivo_id in range(1, 5):
    eleicao_anel.iniciar_eleicao(dispositivo_id)
    time.sleep(random.uniform(0.5, 2.0))  # Simula o tempo entre inícios de eleição
    eleicao_anel.escrever_arquivo(f"Dispositivo {dispositivo_id} é o coordenador atual: {eleicao_anel.coordenador}")
