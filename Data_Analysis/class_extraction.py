import json

def extractProperty(filename, searchtype):
    # Opening JSON file
    f = open(filename)

    # returns JSON object as a dictionary
    data = json.load(f)
    properties = []
    for datum in data:
        for entity in datum["entities"]:
            if entity["type"].split("/")[0] == searchtype:
                start = entity["start"]
                end = entity["end"]
                if end == len(datum["tokens"]):
                    properties.append(" ".join(datum["tokens"][start:]))
                else:
                    properties.append(" ".join(datum["tokens"][start:end]))

    f.close()
    # properties = set((properties))
    return properties

def extractRelation(filename):
    
    f = open(filename)

    # returns JSON object as a dictionary
    data = json.load(f)
    relations = []
    for datum in data:
        for relation in datum["relations"]:
            if relation["type"].split("/")[0] in ["hasParticipant", "hasPatient", "hasAgent"] :
                entitiesIndex = [relation["head"], relation["tail"]]
                relationString = ""
                for i in entitiesIndex:
                    start = datum['entities'][i]["start"]
                    end = datum['entities'][i]["end"]
                    if end == len(datum["tokens"]):
                        relationString += "|" + " ".join(datum["tokens"][start:])
                    else:
                        relationString += "|" + " ".join(datum["tokens"][start:end])
                relations.append(relationString)
    # print(relations)
    print(filename)
    print("Total hasParticipant relations: " + str(len(relations)))
    print("Unique hasParticipant relations: " + str(len(set(relations))))
    f.close()

if __name__ == "__main__":
    searchType = input("Enter the class of data you want to extract in Maintie gold & silver, or 'hasParticipant' to return number of relations (Activity/ Process/ Property/ PhysicalObject/ State/ hasParticipant): ")
    if (searchType == "hasParticipant"):
        extractRelation("../data/gold_release.json")
        extractRelation("../data/silver_release.json")
    else:
        gold_text = extractProperty("../data/gold_release.json", searchType)
        silver_text = extractProperty("../data/silver_release.json", searchType)

        print()
        print("Gold",searchType,": ===========================")
        for i in set((gold_text)):
            print(i)
        print()
        print("Silver",searchType,": ===========================")
        for i in silver_text:
            print(i)

        print("Total Gold Entities: " + str(len(gold_text)))
        print("Total Unique Gold Entities: " + str(len(set((gold_text)))))
        print( "Total Silver Entities: " + str(len(silver_text)))
        print( "Total Unique Silver Entities: " + str(len(set((silver_text)))))