# src/markov_model/node.py
from __future__ import annotations
from typing import List, Optional, Dict

class Node:
    """Classe que representa um nó em um grafo.
    Inicialmente, o nó é vazio e pode ser preenchido com transições.
    Atributos:
        name (str): Nome/identificador único do nó.
        transitions (Dict[str, Edge]): Dicionário que mapeia nomes de nós
                                        para suas transições.
    """
    def __init__(self, name: str):
        """Inicializa um nó com um nome único."""
        if not name:
            raise ValueError("O nome do nó não pode ser vazio.")
        if not isinstance(name, str):
            raise TypeError("O nome do nó deve ser uma string.")
        
        name = name.lower()#padronizacao

        self.name: str = name
        self.transitions: Dict[str, Edge] = {}
        #debug
        print(f"Instância de Node '{name}' criada.")

    def add_edge(self, edge: Edge) -> None:
        """Adiciona uma transição ao nó.
        Args:
            edge (Edge): A transição a ser adicionada.
        """
        if edge is None:
            raise ValueError("A transição não pode ser nula.")
        if edge.get_to_state().get_name() in self.transitions:
            print(f"Transição de '{self.name}' para '{edge.get_to_state().get_name()}' já existe.")
            return
        
        self.transitions[edge.get_to_state().get_name()] = edge
        #debug
        print(f"Transição de '{self.name}' para '{edge.get_to_state().get_name()}' adicionada.")


    def get_name(self) -> str:
        """Retorna o nome do nó."""
        return self.name
    

    def get_transition_probability(self, to_node: str) -> float:
        """Retorna a probabilidade de transição para um nó específico.
        Args:
            to_node (str): Nome do nó de destino.
        Returns:
            float: Probabilidade da transição.
        """
        if to_node is None:
            raise ValueError("O nome do nó de destino não pode ser nulo.")

        to_node = to_node.lower()  # Normalização

        if to_node in self.transitions:
            return self.transitions[to_node].get_weight()
        return 0.0
        
    
    def __repr__(self) -> str:
        return f"Node('{self.name}')"

    def __str__(self) -> str:
        return f"Estado: {self.name.capitalize()}"