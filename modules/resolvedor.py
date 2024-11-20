import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import random

#Agente resolvedor
class Resolvedor(Agent):
    grau = 0

    #Tipifica qual a função
    class setTypeFunction(OneShotBehaviour):
        async def run(self):
            print("===========================================================================")
            print("Resolvedor: Requisitando o grau da função...")
            msg_request = Message(to="gerador@magicbroccoli.de")
            msg_request.set_metadata("performative", "request")
            await self.send(msg_request)
            res_received = await self.receive(timeout=10)
            if res_received:
                Resolvedor.grau = int(res_received.body)
                grau = {
                    1:'linear',
                    2:'quadrática',
                    3:'cúbica'
                    }
                print(f"Resolvedor: A função é {grau[Resolvedor.grau]}")
                print("===========================================================================")
                self.agent.add_behaviour(self.agent.Guess())

    #Chuta valores para a raíz da função
    class Guess(CyclicBehaviour):
        async def run(self):
            x = random.randint(-50,50)
            msg_request = Message(to="gerador@magicbroccoli.de")
            msg_request.set_metadata("performative", "subscribe")
            msg_request.body = str(x)
            print("===========================================================================")
            print(f"Resolvedor: Enviou para o agente Gerador x = {x}")
            await self.send(msg_request)
            res_received = await self.receive(timeout=10)
            if res_received:
                resultado = int(res_received.body)
                if resultado == 0:
                    print(f"Resolvedor: Portanto, a/uma solução é x = {x}")
                    print("===========================================================================")
                    await self.agent.stop()
                else:
                    print("Resolvedor: Solução diferente de zero, tentando novamento...")
                    print("===========================================================================")

    async def setup(self):
        #Grau
        g = self.setTypeFunction()
        self.add_behaviour(g)

async def main():
    resolvedor = Resolvedor("resolvedor@magicbroccoli.de", "Senh@qui12")
    await resolvedor.start()

if __name__=='__main__':
    spade.run(main())