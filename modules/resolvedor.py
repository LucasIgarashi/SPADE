import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message
from numpy import array, roots, isreal
from numpy.linalg import solve

# Agente resolvedor
class Resolvedor(Agent):
    grau = 0

    # Tipifica qual a função
    class setTypeFunction(OneShotBehaviour):
        async def run(self):
            print("===========================================================================")
            print("RESOLVEDOR  - Requisitando o grau da função...")
            msg_request1 = Message(to="gerador@magicbroccoli.de")
            msg_request1.set_metadata("performative", "request")
            await self.send(msg_request1)
            res_received1 = await self.receive(timeout=10)
            if res_received1:
                self.agent.grau = int(res_received1.body)
                graus = {
                    1: 'linear',
                    2: 'quadrática',
                    3: 'cúbica'
                }
                print(f"RESOLVEDOR  - Grau = {self.agent.grau}. Logo, a função é {graus[self.agent.grau]}")
                print("===========================================================================")
                self.agent.add_behaviour(self.agent.Resolve())

    class Resolve(CyclicBehaviour):
        async def run(self):
            resultados = []
            n_const = [i for i in range(self.agent.grau + 1)]

            for x in n_const:
                msg_request2 = Message(to="gerador@magicbroccoli.de")
                msg_request2.set_metadata("performative", "subscribe")
                msg_request2.body = str(x)
                print("===========================================================================")
                print(f"RESOLVEDOR  - Enviou para o agente Gerador x = {x}")
                await self.send(msg_request2)
                res_received2 = await self.receive(timeout=10)
                if res_received2:
                    resultado = float(res_received2.body)
                    resultados.append((x, resultado))
                    print(f"RESOLVEDOR  - Recebeu resultado = {resultado}")
                    if resultado == 0 and self.agent.grau == 1:
                        print(f"RESOLVEDOR  - A solução para a função é x = {x}")
                        await self.agent.stop()
                else:
                    print(f"RESOLVEDOR  - Não recebeu resposta para x = {x}")

            if len(resultados) == self.agent.grau + 1:
                A = []
                B = []
                for x, fx in resultados:
                    r = [x**i for i in reversed(range(self.agent.grau + 1))]
                    A.append(r)
                    B.append(fx)
                A = array(A)
                B = array(B)
                coeficientes = solve(A, B).round().astype(int) #Pelos valores obtidos com os chutes anteriores, encontra os coeficientes da função
                f_x = [f"(({coeficientes[i]})*(x^{self.agent.grau - i}))" for i in range(self.agent.grau + 1)]
                print("===========================================================================")
                print(f"RESOLVEDOR  - A função gerada é: f(x) = {' + '.join(f_x)}")
                raizes = roots(coeficientes)
                raizes_reais = [raiz.real for raiz in raizes if isreal(raiz)]
                print("===========================================================================")

                # Enviar as raízes reais para o agente Gerador e verificar se f(x) = 0
                for raiz in raizes_reais:
                    msg_request3 = Message(to="gerador@magicbroccoli.de")
                    msg_request3.set_metadata("performative", "subscribe")
                    msg_request3.body = str(raiz)
                    await self.send(msg_request3)
                    res_received3 = await self.receive(timeout=10)
                    if res_received3:
                        valor_funcao = float(res_received3.body)
                        if valor_funcao == 0:
                            print(f"RESOLVEDOR  - Como f({raiz}) = 0, a raiz {raiz} é solução.")
                print("===========================================================================")
                await self.agent.stop()

    async def setup(self):
        stf = self.setTypeFunction()
        t = Template()
        t.set_metadata("performative", "inform")
        self.add_behaviour(stf, t)

async def main():
    resolvedor = Resolvedor("resolvedor@magicbroccoli.de", "Senh@qui12")
    await resolvedor.start()

if __name__ == '__main__':
    spade.run(main())
