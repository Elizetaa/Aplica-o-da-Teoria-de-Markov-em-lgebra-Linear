import numpy as np
import pandas as pd

# Definindo estados e matriz de transição
estados = ['Ensolarado', 'Nublado', 'Chuvoso']
P = np.array([
    [0.7, 0.2, 0.1],  # Ensolarado
    [0.3, 0.4, 0.3],  # Nublado
    [0.2, 0.3, 0.5]   # Chuvoso
])

def main():
    print("Simulador de Clima com Cadeia de Markov")
    print("----------------------------------------")

    # Entrada do usuário
    while True:
        try:
            dias = int(input("Quantos dias deseja simular? (3 a 30): "))
            if 3 <= dias <= 30:
                break
            else:
                print("Digite um número entre 3 e 30.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    print("Escolha o clima inicial:")
    for i, estado in enumerate(estados):
        print(f"{i} - {estado}")

    while True:
        try:
            estado_inicial = int(input("Digite o número correspondente: "))
            if 0 <= estado_inicial < len(estados):
                break
            else:
                print("Escolha um número válido.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    # Simulação
    estado_atual = estado_inicial
    historico = []

    for dia in range(1, dias + 1):
        historico.append({
            "Dia": dia,
            "Estado": estados[estado_atual],
            "Código": estado_atual
        })
        estado_atual = np.random.choice([0, 1, 2], p=P[estado_atual])

    # Mostrar resultado
    df = pd.DataFrame(historico)
    print("\nResultado da Simulação:")
    print(df)

    # Salvar CSV
    df.to_csv("clima_simulado.csv", index=False, encoding='utf-8')
    print("\nArquivo 'clima_simulado.csv' salvo com sucesso!")

if __name__ == "__main__":
    main()
