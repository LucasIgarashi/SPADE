import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente gerador
class Gerador(Agent):
    # k = random.randint(-100,100)
    # a = 0
    # b = 0
    # c = 0
    # d = 0

    # while a == 0:
    #     a = random.randint(-10,10)
    # b = random.randint(-10,10)
    # c = random.randint(-10,10)
    # d = random.randint(-10,10)
 
#Tipificar a função
    class Tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                graus = [1, 2, 3]
                grau = random.choice(graus)
                res = Message(to=str(msg.sender))
                res.set_metadata("performative", "inform")
                res.body = str(grau)
                await self.send(res)

# #Função
#     class Funcao(CyclicBehaviour):
#         async def run(self):
#             res = await self.receive(timeout=10)
#             if res:
#                 x = float(res.body)
#                 z = int(Gerador.grau)
#                 if z == 1:
#                     resultado = float((Gerador.a*(x)) + (Gerador.b))
#                 elif z == 2:
#                     resultado = float(Gerador.a*(x**2) + Gerador.b*(x) + Gerador.c)
#                 else:
#                     resultado = float(Gerador.a*(x - Gerador.b)*(x - Gerador.c)*(x - Gerador.d))

#                 print(f"Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
#                 msg = Message(to=str(res.sender))
#                 msg.set_metadata("performative", "inform")
#                 msg.body = str(int(resultado))
#                 await self.send(msg)

    async def setup(self):
        #Tipo da função
        tf = self.Tipo_funcao()
        t1 = Template()
        t1.set_metadata("performative", "request")
        self.add_behaviour(tf, t1)

        # #Função
        # f = self.Funcao()
        # t2 = Template()
        # t2.set_metadata("performative","subscribe")
        # self.add_behaviour(f,t2)

async def main():
    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()

if __name__=='__main__':
    spade.run(main())