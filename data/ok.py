import json, random

with open('hotels.json', 'r') as hotels:
    all_hotels = json.load(hotels)

with open('gazetteer.txt', 'r') as locations:
    all_location = locations.read()
    all_locations = all_location.split("\n")

def write(ok):
    with open('locations.json', 'r+') as outFile:
        data = json.load(outFile)
        data.append(ok)
        outFile.seek(0)
        json.dump(data, outFile)
id = 1
summary = {}
summary['entry']= {}
summary['entry']['id']= {}
summary['entry']['location']= {}
summary['entry']['hotels']= []


for location in all_locations:
    summary['entry']['id']= str(id)
    summary['entry']['location'] = location
    summary['entry']['hotels'] = []
    for hotel in all_hotels:
        if(hotel['address']['city']==location):
            # print("OK")
        # if(location in hotel['address']['label']):

            summary['entry']['hotels'].append(hotel['title'])
            print("Adding "+ hotel['title']+ " to "+location)
    write(summary['entry'])
    print(str(id)+ "-- added to json")
    id= id + 1