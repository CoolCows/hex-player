# Jugador de Hex

_Rodrigo Pino_
_Adrian Portales_
_C512_

Jugador de Hex utilizando Minimax

## Implementación

### Juego

El juego consiste en un tablero de NxN donde cada celda tiene forma hexagonal. En cada casilla puede haber una pieza blanca representada por `W`, una pieza negra `B` o la casilla vacía representada por  `.` .

Para explorar los posibles estados del juego se tiene un árbol donde cada _nodo_ representa uno de esos posible estado del juego y la raíz es el estado actual en el que se encuentra el juego (el tablero está vacío al comienzo del juego)

Las _aristas_ que llevan a a otros nodos (y por ende a nuevos estados de juego) representan jugadas válidas.

Un _camino_ es una secuencia de nodos del árbol enlazados por aristas cuyo último nodo corresponde con un estado terminal del juego para alguno de los dos jugadores.

Una _jugada_ es el acto de cambiar de un estado del juego actual a otro válido. Correspondería a moverse desde el nodo raíz del árbol a algún nodo hijo.

Un _jugador_ verifica los posibles estados del juego y realiza una _jugada_.

### Heurística

Como heurística se analiza en cada jugada el camino más corto necesario para que un jugador gane, donde un camino es la cantidad de piezas necesarias a poner para unir los bordes correspondientes del tablero.

El camino tiene costo _c_ donde _c_ representa la cantidad de piezas que faltan por posicionar.

Desde el punto de vista del jugador blanco, la calidad del tablero queda determinada por la resta entre la cantidad mínima de fichas necesarias por el jugador negro y el jugador blanco para obtener la victoria respectivamente. 

Para calcular le camino más corto se crea un nodo ficticio para las fronteras opuestas del tablero (izquierda y derecha para el jugador blanco; superior e inferior para el jugador negro) y se busca el camino de costo mínimo utilizando `UCS`:

* Caminar a una celda donde haya una casilla ocupada por una ficha del mismo color que el jugador tiene costo 0 
* Costo 1 cuando esta vacía. 
* No se puede caminar por casillas ocupadas por el jugador opuesto.
