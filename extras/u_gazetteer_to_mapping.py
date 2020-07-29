"""
    This is a utility file used to generate mapping.json from gazetteer.txt
    To avoid messing with input file location, just paste this file to the entity folder
    and execute it from there.
    NOTE - Requires a mapping.json file with `[]` as its contents before executing this file 
    [only for Windows]
"""
import json

with open('/home/ajinkya/my_mm_workspace/sara/entities/preference/gazetteer.txt', 'r+', encoding="utf8") as file1:
    all_cities = file1.read()
    # file1.close()

all_cities_set = all_cities.split("\n")
id = 1
summary = {}
summary['entry'] = {}
summary['entry']['id'] = {}
summary['entry']['cname'] = {}
summary['entry']['whitelist'] = []
def write(OK):
    with open("/home/ajinkya/my_mm_workspace/sara/entities/preference/mapping.json", "r+") as file:
        data = json.load(file)
        data.append(OK)
        file.seek(0)
        json.dump(data, file)
    # file.close()

for cname in all_cities_set:
    summary['entry']['id'] = str(id)
    summary['entry']['cname'] = cname
    summary['entry']['whitelist'] = [cname]
    write(summary['entry'])
    id = id + 1

print("DONE")