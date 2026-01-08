# Rapport TP1

## Exercice 1 : Rendu (GitHub) et rapport Markdown — à lire avant de commencer

_DUMANGE Valentine_

**Installation de l'environnement** :
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Versions** :
- Python : 3.12.11
- OS : Linux (WSL2)
- torch : 2.9.1+cu128 , transformers : 4.57.3, plotly : 6.5.1, scikit-learn 1.8.0, pandas : 2.3.3

---

## Exercice 2 : Découverte du tokenizer GPT-2

### Tokenizer
Nous créons le script `ex1_tokenizer.py` qui va charger le tokenizer gpt-2 et tester la tokenisation sur une phrase : ` "Artificial intelligence is metamorphosing the world!" `

![tokenizer_example](./img/Capture%20d’écran%202026-01-08%20100245.png)

La sortie est la suivante :
```
['Art', 'ificial', 'Ġintelligence', 'Ġis', 'Ġmet', 'amorph', 'osing', 'Ġthe', 'Ġworld', '!']
```

On remarque que certains tokens commencent par des symboles spéciaux comme `Ġintelligence`, `Ġis` ou encore `Ġworld`. En réalité, on comprend facilement que le caractère `Ġ` représente un espace avant le mot compréhensible pour le modèle. Ainsi le modèle différencie les mots complets `Ġworld`, des mots scindés `Ġmet` + `amorph` + `osing`. Cela garantit que le modèle peut générer du texte avec un espacement correct et traiter efficacement un vocabulaire étendu.

### Details tokens

|       Token       |  ID   |             Remarque             |
| :---------------: | :---: | :------------------------------: |
|      `'Art'`      | 8001  |    Début de mot (sans espace)    |
|    `'ificial'`    | 9542  | Continuation du mot "Artificial" |
| `' intelligence'` | 4430  |     Mot complet avec espace      |
|      `' is'`      |  318  |     Mot complet avec espace      |
|     `' met'`      | 1138  | Début de mot composé avec espace |
|    `'amorph'`     | 37670 | Continuation de "metamorphosing" |
|     `'osing'`     | 2752  |     Fin de "metamorphosing"      |
|     `' the'`      |  262  |     Mot complet avec espace      |
|    `' world'`     |  995  |     Mot complet avec espace      |
|       `'!'`       |   0   |           Ponctuation            |

**Différence entre tokens et token IDs** :

Les **tokens** sont les représentations textuelles (ex: `'Art'`, `'Ġintelligence'`) tandis que les **token IDs** sont leurs identifiants numériques uniques (ex: 8001, 4430) dans le vocabulaire du modèle.

**Remarques sur la tokenisation GPT-2** :

1. **Mots courants vs rares** : Les mots courants et courts comme `' is'`, `' the'`, `' world'` sont tokenisés en un seul token incluant l'espace. En revanche, le mot rare "metamorphosing" est découpé en 3 sous-tokens (`'Ġmet'` + `'amorph'` + `'osing'`). Cela illustre le principe BPE qui réutilise des fragments fréquents du vocabulaire pour construire des mots rares.

2. **Gestion des espaces** : Le tokenizer encode systématiquement les espaces via le préfixe `Ġ` pour distinguer les frontières de mots. Ainsi `'Art'` (sans espace) se différencie de `'Ġintelligence'` (avec espace initial). Cette approche permet au modèle de reconstruire correctement l'espacement lors de la génération.

3. **Ponctuation** : La ponctuation comme `'!'` est traitée comme un token séparé (ID 0), sans espace attaché. Cela permet au modèle de gérer flexiblement la ponctuation indépendamment des mots adjacents.

4. **Fréquence des IDs** : Les mots courants ont des IDs bas (`' the'` = 262, `' is'` = 318, `' world'` = 995) tandis que les fragments rares ont des IDs très élevés (`'amorph'` = 37670). Cela reflète l'ordre de construction du vocabulaire BPE : les paires les plus fréquentes sont ajoutées en premier.


### Nouvel Exemple

Nous changeons de phrase : ` "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism." `

Nous obtenons ces tokens :

```
['G', 'PT', 'Ġmodels', 'Ġuse', 'ĠB', 'PE', 'Ġtoken', 'ization', 'Ġto', 'Ġprocess', 'Ġunusual', 'Ġwords', 'Ġlike', 'Ġant', 'idis', 'establishment', 'arian', 'ism', '.']
```

