import json
import contractions

def pad_sequence(dataset):
    max_len = len(max(dataset, key=len))
    for i in range(len(dataset)):
        dataset[i] = dataset[i] + ["PAD"] * (max_len - len(dataset[i]))
    return dataset

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


if __name__ == "__main__":
    # dataset = prepare_dataset("../data/gold_release.json")
    dataset = full_dataset("../data/gold_release.json")
    print("Dataset: ", dataset)
