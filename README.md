# Mes Notes ULB

Ce dépôt contient une collection de scripts pour accéder à MonULB.

L'approche prise par ceux-ci peut sembler étrange, mais c'est la première à 
fonctionner, puisque des erreurs de protocole TLS adviennent lorsqu'on utilise
les outils standard (urllib, requests, mechanize, ...).

## Dépendances

* Python 2, virtualenv, pip
* curl

## Installation

	git clone git@github.com:titouanc/MesNotesULB.git
	cd MesNotesULB
	virtualenv --distribute ve
	source ve/bin/activate
	pip install -r requirements.txt

# Les scripts

## mesnotes.py

Permet d'afficher l'ensemble du relevé de notes actuel, ainsi qu'une estimation
de la moyenne pondérée. S'utilise uniquement en ligne de commande

## notify_notes.py

Permet d'envoyer un email dès qu'une nouvelle cote est disponible.
Il est intéressant de noter que les groupes Facebook ont une adresse email.

Ce script nécessite un fichier de configuration. Un exemple est fourni dans
`config.py.example`. Il peut être facilement utilisé dans un cron
