import json

def FilterDataset(filename):
    # Opening JSON file
    f = open(filename)

    # returns JSON object as a dictionary
    data = json.load(f)
    data_one_PO_zero_hasPart = []
    data1_failureWords_dict = {}
    data_more_than_one_PO_more_than_zero_hasPart = []
    data2_failureWords_dict = {}
    data_remove_generic = []
    data3_failureWords_dict = {}
    OG_failureWords_dict = {}
    generic_words = ["unserviceable", "fault", "faulty", "not working"]
    for datum in data:
        physicalObjectCount = 0
        hasPartCount = 0
        failureWords = []
        contains_generic = False

        for entity in datum["entities"]:
            if entity["type"].split("/")[0] == "PhysicalObject":
                physicalObjectCount += 1
            
            if entity["type"].split("/")[0] in ["State", "Process", "Property"]:
                start = entity["start"]
                end = entity["end"]
                if end == len(datum["tokens"]):
                    failureWords.append(" ".join(datum["tokens"][start:]))
                else:
                    failureWords.append(" ".join(datum["tokens"][start:end]))
                if failureWords[-1].lower() in generic_words:
                    contains_generic = True

        for relation in datum["relations"]:
            if relation["type"].split("/")[0] == "hasPart":
                hasPartCount += 1
       
        if physicalObjectCount == 1 and hasPartCount == 0:
            data_one_PO_zero_hasPart.append(datum)
            for obj in failureWords:
                if obj not in data1_failureWords_dict:
                    data1_failureWords_dict[obj] = 1
                data1_failureWords_dict[obj] += 1
        
        if physicalObjectCount > 1 and hasPartCount > 0:
            data_more_than_one_PO_more_than_zero_hasPart.append(datum)
            for obj in failureWords:
                if obj not in data2_failureWords_dict:
                    data2_failureWords_dict[obj] = 1
                data2_failureWords_dict[obj] += 1
        
        if not contains_generic:
            data_remove_generic.append(datum)
            for obj in failureWords:
                if obj not in data3_failureWords_dict:
                    data3_failureWords_dict[obj] = 1
                data3_failureWords_dict[obj] += 1
            
        for obj in failureWords:
            if obj not in OG_failureWords_dict:
                OG_failureWords_dict[obj] = 1
            OG_failureWords_dict[obj] += 1

    f.close()
    jsonString = json.dumps(data_one_PO_zero_hasPart, indent=2)
    with open(filename[:-5]+"_filtered1.json", "w") as outfile:
        outfile.write(jsonString)
    
    jsonString = json.dumps(data_more_than_one_PO_more_than_zero_hasPart, indent=2)
    with open(filename[:-5]+"_filtered2.json", "w") as outfile:
        outfile.write(jsonString)
    
    jsonString = json.dumps(data_remove_generic, indent=2)
    with open(filename[:-5]+"_filtered3.json", "w") as outfile:
        outfile.write(jsonString)

    # sort the dictionary by value
    data1_failureWords_list = sorted(data1_failureWords_dict.items(), key=lambda item: item[1], reverse=True)
    data2_failureWords_list = sorted(data2_failureWords_dict.items(), key=lambda item: item[1], reverse=True)
    data3_failureWords_list = sorted(data3_failureWords_dict.items(), key=lambda item: item[1], reverse=True)
    og_failureWords_list = sorted(OG_failureWords_dict.items(), key=lambda item: item[1], reverse=True)

    return len(data_one_PO_zero_hasPart), len(data_more_than_one_PO_more_than_zero_hasPart), len(data_remove_generic), data1_failureWords_list, data2_failureWords_list, data3_failureWords_list, og_failureWords_list


if __name__ == "__main__":

    gold_len1, gold_len2, gold_len3, gold_dict1, gold_dict2, gold_dict3, gold_og_dict = FilterDataset("../data/gold_release.json")
    silver_len1, silver_len2, silver_len3, silver_dict1, silver_dict2, silver_dict3, silver_og_dict  = FilterDataset("../data/silver_release.json")

    print()
    print("Gold new length: ",gold_len1, ", ", gold_len2, " ", gold_len3)
    
    print()
    print("Gold dict1 ################ ", sum(x[1] for x in gold_dict1))
    for i in range(10):
        print(gold_dict1[i])
    
    print()
    print("Gold dict2 ################ ", sum(x[1] for x in gold_dict2))
    for i in range(10):
        print(gold_dict2[i])

    print()
    print("Gold dict3 ################ ", sum(x[1] for x in gold_dict3))
    for i in range(10):
        print(gold_dict3[i])

    print()
    print("Gold dict og ################ ", sum(x[1] for x in gold_og_dict))
    for i in range(10):
        print(gold_og_dict[i])

    print()
    print("Silver new length: ",silver_len1, ", ", silver_len2, " ", silver_len3)
    
    print()
    print("Silver dict1 ################ " , sum(x[1] for x in silver_dict1))
    for i in range(10):
        print(silver_dict1[i])
    
    print()
    print("Silver dict2 ################ " , sum(x[1] for x in silver_dict2))
    for i in range(10):
        print(silver_dict2[i])

    print()
    print("Silver dict3 ################ " , sum(x[1] for x in silver_dict3))
    for i in range(10):
        print(silver_dict3[i])

    print()
    print("Silver dict og ################ ", sum(x[1] for x in silver_og_dict))
    for i in range(10):
        print(silver_og_dict[i])
