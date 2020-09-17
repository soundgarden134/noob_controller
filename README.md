# noob_controller
Controlador para juego de Knight Chess

### Algoritmo

Para resolver el problema se utiliza minimax. El algoritmo funciona de la siguiente manera:
1. Se obtienen todas las jugadas posibles dado un estado
2. Por cada jugada posible, se utiliza la función best_available_movement, que encuentra la jugada mejor evaluada, ya sea para el jugador o para el rival, un total de n-1 veces, donde n es la profundidad del minimax (por defecto, n es 4).
3. Una vez llega al final de esta búsqueda, compara el puntaje final con el mejor puntaje actual, y si es un mejor puntaje, se almacena como la mejor jugada y se reemplaza el mejor puntaje. En caso de que el puntaje sea igual, se crea una lista con las jugadas de igual puntaje. En caso de ser un puntaje menor, se ignora.
4. Posteriormente, hace lo mismo para todos las otras jugadas posibles y se queda con la mejor.

### Cómo se evalúan los estados
El factor principal es la diferencia entre la cantidad de piezas de cada jugador. Un segundo factor que influye es la posición en la que están las piezas, favoreciendo los estados con caballos posicionados en el centro del tablero y penalizando a los estados con caballos en los bordes, o peor aun, en las esquinas. Este segundo factor es mucho menos importante que la cantidad de piezas, pero ayuda a decidir entre menos jugadas y favorece la abertura del tablero, moviendo los caballos de sus posiciones iniciales, ya que evaluando solo la diferencia de piezas, el algoritmo elegía muy seguido mover un número reducido de piezas que ya se encuentran en posición avanzada.

Para la evaluación de posición se utilizó el [siguiente mapa](https://www.chessprogramming.org/Simplified_Evaluation_Function#Knights):
         
-50,-40,-30,-30,-30,-30,-40,-50,

-40,-20,  0,  0,  0,  0,-20,-40,

-30,  0, 10, 15, 15, 10,  0,-30,

-30,  5, 15, 20, 20, 15,  5,-30,

-30,  0, 15, 20, 20, 15,  0,-30,

-30,  5, 10, 15, 15, 10,  5,-30,

-40,-20,  0,  5,  5,  0,-20,-40,

-50,-40,-30,-30,-30,-30,-40,-50

El puntaje se calcula con la fórmula score = my_knights - enemy_knights + puntaje_posicion_knights + puntaje_posicion_knights_enemigos

Para ejecutar este controlador, se necesita el juego de [Knight Chess de Baxonn2](https://github.com/Baxonn2/Knight-Chess). El controlador se inserta en la carpeta de Knight Chess y dentro de la carpeta se utiliza el comando 'python main.py "python noob_controller.py" "otro_controlador (opcional)" -g. 
