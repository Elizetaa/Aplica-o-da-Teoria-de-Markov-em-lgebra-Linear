# src/markov_model/graph.py
from typing import List, Tuple, Dict, Optional
from .node import Node # Importação relativa continua correta
from .edge import Edge # Importação relativa continua correta
import math

class Graph:
    """Classe que representa uma cadeia de Markov.
    Gerencia os nós (estados) e as arestas (transições com probabilidades) da cadeia.

    Atributos:
        nodes (Dict[str, Node]): Dicionário que mapeia nomes de nós (em minúsculas)
                                 para instâncias da classe Node.
    """
    def __init__(self):
        """Inicializa uma instância vazia de Graph (Cadeia de Markov)."""
        self.nodes: Dict[str, Node] = {}

    def _get_or_create_node(self, name: str) -> Node:
        """
        Método auxiliar privado: Obtém um nó pelo nome ou o cria se não existir.
        Normaliza o nome do nó para minúsculas.
        Args:
            name (str): O nome/identificador único do estado.
        Returns:
            Node: O objeto Node, seja ele novo ou já existente.
        """
        name_lower = name.lower()
        if name_lower not in self.nodes:
            self.nodes[name_lower] = Node(name_lower)
        return self.nodes[name_lower]

    def get_node(self, name: str) -> Optional[Node]:
        """
        Obtém um nó pelo seu nome.
        Args:
            name (str): O nome do nó a ser obtido.
        Returns:
            Node: O objeto Node correspondente ao nome, ou None se não existir.
        """
        name_lower = name.lower()
        return self.nodes.get(name_lower)

    def build_from_observations(self, observations: List[Tuple[str, str, int]]):
        """
        Este método crucial transforma dados brutos de observações em um grafo de cadeia de Markov.
        Ele calcula as probabilidades de transição com base na frequência das observações.

        Args:
            observations: Uma lista de tuplas. Cada tupla é uma observação de tráfego.
                          Formato: (nome_da_origem, nome_do_destino, numero_de_carros)
                          Exemplo: [('A', 'B', 120), ('A', 'C', 80)]
        """
        print("\n--- Construindo grafo a partir das observações ---")

        origin_totals: Dict[str, int] = {}
        for origin, _, count in observations:
            origin_lower = origin.lower()
            origin_totals[origin_lower] = origin_totals.get(origin_lower, 0) + count

        for origin_name, dest_name, count in observations:
            origin_node = self._get_or_create_node(origin_name)
            dest_node = self._get_or_create_node(dest_name)

            total_out_from_origin = origin_totals.get(origin_name.lower(), 0)
            probability = count / total_out_from_origin if total_out_from_origin > 0 else 0.0

            edge = Edge(from_state=origin_node, to_state=dest_node, weight=probability)

            origin_node.add_edge(edge)

        print("Grafo construído com sucesso a partir das observações.")
        self.validate_probabilities() # Valida as probabilidades após a construção

    def validate_probabilities(self, tolerance: float = 1e-9) -> bool:
        """
        Valida se a soma das probabilidades de saída de cada nó é aproximadamente 1.0.
        Args:
            tolerance (float): Margem de erro para comparação de números flutuantes.
        Returns:
            bool: True se todas as somas forem válidas, False caso contrário.
        """
        print("\n--- Validando Probabilidades ---")
        is_valid = True
        if not self.nodes:
            print("Grafo vazio, nenhuma probabilidade para validar.")
            return True

        for node_name in sorted(self.nodes.keys()):
            node = self.nodes[node_name]
            total_prob = 0.0
            if node.transitions:
                for edge in node.transitions.values():
                    total_prob += edge.get_weight()

                if not math.isclose(total_prob, 1.0, rel_tol=tolerance):
                    print(f"AVISO: A soma das probabilidades de saída do nó '{node.get_name().capitalize()}' é {total_prob:.4f}, deveria ser 1.0.")
                    is_valid = False
            # else: # Noção terminal, não precisa somar 1.0
            #     print(f"Nó '{node.get_name().capitalize()}': Não tem transições de saída (nó terminal).")

        if is_valid:
            print("Todas as probabilidades de saída dos nós são válidas (soma ~1.0).")
        else:
            print("Problemas de validação encontrados. Verifique os avisos acima.")
        print("----------------------------------")
        return is_valid

    def calculate_path_probability(self, path: List[str]) -> float:
        """
        Calcula a probabilidade total de seguir uma rota específica em uma cadeia de Markov.
        Args:
            path: Uma lista de nomes de nós que define o caminho. Ex: ['A', 'B', 'D'].
        Returns:
            A probabilidade total (um número entre 0 e 1). Retorna 0.0 se o caminho for inválido
            ou impossível.
        """
        if len(path) < 2:
            print("Erro: O caminho deve conter pelo menos dois nós (origem e destino).")
            return 0.0

        total_prob = 1.0

        for i in range(len(path) - 1):
            origin_name = path[i].lower()
            dest_name = path[i+1].lower()

            origin_node = self.get_node(origin_name)
            if origin_node is None:
                print(f"Erro: Nó de origem '{origin_name.capitalize()}' não foi encontrado no grafo.")
                return 0.0

            step_prob = origin_node.get_transition_probability(dest_name)

            if step_prob == 0.0:
                print(f"Atenção: Transição de '{origin_name.capitalize()}' para '{dest_name.capitalize()}' não existe ou tem probabilidade zero. Caminho impossível.")
                return 0.0

            total_prob *= step_prob

        return total_prob

    def find_all_paths(self, start_node_name: str, end_node_name: str, max_depth: int = 7) -> List[Tuple[List[str], float]]:
        """
        Encontra todos os caminhos possíveis de um nó de início para um nó de destino
        e suas respectivas probabilidades. Utiliza busca em profundidade (DFS).

        Args:
            start_node_name (str): Nome do nó de início.
            end_node_name (str): Nome do nó de destino.
            max_depth (int): Profundidade máxima de busca para evitar loops infinitos
                             em grafos cíclicos e limitar a complexidade.

        Returns:
            List[Tuple[List[str], float]]: Uma lista de tuplas, onde cada tupla contém:
                                            - Uma lista de strings representando o caminho (nomes dos nós).
                                            - A probabilidade acumulada desse caminho.
        """
        start_node_name_lower = start_node_name.lower()
        end_node_name_lower = end_node_name.lower()

        start_node = self.get_node(start_node_name_lower)
        if not start_node:
            print(f"Erro: Nó de início '{start_node_name.capitalize()}' não encontrado no grafo.")
            return []
        
        # O nó de destino não precisa existir no grafo se for um "caminho" que termina nele
        # Mas para a busca, é bom que ele exista para validar a transição final.
        # No entanto, a lógica do DFS já cobre isso ao tentar obter a próxima aresta.

        all_paths: List[Tuple[List[str], float]] = []
        # Inicia a busca DFS. current_path_names começa com o nó inicial.
        # current_path_prob começa em 1.0 porque é a probabilidade do caminho até o nó inicial.
        self._dfs_find_paths(
            current_node=start_node,
            target_node_name=end_node_name_lower,
            current_path_names=[start_node_name_lower], # Caminho atual (lista de nomes)
            current_path_prob=1.0,                       # Probabilidade acumulada do caminho
            found_paths=all_paths,                       # Lista para armazenar caminhos encontrados
            max_depth=max_depth                          # Profundidade máxima
        )
        return all_paths

    def _dfs_find_paths(self, current_node: Node, target_node_name: str,
                       current_path_names: List[str], current_path_prob: float,
                       found_paths: List[Tuple[List[str], float]], max_depth: int):
        """
        Método auxiliar recursivo para busca em profundidade (DFS) de caminhos.
        """
        # Se o caminho atual atingiu a profundidade máxima, pare de explorar este ramo.
        # Usa ">=" porque o `max_depth` inclui o nó de início.
        if len(current_path_names) > max_depth:
            return

        # Se o nó atual é o nó de destino, encontramos um caminho válido.
        if current_node.get_name() == target_node_name:
            found_paths.append((current_path_names.copy(), current_path_prob))
            # Não retorna aqui se você quiser que caminhos mais longos que PASSEM pelo target
            # e continuem (até o max_depth) sejam considerados, mas para "caminhos para o destino",
            # é comum parar aqui. Para uma cadeia de Markov, onde revisitar estados é comum,
            # podemos permitir continuar a explorar a partir do nó de destino *se* o max_depth
            # ainda não foi atingido, mas o pedido é "transição de um ponto a outro", sugerindo
            # que o caminho *termina* no ponto de destino. Vamos manter o `return`.
            return

        # Explora as transições (arestas de saída) do nó atual.
        for dest_node_name, edge in current_node.transitions.items():
            next_node = edge.get_to_state()
            edge_weight = edge.get_weight()

            # Se a probabilidade da aresta for zero, não é uma transição real.
            if edge_weight == 0.0:
                continue

            # Calcula a probabilidade do caminho acumulada até o próximo nó.
            next_path_prob = current_path_prob * edge_weight

            # Chamada recursiva para o próximo nó.
            self._dfs_find_paths(
                current_node=next_node,
                target_node_name=target_node_name,
                current_path_names=current_path_names + [next_node.get_name()], # Adiciona o próximo nó ao caminho
                current_path_prob=next_path_prob,
                found_paths=found_paths,
                max_depth=max_depth
            )


    def display(self):
        """
        Um método de "ajuda" para visualizarmos a estrutura do grafo que foi construído.
        Ele imprime todos os nós e suas conexões de saída com as probabilidades.
        """
        print("\n--- Estrutura do Grafo ---")
        if not self.nodes:
            print("O grafo está vazio.")
            return

        for node_name in sorted(self.nodes.keys()):
            node = self.nodes[node_name]
            if not node.transitions:
                print(f"Nó: {node.get_name().capitalize()} -> (Nenhuma saída/Nó terminal)")
            else:
                print(f"Nó: {node.get_name().capitalize()}")
                for dest_name in sorted(node.transitions.keys()):
                    edge = node.transitions[dest_name]
                    print(f"  -> para {dest_name.capitalize()} (Prob: {edge.get_weight():.4f})")
        print("--------------------------\n")