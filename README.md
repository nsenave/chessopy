# chessopy

NB : `README` in english : later.

`chessopy` est une librairie python qui fournit une interface graphique (`tkinter`) pour apprendre des lignes d'échecs.

Le projet a été conçu pour s'entrainer sur les ouvertures, en jouant contre un ordinateur qui va jouer uniquement des coups d'une ouverture que l'utilisateur souhaite travailler.

La philosophie de l'application est d'apprendre des lignes petit à petit.

## Comment l'installer

```pip3 install -r requirements.txt```
(pas besoin pour l'instant : fichier vide car librairies standard)

Pour lancer l'application :
1. ouvrir le script `chessopy/__init__.py` dans votre éditeur python préféré.
2. Vers le début du script (après les imports), modifier la valeur `FOLDER_PATH`.
3. Excécuter le script, l'interface graphique devrait apparaître.

## Comment l'utiliser

### Jouer des coups

Chaque pièce peut être déplacée sur n'importe quelle case. Un bouton "Undo" permet de revenir en arrière.

### Mode entraînement

Pour l'instant, le choix du dictionnaire de coups à utiliser se fait dans le code :

Au moment où l'application est lancée, un dictionnaire de coup est chargé en fonction de la valeur de la variable `LINES_TO_BE_LOADED` (elle juste après "FOLDER_PATH").

J'ai enregistré les coups de la variante d'avance dans la française, mettre "french" à cette variable va charger ces lignes (qui sont dans le fichier `database/french_database.json`).

```LINES_TO_BE_LOADED = "french"```

Pour s'entraîner appuyer sur "Start training", jouer le premier coup pour jouer avec les blancs, sinon appuyer sur "Play random move" pour faire jouer un coup aux blancs puis jouer un coup avec les noirs, et c'est parti !

### Enregistrer ses lignes

Chaque coup joué est enregistré dans le dictionnaire de coups chargé au lancement de l'appli. Le bouton "Save move lines" va créer (ou écraser) le fichier `database/new_database.json`.

Pour partir d'un dictionnaire vide :

```LINES_TO_BE_LOADED = "new"```

Pour charger ses propres lignes, le fonctionnement actuel est pas compliqué mais dégueu, je change ça bientôt. En attendant, demandez-moi si vous comprenez pas comment faire et que vous voulez vous en servir.

## To do

### Le plus utile / Le plus simple

L'appli remplit le cas d'utilisation pour lequel je l'ai conçue  (enregistrer des lignes puis s'entraîner dessus), mais il y a *beaucoup* de choses à améliorer...

* **En priorité** : ajouter les roques (pour l'instant on peut roquer "à la main", c'est pas fou)
* Utiliser des chemins relatifs pour l'accès au fichier.
* Mettre une barre de menus (`menubar = Menu(root)`, cf. https://pythonspot.com/tk-menubar/ par exemple)
* De manière générale : faire en sorte que tout puisse se faire dans l'interface sans devoir renommer les fichiers (bases de données de coups), ou modifier des variables dans le code.
* Intégrer un système de dictionnaire avec plusieurs "grappes" correspondant à différents ouvertures (un grapge "french" pour l'ouverture française etc.).
* Ajouter un bouton "Record moves"/"Stop recording" qui active/désactive l'enregistrement des coups dans le dictionnaire.
* Ajouter des boutons pour pouvoir ajouter/enlever des pièces.
* Implémenter les promotions (+ penser à l'affichage en san).
* Permettre de commencer un entraînement sans partir forcément de la position de départ.
* Intégrer la lecture FEN, puis ajouter des listes de puzzles.

Et bien d'autres choses...

### Plus lourd

* Désembiguation des coups en notation algébrique.
* Ajouter la possibilité de jouer un coup en donnant sa notation algébrique (par exemple 'exd5') dans un champ de texte.
* Déplacement des pièces en glisser-déplacer
* Visualisation des coups joués sur le côté.

### Allez pourquoi pas / Plus tard

* Implémenter les règles des échecs (vérifier si le roque est possible, s'il y a échec etc.) dans les classes métier.
* OU : Remplacer tous les objets métier par ceux de la librairie `chess` de Niklas Fiekas https://github.com/niklasf/python-chess

NB : la deuxième option impliquerait aussi le changement de toutes les références aux objets métiers dans les objets graphiques, à faire dans un fork indépendant.

* Compatibilité avec `PolyGlot` pour les bases de données.

On pourrait aussi ajouter plein de fonctionnalités classiques des interfaces d'échecs (pas le but initial du projet mais pourquoi pas) :

* Pendule, mode joueur contre joueur, afficher les déplacements possibles d'une pièce une fois sélectionnée, pre-moves etc.
