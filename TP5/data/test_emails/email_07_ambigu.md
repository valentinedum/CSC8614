---
email_id: E07
from: "Bob <bob@gmail.com>"
date: "2026-01-18"
subject: "C'est pour quand ?"
---

CORPS:
<<<
Salut,

Tu penses que tu pourras me l'envoyer avant demain ? J'en ai vraiment besoin pour avancer sur la partie 2.
Dis-moi si c'est chaud.

A+
>>>

ATTENDU:
- intent: ask_clarification
- Demander de quel document/fichier il s'agit ("l'envoyer")
- Demander la date précise du "demain" si le contexte temporel est flou