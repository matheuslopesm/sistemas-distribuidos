import random
import threading
import time

recursoCompartilhado = "recurso_compartilhado.txt"
arrMaquinas = []
arrIdsMaquinas = []
solicitante = random.choice([ip for ip in arrMaquinas if ip != coordenador])
semExclusaoMutua = threading.Semaphore(1)
coordenador = None


def criaMaquinas():
    maquinasEscaneadas = [
        "172.16.100.1",
        "172.16.100.2",
        "172.16.100.3",
        "172.16.100.4",
    ]
    idsDisponiveis = list(range(1, len(maquinasEscaneadas) + 1))

    for ip in maquinasEscaneadas:
        random.shuffle(idsDisponiveis)
        idEscolhido = idsDisponiveis.pop(0)

        arrIdsMaquinas.append(idEscolhido)
        arrMaquinas.append({"ID": idEscolhido, "IP": ip})

    # Ordena as máquinas com base nos IDs
    arrMaquinas.sort(key=lambda x: x["ID"])


def escolheCoordenador():
    while True:
        if coordenador is None:
            coordenador = random.choice(arrMaquinas)
            print(f"O coordenador atual é {coordenador})!")


def limpaArquivo():
    with open(recursoCompartilhado, "w") as arquivo:
        arquivo.write("")


def escreveNoArquivo(solicitante):
    with open(recursoCompartilhado, "a") as arquivo:
        arquivo.write(f"{solicitante} - {time.time()}\n")

def solicitaRecurso():
    while True:
        time.sleep(random.randint(1, 5))
        with semExclusaoMutua:
            if coordenador == solicitante:
                print(f"{idDispositivo} está acessando o recurso")
                escreveNoArquivo()
            else:
                outraMaquina = [
                    ip
                    for ip in arrMaquinas
                    if ip != coordenador and ip != idDispositivo
                ]
                print(f"{idDispositivo} enviou solicitacao.")
                fila.append((outraMaquina, time.time()))


limpaArquivo()
criaMaquinas()
escolheCoordenador()

print(arrMaquinas)
print(arrIdsMaquinas)
