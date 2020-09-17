import random   # Libreria para hacer cosas aleatorias
import json     # Libreria para manipular cadenas en formato json
import sys      # Libreria para los argumentos del programa
import numpy as np
import copy
from typing import List
from typing import Dict
from typing import Tuple
import logging



class Action:
    knight_id = 0
    knight_movement = 0

    def __init__(self, knight_id, knight_movement):
        self.knight_id = knight_id
        self.knight_movement = knight_movement


class State:
    w = 8
    h = 8
    board = np.zeros(shape=(8,8))
    score = 0
    my_knights = []  #almacena id's de mis knights
    enemy_knights = [] #almacena id's de knights enemigos
    turn = 1
    previous_move = []
    pos_eval = np.array(
    [[-50,-40,-30,-30,-30,-30,-40,-50], 
    [-40,-20,  0,  0,  0,  0,-20,-40], 
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]])

    def __init__(self, board, my_knights, enemy_knights):
        self.board = np.array(board)
        self.my_knights = my_knights   #id's de mis knights
        self.enemy_knights = enemy_knights #id's de knights enemigos

    def get_position_score(self, knight_id):
        log = logging.getLogger()
        score = 0
        fact = 0.002 #a mayor valor de factor, mas importancia se dara a la posición de los caballos
        row, col = np.where(self.board == int(knight_id))
        row = row[0]
        col = col[0]
        score = self.pos_eval[row][col]
        if knight_id in self.my_knights:  #
            return score * fact

        elif knight_id in self.enemy_knights:  
            return score * -1 * fact

             
    
    def update_score(self):  #score para evaluar estados
        self.score = len(self.my_knights) - len(self.enemy_knights)
        for knight in self.my_knights:
            self.score += self.get_position_score(knight)
        for knight in self.enemy_knights:
            self.score += self.get_position_score(knight)
            



    def get_movement(self, knight_pos, movement_number: int):  #para obtener las jugadas validas
        x = knight_pos[1]
        y = knight_pos[0]
        is_taken = False
        nx = x
        ny = y
        if movement_number == 0:
            nx += 1
            ny += 2
        elif movement_number == 1:
            nx += 2
            ny += 1
        elif movement_number == 2:
            nx += 2
            ny += -1
        elif movement_number == 3:
            nx += 1
            ny += -2
        elif movement_number == 4:
            nx += -1
            ny += -2
        elif movement_number == 5:
            nx += -2
            ny += -1
        elif movement_number == 6:
            nx += -2
            ny += 1
        elif movement_number == 7:
            nx += -1
            ny += 2
        else:
            print("Error: Movimiento no encontrado")

        if nx < 8 and ny < 8 and nx >= 0 and ny >= 0:
            if self.board[ny][nx]:
                if self.turn == 1:
                    if str(self.board[ny][nx]) in self.my_knights:
                        is_taken = True
                    else: 
                        return movement_number
                else:
                    if str(self.board[ny][nx]) in self.enemy_knights:
                        is_taken = True
                    else:
                        return movement_number
            else:    
                return movement_number    

    def get_movement_trans(self, knight_pos, movement_number: int) -> Tuple[int, int, int]:

        x = knight_pos[1]
        y = knight_pos[0]
        is_taken = False
        nx = x
        ny = y
        if movement_number == 0:
            nx += 1
            ny += 2
        elif movement_number == 1:
            nx += 2
            ny += 1
        elif movement_number == 2:
            nx += 2
            ny += -1
        elif movement_number == 3:
            nx += 1
            ny += -2
        elif movement_number == 4:
            nx += -1
            ny += -2
        elif movement_number == 5:
            nx += -2
            ny += -1
        elif movement_number == 6:
            nx += -2
            ny += 1
        elif movement_number == 7:
            nx += -1
            ny += 2
        else:
            print("Error: Movimiento no encontrado")

        if nx < 8 and ny < 8 and nx >= 0 and ny >= 0:
            if self.board[ny][nx]:
                return nx, ny,self.board[ny][nx]
            else:    
                return nx, ny, None    
   
    def get_knight_actions(self, knight):  #recibe id de knight, retorna acciones posibles ej: (1, 2, 3)
        knight_actions = []
        knight_pos = np.argwhere(self.board == int(knight))
        knight_pos = knight_pos[0]
        for i in range(8):  #agregamos a una lista todos los movimientos posibles del caballo
            move = self.get_movement(knight_pos, i)
            if move != None:
                knight_actions.append(move)
        return knight_actions


    def get_actions(self):  #retorna posibles acciones en una lista de forma ([knight_id, (1,2,3)])
        possible_actions = []
        if self.turn == 1:
            for knight in self.my_knights:
                knight_actions = self.get_knight_actions(knight)
                possible_actions.append([knight, knight_actions])
        else:
            for knight in self.enemy_knights:
                knight_actions = self.get_knight_actions(knight)
                possible_actions.append([knight, knight_actions])  

        return possible_actions

    def transition(self, knight_id, movement_number):  #retorna el estado despues de hacer movimiento
        new_state = copy.deepcopy(self)
        knight_pos = np.argwhere(new_state.board == int(knight_id))
        knight_pos = knight_pos[0]
        x = knight_pos[0]
        y = knight_pos[1]
        new_state.board[x][y] = None  #por alguna razon esta es al reves xd
        new_pos = new_state.get_movement_trans(knight_pos, movement_number) #tupla de nueva posicion
        if new_pos:
            x = new_pos[0]
            y = new_pos[1]
            new_state.board[y][x] = int(knight_id)

            if new_state.turn == 1:  #cambio de turno
                new_state.turn = 2
            else:
                new_state.turn = 1
            new_state.previous_move = [knight_id, movement_number] #almacena la jugada anterior
            if self.turn == 1:
                if new_pos[2]:
                    new_state.enemy_knights.remove(str(new_pos[2]))
            else:
                if new_pos[2]:
                    new_state.my_knights.remove(str(new_pos[2]))
            new_state.update_score() #calcula puntaje del nuevo estado
            return new_state
    
    def minimax(self):
        states = []
        plays = self.get_actions()  #lista de forma [knight_id, [mov_posibles]]
        best_score = -100000
        for knight in plays:
            knight_id = knight[0]
            possible_moves = knight[1]
            for move in possible_moves:
                states.append(self.transition(knight_id, move))  #adiciona cada jugada posible a la lista de estados


        for state in states:  #por cada estado directo desde el primero
            enemy_states = []     
            enemy_plays = state.get_actions()
            for enemy_knight in enemy_plays:
                knight_id = enemy_knight[0]
                possible_moves = enemy_knight[1]
                for enemy_move in possible_moves:
                    enemy_states.append(state.transition(knight_id, enemy_move))  #adiciona cada jugada posible a la lista de estados enemigos
            enemy_states.sort(key=lambda x: x.score)
            best_enemy_state = enemy_states[1]
            last_plays = best_enemy_state.get_actions()  #PROBLEMA
            last_states = []

            
            for knight in last_plays:
                knight_id = knight[0]
                possible_moves = knight[1]
                for move in possible_moves:
                    last_states.append(best_enemy_state.transition(knight_id, move))
            last_states.sort(key = lambda x: x.score, reverse= True)
            best_outcome = last_states[0]   
 
            if best_outcome.score > best_score:
                best_score = best_outcome.score
                best_play = state.previous_move

        return best_play


    
    def minimax_dos(self, depth):
        log = logging.getLogger()
        states = []
        plays = self.get_actions()  #lista de forma [knight_id, [mov_posibles]]
        best_plays = []
        best_score = -100000
        for knight in plays:
            knight_id = knight[0]
            possible_moves = knight[1]
            for move in possible_moves:
                states.append(self.transition(knight_id, move))  #adiciona cada jugada posible a la lista de estados
        
        for state in states:
            if len(state.enemy_knights) > 0:
                for i in range(depth-1):
                    move = state.best_available_movement()
                    next_state = state.transition(move[0], move[1])
                if next_state.score > best_score:
                    best_plays = []
                    best_plays.append(state.previous_move)
                    best_score = next_state.score
                elif next_state.score == best_score:
                    best_plays.append(state.previous_move)
            else :
                best_plays.append(state.previous_move)
        rand = random.randrange(0,len(best_plays))

        log.warning("Mejor movimiento: "+ str(best_plays[rand]))
        log.warning("Puntaje mejor movimiento: " + str(best_score))
        return best_plays[rand]


    def best_available_movement(self):
        log = logging.getLogger()
        states = []
        plays = self.get_actions()  #lista de forma [knight_id, [mov_posibles]]
        if self.turn == 1:
            best_score = -100000
            best_moves = []
            for knight in plays:
                knight_id = knight[0]
                possible_moves = knight[1]
                for move in possible_moves:
                    states.append(self.transition(knight_id, move))  #adiciona cada jugada posible a la lista de estados  


            for state in states:
                if state.score > best_score:
                    best_moves = []
                    best_moves.append(state.previous_move)
                    best_score = state.score
                elif state.score == best_score:
                    best_moves.append(state.previous_move)
        else:
            best_score = 100000
            best_moves = []
            for knight in plays:
                knight_id = knight[0]
                possible_moves = knight[1]
                for move in possible_moves:
                    states.append(self.transition(knight_id, move))  #adiciona cada jugada posible a la lista de estados  


            for state in states:
                if state.score < best_score:
                    best_moves = []
                    best_moves.append(state.previous_move)
                    best_score = state.score
                elif state.score == best_score:
                    best_moves.append(state.previous_move)
        rand = random.randrange(0,len(best_moves))
        return best_moves[rand]
                        

    def return_random_movement(self):  #retorna movimientos aleatorios
        movement = []
        actions = self.get_actions()
        element = random.choice(actions)
        while not element[1]:
            element = random.choice(actions)
        knight_id = element[0]
        knight_movements = element[1]
        if not knight_movements:
            raise Exception(element)
        knight_move = knight_movements[random.randrange(0,len(knight_movements))]
        movement.append(knight_id)
        movement.append(knight_move)

        return movement




        

if __name__ == "__main__":
    # Obteniendo cadena de entrada (formato json)

    state_json = sys.argv[1]

    # Transformando la cadena de entrada en diccionario
    state = json.loads(state_json) 

    current_board = list(state['ids'])
    # Obteniendo lista de caballos
    my_knights = list(state['my_knights_dict'].keys())
    enemy_knights = list(state['enemy_knights_dict'].keys())

    state_class = State(current_board, my_knights, enemy_knights)
    test = state_class.best_available_movement()

    best_outcome = state_class.minimax_dos(4)
    knight_id = random.choice(my_knights)

    # Eligiendo movimiento aleatoriamente
    knight_movement = random.choice(range(7))

    # Creando diccionario de resultado
    result = {
        "knight_id": best_outcome[0],
        "knight_movement": best_outcome[1]
    }


    # Imprimiendo resultado
    print(json.dumps(result))