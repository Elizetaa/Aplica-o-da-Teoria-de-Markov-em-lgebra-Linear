# State (list)

from .state import State
from typing import List, Optional, Dict, Optional

class MarkovChain:
    def __init__(self):
        """Classe que representa uma cadeia de Markov.
        Inicialmente, a cadeia de Markov é vazia e pode ser preenchida com estados.

        Atributos:
            states (Dict[str, State]): Dicionário que mapeia nomes de estados para
                                    instâncias da classe State pelo nome.
        """
        self.states: Dict[str, State] = {}
        #debug
        print("Instância de MarkovChain vazia criada.")


    def add_state(self, state_name: str) -> State:
        """
        Adiciona um novo estado à cadeia se ele não existir.
        
        Args:
            state_name (str): O nome/identificador único do estado.
            
        Returns:
            State: O objeto State, seja ele novo ou já existente.
        """
        if state_name not in self.states:
            self.states[state_name] = State(state_name)
            #debug
            print(f"Estado '{state_name}' adicionado à cadeia de Markov.")

        return self.states[state_name]


"""
Preciso definir melhor quais funções terão em cada classe. e quais serão os atributos de cada classe."""