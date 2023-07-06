import csv

def retrieve(name):
    #read csv, and split on "," the line
    csv_file = csv.reader(open('Popular-Baby-Names-Final.csv', "r"), delimiter=",")
    #loop through the csv list
    for row in csv_file:
        #print(row[0])
        # Si el elemento existe, se devuelve True
        if name == row[0]:
            return True
    return False