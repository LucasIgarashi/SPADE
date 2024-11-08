import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente gerador
class Gerador(Agent):
    graus = [1, 2, 3]
    grau = random.choice(graus) 
    x = random.randint(-10,10) #NÃO_ESQUECER_DE_VOLTAR_OS_VALORES_ORIGINAIS
    a = 0
    b = 0
    c = 0
    d = 0

    while a == 0:
        a = random.randint(-1,1)
    y = 1*(a*x)
    b = random.randint(-1,1)
    w = 1*(a*x*x) + 1*(b*x)
    c = random.randint(-1,1)
    z = 1*(a*x*x*x) + 1*(b*x*x) + 1*(c*x)

# Função de primeiro grau
    class Funcao(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=10)
            if res:
                x = float(res.body)
                if Gerador.grau == 1:
                    resultado = float(Gerador.a*(x) + Gerador.y)
                elif Gerador.grau == 2:
                    resultado = float(Gerador.a*(x*x) + Gerador.b*(x) + Gerador.w)
                elif Gerador.grau == 3:
                    resultado = float(Gerador.a*(x*x*x) + Gerador.b*(x*x) + Gerador.c*(x) + Gerador.z)

                print(f"Enviou para o agente Resolvedor f({res.body})= {resultado} => {int(resultado)}")
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(resultado))
                await self.send(msg)

# Classificar a função
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = f"{Gerador.grau}grau" 
                print("Respondeu para" + str(msg.sender) + " com " + msg.body)
                await self.send(msg)

    async def setup(self):

        #Função
        t = Template()
        t.set_metadata("performative","subscribe")
        tf = self.Funcao()
        print("\n================================================")
        print(f"Funcao de {Gerador.grau}º grau")
        if Gerador.grau == 1:
            print(f"Funcao: {Gerador.a}x + {Gerador.y}")
        elif Gerador.grau == 2:
            print(f"Funcao: {Gerador.a}x^2 + {Gerador.b}x + {Gerador.w}")
        elif Gerador.grau == 3:
            print(f"Funcao: {Gerador.a}x^3 + {Gerador.b}x^2 + {Gerador.c}x + {Gerador.z}")
        print("================================================\n")
        self.add_behaviour(tf,t)

        #tipo da função
        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

# Agente resolvedor
class Resolvedor(Agent):
    class EncontrarX(CyclicBehaviour):
        async def run(self):
            x = random.randint(-10,10) 
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "subscribe")
            msg.body = str(x)
            print("\n================================================")
            print(f"Enviou x = {x} para o agente Gerador")
            await self.send(msg)

            res = await self.receive(timeout=10)
            if res:
                resultado = int(res.body)
                print(f"Recebeu f({x}) = {resultado} do agente Gerador")

                if resultado == 0:
                    print(f"Encontrou a solução: x = {x}")
                    print("================================================\n")
                    await self.agent.stop()
                else:
                    print("Solução diferente de zero, tentando novamento...")
                    print("================================================\n")


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