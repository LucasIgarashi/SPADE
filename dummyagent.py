# #Dummy account

# async def main():
#     dummy = DummyAgent("igarashi@magicbroccoli.de", "andorinha123321")
#     await dummy.start()

# """=========================================================================================="""

# #1º Exemplo: Print
# import spade

# class DummyAgent(spade.agent.Agent):
#     async def setup(self):
#         print("Hello World! I'm agent {}".format(str(self.jid)))

# async def main():
#     dummy = DummyAgent("igarashi@magicbroccoli.de", "andorinha123321")
#     await dummy.start()

# if __name__ == "__main__":
#     spade.run(main())

# """=========================================================================================="""

#2º Exemplo: counter
import asyncio
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class DummyAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehav()
        self.add_behaviour(b)

async def main():
    dummy = DummyAgent("igarashi@magicbroccoli.de", "andorinha123321")
    await dummy.start()
    print("DummyAgent started. Check its console to see the output.")

    print("Wait until user interrupts with ctrl+C")
    await wait_until_finished(dummy)

if __name__ == "__main__":
    spade.run(main())

# """=========================================================================================="""

#3º Exemplo: kill

# import asyncio
# import spade
# from spade.agent import Agent
# from spade.behaviour import CyclicBehaviour

# class DummyAgent(Agent):
#     class MyBehav(CyclicBehaviour):
#         async def on_start(self):
#             print("Starting behaviour . . .")
#             self.counter = 0

#         async def run(self):
#             print("Counter: {}".format(self.counter))
#             self.counter += 1
#             if self.counter > 3:
#                 self.kill(exit_code=10)
#                 return
#             await asyncio.sleep(1)

#         async def on_end(self):
#             print("Behaviour finished with exit code {}.".format(self.exit_code))

#     async def setup(self):
#         print("Agent starting . . .")
#         self.my_behav = self.MyBehav()
#         self.add_behaviour(self.my_behav)

# async def main():
#     dummy = DummyAgent("igarashi@magicbroccoli.de", "andorinha123321")
#     await dummy.start()

#     # wait until user interrupts with ctrl+C
#     while not dummy.my_behav.is_killed():
#         try:
#             await asyncio.sleep(1)
#         except KeyboardInterrupt:
#             break

#     assert dummy.my_behav.exit_code == 10

#     await dummy.stop()


# if __name__ == "__main__":
#         spade.run(main())