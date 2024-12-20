

# Quiz Bot  

A simple yet interactive quiz bot built using Python and Telegram Bot API. This bot supports natural language processing (NLP) to validate user answers without relying on external APIs, making it lightweight and independent.  

## Features  

- **Quiz Questions**: Provides multiple-choice questions to users.  
- **Natural Language Processing**: Uses basic NLP to validate answers with tokenization and stopword removal.  
- **Leaderboard**: Tracks user scores and displays session-based and all-time leaderboards.  
- **Interactive Interface**: Uses inline buttons for answering questions.  
- **Custom Question Upload**: Allows users to upload their own quiz questions in JSON format.  

## Requirements  

- Python 3.9 or higher  
- Telegram Bot API token  

### Python Libraries  

The required dependencies are listed in `requirements.txt`:  

```plaintext  
python-telegram-bot==20.3  
nltk==3.8.1  
python-dotenv==1.0.0  
```  

## Installation  

1. Clone the repository:  
   ```bash  
   git clone
https://github.com/pk1151222/quizzebot 
   cd quizzebot
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up environment variables:  
   - Create a `.env` file in the project directory.  
   - Add your Telegram bot token:  
     ```env  
     BOT_TOKEN=your-telegram-bot-token  
     ```  

4. Run the bot:  
   ```bash  
   python bot.py  
   ```  

## Usage  

1. Start the bot by sending the `/start` command on Telegram.  
2. Answer questions by selecting the options provided.  
3. Use `/leaderboard` to check your ranking.  
4. Use `/help` to view available commands.  

## Commands  

- `/start` - Start the quiz.  
- `/leaderboard` - Display the leaderboard.  
- `/help` - Show help and available commands.  

## Custom Questions  

You can upload your own questions in JSON format using the bot.  
### Example JSON Structure  

```json  
[  
  {  
    "question": "What is the capital of France?",  
    "options": ["Paris", "London", "Berlin", "Madrid"],  
    "correct_answer": "Paris",  
    "explanation": "Paris is the capital city of France."  
  }  
]  
```  

Upload the file by attaching it in the Telegram chat. The bot will validate and integrate the questions.  

## How It Works  

1. **Question Delivery**: Questions are fetched from a JSON file and sent to the user one by one.  
2. **Answer Validation**: User answers are validated using basic NLP techniques, such as token matching.  
3. **Leaderboard**: User scores are saved and displayed for each session.  

## File Structure  

```plaintext  
/  
├── bot.py                # Main bot logic  
├── leaderboard.json      # Stores user scores  
├── questions.json        # Stores quiz questions  
├── requirements.txt      # Project dependencies  
├── .env                  # Environment variables  
└── README.md             # Project documentation  
```  

## Contributions  

Contributions are welcome! Feel free to open issues or submit pull requests.  

## License  

This project is licensed under the MIT License.  

## Author  

**Pappu kumar**  
GitHub: [your-username](https://github.com/pk1151222)  

--- 

