import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

#Agente gerador
class Gerador(Agent):
    grau = 0
    i = 0
    a = 0
    b = 0
    c = 0
    d = 0

    while a == 0:
        a = random.randint(-10,10)
    b = random.randint(-10,10)
    c = random.randint(-10,10)
    d = random.randint(-10,10)
    
    #Gera o grau da função
    class Grau(CyclicBehaviour): #Por quê deve ser CyclicBehaviour e não OneShotBehaviour?
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print("Gerador: Gerando o grau da função")
                Gerador.grau = random.randint(2,3)
                print(f"Gerador: Grau gerado = {Gerador.grau}º")
                res = Message(to=str(msg.sender))
                res.set_metadata("performative", "inform")
                res.body = str(Gerador.grau)
                await self.send(res)

    # #Printa a função
    # class set_Funcao(OneShotBehaviour):
    #     async def run(self):
    #         msg = await self.receive(timeout=10)
    #         if msg:
    #             if Gerador.grau == 1:
    #                 print(f"Gerador: f(x) = ({Gerador.a})*x + ({Gerador.b})")
    #             elif Gerador.grau == 2:
    #                 print(f"Gerador: f(x) = ({Gerador.a})*x^2 + ({Gerador.b})*x + ({Gerador.c})**2")
    #             elif Gerador.grau == 3:
    #                 print(f"Gerador: f(x) = ({Gerador.a})*(x - ({Gerador.b}))*(x - ({Gerador.c}))*(x - ({Gerador.d}))")
    #             print("===========================================================================")
    #             res = Message(to=str(msg.sender))
    #             res.set_metadata("performative", "inform")
    #             await self.send(res)

    #Gera a função
    class Funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=10)
            if res:
                x = float(res.body)
                g = int(Gerador.grau)
                funcoes = {
                    1:float((Gerador.a*(x)) + (Gerador.b)),
                    2:float((Gerador.a*(x**2)) + (2*Gerador.a*(x)) + (Gerador.a**2)),
                    3:float(Gerador.a*(x - Gerador.b)*(x - Gerador.c)*(x - Gerador.d))
                    }
                resultado = funcoes[g]
                print(f"Gerador: Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(resultado))
                await self.send(msg)

    async def setup(self):
        #Gera da grau
        tf = self.Grau()
        t1 = Template()
        t1.set_metadata("performative", "request")
        self.add_behaviour(tf,t1)

        # #Printa a função
        # sf = self.set_Funcao()
        # t2 = Template()
        # t2.set_metadata("performative", "subscribe")
        # self.add_behaviour(sf,t2)

        #Gera função
        f = self.Funcao()
        t3 = Template()
        t3.set_metadata("performative","subscribe")
        self.add_behaviour(f,t3)

async def main():
    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()
    while gerador.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            gerador.stop()
            break
    print("Gerador: Agente encerrou!")

if __name__=='__main__':
    spade.run(main())