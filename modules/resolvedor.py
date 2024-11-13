import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente resolvedor
class Resolvedor(Agent):
    grau = 0
    
    class Grau(OneShotBehaviour):
        async def run(self):
            if Resolvedor.grau == 0:
                print("================================================")
                print(f"Agente Resolvedor requisitando o grau da função...")
                msg = Message(to="gerador@magicbroccoli.de")
                msg.set_metadata("performative", "request")
                await self.send(msg)
                res = await self.receive(timeout=10)
                if res:
                    Resolvedor.grau = int(res.body)
                    print(f"Recebeu do agente Gerador: grau = {Resolvedor.grau}")
                    print("================================================\n")

    # class Chute(CyclicBehaviour):
    #     async def run(self):
    #         x = random.randint(-100,100) 
    #         msg = Message(to="gerador@magicbroccoli.de")
    #         msg.set_metadata("performative", "subscribe")
    #         msg.body = str(x)
    #         print("================================================")
    #         print(f"Enviou para o agente Gerador x = {x}")
    #         await self.send(msg)

    #         res = await self.receive(timeout=10)
    #         if res:
    #             resultado = int(res.body)

    #             if resultado == 0:
    #                 print(f"Encontrou a solução: x = {x}")
    #                 print("================================================")
    #                 await self.agent.stop()
    #             else:
    #                 print("Solução diferente de zero, tentando novamento...")
    #                 print("================================================")

    async def setup(self):
        #Grau
        g = self.Grau()
        t1 = Template()
        t1.set_metadata("performative", "inform")
        self.add_behaviour(g, t1)

        # #Chute
        # c = self.Chute()
        # t2 = Template()
        # t2.set_metadata("performative", "inform")
        # self.add_behaviour(c, t2)

async def main():
    resolvedor = Resolvedor("igarashi@magicbroccoli.de", "andorinha123321")
    await resolvedor.start()

if __name__=='__main__':
    spade.run(main())