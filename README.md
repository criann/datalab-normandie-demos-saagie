# Datalab Normandie examples for Saagie Dataops plateform

Vous trouverez dans ce dépôt des cas exemples pour apprendre à créer des jobs de traitement de la donnée avec l'outil Dataops de Saagie et le datalake S3 dans le contexte de la plateforme Datalab Normandie.

## Usecases

Différents cas exemples sont fournis afin de vous entraîner avant que vous puissiez sereinement créer vos propres traitements en utilisant la plateforme.

- Titanic (prévision sur la survie des passagers du Titanic) :
    - sans datalake, avec un script python utilisant les bibliothèques python pandas et seaborn : [voir ici](usecases/titanic/without_datalake/)
    - avec datalake S3 et un script python utilisant les bibliothèques python pandas et minio (client S3) : [voir ici](usecases/titanic/with_datalake_s3/)
    - avec datalake S3 et un script python utilisant les directives S3 SELECT supportées et la bibliothèque python boto3 : [voir ici](usecases/titanic/s3_select/)
