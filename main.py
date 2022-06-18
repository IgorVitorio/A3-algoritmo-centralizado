# A3 da UC de Sistemas distribuídos e mobile
# Igor Vitório França Araujo - 1271925281

#Algoritmo Centralizado
import time
from random import randint
from threading import Thread

# Classe que trata dos servidores
class Host():
    #Função inicializadora da classe
    def __init__(self, id):
        self.id = id
        self.tag = f'Servidor {id}:'
        self.hostLider = None
        self.isAtivo = True
        Thread(target=self.run_p).start()

    #Função inicializadora de execução
    def run_p(self):
        print('\n')
        print(f'{self.tag} foi inicializado com sucesso.')
        while self.isAtivo:
            self.consumir_recurso()
            time.sleep(randint(3, 5))

    #Função para setar servidor lider e servidor ativo
    def set_hostLider(self, hostLider):
        self.hostLider = hostLider

    def set_ativo(self, ativo):
        self.isAtivo = ativo

    #Função de parada
    def stop(self):
        del self

    #Exibição de objeto (string)
    def __repr__(self):
        return str(self.__dict__)

    #Função de consumo do recurso
    def consumir_recurso(self):
        hostLider = self.hostLider
        if hostLider is None:
            Hosts().gera_novo_hostLider()
        elif hostLider is not None and self.id != self.hostLider.id:
            print('\n')  
            print(f'{self.tag} Solicita acesso do recurso ao líder {hostLider.id}!')
            if hostLider.isRecursoHabilitado == False:
                self.processa_recurso()
            else:
                hostLider.fila.append(self)
                print(f'******** Fila de espera para consumir recurso = {self.fila_hostLider(hostLider)} ********')
                valida = True
                while valida:
                    if hostLider.isRecursoHabilitado == False and hostLider.fila[0].id == self.id:
                        self.processa_recurso()
                        valida = False

    #Função de processamento do recurso
    def processa_recurso(self):
        hostLider = self.hostLider
        if hostLider is not None:
            print(f'******** Líder {hostLider.id} concede acesso ao servidor {self.id} ********')
            print(f'{self.tag} Está consumindo o recurso')
            hostLider.isRecursoHabilitado = True
            sleep = randint(5, 15)
            time.sleep(sleep)
            print(f'{self.tag} Recurso consumido em {sleep}s!')
            print(
                f'******** O servidor {self.id} informa ao líder que o recurso foi liberado ********')
            print('\n')
            hostLider.isRecursoHabilitado = False
            self.remover_fila(hostLider)

    #Remoção de servidor da fila do líder
    def remover_fila(self, hostLider):
        for f in hostLider.fila:
            if f.id == self.id:
                hostLider.fila.remove(self)

    #Array com lista de servidores que requisitaram
    def fila_hostLider(self, hostLider):
        s =[]
        for f in hostLider.fila:
            s.append(f.id)
        return s

#Classe que trata do líder
class HostLider:
    def __init__(self, id):
        self.id = id
        self.isRecursoHabilitado = False
        self.fila = []

    #Função de parada
    def stop(self):
        del self

    #Exibição de objeto (string)
    def __repr__(self):
        return str(self.__dict__)

#Criação da classe singleton
class Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

#Criação de instância única do array de servidores
class Hosts(Singleton):
    hosts = []

# Função de gerar os servidores
    def gera_host(self):
        while (True):
            valida = False
            while valida == False:
                ran_id = randint(100, 200)
                valida = self.verifica_id_existente(ran_id)
            host = Host(ran_id)
            host.set_hostLider(self.get_hostLider())
            self.hosts.append(host)
            sleep = randint(3,5)
            time.sleep(sleep)
            print(f' INFO: Servidor {ran_id} foi gerado em {sleep}s')
            
    #Inativar o líder
    def inativa_hostLider(self):
        while(True):
            time.sleep(randint(30,40))
            if len(self.hosts) > 0:
                hostLider = self.hosts[0].hostLider
                if hostLider is not None:
                    id = hostLider.id
                    host = self.retorna_host(hostLider.id)
                    host.set_ativo(False)
                    self.remove_hostLider()
                    self.hosts.remove(host)
                    hostLider.stop()
                    host.stop()
                    print(f'******** O líder {id} foi inativado ********')

    #Obter o líder
    def get_hostLider(self):
        if(len(self.hosts) > 0 ):
            return self.hosts[0].hostLider
        return None

    #Geração de novo líder
    def gera_novo_hostLider(self):
        if len(self.hosts)>3:
            print('\n')
            print(f'******** Elegendo um novo líder aleatório ********')
            print(f'******** Servidores ativos: {self.hosts_ativos()} ********')
            host = self.hosts[randint(0, len(self.hosts) - 1)] #Líder escolhido aleatóriamente entre os servidores ativos
            hostLider = HostLider(host.id)
            print(f'{host.tag} Novo Líder eleito')
            self.adicionar_hostLider_hosts(hostLider)

    #Troca de mensagem entre os servidores - Aviso do novo líder
    def adicionar_hostLider_hosts(self, hostLider):
        print(f'******** Notificando os servidores do novo líder {hostLider.id} ********')
        for p in self.hosts:
            p.set_hostLider(hostLider)
        print('\n')

    #Array com servidores ativos
    def hosts_ativos(self):
        s = []
        for p in self.hosts:
            s.append(p.id)
        return s

    #Retorno do array com servidores ativos
    def retorna_host(self, id):
        for p in self.hosts:
            if p.id == id:
                return p

    #Remover servidor líder
    def remove_hostLider(self):
        for p in self.hosts:
            p.set_hostLider(None)

    #Verificação dos ids dos servidores para validações
    def verifica_id_existente(self, id):
        for i in self.hosts:
            if i.id == id:
                return False
        return True

    #Tratamento de inicialização
    def run(self):
        Thread(target=self.gera_host).start()
        Thread(target=self.inativa_hostLider).start()

if __name__ == '__main__':
    Hosts().run()