import json

def storeData(filename):
    f = open(filename, "r")
    data = json.load(f)
    PhysicalObjectValid = {} # dictionary or term as key and PhysicalObject subclasses as value

    for datum in data:
        for entity in datum["entities"]:
            if entity["type"].split("/")[0] == "PhysicalObject":
                start = entity["start"]
                end = entity["end"]
                if end == len(datum["tokens"]):
                    text = " ".join(datum["tokens"][start:])
                else:
                    text = " ".join(datum["tokens"][start:end])

                # add to dictionary
                if text not in PhysicalObjectValid.keys():
                    if len(entity["type"].split("/")) > 1: 
                        type = "/".join(entity["type"].split("/")[0:2])
                        PhysicalObjectValid[text] = [type]
                    else:
                        PhysicalObjectValid[text] = [entity["type"]]
                elif entity["type"] not in PhysicalObjectValid[text]:
                    if len(entity["type"].split("/")) > 1: 
                        type = "/".join(entity["type"].split("/")[0:2])
                        PhysicalObjectValid[text].append(type)
                    PhysicalObjectValid[text].append(entity["type"])
    f.close()
    return PhysicalObjectValid


def check_predictions(gold_entities, filename):
    f = open(filename, "r")
    data = json.load(f)
    unseen_text = 0
    unseen_subclass = 0
    seen_text = 0

    for datum in data:
        for entity in datum["entities"]:
            if entity["type"].split("/")[0] == "PhysicalObject":
                start = entity["start"]
                end = entity["end"]
                if end == len(datum["tokens"]):
                    text = " ".join(datum["tokens"][start:])
                else:
                    text = " ".join(datum["tokens"][start:end])

                if text not in gold_entities.keys():
                    unseen_text += 1
                elif entity["type"] not in gold_entities[text]:
                    unseen_subclass += 1
                else:
                    seen_text += 1

    print("Unseen text: ", unseen_text)   
    print("seen text, unseen subclass: ", unseen_subclass)
    print("Seen text, seen subclass: ", seen_text) 


if __name__ == "__main__":
    gold_entities = storeData("../data/gold_release.json")
    check_predictions(gold_entities, "data/predictions_2.json")