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
- torch : 2.9.1+cu128 , transformers : 4.57.3, plotly : 6.5.1, scikit-learn 1.8.0

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


