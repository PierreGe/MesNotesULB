# Mes Notes ULB

Ce dépôt contient une collection de scripts pour accéder à MonULB.

L'outils usuels utilisé est requests. Il n'est pas fournid pas défaut
avec python

## Dépendances

* Python 2
* requests

# Les scripts

## mesnotes.py

Permet d'afficher l'ensemble du relevé de notes actuel, ainsi qu'une estimation
de la moyenne pondérée. S'utilise uniquement en ligne de commande

Utilisation: `python mesnotes.py [netid] [password]`

## notify_notes.py

Permet d'envoyer un message sur un groupe Facebook dès que sortent de nouvelles
notes. Ce script nécessite un fichier de configuration. Un exemple est fourni 
dans `config.py.example`. Il peut être facilement utilisé dans un cron. 
*NB: Si les valeurs de configuration `ULB_USER` et `ULB_PASS` sont définies
dans config.py, mesnotes.py les utilisera par défaut.*

Utilisation:

	cp config.py.exampe config.py
	nano config.py
	python notify_notes.py

## Considérations de sécurité

Il faut y faire **très attention**.

Le fichier config.py contient des informations sensibles (mots de passe).
L'utilisation de mesnotes.py peut laisser une trace du mot de pass dans 
l'historique du shell
...


