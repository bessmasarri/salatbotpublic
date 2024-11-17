# Explication du projet "SalatBot"

## Description
Le "SalatBot" est un bot Telegram simple qui envoie des rappels automatiques pour prier sur le prophète Muhammad (صلى الله عليه وسلم). 

### Fonctionnalités :
1. Lorsque l'utilisateur commence une conversation avec le bot en envoyant `/start`, son ID de chat est enregistré dans un fichier `chat_ids.txt` pour envoyer des rappels à cet utilisateur à intervalles réguliers.
2. Le bot envoie un message toutes les 30 minutes avec le texte suivant : 
   "اللهم صل وسلم وبارك على سيدنا محمد"

### Structure du code :
- **salatbot.py** : Le fichier principal du bot, où l'on initialise le bot, configure les gestionnaires de commandes et envoie les rappels.
- **chat_ids.txt** : Fichier où sont stockés les ID de chat des utilisateurs qui ont démarré le bot. Chaque ID est enregistré sur une nouvelle ligne.
- **requirements.txt** : Liste des dépendances Python nécessaires pour exécuter le bot, notamment `python-telegram-bot`.



