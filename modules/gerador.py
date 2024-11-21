import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
from numpy import array, roots, isreal
import random

#Agente gerador
class Gerador(Agent):
    grau = 0
    coeficientes = []
    
    #Gera os coeficientes da função
    class setCoefficients(OneShotBehaviour):
        async def run(self):
            self.agent.coeficientes = self.generate_coefficients(self.agent.grau) 
        
        def generate_coefficients(self, grau):
            coeficientes = [random.randint(-10, 10) for _ in range(grau + 1)]
            while coeficientes[0] == 0:
                coeficientes[0] = random.randint(-10, 10)
            
            if grau == 1:
                return self.generate_coefficients(grau)

            if grau == 2:
                # Verificar discriminante para função quadrática
                a, b, c = coeficientes
                discriminante = ((b**2) - (4*a*c))
                if discriminante < 0:
                    return self.generate_coefficients(grau)

            if grau == 3:
                # Verificar se a função cúbica tem todas as raízes reais
                raizes = roots(array(coeficientes))
                if not isreal(raizes).all():
                    return self.generate_coefficients(grau)

            return coeficientes

    #Gera o grau da função
    class setDegree(CyclicBehaviour):
        async def run(self):
            msg_received = await self.receive(timeout=10)
            if msg_received:
                print("GERADOR     - Gerando o grau da função")
                self.agent.grau = random.randint(1, 3)
                print(f"GERADOR     - Grau = {self.agent.grau}")
                self.agent.add_behaviour(self.agent.setCoefficients())
                res = Message(to=str(msg_received.sender))
                res.set_metadata("performative", "inform")
                res.body = str(self.agent.grau)
                await self.send(res)

    #Calcula e envia a raiz obtida pelo x dado do Resolvedor
    class FunctionSolver(CyclicBehaviour):
        async def run(self):
            msg_received = await self.receive(timeout=10)
            if msg_received:
                x = float(msg_received.body)
                resultado = sum((coef*(x**i)) for i, coef in enumerate(reversed(self.agent.coeficientes)))
                print(f"GERADOR     - Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
                res = Message(to=str(msg_received.sender))
                res.set_metadata("performative", "inform")
                res.body = str(int(resultado))
                await self.send(res)

    async def setup(self):
        sd = self.setDegree()
        t1 = Template()
        t1.set_metadata("performative", "request")
        self.add_behaviour(sd,t1)

        fs = self.FunctionSolver()
        t2 = Template()
        t2.set_metadata("performative","subscribe")
        self.add_behaviour(fs,t2)

async def main():
    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()

if __name__=='__main__':
    spade.run(main())