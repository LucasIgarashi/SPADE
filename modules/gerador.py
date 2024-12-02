import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
from numpy import array, roots, isreal
import random

#Agente gerador
class Gerador(Agent):
    grau = 0
    coeficientes = []
    
    #Gera os coeficientes da função
    def generate_coefficients(self, grau):
        coeficientes = [random.randint(-10, 10) for _ in range(grau + 1)]
        while coeficientes[0] == 0:
            coeficientes[0] = random.randint(-10, 10)

        if grau == 1:
            return coeficientes

        if grau == 2:
            #Verificar discriminante para função quadrática
            a, b, c = coeficientes
            discriminante = ((b**2) - (4*a*c))
            if discriminante < 0:
                return self.generate_coefficients(grau)

        if grau == 3:
            #Verificar se a função cúbica tem todas as raízes reais
            raizes = roots(array(coeficientes))
            if not isreal(raizes).all():
                return self.generate_coefficients(grau)

        return coeficientes
        
    #Gera o grau da função
    class setDegree(CyclicBehaviour):
        async def run(self):
            msg_received1 = await self.receive(timeout=10)
            if msg_received1:
                print("GERADOR     - Gerando o grau da função")
                self.agent.grau = random.randint(1, 3)
                
                print(f"GERADOR     - Grau = {self.agent.grau}")
                self.agent.coeficientes = self.agent.generate_coefficients(self.agent.grau)
                f_x = [f"(({self.agent.coeficientes[i]})*(x^{self.agent.grau - i}))" for i in range(self.agent.grau + 1)]
                print(f"GERADOR     - A função gerada é: f(x) = {' + '.join(f_x)}")
                res_send1 = Message(to=str(msg_received1.sender))
                res_send1.set_metadata("performative", "inform")
                res_send1.body = str(self.agent.grau)
                await self.send(res_send1)

    #Calcula e envia a raiz obtida pelo x dado do Resolvedor
    class FunctionSolver(CyclicBehaviour):
        async def run(self):
            msg_received2 = await self.receive(timeout=10)
            if msg_received2:
                x = float(msg_received2.body)
                resultado = sum((coef*(x**i)) for i, coef in enumerate(reversed(self.agent.coeficientes)))
                print(f"GERADOR     - Enviou para o agente Resolvedor f({x}) = {resultado} => {int(resultado)}")
                res_send2 = Message(to=str(msg_received2.sender))
                res_send2.set_metadata("performative", "inform")
                res_send2.body = str(int(resultado))
                await self.send(res_send2)

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