import threading
import time
import os
import random

ips = ["172.16.100.2", "172.16.100.3", "172.16.100.4", "172.16.100.5", "172.16.100.6"]
id_dispositivo = random.choice(ips)
arquivo_recurso = "recurso_compartilhado.txt"
fila_pedidos = []
sem_exclusao_mutua = threading.Semaphore(1)
lider = None

def eleger_lider():
    global lider
    while True:
        if lider is None:
            with sem_exclusao_mutua:
                lider = random.choice(ips)
                print(f"\n{lider} elegeu-se como líder.")

def limpar_arquivo():
    with open(arquivo_recurso, "w") as arquivo:
        arquivo.write("") 

def escrever_arquivo():
    with open(arquivo_recurso, "a") as arquivo:
        arquivo.write(f"{id_dispositivo} - {time.time()}\n")

def solicitar_recurso():
    global lider
    while True:
        time.sleep(random.randint(1, 5))
        with sem_exclusao_mutua:
            if lider == id_dispositivo:
                print(f"{id_dispositivo} está acessando o recurso.")
                escrever_arquivo()
            else:
                outras_maquinas = [ip for ip in ips if ip != lider and ip != id_dispositivo]
                if outras_maquinas:
                    outra_maquina = random.choice(outras_maquinas)
                    print(f"{id_dispositivo} enviou uma solicitação para o líder {lider}.")
                    fila_pedidos.append((outra_maquina, time.time()))

def liberar_recurso():
    global lider
    while True:
        time.sleep(random.randint(5, 10))
        with sem_exclusao_mutua:
            if lider == id_dispositivo:
                print(f"{id_dispositivo} liberou o recurso.")
                if fila_pedidos:
                    proximo_cliente, timestamp = fila_pedidos.pop(0)
                    print(f"FILA DE ESPERA: {fila_pedidos}")
                    print(f"Líder {id_dispositivo} concedeu permissão para {proximo_cliente} acessar o recurso.")
                    escrever_arquivo()
            else:
                print(f"{id_dispositivo} não pode liberar o recurso, pois não é o líder.")

def simular_queda_lider():
    global lider
    while True:
        time.sleep(20)
        with sem_exclusao_mutua:
            if lider is not None:
                print(f"{lider} caiu. Simulando nova eleição.")
                lider = None

# Limpa o arquivo antes de começar
limpar_arquivo()

# Inicia a thread para eleger o líder
thread_eleicao = threading.Thread(target=eleger_lider)
thread_eleicao.start()

# Inicia a thread para solicitar o recurso
thread_solicitacao = threading.Thread(target=solicitar_recurso)
thread_solicitacao.start()

# Inicia a thread para liberar o recurso
thread_liberacao = threading.Thread(target=liberar_recurso)
thread_liberacao.start()

# Inicia a thread para simular a queda do líder e iniciar uma nova eleição
thread_simular_queda_lider = threading.Thread(target=simular_queda_lider)
thread_simular_queda_lider.start()

# Aguarda a conclusão das threads (não necessário em um programa em execução contínua)
thread_eleicao.join()
thread_solicitacao.join()
thread_liberacao.join()
thread_simular_queda_lider.join()

# import threading
# import time
# import sys
# from random import randint

# ips = ["172.16.100.2", "172.16.100.3", "172.16.100.4", "172.16.100.5", "172.16.100.6"]
# recursoDisponivel = True
# coordenador = None
# existeCoordenador = False
# filaDeEsperaCoordenador = []
# coordenador_lock = threading.Lock()

# def ElegeCoordenador():
#     global coordenador, existeCoordenador
#     while True:
#         with coordenador_lock:
#             coordenador = pick_random_process(ips)
#             existeCoordenador = True
#             print("Elegendo coordenador...")
#             print(f"Coordenador atual é: {coordenador}")
#         time.sleep(10)
#         derruba_coordenador()

# def SolicitaRecurso():
#     global coordenador, recursoDisponivel
#     while True:
#         time.sleep(3)
#         rand_ip = pick_random_process(ips)
#         with coordenador_lock:
#             if rand_ip != coordenador:
#                 if recursoDisponivel:
#                     ProcessaRecurso(rand_ip)
#                 else:
#                     print("Recurso nao esta disponivel")
#             else:
#                 print("Esta máquina é o coordenador")

# def ProcessaRecurso(ip):
#     global recursoDisponivel
#     with coordenador_lock:
#         recursoDisponivel = False
#     tempo_processamento = randint(0, 6)
#     print(f"Maquina {ip} esta consumindo recurso...")
#     time.sleep(tempo_processamento)
#     print(f"{ip} terminou de processar recurso em {tempo_processamento}s")
#     with coordenador_lock:
#         recursoDisponivel = True

# def pick_random_process(vetor):
#     if not vetor:
#         return None
#     indice_aleatorio = randint(0, len(vetor) - 1)
#     return vetor[indice_aleatorio]

# def derruba_coordenador():
#     global coordenador, ips
#     if not ips:
#         print("Todos os processos caíram, encerrando programa")
#         sys.exit(0)
#     with coordenador_lock:
#         ips.remove(coordenador)
#     print(f"Coordenador {coordenador} caiu, ips restantes = {ips}")
#     coordenador = None

# # Chama a primeira função em uma thread separada
# thread_primeira = threading.Thread(target=ElegeCoordenador)
# thread_primeira.start()

# # Chama a segunda função em uma thread separada
# thread_segunda = threading.Thread(target=SolicitaRecurso)
# thread_segunda.start()
