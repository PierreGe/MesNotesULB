# Mes Notes ULB

Ce dépôt contient une collection de scripts pour accéder à MonULB.

Je n'ai, jusqu'ici, pas réussi à me connecter à MonULB en Python à l'aide des
outils usuels (urllib2, requests, mechanize); ces scripts font donc appel à la
commande curl (une approche qui semble fonctionner).

## Dépendances

* Python 2
* curl

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

Ces scripts utilisent curl en ligne de commande, et font au moins une requête
d'authentification: un utilisateur exécutant `top` ou `ps` pourrait voir le mot
de passe en clair.

D'autre part, afin d'éviter les erreurs de connexion à MonULB, les requêtes
ne sont pas vérifiées et sont forcées à TLSv1.

Enfin, le fichier config.py contient des informations sensibles (mots de passe).
Il faut y faire **très attention**.

