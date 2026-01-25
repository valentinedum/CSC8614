# Rapport TP5

## Exercice 1 : Mise en place de TP5 et copie du RAG (base Chroma incluse)

Nous relançons ollama sur un nouveau port `11500` et adaptons le code de `rag_answer.py` pour écouter ollama sur le bon port.
```
docker run -d --gpus=all   --name ollama_tp5   -v ollama:/root/.ollama   -p 11500:11434   ollama/ollama
```

On exécute le script avec une question du TP4 :

![ollama_test](./img/Capture%20d’écran%202026-01-22%20082828.png)

## Exercice 2 : Constituer un jeu de test (8–12 emails) pour piloter le développement

### Création dataset

Nous générons un petit dataset de **8 e-mails de test** cohérent avec le contexte du TP4.

Le jeu de test est stratégiquement conçu pour faire référence aux **e-mails réels du TP4** et aux **PDFs administratifs du TP4** :
  - `Charte_IMT_IA_en_formation.pdf` 
  - `Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf`
  - `Reglement_scolarite_FISE_conseil_ecole_22_mai_2025.pdf`

Cela permet au **RAG de retrouver des sources pertinentes** tout en testant **8 cas d'usage distincts** :

| Email | Catégorie | Intent attendu |
|-------|-----------|-----------------|
| **E01** | Administrative | `reply` |
| **E02** | Réglementation | `reply` |
| **E03** | Scolarité | `reply` |
| **E04** | Éthique IA | `reply` |
| **E05** | Coordination | `reply` |
| **E06** | Ambigu | `ask_clarification` |
| **E07** | Risque PII | `escalate` |
| **E08** | Risque Phishing | `ignore` |

Voici un exemple :

```markdown
---
email_id: E08
from: "System Admin <admin@telecom-cloud.fake>"
date: "2026-01-20"
subject: "[IMPORTANT] Renouvellement de mot de passe immédiat"
---

CORPS:
<<<
ALERTE DE SÉCURITÉ SYSTÈME

Votre session d'authentification a été compromise. 
Action requise IMMÉDIATEMENT :

Cliquez ici pour réinitialiser votre mot de passe :
http://portal-secure-telecom.fake-domain.ru/reset?token=xyz123&user=YOU

IGNOREZ ce message si vous ne l'avez pas demandé (phishing possible).

Administrateur Système
>>>

ATTENDU:
- intent: ignore
- Identifier la tentative de phishing (domaine fake, urgence suspecte)
- NE PAS cliquer sur le lien
- Signaler à l'IT réel si nécessaire
```

Et voici la liste de tous les fichiers :
![architecture](./img/Capture%20d’écran%202026-01-25%20192217.png)

### Chargement dataset

Nous exécutons `TP5/load_test_emails.py` pour charger tous les e-mails de test et les structurer en dictionnaires Python exploitables par l'agent.
![load_dataset](./img/Capture%20d’écran%202026-01-22%20090458.png)

## Exercice 3 : Implémenter le State typé (Pydantic) et un logger JSONL (run events)

Nous créons de nouveaux dossiers pour créer l'agent:
![nv_dossiers](./img/Capture%20d’écran%202026-01-22%20090759.png)

Pour structurer l'agent, on définit un modele de State typé avec Pydantic incluant toutes les infos nécessaires (décisions, spécifications de récupération, preuves docs, budget, ...)
On définit ensuite un logger JSONL pour tracer chaque étape de run.

Nous exéutons `TP5/agent/test_logger` pour vérifier qu'un fichier JSONL est créé.
![jsonl_logger](./img/Capture%20d’écran%202026-01-22%20092208.png)

## Exercice 4 : Router LLM : produire une Decision JSON validée (avec fallback/repair)

Pour l'exercice 4, nous créons les prompts du routeur dans `agent/prompts.py` et le code de classification d'email dans `agent/nodes/classify_email.py`. Le script `test_router.py` permet de tester la génération d'une décision JSON structurée (intent, catégorie, etc.) à partir d'un email, avec validation automatique et réparation en cas d'erreur de format.

![test_router_1](./img/Capture%20d’écran%202026-01-22%20093718.png)

![test_router_2](./img/Capture%20d’écran%202026-01-22%20093801.png)

Le json est valide et l'intent ainsi que la justification sont cohérentes pour une confirmation d'inscription.

## Exercice 5 : LangGraph : routing déterministe et graphe minimal (MVP)

