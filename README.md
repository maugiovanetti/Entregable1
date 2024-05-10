## Punto 1: Intersección de Gráficos

### Descripción del Problema
Se nos pide encontrar los puntos de intersección de las funciones:
- \( f(x) = (x-3)^2 \)
- \( g(x) = 32(x-3)^{-3} \)

### Solución Analítica
Para encontrar los puntos de intersección analíticamente, igualamos las dos funciones:

\[ (x-3)^2 = \frac{32}{(x-3)^3} \]

Multiplicamos ambos lados por \((x-3)^3\) para eliminar el denominador, obteniendo una ecuación polinómica que podemos resolver para \( x \). Debemos considerar las restricciones, como evitar dividir por cero en \( x=3 \).

### Representación Gráfica
Utilizamos Python para graficar ambas funciones y observar visualmente sus intersecciones. El gráfico nos ayuda a confirmar las soluciones obtenidas y entender mejor el comportamiento de las funciones cerca de sus puntos críticos.

### Código en Python
```python
# Código Python para graficar las funciones
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return (x - 3)**2

def g(x):
    return 32 / (x - 3)**3

x_values = np.linspace(2.9, 3.1, 400)
f_values = f(x_values)
g_values = g(x_values)

plt.plot(x_values, f_values, label='f(x)')
plt.plot(x_values, g_values, label='g(x)')
plt.legend()
plt.show()
