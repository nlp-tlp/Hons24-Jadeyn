import json
import contractions

def pad_sequence(dataset):
    max_len = len(max(dataset, key=len))
    for i in range(len(dataset)):
        dataset[i] = dataset[i] + ["PAD"] * (max_len - len(dataset[i]))
    return dataset

def add_inherent_functions(row):
    for e in row["entities"]:
        tokens = row["tokens"]
        entity_type = e["type"].split("/")
        if entity_type[0] == "PhysicalObject":
            if len(entity_type) > 1 and entity_type[1] not in ["Substance", "Organism"]:
                tokens.append(entity_type[1])
    return tokens

    # BROKEN CODE
    # physical_object_indices = []
    # 
    # for e in row["entities"]:
    #     new_list = row["tokens"]
    #     entity_type = e["type"].split("/")
    #     if entity_type[0] == "PhysicalObject":
    #         if len(entity_type) > 1 and entity_type[1] not in ["Substance", "Organism"]:
    #             new_string = " ".join(new_list)
    #             if e["end"] == len(row["tokens"]):
    #                 replace_index = new_string.find(" ".join(row["tokens"][e["start"]:]))
    #                 new_string = new_string.replace(" ".join(row["tokens"][e["start"]:]))
    #             else:
    #                 replace_index = new_string.find(" ".join(row["tokens"][e["start"]:e["end"]]))
    #                 new_string = new_string.replace(" ".join(row["tokens"][e["start"]:e["end"]]), "")
    #             new_string = new_string[replace_index:]
    #             new_list = new_string.split()
    #             physical_object_indices.append((e["start"], e["end"], entity_type[1]))
    # for i in physical_object_indices:
    #     if i[1] == len(row["tokens"]):
    #         row["tokens"].append(i[2])
        

def clean_tokens(tokens):
    stopwords =["<num>", "<id>", "-"]
    tokens = [i for i in tokens if i not in stopwords]
    tokens = contractions.fix(" ".join(tokens)).split()
    return tokens

def prepare_dataset(filename):
    f = open(filename, "r")
    # returns JSON object as a dictionary
    data = json.load(f)

    dataset = []

    for datum in data:
        keep_indices = []
        for entity in datum["entities"]:
            if entity["type"].split("/")[0] not in ["PhysicalObject", "Activity"]:
                start = entity["start"]
                end = entity["end"]
                for i in range(start, end):
                    keep_indices.append(i)

        tokens = []
        for i in sorted(set(keep_indices)):
            tokens.append(datum["tokens"][i])
        
        tokens = clean_tokens(tokens)
        if tokens:
            dataset.append(" ".join(tokens))
    # dataset = pad_sequence(dataset)
    return dataset

def full_dataset(filename):
    f = open(filename, "r")
    # returns JSON object as a dictionary
    data = json.load(f)

    d = []

    for datum in data:
        types = [e["type"].split("/")[0] for e in datum["entities"]]
        if "State" in types or "Process" in types or "Property" in types:
            tokens = clean_tokens(datum["tokens"])
            d.append(" ".join(tokens))
    # d = pad_sequence(dataset)
    return d

def full_dataset_append_inherent_functions(filename):
    f = open(filename, "r")
    # returns JSON object as a dictionary
    data = json.load(f)

    d = []

    for datum in data:
        types = [e["type"].split("/")[0] for e in datum["entities"]]
        if "State" in types or "Process" in types or "Property" in types:
            tokens = add_inherent_functions(datum)
            tokens = clean_tokens(tokens)
            d.append(" ".join(tokens))
    return d

if __name__ == "__main__":
    # dataset = prepare_dataset("../data/gold_release.json")
    dataset = full_dataset_append_inherent_functions("../data/gold_release.json")
    print("Dataset: ", dataset)