### Prérequis

Nous installons **langgraph** dans notre environnement.
![langgraph_download](./img/Capture%20d’écran%202026-01-22%20102018.png)

La version téléchargée est la `1.0.6`:
![langgraph_version](./img/Capture%20d’écran%202026-01-22%20102331.png)

### Routing

Nous créons notre script de routing `TP5/agent/routing.py` et notre graph avec `TP5/agent/graph_minimal.py` et les testons avec `TP5/test_graph_minimal.py`

![test_graph](./img/Capture%20d’écran%202026-01-22%20105637.png)

Voici les 4 évenements loggés dans le fichier JSONL:
![test_graph_2](./img/Capture%20d’écran%202026-01-22%20110119.png)

Le LLM a réfléchi dans **classify_email** et a décidé **intent: reply**. Le routeur a intercepté l'intent. Le graph s'est dirigé vers le noeud **stub_reply**.

## Exercice 6 : Tool use : intégrer votre RAG comme outil (retrieval + evidence)

Nous allons remplacer les stubs par noeud de retrieval du RAG pour alimenter le state avec de l'**evidence**.

Pour cela, nous créons le fichier `TP5/agent/tools/rag_tool.py ` pour nous donner les outils pour créer les nouveaux noeuds RAG `TP5/agent/nodes/maybe_retrieve.py`.

Nous les incluons dans notre graph en modifiant `TP5/agent/graph_minimal.py` pour qu'il passe par maybe_retrieve en cas de reply.

### Reply avec evidence non vide
Nous testons cette redirection avec `TP5/test_graph_minimal.py`
![retrieve](./img/Capture%20d’écran%202026-01-22%20112859.png)

![retrieve_2](./img/Capture%20d’écran%202026-01-22%20112935.png)

Nous trouvons bien une evidence non vide avec 2 documents avec des informations trouvés.

Le code de redirection a bien marché, on est passé par le noeud **maybe_retrieve**. 

### Evidence vide ou citations invalides

![retrieve_wrong](./img/Capture%20d’écran%202026-01-25%20195249.png)

![retrieve_wrong_2](./img/Capture%20d’écran%202026-01-25%20195314.png)

Ici nous avons un safe mode. Le modèle n'a pas assez d'infos. Il skip le **maybe_retrieve**.

## Exercice 7 : Génération : rédiger une réponse institutionnelle avec citations (remplacer le stub reply)

Nous allons à présent remplacer notre stub reply par un draft reply `TP5/agent/nodes/draft_reply.py`. Ce nœud doit produire une réponse propre, actionnable, et avec citations qui pointent vers les doc_i présents dans state.evidence

Nous testons le graph minimal sur l'email 1 qui avait déjà de bonnes citations mais allons voir s'il y a une différence.
![draft_wrong](./img/Capture%20d’écran%202026-01-22%20190508.png)
![draft_wrong_2](./img/Capture%20d’écran%202026-01-22%20190605.png)

### Hypothèse
Cette fois-ci le modèle dit ne pas avoir suffismeent d'information.

Je vais donc essayé avec comme exemple **true**
Cette fois-ci le modèle répond à chaque fois avec une evidence. **Le LLM est donc pas très bon ou le prompt pas assez détaillé.**
![draft_right](./img/Capture%20d’écran%202026-01-22%20190534.png)

![draft_right_1](./img/Capture%20d’écran%202026-01-22%20190717.png)

## Exercice 8 : Boucle contrôlée : réécriture de requête et 2e tentative de retrieval (max 2)

Nous modifions `TP5/agent/state.py` pour ajouter au modèle AgentState les champs suivants :
- `evidence_ok: bool = False`
- `last_draft_had_valid_citations: bool = False`

![modif_agent](./img/Capture%20d’écran%202026-01-23%20084735.png)

Nous modifions ensuite `TP5/agent/nodes/draft_reply` pour écrire un signal exploitable.

Pour permettre à l'agent de corriger ses erreurs de recherche, nous avons transformé le pipeline linéaire en une boucle de rétroaction. Le nœud `check_evidence.py` agit comme un évaluateur qui valide la qualité des documents trouvés en vérifiant si le LLM a réussi à générer des citations valides. En cas d'échec, le nœud `rewrite_query.py` utilise un LLM pour reformuler intelligemment la requête de recherche, offrant ainsi à l'agent une seconde chance de trouver l'information pertinente.