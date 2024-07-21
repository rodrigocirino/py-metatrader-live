import numpy as np


def calculate_atr(data, period=14):
    """
    Calcula o Average True Range (ATR) com base nos dados fornecidos.
        data (DataFrame): DataFrame contendo os dados do ativo.
        period (int): Período para calcular o ATR. O padrão é 14.
        DataFrame: DataFrame contendo os dados do ativo com a coluna ATR adicionada.
    """
    data["TR"] = np.maximum.reduce(
        [data["High"] - data["Low"], abs(data["High"] - data["Close"].shift()), abs(data["Low"] - data["Close"].shift())]
    )
    data["ATR"] = data["TR"].rolling(period).mean()
    return data
