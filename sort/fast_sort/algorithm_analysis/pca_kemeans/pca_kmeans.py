
"""
    聚类算法
"""
import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)

from sklearn.cluster import DBSCAN

df_data = pd.read_csv('pca_dbscan_CW.csv')
X = df_data.iloc[:, 0:40+104+819]
print(X)

"""
    规范化之后，会分不出类别，都是0.
"""
# X_scaled2 = decomposition.TruncatedSVD(n_components=3).fit_transform(X)
#
# dbscan1 = DBSCAN(eps=50).fit_predict(X)
#
# dbscan2 = dbscan1.tolist()
#
# df_data['svd_dbscan'] = dbscan2
#
# genders = [0, 1]
# df = pd.DataFrame({
#     'X': X[:, 0],
#     'Y': X[:, 1],
#     'label': dbscan1
# })
#
# fg = sns.FacetGrid(data=df, hue='label', hue_order=genders)
# fg.map(plt.scatter, 'X', 'Y').add_legend(title='svd_dbscan')
# # plt.show()
# plt.savefig('svd_dbscan.png')


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN




# pca+kmeans
"""
    pca+kmeans
"""

X_pca2 = decomposition.PCA(n_components=2).fit_transform(X)
kmeans2 = KMeans(n_clusters=2, random_state=0).fit(X_pca2)
c_tsne2 = kmeans2.labels_

c_tsne3 = c_tsne2.tolist()

df_data['pca_kmeans'] = c_tsne3

genders = [0, 1]
df = pd.DataFrame({
    'X': X_pca2[:, 0],
    'Y': X_pca2[:, 1],
    'Class': c_tsne2
})

fg = sns.FacetGrid(data=df, hue='Class', hue_order=genders)
fg.map(plt.scatter, 'X', 'Y').add_legend(title='pca_kmeans')

plt.savefig('pca_kmeans_CW.png')

df_data.to_csv('pca_kmeans_CW.csv')