# command.py
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class TrueRange(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        self.calculate_atr()
        self.is_atr_over()

    def calculate_atr(self):
        print(f"Calculate ATR {self.order.order_id} purchased by {self.order.customer_name}")

    def is_atr_over(self):
        print(f"ATR is Over {self.order.order_id} purchased by {self.order.customer_name}")


class DisplayCommand(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        print(f"Order {self.order.order_id}: {self.order.customer_name}, Amount: {self.order.total_amount}")


# order.py
class GetBars:
    def __init__(self, order_id, customer_name, total_amount):
        self.order_id = order_id
        self.customer_name = customer_name
        self.total_amount = total_amount


# controller.py
class CommandController:
    def __init__(self):
        self.commands = []

    def add_command(self, command: Command):
        self.commands.append(command)

    def process_command(self):
        for command in self.commands:
            command.execute()


# main.py
# Cria uma instância da ordem
bars = GetBars(order_id=1, customer_name="John Doe", total_amount=100.0)

# Cria uma instância do controlador
controller = CommandController()

# Adiciona os comandos ao controlador
controller.add_command(TrueRange(bars))
controller.add_command(DisplayCommand(bars))

# Processa os comandos
controller.process_command()
