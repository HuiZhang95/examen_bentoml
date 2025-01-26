# Examen BentoML
1. import data to local disk:
    import_raw_data.py
2. data preprocessing, train-test split, normalization
    prepare_data.py
3. train a randomforestregression model
    train_model.py
4. Code to perform unit test using pytest
    test_app.py
5. The commands to run unit test:
    python3 -m pytest src/test_app.py
6. compressed container image for the app
    bento_image_final.tar
7. docker image on docker hub:
    rf_exam_service:stbb7hg4googev5i



Ce repertoire contient l'architecture basique afin de rendre l'évaluation pour l'examen BentoML.

Vous êtes libres d'ajouter d'autres dossiers ou fichiers si vous jugez utile de le faire.

Voici comment est construit le dossier de rendu de l'examen:

```bash       
├── examen_bentoml          
│   ├── data       
│   │   ├── processed      
│   │   └── raw           
│   ├── models      
│   ├── src       
│   └── README.md
```

Afin de pouvoir commencer le projet vous devez suivre les étapes suivantes:

- Forker le projet sur votre compte github

- Cloner le projet sur votre machine

- Récuperer le jeu de données à partir du lien suivant: [Lien de téléchargement]( https://datascientest.s3-eu-west-1.amazonaws.com/examen_bentoml/admissions.csv)


Bon travail!
