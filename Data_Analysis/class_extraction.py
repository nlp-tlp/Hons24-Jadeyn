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
    properties = set((properties))
    return properties

if __name__ == "__main__":
    searchType = input("Enter the class of data you want to extract in Maintie gold & silver (Process/ Property/ PhysicalObject/ State): ")
    searchType = searchType.lower().strip().capitalize()
    gold_text = extractProperty("../data/gold_release.json", searchType)
    silver_text = extractProperty("../data/silver_release.json", searchType)

    print()
    print("Gold",searchType,": ")
    for i in gold_text:
        print(i)
    print()
    print("Silver",searchType,": ")
    for i in silver_text:
        print(i)
