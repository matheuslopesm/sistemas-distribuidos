import socket

def solicita_acesso():
    # Endereço do coordenador
    endereco_coordenador = ("172.16.100.2", 37701)  # Substitua pelo IP e porta corretos do coordenador

    # Conecta-se ao coordenador
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(endereco_coordenador)

    # Envia uma mensagem de solicitação ao coordenador
    mensagem = ("Solicitação de acesso ao recurso")
    cliente.sendall(mensagem)

    # Aguarda a resposta do coordenador
    resposta = cliente.recv(1024)
    print(f"Resposta do coordenador: {resposta.decode()}")

    # Fecha a conexão
    cliente.close()

# Solicita acesso ao recurso
solicita_acesso()
