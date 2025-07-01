# src/markov_model/edge.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

class Edge:
    """Classe que representa uma transição entre estados em um grafo.
    Atributos:
        from_state (Node): Estado de origem da transição.
        to_state (Node): Estado de destino da transição.
        weight (float): Peso da transição, representando sua probabilidade, entre 0 e 1."""
    
    def __init__(self, from_state: Node, to_state: Node, weight: float):
        
        if weight < 0 or weight > 1:
            raise ValueError("O peso da transição deve estar entre 0 e 1.")
        if from_state is None or to_state is None:
            raise ValueError("Os estados de origem e destino não podem ser nulos.")
        
        self.from_state = from_state
        self.to_state = to_state
        self.weight = weight

    def get_to_state(self) -> Node:
        """Retorna o estado de destino da transição."""
        return self.to_state

    def get_weight(self) -> float:
        """Retorna o peso da transição."""
        return self.weight
    
    def get_from_state(self) -> Node:
        """Retorna o estado de origem da transição."""
        return self.from_state

    def __repr__(self) -> str:
        return f"Edge({self.from_state.get_name()} -> {self.to_state.get_name()}, W={self.weight:.2f})"

    def __str__(self) -> str:
        return f"{self.from_state.get_name().capitalize()} -> {self.to_state.get_name().capitalize()} (Prob: {self.weight:.2f})"

