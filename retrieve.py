#!/usr/bin/python

# codigo editado de https://stackoverflow.com/questions/26082360/python-searching-csv-and-return-entire-row
# en C, aquí hay un tutorial https://www.geeksforgeeks.org/relational-database-from-csv-files-in-c/ 

import csv
import sys

# Nombre en mayúsculas a quien se desea buscar (se pasa desde la shell)
name = input('¿Qué nombre desea buscar?\n')

#read csv, and split on "," the line
csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")


#loop through the csv list
for row in csv_file:
    #print(row[0])
    # Si el elemento existe, se imprime lo siguiente
    if name == row[0]:
        print('Existe el elemento')
        
    
print(".")