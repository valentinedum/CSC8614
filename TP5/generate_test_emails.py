import os

# Configuration du dossier de destination
output_dir = os.path.join("TP5", "data", "test_emails")
os.makedirs(output_dir, exist_ok=True)

# Dictionnaire avec des e-mails DIFFÉRENTS du TP4 mais cohérents avec les e-mails ET les PDFs admin
emails_data = {
    "email_01_admin_badge_question.md": """---
email_id: E01
from: "Etudiant <etudiant@telecom-sudparis.eu>"
date: "2026-01-21"
subject: "Question : où retirer un nouveau badge ?"
---

CORPS:
<<<
Bonjour,

J'ai égaré mon badge d'accès au campus. Où puis-je en obtenir un nouveau, et y a-t-il des frais ?
Combien de temps faut-il compter pour que je puisse à nouveau accéder au bâtiment ?

Merci.
>>>

ATTENDU:
- intent: reply
- Indiquer la procédure pour remplacer un badge perdu
- Préciser les délais et les coûts éventuels
- Diriger vers le service scolarité""",

    "email_02_reglement_absence_course.md": """---
email_id: E02
from: "Etudiante <sarah.weber@telecom-sudparis.eu>"
date: "2026-01-20"
subject: "Question sur les absences en cours et sanctions"
---

CORPS:
<<<
Bonjour,

Je dois m'absenter à un cours la semaine prochaine pour raison médicale.
Selon le règlement intérieur, qu'est-ce qui est prévu pour les absences justifiées ?
Y a-t-il une limite au nombre d'absences acceptées avant pénalité ?

Merci.
>>>

ATTENDU:
- intent: reply
- Consulter le Règlement Intérieur (absence, justification)
- Expliquer la procédure d'absence justifiée
- Indiquer les seuils ou les conséquences""",

    "email_03_scolarite_dossier_inscription.md": """---
email_id: E03
from: "Nouvel Admis <jean.thomas@telecom-sudparis.eu>"
date: "2026-01-22"
subject: "Inscription FISE - documents à fournir ?"
---

CORPS:
<<<
Bonjour,

Je viens d'être admis en cycle d'ingénieur FISE. Quels documents dois-je fournir pour finaliser mon inscription ?
Y a-t-il des délais stricts à respecter ?
Le Règlement de scolarité FISE dit-il quelque chose sur les frais ou les modalités de paiement ?

Merci.
>>>

ATTENDU:
- intent: reply
- Consulter le Règlement Scolarité FISE
- Lister les documents requis pour l'inscription
- Préciser les délais et frais""",

    "email_04_charte_ia_formation.md": """---
email_id: E04
from: "Groupe IA <groupe.ia.2026@telecom-sudparis.eu>"
date: "2026-01-19"
subject: "Éthique et IA dans nos projets - comment respecter la charte ?"
---

CORPS:
<<<
Bonjour,

Notre groupe travaille sur un projet d'IA (classification d'emails) pour le TP5.
Nous voulons vérifier que nos approches respectent la charte IA de l'IMT.
Y a-t-il des principes ou des restrictions qu'on doit connaître avant de continuer ?

Merci.
>>>

ATTENDU:
- intent: reply
- Consulter la Charte IMT IA en Formation
- Extraire les principes clés (éthique, transparence, etc.)
- Donner des recommandations pour le projet""",

    "email_05_tp3_groupe_remise.md": """---
email_id: E05
from: "Camarade Groupe <olivier.dupuis@telecom-sudparis.eu>"
date: "2026-01-21"
subject: "TP3 - Avez-vous bien remis le fichier requirements.txt ?"
---

CORPS:
<<<
Bonjour à tous,

Avant de faire la soumission finale du TP3 (Tokenizer et Language Model), je veux vérifier :
- Avez-vous tous les fichiers Python (.py) à jour ?
- Est-ce que le requirements.txt est bien complet avec ALL les dépendances ?
- Devons-nous inclure un rapport à part ou tout dans un notebook ?

Une dernière vérification rapide pour éviter une pénalité de retard.

Merci.
>>>

ATTENDU:
- intent: reply
- Coopération : valider que les fichiers sont prêts
- Clarifier les attentes de format/remise
- Coordonner la soumission finale""",

    "email_06_ambigu_fichier_flou.md": """---
email_id: E06
from: "Prof Inconnu <prof@telecom-sudparis.eu>"
date: "2026-01-20"
subject: "Où est le doc ?"
---

CORPS:
<<<
Bonjour,

Le document que je vous ai demandé hier, tu penses l'avoir pour quand ?
C'est pour valider le dossier de l'équipe, donc ça serait bien d'avoir rapidement.

Tiens-moi au courant.
>>>

ATTENDU:
- intent: ask_clarification
- Demander : quel document au juste ? (titre, sujet, format)
- Demander : envoyé comment (email, Teams, clé USB) ?
- Clarifier le contexte (validation de quel dossier ?)""",

    "email_07_risque_donnees_sensibles.md": """---
email_id: E07
from: "Assistant Admin <asst.admin@telecom-sudparis.eu>"
date: "2026-01-18"
subject: "Mise à jour formulaire - données de contact"
---

CORPS:
<<<
Bonjour,

Veuillez m'envoyer une mise à jour de vos coordonnées personnelles pour le registre du labo :
- Numéro de téléphone personnel
- Adresse personnelle complète
- Email personnel
- Numéro de dossier étudiant

Ces infos seront utilisées uniquement à titre interne pour les relances administratives.

Répondez par email simple.
>>>

ATTENDU:
- intent: escalate
- Identifier la demande de données personnelles sensibles par email simple
- Alerter sur le risque de sécurité
- Proposer un formulaire sécurisé (si disponible)""",

    "email_08_risque_lien_suspect.md": """---
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
- Signaler à l'IT réel si nécessaire"""
}

# Génération des fichiers
print(f"Mise à jour des fichiers dans {output_dir}...")
for filename, content in emails_data.items():
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f" -> {filename} mis à jour avec ATTENDU.")

print("\nTerminé ! Le dataset de test est prêt.")