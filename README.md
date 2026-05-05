
# Offres IT France – Analyse des offres d'emploi d'ingénieur logiciel (M18)

## Contexte du projet

Ce projet a pour objectif d’analyser l’évolution des offres d’emploi liées aux métiers de l’informatique et plus particulièrement aux postes d’ingénieur logiciel / développement logiciel en France.

L’idée initiale est née d’une réflexion autour de l’évolution du marché de l’emploi tech : les offres diminuent-elles réellement ? Quels territoires recrutent le plus ? Peut-on reconstruire une tendance fiable à partir des données publiques disponibles ?

Le projet combine :

* l’API France Travail (anciennement Pôle Emploi) pour récupérer les offres récentes
* l’open data historique pour reconstruire une tendance sur plusieurs années
* Python pour l’extraction, le nettoyage et la visualisation

---

## Objectifs

### Objectif principal

Construire un indicateur permettant de suivre l’évolution des offres d’emploi IT en France, avec un focus sur le grand domaine métier :

```text
M18 = Informatique et télécommunications
```

### Objectifs secondaires

* récupérer les offres actuellement diffusées
* contourner les limites de pagination de l’API
* comparer les volumes par département
* analyser la distribution temporelle des offres
* construire une série temporelle exploitable (hebdomadaire / mensuelle)
* produire des visualisations lisibles de type FRED / macro-économie

---

## Stack technique

### Langage

* Python 3

### Librairies principales

* requests
* pandas
* matplotlib
* seaborn
* python-dotenv
* datetime
* time
* logging

---

## Structure du projet

```text
offres_IT_France/
│
├── data/
│   └── series_offres_diffusees_T32025.xlsx
├── notebooks/
├── brouillon.py
├── offres_actives.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Accès à l’API France Travail

L’API utilisée est :

```text
API Offres d’emploi v2 (https://www.data.gouv.fr/dataservices/api-offres-demploi)
```

### Authentification OAuth2

Le projet utilise le flux :

```text
client_credentials
```

### Variables d’environnement

Dans un fichier `.env` :

```env
CLIENT_ID=votre_client_id
FT_API_KEY=votre_client_secret
```

### Génération du token

Le script récupère automatiquement un `access_token` via :

```text
https://entreprise.francetravail.fr/connexion/oauth2/access_token
```

---

## Collecte des données

### Requête principale

Filtre principal utilisé :

```python
grandDomaine = "M18"
```

### Pagination

L’API limite l’accès à :

```text
3000 résultats maximum par requête
```

Le projet contourne cette limite en découpant les requêtes par :

* département
  n- parfois par date

### Départements traités

* France hexagonale : 01 à 95
* Corse : 2A / 2B
* Outre-mer : 971, 972, 973, 974, 976

---

## Difficultés rencontrées

### 1. OAuth / invalid_client

Problème rencontré :

```text
400 invalid_client
```

Cause : mauvaise utilisation du `client_id` / `client_secret` et erreurs de configuration.

### 2. Limite API

Erreur :

```text
La position de début doit être inférieure ou égale à 3000
```

Solution : pagination intelligente par département.

### 3. HTTP 204

```text
204 No Content
```

Ce n’est pas une erreur mais simplement la fin des résultats disponibles.

### 4. Historique limité

L’API ne fournit pas un historique complet depuis 2021.

Conclusion :

* API = photographie actuelle du marché
* Open Data = reconstruction historique

---

## Visualisation

Deux approches ont été testées :

### Histogramme brut des dates

Peu lisible lorsque chaque offre possède une date distincte.

### Agrégation par mois (recommandée)

Transformation des dates en série mensuelle :

* plus lisible
* plus pertinente économiquement
* meilleure comparaison temporelle

Objectif final : produire une courbe claire de l’évolution des offres IT.

---

## Résultats attendus

* volume total des offres M18 disponibles
* distribution temporelle des publications
* tendance mensuelle / hebdomadaire
* base exploitable pour analyse du marché de l’emploi tech

---

## Perspectives

Améliorations possibles :

* déduplication des offres
* segmentation par métier précis (développeur, DevOps, Data Engineer…)
* analyse des salaires
* analyse des types de contrat
* dashboard interactif
* comparaison France / international

---

## Lancement du projet

```bash
git clone https://github.com/SraaaaS/offres_IT_France.git
```
```bash
pip install -r requirements.txt
```


## Auteur

Projet personnel réalisé dans une logique de montée en compétences Data / Data Engineering.
