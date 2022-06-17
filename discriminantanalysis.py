# -*- coding: utf-8 -*-
"""DiscriminantAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J2t9Xc1EU-uoEROeNqOFvkpwgV3Rb76V

**Análise Discriminante**

> Utilizando o dataset load_wine, importado pelo **sklearn.datasets**

**Parte 1 - Variância**
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np

dadosVariancia = [20, 32, 32, 36, 39, 43, 46, 48, 49, 50, 52, 53, 56, 57, 63,
                  64, 65, 74, 75, 90]

variancia = np.var(dadosVariancia)
print('O resultado da variância é: ', variancia)

"""**Parte 2 - Discriminante Linear**"""

from sklearn.datasets import load_wine
import pandas as pd
import numpy as np
np.set_printoptions(precision=4)
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

wine = load_wine()

X = pd.DataFrame(wine.data, columns=wine.feature_names)
Y = pd.Categorical.from_codes(wine.target, wine.target_names)

X.head()

Y

df = X.join(pd.Series(Y, name='class'))

"""**Criando as matrizes de dispersão**"""

class_feature_means = pd.DataFrame(columns=wine.target_names)

for c, rows in df.groupby('class'):
  class_feature_means[c] = rows.mean()

  class_feature_means

class_feature_means

within_class_scatter_matrix = np.zeros((13, 13))

for c, rows in df.groupby('class'):
  rows = rows.drop(['class'], axis = 1)
  s = np.zeros((13, 13))

  for index, row in rows.iterrows():
      x = row.values.reshape(13, 1)
      mc = class_feature_means[c].values.reshape(13,1)
      s += (x - mc).dot((x-mc).T)
      within_class_scatter_matrix += s

within_class_scatter_matrix

feature_names = df.mean()

between_class_scatter_matrix = np.zeros((13, 13))
for c in class_feature_means:
  n = len(df.loc[df['class'] == c].index)
  mc = class_feature_means[c].values.reshape(13, 1)
  m = feature_names.values.reshape(13, 1)
  between_class_scatter_matrix += n * (mc - m).dot((mc - m).T)

feature_names

between_class_scatter_matrix

eigen_values, eigen_vectors = np.linalg.eig(np.linalg.inv(
    within_class_scatter_matrix).dot(between_class_scatter_matrix))

pairs = [(np.abs(eigen_values[i]), eigen_vectors[:, i])
for i in range(len(eigen_values))]

pairs = sorted(pairs, key=lambda x: x[0], reverse=True)

for pair in pairs:
  print(pair[0])

w_matrix = np.hstack((pairs[0][1].reshape(13, 1),
                      pairs[1][1].reshape(13, 1))).real
X_lda = np.array(X.dot(w_matrix))
X_lda

le = LabelEncoder()
y = le.fit_transform(df['class'])
plt.xlabel('LD1')
plt.ylabel('LD2')
plt.scatter(X_lda[:,0], X_lda[:,1], c=y, cmap='rainbow', alpha=0.7,
            edgecolors='b')

"""**Aplicando de forma mais simples**"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

wine = load_wine()

X = pd.DataFrame(wine.data, columns = wine.feature_names)
Y = pd.Categorical.from_codes(wine.target, wine.target_names)

df = X.join(pd.Series(Y, name = 'class'))

le = LabelEncoder()
y = le.fit_transform(df['class'])

y

lda = LinearDiscriminantAnalysis()
X_lda = lda.fit_transform(X, y)
plt.xlabel('LD1')
plt.ylabel('LD2')
plt.scatter(X_lda[:,0], X_lda[:,1], c=y, cmap='rainbow', alpha=0.7
            , edgecolors='b')

"""**Representação visual por meio de Árvore de Decisão**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

wine = load_wine()

X = pd.DataFrame(wine.data, columns=wine.feature_names)
y = pd.Categorical.from_codes(wine.target, wine.target_names)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state = 1)

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print('Accuracy: ', metrics.accuracy_score(y_test, y_pred))

from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus

dot_data = StringIO()
export_graphviz(clf, out_file = dot_data, filled=True, rounded=True,
                special_characters = True, feature_names=wine.feature_names,
                class_names=wine.target_names)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('wines.png')
Image(graph.create_png())

clf = DecisionTreeClassifier(criterion='entropy', max_depth=3)
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print('Accuracy: ', metrics.accuracy_score(y_test, y_pred))

#vinho!!
dot_data = StringIO()
export_graphviz(clf, out_file = dot_data, filled=True, rounded=True,
                special_characters = True, feature_names=wine.feature_names,
                class_names=wine.target_names)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('wines.png')
Image(graph.create_png())