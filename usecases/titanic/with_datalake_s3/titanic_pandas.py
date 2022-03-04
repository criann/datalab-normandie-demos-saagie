# -*- coding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
import os
import sys
from minio import Minio
from minio.error import InvalidResponseError
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

# Etape 2 connexion au datalake S3
endpoint = os.getenv('DATALAKE_HOST') \
    or sys.exit("DATALAKE_HOST is not set")
access_key = os.getenv('DATALAKE_ACCESS_KEY') \
    or sys.exit("DATALAKE_ACCESS_KEY is not set")
secret_key = os.getenv('DATALAKE_SECRET_KEY') \
    or sys.exit("DATALAKE_SECRET_KEY is not set")
bucket = os.getenv('DATALAKE_BUCKET', 'group-prj00001')
# or sys.exit("DATALAKE_BUCKET is missing")

client = Minio(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=True
)
try:
    with client.get_object(
        bucket_name=bucket,
        object_name='titanic/data/train.csv'
    ) as object:
        titanic = pd.read_csv(object)
except InvalidResponseError as err:
    print(err)
    sys.exit("Connection error")

# Etape 3 read_csv depuis l'objet S3
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
