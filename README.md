# ezeval

## Installation

1. Dans un terminal ou une invite de commandes, taper ```pip install ezeval -U```
1. Créer un fichier ezeval.sty avec un éditeur tex et y copier le contenu de [ezeval.sty](tex/ezeval.sty). Enregistrer ce fichier dans le répertoire où se trouve le fichier .tex du formulaire ou, pour qu'il soit accessible de n'importe quel répertoire, dans :
* ```TEXMFHOME/tex/xelatex/ezeval/```, si xelatex est utilisé pour compiler les fichiers
* ```TEXMFHOME/tex/latex/ezeval/``` si pdflatex est utilisé. 

Remarque : sur macOS, ```TEXMFHOME``` est situé dans ```~/Library/texmf/```

## Objectif

ezeval.sty permet de générer automatiquement :
1. un formulaire avec des champs vides pour les élèves
1. un formulaire avec les réponses dans les champs
1. un fichier correction.py qui permet de corriger automatiquement les formulaires remplis par les élèves.

## Utilisation

### Génération des fichiers

Dans le préambule du document, ajouter \usepackage{ezeval.sty}
Après ```\begin{document}```, taper la commande ```\afficherreponses``` (pour générer le formulaire élève, il suffit de commenter cette commande).
Avant ```\end{document}```, taper la commande ```\fin```.

La compilation du fichier .tex génère automatiquement un .pdf (avec les champs vides ou avec la correction) et un fichier correction.py qui sera utilisé pour la correction automatique.

### Utilisation

Pour chaque champ à créer dans le formulaire, on utilise la syntaxe suivante :

\champ{1er paramètre}{2e paramètre}{3e paramètre}{4e paramètre}


Exemples de création d'un champ de réponse dans le formulaire :
```
\champ{0.2}{ITALIE}{chaine}{[0]}\\
\champ{0.95}{Ce sont les bars$\text{,}$ restaurants et magasins de vêtements.}{mots}{['bar','cafe','restaurant','vêtement']}
\champ{0.85}{2h48}{nombres}{[15]}\\
\champ{0.25}{1°26’33.85’’E}{mixte}{[9999,0]} \\
\champ{0.8}{Le palais des sports n’existait pas entre 1950 et 1965.}{texte}{[0]}
```


Rôles des différents paramètres :
1. le premier renseigne largeur du champ de saisie (proportion de la largeur du doc) ;
1. le second contient la réponse qui sera affichée dans le corrigé (attention, on ne peut pas mettre de virgule dans un paramètre, si besoin d'une virgule dans la réponse du corrigé taper $\text{,}$);
1. le troisième indique le type d'évaluation utilisé (chaine, nombres, texte, mixte, mots)
1. le quatrième contient une liste (ne pas oublier les crochets). Selon le type d'évaluation, on indique l'éventuelle distance à ne pas dépasser entre la réponse du corrigé et la réponse de l'élève ou les mots que doit contenir la réponse de l'élève. Si ces informations ne sont pas nécessaires, peu importe ce que l'on met dans la liste.


Attention, les trois premiers champs du formulaire correspondent respectivement au nom, prénom et classe de l'élève. Leur contenu est reporté dans les trois premières colonnes du fichier .xlsx. Ils ne font pas partie de l'évaluation.

### Types d'évaluation

#### type chaine

Peu importe ici le contenu du 4e paramètre.
Le contenu de la réponse de l'élève et le contenu du corrigé sont normalisés (suppression des accents, caractères spéciaux, espaces et passage à la casse minuscule). Les contenus sont ensuite comparés. Si les deux chaines de caractères sont les mêmes, la cellule correspondant au champ dans le fichier .xlsx contient 1, sinon 0.


#### type nombres

Le 4e paramètre est une liste contenant un nombre.
Seuls les chiffres de la réponse de l'élève et de la réponse du corrigé sont conservés. 
Par exemple : 
* 43°49.12' devient 434912
* 3h12 devient 312
* L'altitude est de 46,4m devient 464.

On calcule la valeur absolue de la différence des deux entiers ainsi obtenus, ce qui définit une distance.
Si cette distance est inférieure ou égale à la valeur indiquée dans le 4e paramètre alors la cellule correspondant au champ dans le fichier .xlsx contient 1, sinon 0.

#### type mixte

Le 4e paramètre contient une liste de deux éléments, le 1er élément est un nombre, le 2e élément est nécessairement 0.
Ce type générera deux cellules dans le fichier .xlsx (avec le même numéro de question). 
On évalue les nombres contenus dans la réponse sur le même mode que le type nombres. La distance à ne pas dépasser avec le corrigé correspond au 1er élément de la liste du 4e paramètre.
On évalue la chaîne des caractères contenue dans la réponse sur le même mode que le type chaine. 

#### type texte

Peu importe ici le contenu du 4e paramètre.
La cellule correspondant au champ dans le fichier .xlsx sera vide. L'évaluation se fera manuellement.

#### type mots

Le 4e paramètre contient une liste de mots (considérés comme des chaînes de caractères : ne pas oublier les guillemets).
Pour chacun des mots contenus dans la liste du 4e paramètre, on teste sa présence dans la réponse de l'élève. Le contenu de la cellule correspondant au champ dans le fichier .xlsx contient de nombre de mots de la liste présents dans la réponse de l'élève.
Attention penser à adapter le barème de la question dans le fichier .xslx.


## Correction automatique

1. Créer un répertoire ```copies```
1. Placer les pdf des élèves dans ce répertoire
1. Mettre le corrigé (compilé par le fichier .tex du formulaire avec la commande ```\afficherreponses```) dans ce répertoire et le renommer ```corrige.pdf```
1. Exécuter le fichier ```correction.py``` avec la commande ```python correction.py```

Si tout se passe bien, un fichier ```notes.xlsx``` va être créé.

Les trois premières colonnes contiennent les noms, prénoms et classe des élèves.
Le barème par défaut est de 1 par cellule créée (si évaluation mixte, il y a deux cellules) pour un champ. Ce barème peut être modifié.
Pour une réponse fausse ou une absence de réponse, la cellule contient 0 et elle a un fond rose.
Les cellules d'évaluation manuelle sont vides et ont un fond vert.
A la fin de la ligne se trouve la somme des points obtenus par l'élève.