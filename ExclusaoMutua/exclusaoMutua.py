import socket
import threading
import queue
import time

class Coordenador:
    def __init__(self):
        self.lider = None
        self.fila_de_requisicoes = queue.Queue()
        self.mutex = threading.Lock()

    def inicia_coordenador(self):
        # Inicia o coordenador em uma porta disponível
        self.lider = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lider.bind(('0.0.0.0', 0))  # 0 indica que a porta será atribuída automaticamente
        endereco = self.lider.getsockname()
        print(f"Coordenador iniciado na porta {endereco[1]}")

        self.lider.listen(5)

        while True:
            # Aguarda uma conexão de um processo
            cliente, endereco_cliente = self.lider.accept()
            threading.Thread(target=self.lida_com_requisicao, args=(cliente, endereco_cliente)).start()

    def lida_com_requisicao(self, cliente, endereco_cliente):
        with self.mutex:
            # Verifica se há outros processos acessando o recurso
            if not self.fila_de_requisicoes.empty():
                print(f"Recurso ocupado. Adicionando à fila. Solicitação de {endereco_cliente}.")
                self.fila_de_requisicoes.put((cliente, endereco_cliente))
            else:
                print(f"Recurso livre. Concedendo acesso a {endereco_cliente}.")
                self.concede_acesso(cliente, endereco_cliente)

    def concede_acesso(self, cliente, endereco_cliente):
        # Simula o acesso ao recurso compartilhado com um tempo mais realista
        tempo_processamento = 5  # 5 segundos de processamento
        print(f"Iniciando acesso ao recurso por {tempo_processamento} segundos.")
        time.sleep(tempo_processamento)
        print("Acesso concluído.")

        # Libera o próximo processo na fila
        if not self.fila_de_requisicoes.empty():
            proximo_cliente, proximo_endereco_cliente = self.fila_de_requisicoes.get()
            print(f"Concedendo acesso a {proximo_endereco_cliente}.")
            proximo_cliente.sendall(b"Acesso concedido.")
            proximo_cliente.close()
        else:
            cliente.sendall(b"Acesso concedido.")
            cliente.close()

# Inicia o coordenador
coordenador = Coordenador()
coordenador.inicia_coordenador()
