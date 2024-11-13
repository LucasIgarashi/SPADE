import spade
from modules.gerador import Gerador
from modules.resolvedor import Resolvedor

async def main():

    gerador = Gerador("gerador@magicbroccoli.de", "Senh@qui12")
    await gerador.start()
    print("\nAgente Gerador iniciado\n")


    resolvedor = Resolvedor("igarashi@magicbroccoli.de", "andorinha123321")
    await resolvedor.start()
    print("\nAgente Resolvedor iniciado\n")


if __name__ == "__main__":
    spade.run(main())