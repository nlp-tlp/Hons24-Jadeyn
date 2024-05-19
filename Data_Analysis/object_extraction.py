import json

# Opening JSON file
f = open('./data/gold_release.json')

# returns JSON object as a dictionary
data = json.load(f)

# entity classes we are concerned with for head entities in hasAgent/hasPatient relations
heads = ["State", "Process", "Property"]

states = {}
terms = {}
exception_states = []
non_object_tails = []
non_object_heads = []

# Extract relevant data from the dataset
for d in data:
    for relation in d['relations']:
        r_type = relation['type']
        if r_type == "hasParticipant/hasPatient":
            head = relation['head']
            tail = relation['tail']
            # removing relations where the tail is not a PhysicalObject entity
            if d['entities'][tail]['type'].split("/")[0] != "PhysicalObject":
                start = d['entities'][head]['start']
                end = d['entities'][head]['end']
                if end == len(d['tokens']):
                    state_words = " ".join(d['tokens'][start:])
                else: 
                    state_words = " ".join(d['tokens'][start:end])
                non_object_heads.append(state_words)
                non_object_tails.append(d['entities'][tail]['type'])
                continue
            # removing relations where the head is not a State entity
            if d['entities'][head]['type'].split("/")[0] not in heads:
                start = d['entities'][head]['start']
                end = d['entities'][head]['end']
                if end == len(d['tokens']):
                    state_words = " ".join(d['tokens'][start:])
                else: 
                    state_words = " ".join(d['tokens'][start:end])
                non_object_heads.append(state_words)
                # non_object_tails.append(d['entities'][tail]['type'])
                continue
            # if the tail is only labelled PhysicalObject with no functional property 
            if len(d['entities'][tail]['type'].split("/")) < 2:
                exception_states.append((d,d['entities'][tail]['type']))
                continue

            # state dictionary
            state_type = d['entities'][tail]['type'].split("/")[1]
            start = d['entities'][head]['start']
            end = d['entities'][head]['end']
            if end == len(d['tokens']):
                state_words = " ".join(d['tokens'][start:])
            else: 
                state_words = " ".join(d['tokens'][start:end])
            if state_type in states.keys():
                states[state_type].append(state_words)
            else: 
                states[state_type] = [state_words]

            # terms dictionary
            tail_start = d['entities'][tail]['start']
            tail_end = d['entities'][tail]['end']
            if tail_end == len(d['tokens']):
                object_words = " ".join(d['tokens'][tail_start:])
            else: 
                object_words = " ".join(d['tokens'][tail_start:tail_end])
            if state_words in terms.keys():
                terms[state_words].append(object_words)
            else: 
                terms[state_words] = [object_words]

        if r_type == "hasParticipant/hasAgent":
            head = relation['head']
            tail = relation['tail']
            if d['entities'][tail]['type'].split("/")[0] != "PhysicalObject":
                start = d['entities'][head]['start']
                end = d['entities'][head]['end']
                if end == len(d['tokens']):
                    state_words = " ".join(d['tokens'][start:])
                else: 
                    state_words = " ".join(d['tokens'][start:end])
                non_object_heads.append(state_words)
                non_object_tails.append(d['entities'][tail]['type'])
                continue
            if d['entities'][head]['type'].split("/")[0] not in heads:
                start = d['entities'][head]['start']
                end = d['entities'][head]['end']
                if end == len(d['tokens']):
                    state_words = " ".join(d['tokens'][start:])
                else: 
                    state_words = " ".join(d['tokens'][start:end])
                non_object_heads.append(state_words)
                # non_object_tails.append(d['entities'][tail]['type'])
                continue
            if len(d['entities'][tail]['type'].split("/")) < 2:
                exception_states.append((d,d['entities'][tail]['type']))
                continue
            state_type = d['entities'][tail]['type'].split("/")[1]
            start = d['entities'][head]['start']
            end = d['entities'][head]['end']
            if end == len(d['tokens']):
                state_words = " ".join(d['tokens'][start:])
            else: 
                state_words = " ".join(d['tokens'][start:end])
            if state_type in states.keys():
                states[state_type].append(state_words)
            else: 
                states[state_type] = [state_words]
            
            # terms dictionary
            tail_start = d['entities'][tail]['start']
            tail_end = d['entities'][tail]['end']
            if tail_end == len(d['tokens']):
                object_words = " ".join(d['tokens'][tail_start:])
            else: 
                object_words = " ".join(d['tokens'][tail_start:tail_end])
            if state_words in terms.keys():
                terms[state_words].append(object_words)
            else: 
                terms[state_words] = [object_words]



######################################

print("Select the experiment to run below: ")
print()
print("1. For each tail entity, extract the associated inherent function found in "
      "the PhysicalObject subclass and all their corresponding head entities.")
print("2a. Count the number of times each head entity appears. ")
print("2b. Count the number of equipment functions each head entity was associated with.")
print("3. Determine the head entities that are unique to each equipment function. ")
print("4. For each head entity, get all the associated tail entities.")
print()
print("Run experiment: ")
experiment = input()
print()

if experiment == "1":
    for key, item in states.items():
        print(key)
        for i in set((item)):
            print("    "+i)
        print()

elif experiment =="2a":
    state_terms_count = {}
    for s in states.items():
        state_type = s[0]
        states_group = s[1]
        for i in states_group:
            if i in state_terms_count.keys():
                state_terms_count[i].append(state_type)
            else:
                state_terms_count[i]=[state_type]
    sorted_state_term_count = sorted(
        state_terms_count.items(),
        key=lambda x: len(x[1])
    )

    for i in sorted_state_term_count:
        print(i[0], len(i[1]))

elif experiment=="2b":
    state_terms_count = {}
    for s in states.items():
        state_type = s[0]
        states_group = set((s[1]))
        for i in states_group:
            if i in state_terms_count.keys():
                state_terms_count[i].append(state_type)
            else:
                state_terms_count[i]=[state_type]

    sorted_state_term_count = sorted(
        state_terms_count.items(), 
        key=lambda x: len(x[1])
    )

    for i in sorted_state_term_count:
        print(i[0], len(i[1]))

elif experiment =="3":
    state_terms_count = {}
    for s in states.items():
        state_type = s[0]
        states_group = set((s[1]))
        for i in states_group:
            if i in state_terms_count.keys():
                state_terms_count[i].append(state_type)
            else:
                state_terms_count[i]=[state_type]

    for i in states.items():
        print("\n"+i[0])
        set_terms = set((i[1]))
        contains_unique = False
        for j in set_terms:
            if len(state_terms_count[j]) == 1:
                print("   ", j)
                contains_unique = True
        if not contains_unique:
            print("    No unique head terms for this PhysicalObject subclass.")

elif experiment =="4":
    term_sort = sorted(terms.items(),key=lambda x: x[0])
    for t in term_sort:
        object_list = ", ".join(sorted(set((t[1]))))
        print("\n"+ t[0].upper())
        print("   ",object_list)
else:
    print( "Invalid input value")

print()

# Closing file
f.close()