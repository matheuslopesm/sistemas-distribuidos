import threading
import time
import random

class ExclusaoMutuaCentralizado:
    def __init__(self, recurso_arquivo):
        self.coordenador = None
        self.mutex = threading.Lock()
        self.recurso_arquivo = recurso_arquivo

    def solicitar_acesso(self, dispositivo_id):
        with self.mutex:
            if self.coordenador is None:
                self.coordenador = dispositivo_id
                print(f"Dispositivo {dispositivo_id} tornou-se o coordenador.")
            else:
                print(f"Dispositivo {dispositivo_id} solicitou acesso ao coordenador {self.coordenador}.")
                self.escrever_arquivo(dispositivo_id)

    def liberar_acesso(self, dispositivo_id):
        with self.mutex:
            if self.coordenador == dispositivo_id:
                print(f"Dispositivo {dispositivo_id} liberou o acesso.")
                self.coordenador = None
            else:
                print(f"Dispositivo {dispositivo_id} não é o coordenador atual. Não pode liberar acesso.")

    def escrever_arquivo(self, dispositivo_id):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.recurso_arquivo, 'a') as arquivo:
            arquivo.write(f"Dispositivo {dispositivo_id}, Timestamp: {timestamp}\n")

# Exemplo de uso
recurso_arquivo = "recurso.txt"
exclusao_mutua = ExclusaoMutuaCentralizado(recurso_arquivo)

# Simulação de solicitações de acesso
for dispositivo_id in range(1, 5):
    exclusao_mutua.solicitar_acesso(dispositivo_id)
    time.sleep(random.uniform(0.5, 2.0))  # Simula o tempo entre solicitações
    exclusao_mutua.liberar_acesso(dispositivo_id)
