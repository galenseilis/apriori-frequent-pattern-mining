import numpy as np
import matplotlib.pyplot as plt

from apriori import scan_db, get_db_size
from scipy.sparse import csr_matrix, lil_matrix
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram

def jaccard(u, v):
    return len(u.symmetric_difference(v)) / len(u.union(v))

file = '1k5L.txt'
N = get_db_size(file)
X = np.zeros((N,N))
for i, s_i in enumerate(scan_db(file)):
    for j, s_j in enumerate(scan_db(file)):
        if i < j:
            X[i,j] = jaccard(s_i[-1], s_j[-1])
X = X + X.T

Y = squareform(X)
L = linkage(Y)
D = dendrogram(L)
plt.show()
