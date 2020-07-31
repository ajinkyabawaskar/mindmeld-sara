import json, random

with open('tourist_attractions.json', 'r') as attractions:
    attractions = json.load(attractions)

id = 1
summary = {}
summary['entry']= {}
summary['entry']['id']= {}
summary['entry']['name']= {}
summary['entry']['city']= {}
summary['entry']['url']= {}

def write(ok):
    with open('toursut.json', 'r+') as outFile:
        data = json.load(outFile)
        data.append(ok)
        outFile.seek(0)
        json.dump(data, outFile)

for attraction in attractions:
    summary['entry']['id']= str(id)
    summary['entry']['name'] = attraction['name']
    summary['entry']['city'] = attraction['city']
    summary['entry']['url'] = attraction['url']

    write(summary['entry'])
    print(str(id)+ " -- added to json")
    id= id + 1