`antidisestablishmentarianism` a 5 sous tokens : `['ant', 'idis', 'establishment', 'arian', 'ism']`

**Explication du découpage** :

On remarque que ce mot très rare de 28 lettres n'existe pas tel quel dans le vocabulaire GPT-2. Le tokenizer utilise donc le principe BPE pour le découper en morceaux qu'il connaît déjà : `'ant'` (préfixe), `'idis'`, `'establishment'` (mot courant), `'arian'` et `'ism'` (suffixe fréquent). Cela permet au modèle de comprendre n'importe quel mot, même jamais vu auparavant, en le reconstruisant à partir de fragments déjà présents dans son vocabulaire. BPE essaie d'avoir un vocabulaire limité tout en étant capable de représenter n'importe quel texte.

---

## Exercice 3 : Analyse des encodages positionnels dans GPT-2

### Encodage Positionnel

Nous créons à présent un fichier `TP1/ex2_positions.py` pour charger le modèle GPT-2 et extraire les encodages positionnels.

Voici l'output de notre script : 
```bash
Shape position embeddings: torch.Size([1024, 768])
n_embd: 768
n_positions: 1024
```

**Interprétation de la shape `[1024, 768]`** :

- **1024** = Le contexte peut contenir jusqu'à 1024 tokens (nombre de positions possibles des tokens : `n_positions = 1024`). Si le texte est trop long, il faut le tronquer ou utiliser des fenêtres glissantes.
- **768** = dimension de l'embedding pour chaque position (`n_embd: 768)

### Visualisation des encodages TOP 50

Nous rajoutons un bout de code au script pour pouvoir afficher une pca des 50 premières positions.

![encoding_positions_50](./img/Capture%20d’écran%202026-01-08%20105944.png)

**Observations sur la visualisation PCA** :

On observe que les encodages positionnels forment une **trajectoire courbe continue** dans l'espace réduit à 2 dimensions. Les points sont colorés selon leur position (du bleu foncé pour la position 0 au jaune pour la position 50) et font une parabole. Cette continuité montre que les positions voisines ont des encodages similaires, ce qui permet au modèle de comprendre la notion de proximité temporelle. Les premieres positions sont assez éloignées surtout entre 0 et 1 puis se rapproche petit à petit, ce qui montre que les débuts de séquence sont plus critiques pour le modèle. Les encodages de début de texte sont plus distinctifs que ceux de fin où l'on voit un regroupement de points.

**Intérêt de la PCA** :

La PCA (Analyse en Composantes Principales) permet de réduire les 768 dimensions originales à seulement 2 dimensions visualisables. Cela nous aide à comprendre la structure des encodages positionnels qui serait impossible à observer directement dans l'espace à 768 dimensions.

### Visualisation des encodages TOP 200

Nous essayons maintenant de visualiser le top 200 des positions.

![encoding_positions_200](./img/Capture%20d’écran%202026-01-08%20111000.png)

**Comparaison (0-50) vs (0-200)** :

Avec 200 positions, on voit que les points forment un **cercle** ou une **spirale**, alors qu'avec 50 positions on ne voyait qu'un petit arc. L'échelle plus grande révèle que GPT-2 organise les positions de manière circulaire. Les 50 premiers points sont juste un petit morceau de la spirale. En réalité, la représentation a changé car la pca aussi.

**Hypothèse sur la représentation des positions** :

GPT-2 utilise probablement des **fonctions sinusoïdales** (sin/cos) pour encoder les positions, ce qui crée cette forme circulaire. Cela permet de garder les positions voisines proches tout en évitant de confondre des positions éloignées. C'est plus efficace qu'un simple compteur linéaire (1, 2, 3...) car ça permet de représenter 1024 positions dans seulement 768 dimensions.

---

## Exercice 4 : Probabilités et génération de texte avec GPT-2

Dans cet exercice, nous allons étudier comment les modèles de type Transformer génèrent du texte et comment ils attribuent des probabilités à chaque tokens.

### Probabilités conditionnelles

Nous commençons par créer `TP1/ex3_probs.py` dans lequel nous chargeons GPT2LMHeadModel et le tokenizer correspondant. Puis nous calculons pour chaque token de la phrase ` "Artificial intelligence is fascinating." ` sa probabilité conditionnelle.

