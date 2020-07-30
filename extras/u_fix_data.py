# with open('/home/ajinkya/my_mm_workspace/sara/data/location/gazetteer.txt', 'r+') as cities:
#     all_cities = cities.read().split("\n")


# import random
with open('D:/mindmeld-sara/data/airports.json' , 'r', encoding="utf-8") as training:
    with open('airports.json', 'w') as update:
        queries = training.read().split("\n")
        for query in queries:
            if(("iata" in query) or ("ident" in query) or ("elevation_ft" in query) or ("scheduled_service" in query) or ("gps_code" in query)or ("iata_code" in query) or ("local_code" in query) or("home_link" in query) or("wikipedia_link" in query)) :
                pass
            else:
                update.write(query + "\n")