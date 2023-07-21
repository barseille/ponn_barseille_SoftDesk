# Softdesk

Softdesk est une application de gestion de projet qui permet aux utilisateurs de créer des projets, de les gérer, d'assigner des problèmes et de commenter sur ces problèmes. L'application a été construite avec Django et Django Rest Framework.


### Configuration du projet: 

Cloner le projet depuis votre éditeur de code : 

```
git clone https://github.com/barseille/ponn_barseille_SoftDesk.git
```

### Créer un environnement virtuel : 

```
python -m venv env
```

### Activer l'environnement virtuel :

Pour Windows :

```
env/Scripts/Activate.ps1
```

Pour macOS ou Linux :

```
source env/bin/activate

```
### Mise à jour "pip" si besoin à l'aide cette commande :

```
python -m pip install --upgrade pip
```

### Installez les dépendances :

Avec l'environnement virtuel activé, installez les dépendances requises :

```
pip install -r requirements.txt
```

### Configuration de la base de données : 

Exécutez les migrations de la base de données avec :

```
python manage.py migrate
```

### Exécution du serveur : 

```
python manage.py runserver
```

## Documentation API

La documentation complète de l'API est disponible sur : 

```
https://documenter.getpostman.com/view/19023915/2s946k5qZ3
```