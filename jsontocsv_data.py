#converting the extracted json to csv
import json

import csv

def json_to_csv():
    with open('data.json') as json_file:
        data=json.load(json_file)
    #open a file for writing

    employ_data = open('C:/Users/LLENOVO/Desktop/project/myanalysis/reviews_Data.csv', 'w')

    #create the csv writer object

    csvwriter = csv.writer(employ_data)

    count = 0
    for d in data:
        m=d['reviews']
        for emp in m:
            if count == 0:
                header = emp.keys()
                csvwriter.writerow(header)
                count=count+1
            csvwriter.writerow(emp.values())
    employ_data.close()
    print("finshed converting")
    return True


    



