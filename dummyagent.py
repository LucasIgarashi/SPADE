import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente gerador
class Gerador(Agent):
    x = random.randint(-3,3) #NÃO_ESQUECER_DE_VOLTAR_OS_VALORES_ORIGINAIS
    a=0
    while a == 0:
        a = random.randint(-3,3)
    y = -1 * (a*x)

    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.a*x + Gerador.y )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x,"=>",int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)

    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = "1grau" 
                await self.send(msg)
                print("Respondeu para" + str(msg.sender) + " com " + msg.body)


    async def setup(self):
        t = Template()
        t.set_metadata("performative","subscribe")

        tf = self.funcao_1grau()
        print("Funcao de 1o grau: ", Gerador.x)
        print("Funcao: ", Gerador.a, "x + (", Gerador.y, ")")

        self.add_behaviour(tf,t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

# Agente resolvedor
class Resolvedor(Agent):
    class EncontrarX(CyclicBehaviour):
        async def run(self):
            x = random.randint(-3,3) 
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            await self.send(msg)
            print(f"Enviou x = {x} para o agente Gerador")

            res = await self.receive(timeout=5)
            if res:
                resultado = int(res.body)
                print(f"Recebeu f({x}) = {resultado} do agente Gerador")

                if resultado == 0:
                    print(f"Encontrou a solução: x = {x}")
                else:
                    x = random.randint(-3,3)
                    print(f"Ajustando x para {x}")
                    msg.body = str(x)
                    await self.send(msg)

    async def setup(self):
        print("Agente Resolvedor iniciado")
        resolver = self.EncontrarX()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(resolver, template)

async def main():

    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()

    resolvedor = Resolvedor("igarashi@magicbroccoli.de", "andorinha123321")
    await resolvedor.start()

if __name__ == "__main__":
    spade.run(main())