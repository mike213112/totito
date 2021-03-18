# Imports
from math import inf as infinity
from random import choice
import platform
import time
from os import system
from getpass import getuser


"""
    Implementaciòn del Juego Tic Tac Toe con Inteligencia Articial
    Autor: Miguel Mazariegos
    Año: 2021
"""

HUMANO = -1
COMPUTADORA = +1
matrix = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
USER = getuser()


def evaluar(estado):
    if victoria(estado, COMPUTADORA):
        score = +1
    elif victoria(estado, HUMANO):
        score = -1
    else:
        score = 0

    return score


def victoria(estado, jugador):
    estado_de_la_victoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jugador, jugador, jugador] in estado_de_la_victoria:
        return True
    else:
        return False


def juego_terminado(estado):
    return victoria(estado, HUMANO) or victoria(estado, COMPUTADORA)


def celdas_vacias(estado):
    celdas = []

    for x, row in enumerate(estado):
        for y, celda in enumerate(row):
            if celda == 0:
                celdas.append([x, y])

    return celdas


def movimiento_valido(x, y):
    if [x, y] in celdas_vacias(matrix):
        return True
    else:
        return False


def mandar_movimiento(x, y, jugador):
    if movimiento_valido(x, y):
        matrix[x][y] = jugador
        return True
    else:
        return False


def minimax(estado, profundidad, jugador):
    if jugador == COMPUTADORA:
        mejor = [-1, -1, -infinity]
    else:
        mejor = [-1, -1, +infinity]

    if profundidad == 0 or juego_terminado(estado):
        score = evaluar(estado)
        return [-1, -1, score]

    for celda in celdas_vacias(estado):
        x, y = celda[0], celda[1]
        estado[x][y] = jugador
        score = minimax(estado, profundidad - 1, -jugador)
        estado[x][y] = 0
        score[0], score[1] = x, y

        if jugador == COMPUTADORA:
            if score[2] > mejor[2]:
                mejor = score  # max value
        else:
            if score[2] < mejor[2]:
                mejor = score  # min value

    return mejor


def limpiar():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def hacer(estado, c_choice, h_choice):

    caracteres = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in estado:
        for celda in row:
            symbol = caracteres[celda]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def turno_de_la_ia(c_choice, h_choice):
    profundidad = len(celdas_vacias(matrix))
    if profundidad == 0 or juego_terminado(matrix):
        return

    limpiar()
    print(f'Es turno de la computadora [{c_choice}]')
    hacer(matrix, c_choice, h_choice)

    if profundidad == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(matrix, profundidad, COMPUTADORA)
        x, y = move[0], move[1]

    mandar_movimiento(x, y, COMPUTADORA)
    time.sleep(1)


def turno_del_jugador(c_choice, h_choice):
    profundidad = len(celdas_vacias(matrix))
    if profundidad == 0 or juego_terminado(matrix):
        return

    # Dictionary of valid moves
    moverse = -1
    movimientos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpiar()
    print(f'Es tu turno [{h_choice}]')
    hacer(matrix, c_choice, h_choice)

    while moverse < 1 or moverse > 9:
        try:
            moverse = int(input('Usa el teclado numerico (1..9): '))
            coordenadas = movimientos[moverse]
            puedes_moverte = mandar_movimiento(coordenadas[0], coordenadas[1], HUMANO)

            if not puedes_moverte:
                print('Bad move')
                moverse = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    limpiar()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    primero_en_moverse = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Puedes escoger X or O\nElegida: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Hasta Luego')
            exit()
        except (KeyError, ValueError):
            print('Mala Eleccion')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    limpiar()
    while primero_en_moverse != 'Y' and primero_en_moverse != 'N':
        try:
            primero_en_moverse = input('¿Quieres ser el primero en comenzar?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Hasta Luego')
            exit()
        except (KeyError, ValueError):
            print('Mala Eleccion')

    # Main loop of this game
    while len(celdas_vacias(matrix)) > 0 and not juego_terminado(matrix):
        if primero_en_moverse == 'N':
            turno_de_la_ia(c_choice, h_choice)
            primero_en_moverse = ''

        turno_del_jugador(c_choice, h_choice)
        turno_de_la_ia(c_choice, h_choice)

    # Game over message
    if victoria(matrix, HUMANO):
        limpiar()
        print(f'{USER} Es tu turno [{h_choice}]')
        hacer(matrix, c_choice, h_choice)
        print(f'{USER} Felicidades, Ganaste!')
    elif victoria(matrix, COMPUTADORA):
        limpiar()
        print(f'Es turno de la computadora [{c_choice}]')
        hacer(matrix, c_choice, h_choice)
        print(f'Te gane {USER} :>!')
    else:
        limpiar()
        hacer(matrix, c_choice, h_choice)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()
