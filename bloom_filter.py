import numpy as np
import random
from bitarray import bitarray

P = 2**31 - 1 # Mersenne primo M31 (el mas grande que cabe en 32 bits)

# Crea k funciones de hashing universales del tipo sum(ai xi)+b
# Cada x a buscar necesita len(x) coeficientes a_i y un coeficiente b
# Por lo que creamos suficientes a_i segun el largo maximo de los elementos de X
def generate_coefficients(k, max_length_word):
    H = []
    for i in range(k):
        A = []
        for _ in range(max_length_word):
            a_i = random.randint(1, P-1)
            A.append(a_i)
        b = random.randint(0, P-1)
        H.append((A,b))
    return H

# Retorna un arreglo de bits con todas las posiciones j=h(x) por modificar en M
def calculate_hashing(x,H,m):
    # Recibe un elemento x y los coeficientes de las funciones de hashing H
    Y = bitarray(m) # Arreglo de bits
    Y.setall(0) # Inicializamos el arreglo en 0
    for h in H:
        sum = 0
        A = h[0]
        b = h[1]
        for i in range(len(x)):
            sum += A[i]*ord(x[i]) # caracter a ASCII multiplicado por a_i
        j = ((sum + b) % P) % m # Funcion de hashing ax+b mod p mod m
        Y[j-1] = 1  # Se modifica el bit j-1
    return Y

# Actualiza M para un elemento x
def insert(x,H,m,M):
    # Calculamos los h(x) y los guardamos en Y
    Y = calculate_hashing(x,H,m)
    # Actualizamos M
    oldM = M.copy()
    newM = oldM | Y
    return newM

# Ocupa el filtro de Bloom para buscar el elemento x en M 
# Retorna True si la tabla tiene 1 en las posiciones de h(x)
# False en otro caso
def search(x,H,m,M):
    # Calculamos los h(x) y los guardamos en Y
    Y = calculate_hashing(x,H,m)
    return (M & Y) == Y # Si M & Y == Y entonces x esta en M (puede ser falso positivo)