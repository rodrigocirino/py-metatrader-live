from abc import ABC, abstractmethod


class Transporte(ABC):
    @abstractmethod
    def move(self):
        pass


class Carro(Transporte):
    def move(self):
        return "Dirigindo um carro"


class Bicicleta(Transporte):
    def move(self):
        return "Pedalando uma bicicleta"


class TransporteFactory:
    @staticmethod
    def criar_transporte(tipo: str) -> Transporte:
        if tipo == "carro":
            return Carro()
        elif tipo == "bicicleta":
            return Bicicleta()
        else:
            raise ValueError("Tipo de transporte desconhecido")


def main():
    tipo_transporte = "carro"
    transporte = TransporteFactory.criar_transporte(tipo_transporte)
    print(transporte.move())

    tipo_transporte = "bicicleta"
    transporte = TransporteFactory.criar_transporte(tipo_transporte)
    print(transporte.move())


if __name__ == "__main__":
    main()
