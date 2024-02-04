import random
import time
from random import randint
import uuid


class Processo:
    def __init__(self) -> None:
        self.coordenador = None
        self.solicitante = None
        self.recursoEmUso = False
        self.arrIpsMaquinas = []
        self.idsJaAtribuidos = []
        self.filaDeEspera = []

    # def mapeiaMaquinas(self): DESCOMENTAR. SÓ SERÁ IMPLEMENTADO QUANDO FOR USAR AS MÁQUINAS DE VEZ.
    #     """
    #         Mapeia as máquinas que estão no docker e joga dentro de uma lista.
    #         Após isso chama a função "atribuiIdNasMaquinas".
    #     """
    #     nomeHost = socket.gethostname()
    #     ipHost = socket.gethostbyname(nomeHost)

    #     network = ipaddress.IPv4Network(f"{ipHost}/24", strict=False)

    #     for ip in network.hosts():
    #         self.arrIpsMaquinas.append(str(ip))

    #     self.atribuiIdNasMaquinas(self.arrIpsMaquinas)

    def mapeiaMaquinasTeste(self):
        maquinasEscaneadas = [
            "172.16.100.1",
            "172.16.100.2",
            "172.16.100.3",
            "172.16.100.4",
        ]
        for ip in maquinasEscaneadas:
            self.arrIpsMaquinas.append(str(ip))

        self.atribuiIdNasMaquinas()

    def atribuiIdNasMaquinas(self):
        """
        Cria um arr (lista) de IDs já atribuídos às máquinas do docker.
        Verifica se o ID já foi atribuído. Caso não tenha sido, realmente
        atribui um ID a uma máquina.
        Após isso chama a função "escolheCoordenadorAleatorio".
        """
        for i, ip in enumerate(self.arrIpsMaquinas):
            id_maquina = str(uuid.uuid4())
            self.idsJaAtribuidos.append(id_maquina)
            self.arrIpsMaquinas[i] = {"ID": id_maquina, "IP": ip}

        self.escolheCoordenadorAleatorio()

    def escolheCoordenadorAleatorio(self):
        """
        Dentre as máquinas, escolhe uma aleatória para ser o coordenador (líder),
        de forma randômica.
        """
        coordenador = random.choice(self.arrIpsMaquinas)

        if coordenador in self.filaDeEspera:
            self.removeDaFilaDeSolicitantes(coordenador)

        self.coordenador = coordenador

        if isinstance(coordenador, dict):
            print("\n")
            print(f"O coordenador atual é {dict(coordenador)})!")
            with open("recurso_compartilhado.txt", "a") as arquivo:
                arquivo.write("\n")
                arquivo.write(
                    f"Coordenador: {coordenador} - {time.strftime('%d-%m-%Y %H:%M:%S')}\n"
                )

        self.criaSolicitante()

    def escolheSolicitante(self):
        solicitante = random.choice(
            [ip for ip in self.arrIpsMaquinas if ip != self.coordenador]
        )

        return solicitante

    def criaSolicitante(self):
        """
        Consome recurso de um solicitante, que é diferente do coordenador.
        """
        coordenador = self.coordenador

        if coordenador is None:
            self.escolheCoordenadorAleatorio()

        # Escolhe um solicitante (que seja diferente do coordenador)
        if self.solicitante is None:
            self.solicitante = self.escolheSolicitante()
        elif self.filaDeEspera[0] is not None:
            self.solicitante = self.filaDeEspera[0]

        if self.recursoEmUso == False and len(self.filaDeEspera) == 0:
            self.processaRecurso()
        elif self.recursoEmUso == False and self.filaDeEspera[0] == self.solicitante:
            self.processaRecurso()
        elif self.recursoEmUso == True:
            self.povoaFilaDeSolicitantes(self.solicitante)

    def processaRecurso(self):
        print(f"Máquina {self.solicitante} solicita acesso ao Coordenador")
        print(f"Coordenador libera acesso.")

        self.recursoEmUso = True

        sleep = randint(1, 20)
        print(f"Consumindo recurso em {sleep}s...")
        time.sleep(sleep)

        with open("recurso_compartilhado.txt", "a") as arquivo:
            arquivo.write(
                f"{self.solicitante} consumiu o recurso - {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        print(f"Solicitante {self.solicitante} liberou o recurso.")
        print("\n")
        self.recursoEmUso = False

        if len(self.filaDeEspera) == 0:
            self.solicitante = None
            self.criaSolicitante()
        else:
            self.solicitante = self.filaDeEspera[0]
            self.processaRecurso()

    def povoaFilaDeSolicitantes(self, solicitante):
        self.filaDeEspera.append(solicitante)
        print(f"Máquina {self.solicitante} entrou na fila de solicitantes!")
        print(f"Fila de espera atual:")

        for item in self.filaDeEspera:
            print(f"{item}")

    def removeDaFilaDeSolicitantes(self, maquina):
        self.filaDeEspera.remove(maquina)


processo = Processo()
processo.mapeiaMaquinasTeste()
