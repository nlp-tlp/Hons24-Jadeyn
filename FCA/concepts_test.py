import concepts
import pandas as pd

# c = concepts.load_csv('data2.csv')
# print(c)

df = pd.read_csv('data.csv', index_col=0)
df = df.transpose()
objects = df.index.tolist()
properties = list(df)
bools = list(df.fillna(False).astype(bool).itertuples(index=False, name=None))

c = concepts.Context(objects, properties, bools)
print(c)
l = c.lattice

import graphviz 
g = l.graphviz()
g.render(view=True)