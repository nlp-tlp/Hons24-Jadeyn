import pandas as pd
from fcapy.context import FormalContext
url = 'inherent_functions_vs_FM.csv'
df = pd.read_csv(url, index_col=0)
df=df.transpose()
K = FormalContext.from_pandas(df)

# # Print the first five objects data
# print(K)

from fcapy.lattice import ConceptLattice
L = ConceptLattice.from_context(K)

for i, c in enumerate(L):
    print(f"Concept {i}:\nextent {c.extent}\nintent {c.intent}\n")

import matplotlib.pyplot as plt
from fcapy.visualizer import LineVizNx
fig, ax = plt.subplots(figsize=(10, 5))
vsl = LineVizNx(node_label_font_size=8)


vsl.draw_concept_lattice(
    L, ax=ax, 
    max_new_extent_count=10, max_new_intent_count=10, flg_new_intent_count_prefix=False, flg_new_extent_count_prefix=False
)
# ax.set_title('"Animal movement" concept lattice', fontsize=18)
plt.tight_layout()
plt.show()
