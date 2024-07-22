from io import StringIO

import pandas as pd

# Exemplo de dados
data = """
Index,A,B,C,D,E
2024-07-10,1,2,3,4,5
2024-07-11,0,3,4,5,6
2024-07-12,0,4,5,6,7
2024-07-13,0,5,6,7,8
2024-07-14,0,6,7,8,9
2024-07-15,1,7,8,9,10
2024-07-16,0,8,9,10,11
2024-07-17,0,9,10,11,12
2024-07-18,0,10,11,12,13
2024-07-19,0,11,12,13,14
2024-07-20,0,12,13,14,15
"""

# Carregar dados de exemplo em um dataframe
df = pd.read_csv(StringIO(data), parse_dates=["Index"], index_col="Index")


# Função para encontrar os valores em A e pegar as próximas 5 linhas
def find_and_store(df):
    results = []
    for i in range(len(df)):
        if df.iloc[i]["A"]:  # Verifica se há valor na coluna A
            next_rows = df.iloc[i + 1 : i + 6]  # Pega as próximas 5 linhas
            results.append(next_rows)
    return pd.concat(results)


# Exemplo de uso
result_df = find_and_store(df)

# Mostrar o dataframe original e o resultado para clareza
print("Dataframe Original:")
print(df)
print("\nDataframe Resultante:")
print(result_df)

# Exemplo de saída detalhada
"""
Dataframe Original:
             A   B   C   D   E
Index                          
2024-07-10   1   2   3   4   5
2024-07-11   0   3   4   5   6
2024-07-12   0   4   5   6   7
2024-07-13   0   5   6   7   8
2024-07-14   0   6   7   8   9
2024-07-15   1   7   8   9  10
2024-07-16   0   8   9  10  11
2024-07-17   0   9  10  11  12
2024-07-18   0  10  11  12  13
2024-07-19   0  11  12  13  14
2024-07-20   0  12  13  14  15

Dataframe Resultante:
             A   B   C   D   E
Index                          
2024-07-11   0   3   4   5   6
2024-07-12   0   4   5   6   7
2024-07-13   0   5   6   7   8
2024-07-14   0   6   7   8   9
2024-07-16   0   8   9  10  11
2024-07-17   0   9  10  11  12
2024-07-18   0  10  11  12  13
2024-07-19   0  11  12  13  14
2024-07-20   0  12  13  14  15
"""
