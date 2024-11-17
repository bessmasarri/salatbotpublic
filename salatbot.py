import time  # Importer la bibliothèque time pour gérer les délais
from telegram import Bot, Update  # Importer les objets Bot et Update de la bibliothèque telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters  # Importer les modules nécessaires de telegram.ext

# Remplacez par votre propre TOKEN
TOKEN = ''  # Insérez ici votre token généré par le BotFather

# Fonction qui s'exécute lorsque l'utilisateur lance la commande /start
def start(update, context):
    chat_id = update.message.chat_id  # Récupérer l'ID de chat de l'utilisateur
    # Enregistrer le chat ID dans un fichier si ce n'est pas déjà fait
    with open('chat_ids.txt', 'a+') as file:  # Ouvrir le fichier chat_ids.txt en mode ajout
        file.seek(0)  # Se placer au début du fichier pour lire son contenu
        chat_ids = file.read().splitlines()  # Lire les IDs des chats et les convertir en liste
        if str(chat_id) not in chat_ids:  # Vérifier si l'ID de chat n'est pas déjà dans la liste
            file.write(f"{chat_id}\n")  # Si ce n'est pas le cas, ajouter cet ID au fichier
    update.message.reply_text("بوت منبه الصلاة على النبي ﷺ |  لإرسال تذكيرات بالصلاة على سيدنا محمد عليه أفضل الصلاة والسلام بشكل تلقائي")  # Répondre à l'utilisateur

# Fonction pour envoyer le message périodiquement
def send_message_periodically(bot):
    with open('chat_ids.txt', 'r') as file:  # Ouvrir le fichier chat_ids.txt en mode lecture
        chat_ids = file.read().splitlines()  # Lire les IDs des chats et les convertir en liste
    for chat_id in chat_ids:  # Pour chaque ID de chat
        bot.send_message(chat_id=chat_id, text="اللهم صل وسلم وبارك على سيدنا محمد")  # Envoyer un message de prière sur le Prophète ﷺ
    time.sleep(1800)  # Attendre 30 minutes (1800 secondes) avant d'envoyer un autre message

if __name__ == '__main__':
    # Initialisation du bot et mise en place des handlers
    updater = Updater(token=TOKEN, use_context=True)  # Créer un objet Updater avec le token du bot
    dispatcher = updater.dispatcher  # Obtenir le dispatcher pour enregistrer les handlers

    # Commande /start pour démarrer la conversation avec le bot
    start_handler = CommandHandler('start', start)  # Créer un handler pour la commande /start
    dispatcher.add_handler(start_handler)  # Ajouter ce handler au dispatcher

    bot = Bot(token=TOKEN)  # Créer un objet Bot avec le token

    # Lancer le bot en mode "polling" pour écouter les nouveaux messages
    updater.start_polling()

    # Boucle infinie pour envoyer des messages périodiquement toutes les 30 minutes
    while True:
        send_message_periodically(bot)  # Appeler la fonction pour envoyer le message périodiquement
