# -*- coding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
import os
import requests
from hdfs.ext.kerberos import KerberosClient
import numpy as np
import pandas as pd


# # Chargement et nettoyage des données

# ## Chargement du fichier de training
# Ici chargement le fichier data/train.csv et nettoyage :
# - conservation uniquement des colonnes d'intérêt
# - élimination des lignes avec des valeurs manquantes
# - numérisation de l'attribut 'Sex'
# - renommage des attributs (pour uniformisation avec l'exemple seaborn)

column_name = {
    'PassengerId': 'passengerid',
    'Survived': 'survived',
    'Pclass': 'pclass',
    'Sex': 'sex',
    'Age': 'age'
}

# Etape 2 connexion à HDFS
session = requests.Session()
session.verify = False
client = KerberosClient(
    'https://' + os.environ['HDFS_HOST'] + ':'+os.environ['HDFS_PORT'],
    mutual_auth="REQUIRED", session=session,
    root='/projects/sandbox/titanic')

# Etape 3 read_csv sur HDFS
with client.read('data/train.csv', encoding='utf-8') as reader:
    titanic = pd.read_csv(reader)

print(titanic.head())
titanic = titanic[['Survived', 'Pclass', 'Sex', 'Age']]
titanic.dropna(axis=0, inplace=True)
titanic['Sex'].replace(['male', 'female'], [0, 1], inplace=True)
titanic.rename(columns=column_name, inplace=True)
print(titanic.head())


# # Entrainement du modèle

# ## Sélection de la cible et des features d'entraînement
y_train = titanic['survived']
X_train = titanic.drop('survived', axis=1)


# ## Entraînement sur un modèle KNN

model = KNeighborsClassifier()
model.fit(X_train, y_train)  # entrainement du modele
print(model.score(X_train, y_train))  # évaluation
