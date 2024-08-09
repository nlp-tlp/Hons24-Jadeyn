import os
from similarity import similarity
import nltk
nltk.download('wordnet')
nltk.download('brown')
import numpy as np
import time
from create_dataset import full_dataset
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

start = time.time()

simList = []

dataset = full_dataset("../data/gold_release.json")
np.random.seed(42)
random_sampled_dataset = np.random.choice(dataset, 100, replace=False)
print(random_sampled_dataset)
similarity_matrix=[]
for i in range(0,len(random_sampled_dataset)):
    for j in range(i+1, len(random_sampled_dataset)):
        sentList1=random_sampled_dataset[i]
        sentList2=random_sampled_dataset[j]
        sim = similarity(sentList1,sentList2)
        
        # print(sentList1,"&",sentList2)
        # print(sim)
        similarity_matrix.append(sim)
    print(i/len(random_sampled_dataset)*100,"% done")

Z = linkage(similarity_matrix, 'average')
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)
plt.show()
# for i in range(0,len(file_name)):
#     for j in range(0, len(file_name)):
#         if i!=j:
           
#            sentList1=file_text[i]
#            sentList2=file_text[j]


#Link to the path of the sub-folder 'dataset'
# data_PATH=r'dataset'

# file_name = []
# file_text = []
# for filename in os.listdir(data_PATH):
#     if filename.endswith(".txt"):
        
#         with open(data_PATH+"/"+filename) as ff:
#             file_name.append(filename)
            
#             text = ff.readlines()[0]

#             sent_text = nltk.sent_tokenize(text)
#             file_text.append(sent_text)

# print(file_name)
# print(file_text)

           
           

# for i in range(0,len(file_name)):
#     for j in range(0, len(file_name)):
#         if i!=j:
           
#            sentList1=file_text[i]
#            sentList2=file_text[j]
           
#            print(file_name[i],"&",file_name[j])

#            for sentList1Text in sentList1:
#                max = 0
#                sim=0
#                comparedStatement = None
#                for sentList2Text in sentList2:
#                    sim = similarity(sentList1Text,sentList2Text)
#                    if sim>0.5:
#                        if max<sim:
#                            max = sim
#                            comparedStatement = sentList2Text
#                print(sentList1Text,"&",comparedStatement)
#                print(max)
#                simList.append(max)

#            simListArr = np.array(simList)
#            print("Similarity:",np.sqrt(np.mean(simListArr**2)))
#            print("")

# Calculate execution time
end = time.time()
dur = end-start
print("")
if dur<60:
    print("Execution Time:",dur,"seconds")
elif dur>60 and dur<3600:
    dur=dur/60
    print("Execution Time:",dur,"minutes")
else:
    dur=dur/(60*60)
    print("Execution Time:",dur,"hours")
