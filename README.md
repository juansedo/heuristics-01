## Explicación del formato de los archivos de entrada

La primera fila indica el número de nodos de demanda (sin incluir el depósito) $n$, el número de vehículos $R$, la capacidad de cada vehículo $Q$ y la máxima distancia que puede recorrer cada vehículo $T_H$.

Las siguientes $n + 1$ filas indican, para cada nodo (incluyendo el depósito), el índice del nodo correspondiente, las coordenadas ($x$, $y$) y la demanda. La demanda del depósito se asume igual a cero para cada instancia del problema.

La distancia entre cada par de nodos se calcula utilizando la distancia euclídea.

A continuación se presenta un ejemplo con $n$ = 5:

| | | | |
|-:|-:|-:|-:|
|5|2|8|35|
|0|0|0|0|
|1|1|8|3|
|2|5|7|6|
|3|2|10|2|
|4|3|4|7|
|5|10|2|1|