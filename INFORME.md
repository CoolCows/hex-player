# Jugador de Hex

_Rodrigo Pino_
_Adrian Portales_
_C512_

Jugador de Hex utilizando Minimax con Alpha-Beta Prunning

## Implementación

_Heurística implementada en coolcow_player.py_

_Alpha-Beta Prunning implementado en coolcow_minimax.py_

### Juego

El juego consiste en un tablero de NxN donde cada celda tiene forma hexagonal. En cada casilla puede haber una pieza blanca representada por `W`, una pieza negra `B` o la casilla vacía representada por  `.` .

Para explorar los posibles estados del juego se tiene un DAG donde cada _nodo_ representa uno de esos posible estado del juego y la raíz es el estado actual en el que se encuentra el juego (el tablero está vacío al comienzo del juego). 

Las _aristas_ que unen a otros nodos (y por ende a nuevos estados de juego) son transiciones válidas entre posibles estados del juego. Una transición válida consiste cuando el jugador correspondiente pone una ficha de su color en una casilla vacía, generando un nuevo estado del juego. Como los estados del juego son únicos y no se pueden levantar piezas del tablero entonces las aristas son dirigidas.

Un _camino_ es una secuencia de nodos del árbol enlazados por aristas cuyo último nodo corresponde con un estado terminal del juego para alguno de los dos jugadores. Se puede ver también como una secuencia de estados del juego hasta que ocurre un ganador, donde solo ocurren transiciones válidas.

Una _jugada_ es el acto de cambiar de un estado del juego actual a otro válido. Correspondería a moverse desde el nodo raíz del árbol a algún nodo directamente descendiente de este.

Un _jugador_ verifica los posibles estados del juego y realiza una _jugada_.

### Heurística

Como heurística se analiza en cada jugada el camino más corto necesario para que un jugador gane, donde un camino es la cantidad de piezas necesarias a poner para unir los bordes correspondientes del tablero.

El camino tiene costo _c_ donde _c_ representa la cantidad de piezas que faltan por posicionar.

Desde el punto de vista del jugador blanco, la calidad del tablero queda determinada por la resta entre la cantidad mínima de fichas necesarias por el jugador negro y el jugador blanco para obtener la victoria respectivamente. Sería: _blackMinPath - whiteMinPath_. Es análogo para el jugador negro: _whiteMinPath - blackMinPath_.

Para calcular le camino más corto se crea un nodo ficticio enlazado con todas las casillas de cada fronteras del tablero (izquierda y derecha para el jugador blanco; superior e inferior para el jugador negro). No se enlazan con el nodo ficticio las casillas de la frontera ocupadas por una pieza de color opuesto.

Después, se busca el camino de costo mínimo entre los nodos ficticios que unen fronteras del tablero opuestas (fronteras que dependen del jugador en cuestión) utilizando `UCS`:

* Caminar a una celda donde haya una casilla ocupada por una ficha del mismo color que el jugador tiene costo 0 
* Costo 1 cuando esta vacía. 
* No se puede caminar por casillas ocupadas por el jugador opuesto.

### Alpha-Beta Prunning

Se modifica la lógica de minimax adicionando _fail-hard_ _Alpha-Beta Prunning_.

_Fail-hard_ obliga al valor de retorno de la función a estar acotado por $\alpha$ y $\beta$.

#### Modificación

En _coolcow_minimax.py_ se añaden a las funciones _maxplay_ y _minplay_ los parámetros $\alpha$ y $\beta$, iniciados en $-\infin$ y $\infin$ respectivamente.

En _maxplay_ después de minimizar una rama del nodo actual, si se encuentra una tal que el valor es mayor que $\beta$ se deja de analizar.

En _minplay_ después de maximizar una rama del nodo actual, si se encuentra una tal que su valor es menor que el $\alpha$ actual, se deja de analizar.

#### Observaciones

Después de aplicar _Alpha-Beta Prunning_ se encontró un aumento importante en el performance del jugador _coolcow_minimax_ pues disminuyó enormemente el tiempo de análisis de jugadas sin perderse calidad.