**Sortie du script** :
```bash
1 'ificial' 1.920e-05
2 ' intelligence' 1.505e-01
3 ' is' 1.955e-01
4 ' fascinating' 6.504e-04
5 '.' 1.773e-01
```

**Explication de l'alignement** :

On lit la probabilité du token `t` dans les logits à la position `t-1` car GPT-2 prédit toujours le **token suivant**. Quand le modèle traite les tokens de 0 à `t-1`, il calcule des scores pour prédire ce qui vient après, soit le token à la position `t`. Donc les logits à `t-1` contiennent les probabilités de tous les tokens possibles pour la position `t`. C'est pour ça qu'on regarde `probs[0, t-1, tok_id]` pour connaître la probabilité du token `t`.

Dans notre cas, après avoir vu `Art`, GPT-2 a une probabilité de **0.002%** de prédire `ificial`.
La probabilité la plus élevée est celle du `.`. Sachant toute la phrase, il y a une probabilité `17,7%` de mettre un point.

### Log-probabilité totale et Perplexité

Nous rajoutons une partie de code pour calculer la log-probabilité totale ainsi que la perplexité.

**Résultats** :
```bash
total_logp: -23.454866409301758
avg_neg_logp: 4.690973281860352
perplexity: 108.95917620658308
```

**Interprétation de la perplexité** :

La perplexité est un concept clé dans l'évaluation des modèles de langage. Elle mesure la capacité de prédiction d'un modèle en quantitfiant le degré d'incertitude qu'il éprouve face à une séquence de mot.
Plus le chiffre est bas, mieux c'est : le modèle est plus sûr de lui. Une perplexité de **1** = le modèle est certain à 100%. Une perplexité de **50 000** (la taille du vocabulaire) = le modèle devine au hasard. Notre **109** est correct : GPT-2 comprend bien la structure générale (`"Artificial intelligence is..."`) mais est surpris par "fascinating" (seulement **0.065%** de proba).

### Comparaisons

Nous allons calculer maintenant les log-proba et perplexité de ` "Artificial fascinating intelligence is." `

**Résultats** :
```bash
total_logp: -42.16457986831665
avg_neg_logp: 8.43291597366333
perplexity: 4595.882043770468
```

**Comparaison des perplexités** :

| Phrase | Perplexité |
|--------|-----------|
| "Artificial intelligence is fascinating." | **109** |
| "Artificial fascinating intelligence is." | **4596** |
| "L'intelligence artificielle est fascinante." | **383** |


**Interprétations**

**Phrase anglaise**

