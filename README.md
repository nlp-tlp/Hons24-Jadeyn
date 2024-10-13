# Semantic and Engineering Knowledge based Embedding for Maintenance Work Order Clustering

This is the repository for the honours thesis "Semantic and Engineering Knowledge based Embedding for Maintenance Work Order Clustering" by Jadeyn Feng (2024) and supervised by Prof. Melinda Hodkiewicz, Dr. Caitlin Woods and Dr. Michael Stewart. The project aim is generate a set of generic failure mode categories for industrial maintenance. 

## Dataset

The datasets used in this study include: 
- [MaintIE](https://github.com/nlp-tlp/maintie)
- [Synthetic Data Generated from Maintie](https://github.com/nlp-tlp/Hons24_AllisonLau)
 
Data files are stored in the `data/`directory. 

## Embedding and Clustering MWOs
This section contains an overview of code in `Sentence_Embeddings/MWO_Embedding_and_Clustering.ipynb`.  
### Embeddings
In this project, Word2Vec Bi-LSTM embeddings and SBERT NN embeddings were developed to incorporate engineering knowledge in the form of equipment inherent functions, together with semantic representatons of Maintenance Work Orders. 

The first method for getting deep embeddings was from a Bi-LSTM trained on classifying Word2Vec embedded MWOs to their inherent function. The second method is training a Neural Network on SBERT embedding inputs to classify MWO by inherent function. For both these methods, the hidden layer before the output layer was taken as the new sentence embeddings for the MWO. 

This was compared to averaged Word2Vec and pure SBERT approaches. 

### Clustering
The three clustering approaches used were K-means, average agglomerative hierarchical, and ward agglomerative hierarchical. All combinations of clustering and embedding approaches were tested. 

## Data Analysis
This section contains an overview of the code in the `Data_Analysis\` directory.

### class_extraction.py
allows the user to query all the unique terms that are annotated by a certain user-specified class. 

### dataset_analysis.py
allows the user to run the following experiments on the MaintIE dataset: 
1. For each tail entity, extract the associated inherent function found in the PhysicalObject subclass and all their corresponding head entities. 

2. Count the number of times each head entity appears, or count the number of equipment functions each head entity was associated with.

3. Determine the head entities that are unique to each equipment function. 

4. For each head entity, get all the associated tail entities.

## Topic Modelling
This section descibed the code in the `TopicModelling\topicmodelling.ipynb` file. 

Three topic modelling approaches that were tested were: 
- GSDMM
- BERTopic
- Top2vec
