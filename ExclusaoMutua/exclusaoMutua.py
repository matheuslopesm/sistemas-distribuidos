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
        self.lider.bind(
            ("0.0.0.0", 37701)
        )  # 0 indica que a porta será atribuída automaticamente
        endereco = self.lider.getsockname()
        print(f"Coordenador iniciado na porta {endereco[1]}")

        self.lider.listen(5)

        while True:
            # Aguarda uma conexão de um processo
            cliente, _ = self.lider.accept()
            threading.Thread(target=self.lida_com_requisicao, args=(cliente,)).start()

    def lida_com_requisicao(self, cliente):
        with self.mutex:
            # Verifica se há outros processos acessando o recurso
            if not self.fila_de_requisicoes.empty():
                print("Recurso ocupado. Adicionando à fila.")
                self.fila_de_requisicoes.put(cliente)
            else:
                print("Recurso livre. Concedendo acesso.")
                self.concede_acesso(cliente)

    def concede_acesso(self, cliente):
        # Simula o acesso ao recurso compartilhado
        time.sleep(2)
        print("Acesso concedido.")
        # Libera o próximo processo na fila
        if not self.fila_de_requisicoes.empty():
            proximo_cliente = self.fila_de_requisicoes.get()
            proximo_cliente.sendall(b"Acesso concedido.")
            proximo_cliente.close()
        else:
            cliente.sendall(b"Acesso concedido.")
            cliente.close()


# Inicia o coordenador
coordenador = Coordenador()
coordenador.inicia_coordenador()
