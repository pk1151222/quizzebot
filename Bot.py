import os
import json
import random
import nltk
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data (first-time usage)
nltk.download('punkt')
nltk.download('stopwords')

# Load environment variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")

# File paths
LEADERBOARD_FILE = "leaderboard.json"
QUESTIONS_FILE = "questions.json"

# Initialize global variables
global_questions = []
quiz_data = {"questions": [], "current_question": 0, "score": 0}
TOP_N = 10  # Limit leaderboard to top N users

# Generate a unique session ID for the current session
SESSION_ID = datetime.now().strftime("%Y%m%d%H%M%S")

# Load or initialize leaderboard
if os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        leaderboard = json.load(f)
else:
    leaderboard = {}

# Load or initialize questions
if os.path.exists(QUESTIONS_FILE):
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        global_questions = json.load(f)
else:
    global_questions = []

# Utility functions
def save_leaderboard():
    """Save the leaderboard to the JSON file."""
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)

def save_questions():
    """Save the questions to the JSON file."""
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(global_questions, f, ensure_ascii=False, indent=4)

def validate_answer(user_answer, correct_answer):
    """Validate the user's answer using basic NLP techniques."""
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    user_tokens = [word.lower() for word in word_tokenize(user_answer) if word.lower() not in stop_words]
    correct_tokens = [word.lower() for word in word_tokenize(correct_answer) if word.lower() not in stop_words]

    # Check if the user's answer contains any correct tokens
    matching_tokens = set(user_tokens) & set(correct_tokens)
    
    # If at least one matching token exists, consider it a correct answer
    if matching_tokens:
        return True
    return False

# Command handlers
async def send_question(update: Update):
    """Send the current quiz question."""
    user = update.effective_user
    user_data = leaderboard.get(user.id, {"questions_answered": [], "score": 0, "session": SESSION_ID})

    if len(user_data["questions_answered"]) == len(global_questions):
        await update.message.reply_text("🎉 You have completed all questions!")
        return

    remaining_questions = [
        q for i, q in enumerate(global_questions) if i not in user_data["questions_answered"]
    ]
    question = random.choice(remaining_questions)
    question_index = global_questions.index(question)

    question_text = f"Q{question_index + 1}: {question['question']}"
    options = [
        InlineKeyboardButton(opt, callback_data=opt) for opt in question["options"]
    ]
    keyboard = InlineKeyboardMarkup.from_column(options)

    await update.message.reply_text(question_text, reply_markup=keyboard)

    # Track current question for the user
    user_data["current_question"] = question_index
    leaderboard[user.id] = user_data
    save_leaderboard()

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's answer and provide feedback."""
    query = update.callback_query
    await query.answer()
    selected_answer = query.data

    user = update.effective_user
    user_data = leaderboard.get(user.id, {"questions_answered": [], "score": 0, "session": SESSION_ID})
    current_question_index = user_data.get("current_question")
    question = global_questions[current_question_index]
    correct_answer = question["correct_answer"]

    if validate_answer(selected_answer, correct_answer):
        user_data["score"] += 1
        await query.edit_message_text("✅ Correct!")
    else:
        await query.edit_message_text(f"❌ Incorrect! Correct answer: {correct_answer}")

    # Mark question as answered
    user_data["questions_answered"].append(current_question_index)
    leaderboard[user.id] = user_data
    save_leaderboard()

    await send_question(update)

async def show_leaderboard(update: Update):
    """Display the leaderboard with top scores for the current session."""
    if not leaderboard:
        await update.message.reply_text("🏆 No scores available yet.")
        return

    leaderboard_text = f"🏆 Top {TOP_N} Leaderboard (Session {SESSION_ID}):\n"
    session_leaderboard = [
        (user_id, data) for user_id, data in leaderboard.items() if data["session"] == SESSION_ID
    ]
    sorted_session = sorted(session_leaderboard, key=lambda x: x[1]["score"], reverse=True)
    for rank, (user_id, data) in enumerate(sorted_session[:TOP_N], 1):
        leaderboard_text += (
            f"{rank}. @{data['username']}: {data['score']} points\n"
        )

    await update.message.reply_text(leaderboard_text)

async def show_commands(update: Update):
    """Show the available commands to the user."""
    commands_text = """
    Here are the available commands:
    /start - Start the quiz
    /leaderboard - Show the leaderboard
    /help - Show this help message
    """
    await update.message.reply_text(commands_text)

def main():
    """Main function to start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", send_question))
    application.add_handler(CommandHandler("leaderboard", show_leaderboard))
    application.add_handler(CommandHandler("help", show_commands))
    application.add_handler(CallbackQueryHandler(handle_answer))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
