import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline
import os

# Set up a SQLite database to store messages
def setup_database():
    conn = sqlite3.connect("chat_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            user_id INTEGER,
            username TEXT,
            message TEXT,
            chat_id INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Log messages to the database
def log_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"
    message = update.message.text
    chat_id = update.message.chat_id
    timestamp = update.message.date.isoformat()

    conn = sqlite3.connect("chat_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_id, username, message, chat_id, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, message, chat_id, timestamp))
    conn.commit()
    conn.close()

# Analyze stored messages (example: word frequency)
def analyze_chats(update: Update, context: CallbackContext):
    conn = sqlite3.connect("chat_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM chats")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Example: Count word frequency
    word_count = {}
    for message in messages:
        for word in message.split():
            word_count[word] = word_count.get(word, 0) + 1

    top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
    result = "\n".join([f"{word}: {count}" for word, count in top_words])
    update.message.reply_text(f"Top Words:\n{result}")

# Predefined Responses
def auto_reply(update: Update, context: CallbackContext):
    message = update.message.text.lower()

    # Define some keywords and responses
    responses = {
        "hello": "Hi there! How can I help you?",
        "help": "Here are some commands you can use: /start, /help, /analyze",
        "rules": "Please follow the group rules and be respectful to others."
    }

    # Find a matching response
    for keyword, reply in responses.items():
        if keyword in message:
            update.message.reply_text(reply)
            return

    # Default reply
    update.message.reply_text("I'm sorry, I didn't understand that.")

# NLP-based responses
chat_model = pipeline("conversational", model="microsoft/DialoGPT-medium")

def auto_reply_nlp(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = chat_model(user_message)
    update.message.reply_text(bot_reply[0]["generated_text"])

# Main function
def main():
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Make sure to set your bot token in the environment

    setup_database()  # Initialize database
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("analyze", analyze_chats))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, log_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply_nlp))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
