import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente gerador
class Gerador(Agent):
    graus = [3]
    grau = random.choice(graus) 
    k = random.randint(-100,100) #NÃO_ESQUECER_DE_VOLTAR_OS_VALORES_ORIGINAIS
    a = 0
    b = 0
    c = 0
    d = 0

    while a == 0:
        a = random.randint(-10,10)
    b = random.randint(-10,10)
    c = random.randint(-10,10)
    d = random.randint(-10,10)
 
# #Tipificar a função
#     class tipo_funcao(CyclicBehaviour):
#         async def run(self):
#             msg = await self.receive(timeout=10)
#             if msg:
#                 msg = Message(to=str(msg.sender))
#                 msg.set_metadata("performative", "inform")
#                 msg.body = f"{Gerador.grau}º"
#                 print(f"Respondeu para {str(msg.sender)} com {msg.body}")
#                 await self.send(msg)

#Função
    class Funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=10)
            if res:
                x = float(res.body)
                z = int(Gerador.grau)
                if z == 1:
                    resultado = float((Gerador.a*(x)) + (Gerador.b))
                elif z == 2:
                    resultado = float(Gerador.a*(x**2) + Gerador.b*(x) + Gerador.c)
                else:
                    resultado = float(Gerador.a*(x - Gerador.b)*(x - Gerador.c)*(x - Gerador.d))

                print(f"Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(int(resultado))
                await self.send(msg)

    async def setup(self):
        print("Agente Gerador iniciado\n")

        #Função
        t = Template()
        t.set_metadata("performative","subscribe")
        tf = self.Funcao()
        print("================================================")
        print(f"Funcao de {Gerador.grau}º grau")
        if Gerador.grau == 1:
            print(f"Funcao: f(x) = ({Gerador.a})*x + ({Gerador.b})")
        elif Gerador.grau == 2:
            print(f"Funcao: f(x) = ({Gerador.a})*x^2 + ({Gerador.b})*x + ({Gerador.c})")
        else:
            print(f"Funcao: f(x) = a*(x - {Gerador.b})*(x - {Gerador.c})*(x - {Gerador.d})")
        print("================================================")
        self.add_behaviour(tf,t)

        # #Tipo da função
        # ft = self.tipo_funcao()
        # template = Template()
        # template.set_metadata("performative", "request")
        # self.add_behaviour(ft, template)

#Agente resolvedor
class Resolvedor(Agent):
    class Chute(CyclicBehaviour):
        async def run(self):
            x = random.randint(-100,100) 
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            print("================================================")
            print(f"Enviou para o agente Gerador x = {x}")
            await self.send(msg)

            res = await self.receive(timeout=10)
            if res:
                resultado = int(res.body)

                if resultado == 0:
                    print(f"Encontrou a solução: x = {x}")
                    print("================================================")
                    await self.agent.stop()
                else:
                    print("Solução diferente de zero, tentando novamento...")
                    print("================================================")


    async def setup(self):
        print("\nAgente Resolvedor iniciado\n")

        resolver = self.Chute()
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