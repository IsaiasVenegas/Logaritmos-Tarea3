import csv
import time
import sys
import numpy as np
from retrieveName import retrieve
from bloom_filter import generate_coefficients, insert, search
from bitarray import bitarray

def main():
    # Lectura de datos
    baby_names = [] # Lista de nombres
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    for row in csv_file:
        if(row[0] == 'Name'):
            continue
        baby_names.append(row[0])
    N = len(baby_names) # Cantidad de nombres
    print("=================================")
    print("Cantidad de nombres insertados N:", N)
    print("Nombres por buscar:", 3000)
    print("Nombres no existentes:", 1000)
    print("=================================")
    film_names = [] # Lista de nombres no existentes
    csv_file = csv.reader(open('Film-Names.csv', "r"), delimiter=",")
    for row in csv_file:
        if(row[0] == '0'):
            continue
        film_names.append(row[0])

    # Genera un arreglo de busqueda con 2000 nombres existentes y 1000 no existentes
    existing_names = np.random.choice(baby_names, 2000, replace=False)
    non_existing_names = np.random.choice(film_names, 1000, replace=False)
    X = np.concatenate((existing_names, non_existing_names), axis=None)

    # Encontramos la palabra mas larga
    # entre los elementos a insertar y los posibles a buscar
    # Esto lo necesitaremos para que cada funcion de hashing
    # pueda tener a_i suficientes para cada palabra
    max_length_word = 0
    for i in range(len(baby_names)):
        name = baby_names[i]
        if(len(name) > max_length_word):
            max_length_word = len(name)
    for i in range(len(non_existing_names)):
        name = non_existing_names[i]
        if(len(name) > max_length_word):
            max_length_word = len(name)

    # Pruebas con busqueda iterativa
    # Buscamos los nombres del arreglo X
    avg = 0.0
    for i in range(5):
        start_time_1 = time.time()
        for x in X:
            retrieve(x)
        end_time_1 = time.time()
        elapsed_time = (end_time_1 - start_time_1)*1000
        avg += elapsed_time
        print("Sin filtro | Tiempo (ms): {:}".format(elapsed_time).replace('.',','))
    print("---------------------------------")
    print("Sin filtro | Tiempo promedio (ms): {:}".format(avg/5).replace('.',','))
    print("---------------------------------")

    # Pruebas con Bloom
    test_M = [i for i in range(8, 31)] # exponentes de 2
    test_K = [i for i in range(1,11)] # creamos k funciones de hashing

    for exp_m in test_M:
        # Creamos un numero binario de m bits en 0
        m = 1 << exp_m # Largo del arreglo M
        M = bitarray(m)  # Arreglo de bits
        M.setall(0) # Inicializamos el arreglo en 0
        # Calculamos el uso de memoria    
        memory_usage = sys.getsizeof(M)
        memory_in_bits = memory_usage*8
        print("M:", m,"Memoria requerida:", memory_usage, "bytes")
        print("Relacion M/bits: {}".format(m/memory_in_bits).replace('.',','))
        print("Relacion bits/M: {}".format(memory_in_bits/m).replace('.',','))
        print("=================================")
        for k in test_K:
            # Generamos las k funciones de hashing
            H = generate_coefficients(k, max_length_word)
            # Insertamos los nombres de bebe en el arreglo M
            for i in range(len(baby_names)):
                name = baby_names[i]
                M = insert(name,H,m,M) # Aplicamos las funciones de hashing a cada nombre
            # Buscamos los nombres del arreglo X
            positives = 0
            negatives = 0
            falses_positives = 0
            start_time_2 = time.time()
            for i in range(len(X)):
                x = X[i]
                rc = search(x,H,m,M)
                if(rc and i>=2000):
                    falses_positives += 1
                elif(rc):
                    positives += 1
                else:
                    negatives += 1
            end_time_2 = time.time()
            print(
                "Bloom (exp_m: {}, K: {}) | Tiempo (ms): {} | Falsos positivos: {}".format(exp_m, 
                                                                                           k, 
                                                                                           (end_time_2 - start_time_2)*1000, 
                                                                                           falses_positives
                                                                                           ).replace('.',','))
            print("---------------------------------")
            M.setall(0) # Inicializamos el arreglo en 0
        
if __name__ == "__main__":     
    main()
    