import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

#Agente resolvedor
class Resolvedor(Agent):
    grau = 0

    #Tipifica qual a função
    class Tipo_funcao(OneShotBehaviour):
        async def run(self):
            print("===========================================================================")
            print("Resolvedor: Requisitando o grau da função")
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "request")
            await self.send(msg)
            res = await self.receive(timeout=10)
            if res:
                Resolvedor.grau = int(res.body)
                grau = {
                    1:'linear',
                    2:'quadrática',
                    3:'cúbica'
                    }
                print(f"Resolvedor: A função é {grau[Resolvedor.grau]}")
                print("===========================================================================")
                self.agent.add_behaviour(self.agent.Chute())

    # #Printa a função
    # class get_Function(OneShotBehaviour):
    #     async def run(self):
    #         msg = Message(to="gerador@magicbroccoli.de")
    #         msg.set_metadata("performative", "subscribe")
    #         await self.send(msg)

    #Chuta valores para a raíz da função
    class Chute(CyclicBehaviour):
        async def run(self):
            x = random.randint(-100,100) 
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            print("===========================================================================")
            print(f"Resolvedor: Enviou para o agente Gerador x = {x}")
            await self.send(msg)
            res = await self.receive(timeout=10)
            if res:
                resultado = int(res.body)
                if resultado == 0:
                    print(f"Resolvedor: Portanto, a/uma solução é x = {x}")
                    print("===========================================================================")
                    await self.agent.stop()
                else:
                    print("Resolvedor: Solução diferente de zero, tentando novamento...")
                    print("===========================================================================")

    async def setup(self):
        #Grau
        g = self.Tipo_funcao()
        self.add_behaviour(g)

async def main():
    resolvedor = Resolvedor("igarashi@magicbroccoli.de", "andorinha123321")
    await resolvedor.start()
    while resolvedor.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            resolvedor.stop()
            break
    print("Resolvedor: Agente encerrou!")

if __name__=='__main__':
    spade.run(main())