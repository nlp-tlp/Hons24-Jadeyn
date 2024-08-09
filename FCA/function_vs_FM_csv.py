import json

def function_vs_FM(filename):
    f = open(filename)

    # returns JSON object as a dictionary
    data = json.load(f)
    inherent_functions_vs_FM = {}
    set_failure_modes = []
    for datum in data:
        inherent_functions = []
        failure_modes = []
        types = [e["type"].split("/")[0] for e in datum["entities"]]

        # if there is no failure mode or Inherent function, skip
        if not ("State" in types or "Process" in types or "Property" in types) or "PhysicalObject" not in types:
            continue

        # get all inherent functions and failure modes in this MWO
        for entity in datum["entities"]:
            entity_type = entity["type"].split("/")[0]
            # if inherent function
            if entity_type == "PhysicalObject":
                if len(entity["type"].split("/")) > 1:
                    inherent_functions.append(entity["type"].split("/")[1])

            # if a failure mode
            if entity_type in ["State", "Process", "Property"]:
                start = entity["start"]
                end = entity["end"]
                if end == len(datum['tokens']):
                    failure_modes.append(" ".join(datum['tokens'][start:]))
                else: 
                    failure_modes.append(" ".join(datum['tokens'][start:end]))
        
        # add the inherent functions and failure modes to the dictionary
        for function in inherent_functions:
            if function not in inherent_functions_vs_FM:
                inherent_functions_vs_FM[function] = []
            for fm in failure_modes:
                if fm not in inherent_functions_vs_FM[function]:
                    inherent_functions_vs_FM[function].append(fm)
                if fm not in set_failure_modes:
                    set_failure_modes.append(fm)
    set_failure_modes = list(set(set_failure_modes))
    return inherent_functions_vs_FM, set_failure_modes

def dict_to_csv(dict, failure_modes):
    with open("inherent_functions_vs_FM.csv", "w") as f:
        f.write(","+",".join(failure_modes)+"\n")
        for key in dict:
            line = [key] +["False"]*len(failure_modes)
            for i in dict[key]:
                index = failure_modes.index(i)+1
                line[index] = "True"

            f.write(",".join(line)+"\n")



if __name__ =="__main__":
    inherent_functions_vs_FM, failure_mode = function_vs_FM("../data/gold_release.json")
    dict_to_csv(inherent_functions_vs_FM, failure_mode)