import math
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade.message import Message

# Agente resolvedor
class Resolvedor(Agent):
    grau = 0

    # TODO: remover os 'for' e substituir pelas ferramentas que o próprio SPADE dá, como o CyclicBehavior

    #Tipifica qual a função
    class setTypeFunction(OneShotBehaviour):
        async def run(self):
            print("===========================================================================")
            print("RESOLVEDOR  - Requisitando o grau da função...")
            msg = Message(to="gerador@magicbroccoli.de")
            msg.set_metadata("performative", "request")
            await self.send(msg)
            res = await self.receive(timeout=10)
            if res:
                self.agent.grau = int(res.body)
                graus = {
                    1: 'linear',
                    2: 'quadrática',
                    3: 'cúbica'
                }
                print(f"RESOLVEDOR  - Grau = {self.agent.grau}. Logo, a função é {graus[self.agent.grau]}")
                print("===========================================================================")
                self.agent.add_behaviour(self.agent.Resolve())

    class Resolve(CyclicBehaviour):
        # Soluciona um sistema linear da forma Ax=b
        def gaussian_elimination(self, A, b):
            n = len(A)

            for i in range(n):
                # Confere se o valor da diagonal é zero, e troca com outra linha caso necessário
                if A[i][i] == 0:
                    for k in range(i + 1, n):
                        if A[k][i] != 0:
                            A[i], A[k] = A[k], A[i]
                            b[i], b[k] = b[k], b[i]
                            break
                    else:
                        raise ValueError("Matriz é singular e não pode ser resolvida.")

                # Normaliza a linha pela diagonal
                factor = A[i][i]
                for j in range(i, n):
                    A[i][j] /= factor
                b[i] /= factor

                # Elimina as linhas inferiores
                for k in range(i + 1, n):
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]

            # Faz a substituição regressiva
            x = [0] * n
            for i in range(n - 1, -1, -1):
                x[i] = b[i]
                for j in range(i + 1, n):
                    x[i] -= A[i][j] * x[j]

            return x

        # Acha as raízes reais de um polinômio de até grau 3
        def solve_polynomial(self, coefficients):
            if (len(coefficients) == 4): # Polinômio de terceiro grau
                a, b, c, d = coefficients

                # Este método utiliza as fórmulas de Cardano
                # https://pt.wikipedia.org/wiki/Fórmulas_de_Cardano

                # Converter para a forma reduzida z^3 + pz + q = 0 usando x = z - b/(3a)
                p = (3*a*c - b**2) / (3*a**2)
                q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27*a**3)
                delta = (q**2 / 4) + (p**3 / 27)
        
                if delta > 0: # Uma raíz real
                    u = (-q / 2 + delta**0.5)**(1/3)
                    v = (-q / 2 - delta**0.5)**(1/3)
                    t1 = u + v
                    root = t1 - b / (3*a)
                    return [root]
                elif delta == 0: # Três raizes reais, pelo menos duas iguais
                    u = (-q / 2)**(1/3)
                    t1 = 2*u
                    t2 = -u
                    root1 = t1 - b / (3*a)
                    root2 = t2 - b / (3*a)
                    return [root1, root2]
                else: # Três raízes reais e distintas
                    r = (-p**3 / 27)**0.5
                    theta = (1 / 3) * math.acos(-q / (2 * r))
                    r = (-p / 3)**0.5
                    t1 = 2 * r * math.cos(theta)
                    t2 = 2 * r * math.cos(theta + 2 * math.pi / 3)
                    t3 = 2 * r * math.cos(theta + 4 * math.pi / 3)
                    root1 = t1 - b / (3*a)
                    root2 = t2 - b / (3*a)
                    root3 = t3 - b / (3*a)
                    return [root1, root2, root3]
            elif (len(coefficients) == 3): # Polinômio de segundo grau
                a, b, c = coefficients

                # Este método utiliza a fórmula quadrática padrão
                delta = b**2 - 4*a*c

                if delta > 0: # Duas raízes reais e distintas
                    root1 = (-b + delta**0.5) / (2*a)
                    root2 = (-b - delta**0.5) / (2*a)
                    return [root1, root2]
                elif delta == 0: # Duas raízes reais e iguais
                    root = -b / (2*a)
                    return [root]
                else: # Nenhuma raíz real
                    return []
            elif (len(coefficients) == 2): # Polinômio de primeiro grau
                a, b = coefficients

                # Este é simplesmente uma reta
                if (a == 0):
                    return []
                return [-b / a]
            else:
                return []
            

        async def run(self):
            resultados = []
            n_const = [i for i in range(self.agent.grau + 1)]

            for x in n_const:
                msg = Message(to="gerador@magicbroccoli.de")
                msg.set_metadata("performative", "subscribe")
                msg.body = str(x)
                print("===========================================================================")
                print(f"RESOLVEDOR  - Enviou para o agente Gerador x = {x}")
                await self.send(msg)
                res = await self.receive(timeout=10)
                if res:
                    resultado = float(res.body)
                    resultados.append((x, resultado))
                    print(f"RESOLVEDOR  - Recebeu resultado = {resultado}")
                    if resultado == 0 and self.agent.grau == 1:
                        print(f"RESOLVEDOR  - A solução para a função é x = {x}")
                        await self.agent.stop()
                else:
                    print(f"RESOLVEDOR  - Não recebeu resposta para x = {x}")

            if len(resultados) == self.agent.grau + 1:
                A = []
                b = []
                for x, fx in resultados:
                    r = [x**i for i in reversed(range(self.agent.grau + 1))]
                    A.append(r)
                    b.append(fx)

                # Pelos valores obtidos com os chutes anteriores, encontra os coeficientes da função
                coeficientes = self.gaussian_elimination(A, b)
                f_x = [f"(({coeficientes[i]})*(x^{self.agent.grau - i}))" for i in range(self.agent.grau + 1)]
                print("===========================================================================")
                print(f"RESOLVEDOR  - A função gerada é: f(x) = {' + '.join(f_x)}")
                raizes_reais = self.solve_polynomial(coeficientes)
                print(raizes_reais)
                print("===========================================================================")

                #Enviar as raízes reais para o agente Gerador e verificar se f(x) = 0
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
