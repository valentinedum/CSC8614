---
email_id: E04
from: "Alice Etudiante <alice.etudiante@tsp-exemple.fr>"
date: "2026-01-12"
subject: "Question sur le cours de Deep Learning"
---

CORPS:
<<<
Monsieur,

Je ne comprends pas bien la formule de la rétropropagation vue au slide 42 du cours d'hier.
Est-ce que le gradient s'annule si la fonction d'activation est une ReLU pour les valeurs négatives ?

Merci d'avance pour votre aide.
Alice.
>>>

ATTENDU:
- intent: reply
- Fournir une explication technique sur la dérivée de ReLU
- Confirmer que le gradient est nul pour x < 0