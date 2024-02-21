oponente, jugador = 'o', 'x'

def imprimir_tablero(tablero):
    for i, fila in enumerate(tablero):
        print(" | ".join(map(str, fila)))
        if i < 2:
            print("-" * 10)

def quedanMovimientos(tablero):
    return any(cell.isdigit() for row in tablero for cell in row)

def evaluar(b):
    # Comprobando filas, columnas y diagonales para victoria de X u O.
    lineas = [b[i] for i in range(3)] + \
             [[b[j][i] for j in range(3)] for i in range(3)] + \
             [[b[i][i] for i in range(3)], [b[i][2 - i] for i in range(3)]]

    for linea in lineas:
        if all(cell ==oponente for cell in linea):
            return 10
        elif all(cell == jugador for cell in linea):
            return -10

    # Si ninguno ha ganado, devuelve 0
    return 0


# Esta es la función minimax. Considera todas
# las posibles formas en que el juego puede ir y devuelve
# el valor del tablero.
def minimax(tablero, esMax):
    puntaje = evaluar(tablero)
    if puntaje != 0 or not quedanMovimientos(tablero):
        return puntaje

    mejor_puntaje = float('-inf') if esMax else float('inf')

    for i in range(3):
        for j in range(3):
            if tablero[i][j].isdigit():
                tablero[i][j] =oponente if esMax else jugador
                puntaje = minimax(tablero, not esMax)
                tablero[i][j] = str(i * 3 + j + 1)

                if (esMax and puntaje > mejor_puntaje) or (not esMax and puntaje < mejor_puntaje):
                    mejor_puntaje = puntaje

    return mejor_puntaje

def encontrarMejorMovimiento(tablero):
    mejorValor = float('-inf')
    mejorMovimiento = (-1, -1)

    for i in range(3):
        for j in range(3):
            if tablero[i][j].isdigit():
                tablero[i][j] =oponente 
                valorMovimiento = minimax(tablero, False)
                tablero[i][j] = str(i * 3 + j + 1)

                if valorMovimiento > mejorValor:
                    mejorMovimiento = (i, j)
                    mejorValor = valorMovimiento

    #print("Mejor valor del movimiento:", mejorValor)
    print()
    return mejorMovimiento

def pedirMovimiento(tablero):
    while True:
        try:
            movimiento = int(input("Ingresa el número de la celda (1-9): "))
            if 1 <= movimiento <= 9:
                fila, columna = (movimiento - 1) // 3, (movimiento - 1) % 3
                if tablero[fila][columna].isdigit():
                    return fila, columna
                else:
                    print("La celda está ocupada. Elige otra.")
            else:
                print("Número fuera de rango. Ingresa un número del 1 al 9.")
        except ValueError:
            print("Ingresa un número válido.")

def inicializar_tablero():
    return [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]
            



def jugar(tablero):
    i = 0
    
    while quedanMovimientos(tablero) and evaluar(tablero) == 0:
        print(f" \nJugada: {i + 1}")
        
        # Jugador humano
        imprimir_tablero(tablero)
        fila, columna = pedirMovimiento(tablero)
        tablero[fila][columna] = jugador
        print("\nTu jugada:")
        imprimir_tablero(tablero)

        # Jugador de la IA
        mejorMovimiento = encontrarMejorMovimiento(tablero)
        fila, columna = mejorMovimiento
        tablero[fila][columna] = oponente
        print("Jugada de IA:\n")
        imprimir_tablero(tablero)

        i += 1

    print("Resultados: \n")
    imprimir_tablero(tablero)
    resultado = evaluar(tablero)

    if resultado == 10:
        print("La IA ha ganado")
    elif resultado == -10:
        print("¡Has ganado!")
    else:
        print("Es un empate.")

    jugar_otra_partida = input("¿Quieres jugar otra partida? (s/n): ")
    if jugar_otra_partida.lower() == 's':
        nuevo_tablero = inicializar_tablero()  # Asegúrate de tener una función para reiniciar el tablero
        jugar(nuevo_tablero)
    else:
        print("¡Gracias por jugar!")
        
jugar(inicializar_tablero())
