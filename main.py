# main.py
import sys
import os

# Adiciona o diretório 'src' ao PATH do Python
# Isso permite importar 'markov_model' de 'src'
# Supondo que main.py está na mesma pasta que 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Agora a importação correta para sua estrutura:
from src.markov_model.graph import Graph

def main():
    print("Iniciando a aplicação de Modelo de Markov.")

    # 1. Instanciar o grafo
    markov_model = Graph()

    # 2. Definir observações de tráfego
    observations = [
        ('A', 'B', 120),
        ('A', 'C', 80),
        ('B', 'D', 70),
        ('B', 'E', 50),
        ('C', 'B', 30),
        ('C', 'F', 50),
        ('D', 'G', 40),
        ('D', 'H', 30),
        ('E', 'D', 20),
        ('E', 'G', 30),
        ('F', 'C', 10),
        ('F', 'H', 40),
        ('G', 'I', 70),
        ('H', 'I', 70)
    ]

    # 3. Construir o grafo a partir das observações
    markov_model.build_from_observations(observations)

    # 4. Exibir a estrutura do grafo construído
    markov_model.display()

    # 5. Validar as probabilidades
    markov_model.validate_probabilities()

    # 6. Calcular a probabilidade de caminhos específicos
    print("\n--- Calculando Probabilidades de Caminhos Predefinidos ---")

    path1 = ['A', 'B', 'D', 'G', 'I']
    prob1 = markov_model.calculate_path_probability(path1)
    print(f"Probabilidade do caminho {PathFormatter.format_path(path1)}: {prob1:.6f}")

    path2 = ['A', 'C', 'F', 'H', 'I']
    prob2 = markov_model.calculate_path_probability(path2)
    print(f"Probabilidade do caminho {PathFormatter.format_path(path2)}: {prob2:.6f}")

    path3 = ['A', 'D', 'G'] # Caminho impossível (A -> D não existe diretamente)
    prob3 = markov_model.calculate_path_probability(path3)
    print(f"Probabilidade do caminho {PathFormatter.format_path(path3)}: {prob3:.6f}")

    path4 = ['B', 'E', 'D', 'H'] # Caminho existente
    prob4 = markov_model.calculate_path_probability(path4)
    print(f"Probabilidade do caminho {PathFormatter.format_path(path4)}: {prob4:.6f}")


    # 7. Demonstrar as possibilidades de transição de um ponto a outro (Nova Funcionalidade!)
    print("\n--- Possibilidades de Transição entre Pontos ---")

    start_node_find = 'A'
    end_node_find = 'I'
    # max_depth é importante para evitar loops infinitos em grafos cíclicos.
    # Um valor de 7 permite caminhos com até 7 nós (6 transições).
    found_paths = markov_model.find_all_paths(start_node_find, end_node_find, max_depth=7)

    if found_paths:
        print(f"Todos os caminhos possíveis de '{start_node_find.capitalize()}' para '{end_node_find.capitalize()}' (Max Profundidade: 7):")
        # Ordena os caminhos por probabilidade (maior para menor) e depois por comprimento (menor para maior)
        found_paths.sort(key=lambda x: (-x[1], len(x[0])))
        for i, (path, prob) in enumerate(found_paths):
            formatted_path = PathFormatter.format_path(path)
            print(f"  {i+1}. {formatted_path} (Prob: {prob:.6f})")
    else:
        print(f"Nenhum caminho encontrado de '{start_node_find.capitalize()}' para '{end_node_find.capitalize()}' dentro da profundidade máxima.")

    print("\n--- Testando outro par de pontos (Ex: B para G) ---")
    start_node_find_2 = 'B'
    end_node_find_2 = 'G'
    found_paths_2 = markov_model.find_all_paths(start_node_find_2, end_node_find_2, max_depth=5)
    if found_paths_2:
        print(f"Todos os caminhos possíveis de '{start_node_find_2.capitalize()}' para '{end_node_find_2.capitalize()}' (Max Profundidade: 5):")
        found_paths_2.sort(key=lambda x: (-x[1], len(x[0])))
        for i, (path, prob) in enumerate(found_paths_2):
            formatted_path = PathFormatter.format_path(path)
            print(f"  {i+1}. {formatted_path} (Prob: {prob:.6f})")
    else:
        print(f"Nenhum caminho encontrado de '{start_node_find_2.capitalize()}' para '{end_node_find_2.capitalize()}' dentro da profundidade máxima.")

    print("\n--- Fim da Aplicação ---")

# Classe auxiliar para formatar caminhos para exibição
class PathFormatter:
    @staticmethod
    def format_path(path_names: list[str]) -> str:
        """Formata uma lista de nomes de nós em uma string de caminho legível."""
        return " -> ".join([name.capitalize() for name in path_names])

if __name__ == "__main__":
    main()