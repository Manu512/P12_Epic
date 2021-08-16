# __P12 Projet EPIC Event__

## Information :
Le hashage des mots de passe est effectué par le hasheur **Argon2** pour **augmenter la sécurité.**

Pour nos tests et nos exemples d'utilisateurs, la complexité des mots de passe a été bypassé.  
Lors de la création de nouveaux users, les mots de passe devront etre complexe.


## Etat d'avancement :

~~En dev -~~ **Préparation pour la soutenance**

## Description :

Ce projet utilise les technologies suivantes :

* Python v3.9+
* Django 3.2.5
* SimpleJWT for API security Token
* PostGreSQL
    
## Pré-Requis
1. Serveur PostGreSLQ fonctionnel.
2. Avoir les droits pour créer une base de données.

###Créer la base de donnée PostgreSQL
* Créez la base de donnée SQL : postgres=# CREATE DATABASE epic_event;

## Installation de l'application
Se diriger sur le repertoire où l'on souhaite installer l'application.
1. Cloner le repository via la commande : 
`git clone https://github.com/Manu512/P12_EPICEvent.git`

  
2. Création de l'environnement virtuel

Exécuter la commande :
* `python3 -m venv 'env'` ('env' sera le repertoire où seront stocké les données de l'environnement python)
  
3. Activation et installations des dépendances nécessaires au script dans l'environnement virtuel   
   `env/Script/activate`
   
   `pip install -r requirements.txt'`


4. Premiere installation :
    * Configuration de la base de données que l'application va utiliser :
Dans le fichier settings.py renseigner correctement les données suivantes : 
      

        'default': {
                'ENGINE':   'django.db.backends.postgresql_psycopg2',
                'NAME':     'epic_event',
                'USER':     'epic',
                'PASSWORD': 'xxxx',
                'HOST':     '192.168.1.8',
                'PORT':     '5432',
        }


   Je vous conseille de charger les variables d'environnement cf Utilisation: via env.bat
   puis au choix  
   * `manage.py makemigrations` / `django-admin makemigrations`  
   * `manage.py migrate` / `django-admin migrate` 
   * `manage.py loaddata init.json` / `django-admin loaddata init.json` 


5. Lancement du serveur Django :
* Puis exécuter `python manage.py runserver`

A ce moment, l'api sera accessible à l'URL [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
L'interface web est accessible à l'URL : [http://127.0.0.1:8000/administration/](http://127.0.0.1:8000/administration/)

## Utilisation


lien documentation PostMan : https://documenter.getpostman.com/view/15567806/TzRX9kbR

  QuickStart pour Windows : exécutez `env.bat` ou `env.ps1` selon l'environnement, il définira les variables d'environnement. Les détails étape par 
  pas à pas ci-dessous.

  - Pour Windows, dans le répertoire : 
    - `set PYTHONPATH=%cd%` 
    - `set DJANGO_SETTINGS_MODULE=EPIC_Event.settings` 
  - Pour Windows avec PowerShell : 
    - `$env:PYTHONPATH=$pwd` 
    - `$env:DJANGO_SETTINGS_MODULE="EPIC_Event.settings"` 

- Vous devriez maintenant être prêt à tester l'application. Dans le répertoire, tapez soit <code>django-admin run</code>.
L'application devrait répondre avec une adresse à laquelle vous devriez pouvoir vous rendre en utilisant votre navigateur.
  
Pour se loger à l'API, il faut un jeton JWT que l'on peut obtenir à l'URL :  [http://127.0.0.1:8000/api/login/](http://127.0.0.1:8000/api/login/)


## Les utilisateurs de base
### Administrateur

- admin / 1234 : Full acces à l'administration. À utiliser avec parcimonie permet de modifier les autorisations des groupes.
- En cas de modification, cela impactera également le fonctionnement de l'api.

### Equipe de management

- management / 1234 : Acces à l'administration avec presque tous les droits. (Cf les consignes du client).

C'est cette equipe qui va affecter un personnel support à un event lors de la signature du contrat.

### Equipe de support

- support1 / 1234 
- support2 / 1234  

C'est une de ces personnes qui va etre en charge d'un évènement une fois celui-ci crée.

### Equipe commerciale

- commercial1 / 1234  
- commercial2 / 1234  

C'est une de ces personnes qui va créer les clients/prospects ainsi que les contrats pour les evenements.
Ils ont aussi acces aux évènements des contrats qui leur sont rattachés.