L'écart est énorme : la deuxième phrase a une perplexité **42 fois plus élevée** ! Cela s'explique par la grammaticalité. La première phrase est correcte ("L'IA est fascinante"), tandis que la deuxième mélange les mots dans un ordre incorrect ("Artificial fascinating intelligence is" n'a aucun sens). GPT-2 a été entraîné sur, je l'imagine, plus de textes bien formés que des mal formés. Il a donc appris les structures grammaticales courantes. Quand on lui présente "Artificial intelligence is", il trouve ça normal (faible perplexité). Mais quand on lui donne "Artificial fascinating intelligence", il est très surpris car cette séquence n'apparaît jamais dans des textes normaux (haute perplexité). Le modèle a appris que les adjectifs viennent généralement après "is" et non entre "Artificial" et "intelligence". GPT-2 a bien capturé les régularités linguistiques et grammaticales de la langue anglaise durant son entraînement.

---
**Phrase française**

La phrase française bien formée a une perplexité de **383**, soit entre les deux phrases anglaises. C'est intéressant : bien que grammaticalement correcte, elle surprend plus le modèle que la phrase anglaise correcte. Cela s'explique par la **distribution d'entraînement** de GPT-2 : le modèle a surement été davantage entraîné sur des textes anglais. Les tokens français sont moins fréquents dans son corpus d'entraînement, donc même une phrase française parfaitement correcte génère plus d'incertitude. De plus, on peut remarquer que les phrases françaises sont découpés en plus de sous tokens que leurs équivalents anglais, augmentant la perplexité. GPT-2 "comprend" un peu le français mais est moins fort qu'en anglais. Ce qui n'est pas étonnant

### Token le plus probable

Après ` "Artificial intelligence is" `, les tokens les plus probables sont :

```bash
' a' 1.204e-01
' the' 5.254e-02
' not' 4.324e-02
' an' 3.092e-02
' now' 2.062e-02
' one' 1.890e-02
' also' 1.880e-02
' already' 1.716e-02
' becoming' 1.606e-02
' just' 1.422e-02
```

**Interprétation**

Les propositions sont plausibles : articles (`' a'`, `' the'`), négation (`' not'`), adverbes (`' now'`, `' already'`, `' becoming'`). Tous commencent par un espace (normal en milieu de phrase) et il n'y a pas de ponctuation dans le top 10 (logique après "is"). Ils sont, de plus, très cohérents grammaticallemnt.

---

## Exercice 5 : Exploration des méthodes de génération avec GPT-2

### Chargement GPT-2 et tokenizer

Nous allons dans cette partie explorer plusieurs méthodes de génération de texte à partir d'un modèle Transformer comme GPT-2.

Pour cela, nous commençons par créer un script `TP1/ex4_generation.py` pour charger GPT-2 et le tokenizer.

Nous fixons la **seed** à **42** pour permettre la reproducibilité.

### Décodage glouton (greedy decoding)

Nous rajoutons un décodage glouton et exécutons le script à 3 reprise.
Voici la première réponse:

```
"We're not sure what the future will look like," said Dr. Michael S. Schoenfeld, a professor of computer science at the University of California, Berkeley. "But we're not
```

![decodage_glouton](./img/Capture%20d’écran%202026-01-08%20112510.png)

Les trois exécutions donnent exactement le même résultat grâce à la **seed fixée à 42**. Le décodage glouton est déterministe : à chaque étape, il choisit toujours le token le plus probable. Avec la même seed, les poids du modèle et l'initialisation sont identiques, donc la génération est parfaitement reproductible.

### Décodage par échantillonnage

Cette fois ci, on génère du texte avec du sampling en utilisant : `température = 0.7, top-k = 50, top-p = 0.95`. Nous faisons 5 générations en changeant la seed.

Voici 2 exemples de génération:

**Résultats**
```
SEED 1
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is up in the air, and the future of artificial intelligence is now about to change. For now, we're just waiting for the technology to be perfected so that we can take it to the next level.

The

----------------------------------------
SEED 3
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is bright and bright. The future of the Internet of Things, and the future of the future of the Internet of Things industry.

The future of the Internet of Things, and the future of the Internet of Things industry
----------------------------------------
```

**Comparaison avec le décodage glouton** :

1. **Respect du prompt** : Le sampling respecte le début "The future of artificial intelligence is..." alors que le greedy a généré un texte différent ("We're not sure..."). 
2. La **diversité** est beaucoup plus élevée avec le sampling : chaque génération est différente alors que greedy donne toujours le même résultat (déterministe). 
3. Par contre, la **cohérence** peut baisser. On distingue des répétitions comme "The future of the Internet of Things, and the future of the Internet of Things" ou "bright and bright". Les **répétitions** sont plus fréquentes avec le sampling car il explore des chemins moins probables qui peuvent créer des boucles.

**Rôle des paramètres** :

- **Température (0.7)** : Contrôle la créativité du modèle. Une température < 1 rend le modèle plus conservateur (favorise les tokens probables), > 1 le rend plus créatif. 0.7 est un bon équilibre.
- **Top-k (50)** : Ne garde que les 50 tokens les plus probables à chaque étape, éliminant les choix très improbables.
- **Top-p (0.95)** : Garde les tokens dont la somme des probabilités atteint 95%, s'adaptant dynamiquement au contexte (parfois beaucoup de tokens, parfois peu).

#### Repetition penalty

Nous rajoutons maintenant une `repetition_penalty=2.0` pour comparer l'effet sur les répétitions. Nous utilisons la même seed (3) et les mêmes paramètres de sampling pour isoler l'effet de la pénalité.

**Sans pénalité (SEED 3, baseline)** :
```
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is bright and bright. The future of the Internet of Things, and the future of the future of the Internet of Things industry.

The future of the Internet of Things, and the future of the Internet of Things industry
```

**Avec pénalité (SEED 3, repetition_penalty=2.0)** :
```
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is bright and exciting. We need a way to capture that information, but it has been very challenging for us," said James Pritchard from the University's Centre on Artificial Intelligence (CAI), who was not involved in
```

**Interprétation** :

Sans pénalité, on observe des répétitions massives tandis qu'avec aucune répétition n'est visible. Le texte est beaucoup plus varié et naturel.
Mais, le texte avec pénalité change de style. Il devient plus formel et structuré (citation d'un professeur, mention d'une institution). 
Il introduit de nouveaux concepts `capture information`, `University's Centr`
On peut imaginer qu'avec une pénalité trop forte, le modèle pourrait s'éloigner du sujet initial et complétement dérivé. Ici ça reste cohérent.

#### Changement température

Nous allons maintennat tester les sorties avec une température très basse puis très élevée.

**Température basse (SEED 3, temperature=0.1)** :
```
SEED 3
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is uncertain. The future of artificial intelligence is uncertain.

The future of artificial intelligence is uncertain. The future of artificial intelligence is uncertain.

The future of artificial intelligence is uncertain. The future of artificial intelligence is
----------------------------------------
```

**Température haute (SEED 3, temperature=2.0)** :
```
SEED 3
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is bright and diverse. That in a way could not occur, but what remains clear is that all these technologies must not fail without a corresponding revolution from a completely autonomous, controlled, well-grounded and autonomous body that can
----------------------------------------
```

**Interprétation** :

La température contrôle l'équilibre entre la **cohérence** (texte prévisible et grammatical) et la **diversité** (texte créatif et varié).

Avec une température très basse de **0.1** , le modèle devient ultra-conservateur : il choisit presque toujours les tokens les plus probables. Résultat : des répétitions en boucle ("The future of artificial intelligence is uncertain" répété 4 fois). Le texte est cohérent grammaticalement mais sans aucune créativité.

Au contraire avec une température très haute de **2.0**, le modèle devient très créatif : il explore des tokens beaucoup moins probables. Le texte est plus diversifié et original ("bright and diverse", "autonomous, controlled, well-grounded"), mais la cohérence devient moins bonne. On voit des formulations étranges comme "That in a way could not occur" ou "must not fail without a corresponding revolution" qui sont grammaticalement justes mais un peu bizarres ensemble.

En réalité, il faut trouver un compromis pour rester cohérent mais en faisant preuve de créativité. Tout dépend de l'application.

### Recherche par faisceau

Nous finissons en essayant la génération avec beam search

#### num_beams=5

**Résultat** :
```
Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.
The future of artificial intelligence is in the hands of the next generation of scientists and engineers.

The future of artificial intelligence is in the hands of the next generation of scientists and engineers.

The future of artificial intelligence is in the hands of
```

**Interprétation** :

Le beam search produit des répétitions encore plus fortes que le greedy ! La même phrase "The future of artificial intelligence is in the hands of the next generation of scientists and engineers" est répétée exactement 2 fois complètes, puis recommence une 3ème fois. Cela ressemble beaucoup au sampling avec une toute petite température. 

C'est paradoxal car le beam search explore 5 chemins différents (num_beams=5), mais converge vers la même séquence répétitive. Le beam search optimise la probabilité globale, pas la diversité ni l'originalité. Sans pénalité de répétition, il tombe dans une boucle car répéter une phrase déjà probable reste probabilistiquement optimal pour le modèle.

#### Augmentation du nombre de beams et impact sur le temps

Nous mesurons maintenant le temps de génération avec différents nombres de beams : 5, 10 et 20.

**Résultats mesurés** :

| num_beams | Temps (secondes) |        Résultat        |
|-----------|------------------|------------------------|
|     5     |      2.137       | Même répétition (2x)   |
|    10     |      2.506       | Même répétition (2x)   |
|    20     |      3.628       | Même répétition (2x)   |

**Observations** :

1. **Augmentation du temps** : Plus on augmente le nombre de beams, plus c'est long.

2. **Résultats identiques** : Malgré l'augmentation des beams, le texte généré reste exactement le même avec les mêmes répétitions. La phrase trouvée est vraiment la plus probable selon le modèle.

**Explications** :

Le beam search garde les `k` meilleures séquences en mémoire à chaque étape. Plus on a de beams, plus le modèle doit faire de calculs à chaque position. Avec 20 beams au lieu de 5, il y a 4 fois plus de chemins à explorer, donc ça prend plus de temps.