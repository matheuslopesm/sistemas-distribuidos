import socket
import threading
import queue
import time

class Coordenador:
    def __init__(self):
        self.lider = None
        self.processos_em_funcionamento = set()
        self.fila_de_requisicoes = queue.Queue()
        self.mutex = threading.Lock()

    def inicia_coordenador(self):
        # Inicia o coordenador na porta 37701
        self.lider = socket.gethostname()  # Coordenador inicial é aleatório entre as VMs
        self.processos_em_funcionamento.add(self.lider)
        endereco = (self.obter_ip(), 37701)
        print(f"Coordenador {self.lider} iniciado no endereço {endereco[0]}:{endereco[1]}")

        self.lider = self.eleicao_do_anel(self.lider)

        print(f"Coordenador eleito: {self.lider}")

        self.lider.listen(5)

        while True:
            # Aguarda uma conexão de um processo
            cliente, endereco_cliente = self.lider.accept()
            threading.Thread(target=self.lida_com_requisicao, args=(cliente, endereco_cliente)).start()

    def eleicao_do_anel(self, remetente):
        mensagem_eleicao = {
            'remetente': remetente,
            'lider_atual': self.lider,
            'processos_em_funcionamento': list(self.processos_em_funcionamento)
        }

        sucessor = self.encontrar_sucessor(remetente)

        while True:
            try:
                with socket.create_connection((sucessor, 37701)) as conexao:
                    # Envia mensagem de eleição para o sucessor
                    conexao.sendall(str(mensagem_eleicao).encode())

                    # Aguarda resposta
                    resposta = conexao.recv(1024).decode()

                    if resposta.startswith("Coordenador eleito:"):
                        # Atualiza o líder com base na resposta
                        self.lider = resposta.split(":")[1].strip()
                        return self.lider
                    else:
                        # Continua a eleição com o próximo sucessor
                        sucessor = resposta.split(":")[1].strip()

            except ConnectionRefusedError:
                # Se a conexão for recusada, continua tentando com o próximo sucessor
                sucessor = self.encontrar_sucessor(sucessor)

    def encontrar_sucessor(self, remetente):
        lista_processos = list(self.processos_em_funcionamento)
        index_remetente = lista_processos.index(remetente)
        return lista_processos[(index_remetente + 1) % len(lista_processos)]

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
        # Adiciona hostname e timestamp ao arquivo
        with open("recurso_compartilhado.txt", "a") as arquivo:
            arquivo.write(f"{socket.gethostname()} - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Simula o acesso ao recurso compartilhado com um tempo mais realista
        tempo_processamento = 15  # 15 segundos de processamento
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

    def obter_ip(self):
        return socket.gethostbyname(socket.getfqdn())

# Função para iniciar um novo coordenador quando o atual não está funcionando
def inicia_novo_coordenador():
    novo_coordenador = Coordenador()
    novo_coordenador.inicia_coordenador()

# Verifica se o coordenador está em execução
def coordenador_esta_funcionando(coordenador, endereco):
    try:
        with socket.create_connection(endereco):
            return True
    except (ConnectionRefusedError, TimeoutError):
        return False

# Inicia o coordenador ou um novo coordenador se o atual não estiver funcionando
coordenador = Coordenador()
if coordenador_esta_funcionando(coordenador, (coordenador.obter_ip(), 37701)):
    coordenador.inicia_coordenador()
else:
    # Se o coordenador não estiver funcionando, inicia um novo coordenador
    print("Coordenador não está funcionando. Iniciando novo coordenador.")
    threading.Thread(target=inicia_novo_coordenador).start()
