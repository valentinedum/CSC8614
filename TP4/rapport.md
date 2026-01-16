# Rapport TP4

## Exercice 1 : Démarrage d'Ollama (local ou cluster)

### Téléchargement de l'image et run du Conteneur
Nous choisissons de faire l'installation de Ollama via Docker avec la commande suivante :

```bash
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama
```

Nous pouvons vérifier que ça a bien été installé (le port de Ollama étant `11434` par défaut):
![ollama_check](./img/Capture%20d’écran%202026-01-16%20093357.png)

### Téléchargement du modèle
Nous faisons le choix de travailler avec mistral (IA française donc très à l'aise avec la langue).

```bash
(base) duman@PC-Valentine:~/CSC8614$ docker exec -it ollama ollama pull mistral
pulling manifest
pulling f5074b1221da: 100% ▕██████████████████████████████████████████████████▏ 4.4 GB
pulling 43070e2d4e53: 100% ▕██████████████████████████████████████████████████▏  11 KB
pulling 1ff5b64b61b9: 100% ▕██████████████████████████████████████████████████▏  799 B
pulling ed11eda7790d: 100% ▕██████████████████████████████████████████████████▏   30 B
pulling 1064e17101bd: 100% ▕██████████████████████████████████████████████████▏  487 B
verifying sha256 digest
writing manifest
success
```

Petit test :
![test_mistral](./img/Capture%20d’écran%202026-01-16%20093220.png)

## Exercice 2 : Constituer le dataset (PDF administratifs + emails IMAP) et installer les dépendances

Nous consituons notre dataset qui sera composé de `cache`, `admin_pdfs` et d'`emails`
.
Pour les pdf de l'administration, nous choisissons ceux-ci:
![admin_pdfs](./img/Capture%20d’écran%202026-01-16%20094542.png)

Pour les emails, nous écrivons un petit script `download_emails_imap.py` qui se connecte à IMAP (z.imt.fr) et qui sauvegarde tous les emails depuis une date donnée en .md .
![emails_download](./img/Capture%20d’écran%202026-01-16%20095523.png)

`51` emails on été téléchargés. Voici un exemple du début d'un mail :
![emails_head](./img/Capture%20d’écran%202026-01-16%20095905.png)

## Exercice 3 : Indexation : charger PDFs + emails, chunker, créer l’index Chroma (persistant)

Nous allons écrire un script `TP4/build_index.py` qui va charger les documents, les chunker et les indexer via Chroma.
Nous éxecutons le script.
![index_chroma](./img/Capture%20d’écran%202026-01-16%20105556.png)

L'index existe bien.
![chrom_check](./img/Capture%20d’écran%202026-01-16%20104549.png)

## Exercice 4 : Retrieval : tester la recherche top-k (sans LLM) et diagnostiquer la qualité

Nous créons cette fois-ci un script `TP4/test_retrieval.py` pour le top-k chunks et voir si ce sont les bons documents qui remontent.

Puis nous testons le script avec : 

```
python TP4/test_retrieval.py "Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?"
python TP4/test_retrieval.py "Comment valider une UE ?"
```

Les résultats étant peu satisfaisant avec `CHUNK_SIZE=2000` et `CHUNK_OVERLAP=200` pour la premiere question, j'ai pris `CHUNK_SIZE=500` et `CHUNK_OVERLAP=50`. Ainsi, je pensais que ça aiderait à chercher l'information spécifique `Luca Benedetto`.

### 1
```bash
python TP4/test_retrieval.py "Comment valider une UE ?"
================================================================================
[QUERY] Comment valider une UE ?
[RESULTS] top-5
================================================================================

[1] (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
     - un diplômé de Télécom SudParis choisi par le Directeur de l’Ecole. ...

[2] (admin_pdf) Reglement_scolarite_FISE_conseil_ecole_22_mai_2025.pdf
     la composent n'est strictement inférieure à 7/20.  La validation d'une UE du tronc commun entraîne pour l'étudiant l'acquisition de la totalité  des crédits ECTS attribués aux ECUE qui la composent (voir fiche programme). En cas de  non validation d'une UE, l'étudiant n'acquiert que les crédits ECTS ...

[3] (admin_pdf) Reglement_scolarite_FISE_conseil_ecole_22_mai_2025.pdf
     durant cette deuxième année est telle qu'un étudiant bénéficie d’un certain degré de liberté  dans ses choix en ayant la possibilité d’obtenir jusqu'à 14 ECTS de plus que les 60 exigés  (cf § 8.8) gardant ainsi la possibilité de valider son année même s’il ne valide pas tous les  enseignements sur l ...
```
### 2
```bash
python TP4/test_retrieval.py "Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?"
================================================================================
[QUERY] Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?
[RESULTS] top-5
================================================================================

[1] (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
     - un diplômé de Télécom SudParis choisi par le Directeur de l’Ecole. ...

[2] (email) 202512_re_env_5001__retours_soutenance_intermdiaire_1986273039.md
     Bonsoir,    Je vous contacte par rapport aux retours sur les soutenances de mi-parcours.    Comme mon groupe (MAIA - Sujet 2, Groupe 1) et moi-même vous l'avions fait remonter le 18 novembre, nous avons énormément peiné à débuter le projet. ...

[3] (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
     - le Directeur des relations internationales ou son représentant ; ...
```


**Interprétation**:
1. Les chunks contiennent des réponses correctes. Mais il y a une légère redondance sur le même PDF (normal vu que le PDF détaille différents aspects). Avoir diminué la chunk_size n'a pas amélioré la réponse.
2. Aucune réponse directe à la question. Les sujets sont en liens avec le PFE pour certains ou avec des projets (2) mais pas avec `Luca Benedetto`.

## Exercice 5 : RAG complet : génération avec Ollama + citations obligatoires

Nous allons, à présent, créer un script `TP4/rag_answer.py` pour passer du retrieval à une réponse générée et sourcée. 

### Test avec contexte connu

Puis nous testons l'exécution.
![test_rag](./img/Capture%20d’écran%202026-01-16%20113322.png)

**Interprétation**:
1. Pour la première exécution, le rag répond en français mais "déduit" qu'un sujet est proposé par Luca Benedetto même si le modèle ne le mentionne pas. Le modèle invente un lien avec un mail que j'ai envoyé pour suggérer mon sujet de PFE. Cela indique, que le contexte n'a pas été considéré comme non suffisant. Peut-être faudrait-il rajouter des règles plus strictes.
2. La deuxième exécution a très bien marché. La réponse est en claire et français. La citation est présente et les sources sont courectes.

### Test avec contexte inconnu

Cette fois-ci nous testons avec une information que le rag ne contient pas dans son contexte. 

![test_rag_inconnu](./img/Capture%20d’écran%202026-01-16%20114450.png)

**Interprétation**:
Le nouveau prompt stricte fonctionne correctement. Le RAG refuse de répondre sur un sujet hors-domaine (météo). Il indique les 2 informations manquantes et justifie qu'il ne le trouve pas dans les sources.
Ici, contrairement à la question avec Benedetto, le RAG comprend qu'il n'a absolument pas la réponse.

## Exercice 6 : Évaluation : créer un mini dataset de questions + mesurer Recall@k + analyse d’erreurs

