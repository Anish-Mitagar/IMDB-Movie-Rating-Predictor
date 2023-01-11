import ast
import csv
import pandas as pd

f = open("data_files/dataset.txt", "r")
dictionaries = f.readlines()

for i in range(len(dictionaries)):
    dictionaries[i] = (dictionaries[i]).strip()

def data():
    
    for j in range(len(dictionaries)):
        try: 
            if len(dictionaries[j]) != 0:
                elements = ast.literal_eval((dictionaries[j]))

                mr  = elements["movie rating"]
                pmr = elements["percent male reviewers"]
                pfr = elements["percent female reviewers"]
                put = elements["percent under 30 reviewers"]
                ptf = elements["percent 30-45 reviewers"]
                pof = elements["percent over 45 reviewers"]
                cao = elements["cumulative actor oscars"]
                caw = elements["cumulative actor wins"]
                can = elements["cumulative actor nominations"]

            x_val = [pmr,put,ptf,pof,cao,caw,can]
            y_val_continuous = [float(mr)]

            if y_val_continuous[0] >= 8.0:
                y_val_classification = [1, 0, 0, 0, 0]
            elif y_val_continuous[0] >= 7.0:
                y_val_classification = [0, 1, 0, 0, 0]
            elif y_val_continuous[0] >= 6.0:
                y_val_classification = [0, 0, 1, 0, 0]
            elif y_val_continuous[0] >= 3.0:
                y_val_classification = [0, 0, 0, 1, 0]
            else:
                y_val_classification = [0, 0, 0, 0, 1]

            with open('csv_files/test_x.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(x_val)

            f.close()

            with open('csv_files/test_y_continuous.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(y_val_continuous)

            f.close()

            with open('csv_files/test_y_classification_2.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow([y_val_classification])

            f.close()

        except Exception as e:
            print(e)
            print("Failed at row " + str(j))

data()
