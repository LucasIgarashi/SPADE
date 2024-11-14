import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
import random

#Agente gerador
class Gerador(Agent):
    grau = 0
    coeficientes = []

    class setCoefficients(OneShotBehaviour):
        async def run(self):
            g = self.agent.grau
            self.agent.coeficientes = [random.randint(-5,5) for _ in range(self.agent.grau + 1)]
            while self.agent.coeficientes[0] == 0:
                self.agent.coeficientes[0] = random.randint(-5,5)
            for i in range(1, self.agent.grau + 1):
                self.agent.coeficientes[i] = self.agent.coeficientes[0]*random.randint(-5,5)
    
    class printFunction(OneShotBehaviour):
        async def run(self):
            termos = [f"(({coef})*(x^{i}))" for i, coef in enumerate(reversed(self.agent.coeficientes))]
            print(termos)
            funcao = " + ".join(reversed(termos))
            print(f"Gerador: f(x) = {funcao}")

    #Gera o grau da função
    class setDegree(CyclicBehaviour):
        async def run(self):
            msg_received = await self.receive(timeout=10)
            if msg_received:
                print("Gerador: Gerando o grau da função")
                self.agent.grau = random.randint(1,3)
                self.agent.add_behaviour(self.agent.setCoefficients())
                self.agent.add_behaviour(self.agent.printFunction())
                res = Message(to=str(msg_received.sender))
                res.set_metadata("performative", "inform")
                res.body = str(self.agent.grau)
                await self.send(res)

    #Resolve a função
    class FunctionSolver(CyclicBehaviour):
        async def run(self):
            msg_received = await self.receive(timeout=10)
            if msg_received:
                x = float(msg_received.body)
                resultado = sum(coef*(x**i) for i, coef in enumerate(reversed(self.agent.coeficientes)))
                x_variando = [f"(({coef})*(({x})^{i}))" for i, coef in enumerate(reversed(self.agent.coeficientes))]
                print(f"Gerador: f({x}) = {' + '.join(reversed(x_variando))}")
                print(f"Gerador: Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
                res = Message(to=str(msg_received.sender))
                res.set_metadata("performative", "inform")
                res.body = str(int(resultado))
                await self.send(res)

    async def setup(self):
        #Gera da grau
        sd = self.setDegree()
        t1 = Template()
        t1.set_metadata("performative", "request")
        self.add_behaviour(sd,t1)

        #Gera função
        fs = self.FunctionSolver()
        t2 = Template()
        t2.set_metadata("performative","subscribe")
        self.add_behaviour(fs,t2)

async def main():
    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()

if __name__=='__main__':
    spade.run(main())