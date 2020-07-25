with open('/home/ajinkya/my_mm_workspace/sara/entities/location/gazetteer.txt', 'r+') as cities:
    all_cities = cities.read().split("\n")


import random
with open('/home/ajinkya/my_mm_workspace/sara/domains/get_info/get_location_info/train.txt' , 'r') as training:
    with open('train2.txt', 'w') as update:
        queries = training.read().split("\n")
        for query in queries:
            if(("Transporatation" in query) or ("Climatic conditions" in query)) :
                pass
            else:
                update.write(query + "\n")