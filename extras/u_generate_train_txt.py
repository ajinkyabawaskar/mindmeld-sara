import json, random

with open('train2.txt', 'r') as inFile:
    all_queries = inFile.read()
    all_queries = all_queries.split("\n")

with open('location.txt', 'r') as inFile1:
    all_cities = inFile1.read()
    all_cities = all_cities.split("\n")

with open('poi.txt', 'r') as inFile2:
    all_poi = inFile2.read()
    all_poi = all_poi.split("\n")

with open('train.txt', 'r+') as outFile:  
    for i in range (250):
        query = random.choice(all_queries)
        location = random.choice(all_cities)
        poi = random.choice(all_poi)
        query = query.replace("__poi__", "{"+poi+"|"+"point_of_interest}")
        query = query.replace("__location__", "{"+location+"|"+"location}")
        outFile.write(query+"\n")