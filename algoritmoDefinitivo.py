import time
from random import randint
from threading import Thread

class Processo:
    def __init__(self) -> None:
        self.id = id
        self.tag = f"Processo {id}:"
        self.coordenador = None
        self.isAtivo = True
        Thread(target=self.run_p).start()

    def run_p(self):
        """
        Método chamado no início do programa.
        """
        print(f"{self.tag} inicializando!")
        while self.isAtivo:
            self.consumir_recurso()
            time.sleep(randint(10, 25))

    def set_coordenador(self, coordenador):
        """
        Método chamado no início do programa.
        """
        self.coordenador = coordenador

    def set_Ativo(self, ativo):
        self.isAtivo = ativo

    def stop(self):
        del self

    def __repr__(self):
        return str(self, __dict__)

    def consumir_recurso(self):
        """
        Recebe o coordenador, mas se ele for nulo, vai gerar um novo coordenador
        fazendo uma nova eleição.
        Se não for nulo e o processo não for o próprio coordenador, ele vai solicitar
        o coordenador se o recurso está sendo utilizado ou não.
        Se não está sendo utilizado, vai processar o recurso. Se está sendo utilizado,
        ele vai colocar o processo na fila e aguardar ser o primeiro da fila, para assim
        processar o recurso.
        """
        coordenador = self.coordenador
        if coordenador is None:
            Processo().gera_novo_coordenador()
        elif coordenador is not None and self.id != self.coordenador.id:
            print("\n")
            print(f"{self.tag} Solicita acesso do recurso ao coordenador {coordenador.id}!")
            if coordenador.isRecursoHabilitado == False:
                self.processa_recurso()
            else:
                coordenador.fila.append(self)
                print(
                    f"***** Fila do coordenador = {self.fila_coordenador(coordenador)}"
                )
                valida = True
                while valida:
                    if (
                        coordenador.isRecursoHabilitado == False
                        and coordenador.fila[0].id == self.id
                    ):
                        self.processa_recurso()
                        valida = False

    def processa_recurso(self):
        """
        Recebe o coordenador se ele for diferente de nulo e setar o recursoHabilitado como True
        e vai começar a esperar o tempo de processamento do recurso. Depois que finalizar, ele
        vai retornar o tempo e setar o isRecursoHabilitado como False e remover o processo da fila.

        Processo deve escrever seu ID no txt recurso_compartilhado
        """
        coordenador = self.coordenador
        if coordenador is not None:
            print(
                f"******** Coordenador {coordenador.id} concede acesso ao processo {self.id}"
            )
            print(f"{self.tag} Iniciado processo do recurso!")
            coordenador.isRecursoHabilitado = True
            # Escrita no TXT
            sleep = randint(5, 15)
            time.sleep(sleep)
            print(f"{self.tag} Recurso processado em {sleep}s!")
            print(
                f"******** O processo {self.id} informa ao coordenador que o recurso foi liberado"
            )
            print("\n")
            coordenador.isRecursoHabilitado = False
            self.remover_fila(coordenador)

    def remover_fila(self, coordenador):
        for f in coordenador.fila:
            if f.id == self.id:
                coordenador.fila_remove(self)

    def fila_coordenador(self, coordenador_fila):
        s = []
        for f in coordenador_fila:
            s.append(f.id)
        return s


class Coordenador:
    def __init__(self, id):
        self.id = id
        self.isRecursoHabilitado = False
        self.fila = []

    def stop(self):
        del self

    def __repr__(self):
        return str(self, __dict__)


class Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Processos(Singleton):
    processos = []
    ips = ["172.16.100.2", "172.16.100.3", "172.16.100.4", "172.16.100.5", "172.16.100.6"]

    def gera_processo(self):
        """
        Vai validar se o id do processo, pego randomicamente, existe. Se existir vai criar um processo
        com esse id randomico e setar o coordenador se ele existir. Ele vai ser chamado a cada 40 segundos.

        adaptar para pegar um ip randomico da lista de IPs disponíveis
        """
        while True:
            valida = False
            while valida == False:
                ran_ip = self.pick_random_process(self.ips)
                valida = self.verifica_id_existente(ran_ip)
            processo = Processo(ran_ip)
            processo.set_coordenador(self.get_coordenador())
            self.processos.append(processo)
            time.sleep(40)

    def inativa_coordenador(self):
        """
        É chamado a cada 60 segundos. Vai pegar o coordenador e se ele for diferente
        de nulo, vai buscar o processo pelo id do coordenador, setar o processo como False, remover
        o coordenador e tirar o processo dos processos ativos.
        """
        while True:
            time.sleep(60)
            if len(self.processos) > 0:
                coordenador = self.processos[0].coordenador
                if coordenador is not None:
                    id = coordenador.id
                    processo = self.retorna_processo(coordenador.id)
                    processo.set_ativo(False)
                    self.remove_coordenador()
                    self.processos.remove(processo)
                    coordenador.stop()
                    processo.stop()
                    print(f"****** Coordenador inativo {id} !")

    def get_coordenador(self):
        if len(self.processos) > 0:
            return self.processos[0].coordenador
        return None

    def gera_novo_coordenador(self):
        if len(self.processos):
            print("\n")
            print(f" ****** Elegendo novo coordenador randômico")
            print(f" ****** Processos Ativos: {self.processos_ativos()}")
            processo = self.processos[randint(0, len(self.processos) - 1)]
            coordenador = Coordenador(processo.id)
            print(f'{processo.tag} Novo Coordenador!')
            self.adicionar_coordenador_processos(coordenador)

    def adicionar_coordenador_processos(self, coordenador):
        print(f'******** Notificando processos do novo coordenador')
        for p in self.processos:
            p.set_coordenador(coordenador)
        print('ln')

    def processos_ativos(self):
        s = []
        for p in self.processos:
            s.append(p.id)
        return s
    
    def retorna_processo(self, id):
        for p in self.processos:
            if p.id == id:
                return p

    def remove_coordenador(self):
        for p in self.procesos:
            p.set_coordenador(None)

    def verifica_id_existente(self, id):
        for i in self.processos:
            if i.id == id:
                return False
        return True
    
    def pick_random_process(vetor):
        # Verifique se o vetor não está vazio
        if not vetor:
            return None
        # Gere um índice aleatório dentro do intervalo válido
        indice_aleatorio = randint(0, len(vetor) - 1)
        # Retorne o item correspondente ao índice aleatório
        return vetor[indice_aleatorio]

    def run(self):
        Thread(target=self.gera_processo).start()
        Thread(target=self.inativa_coordenador).start()

if __name__ == "__main__":
    Processos.run()
