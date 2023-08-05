from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters , ContextTypes 

#for dictionary
import json
from difflib import get_close_matches 
import re

max_words = 100

data = json.load(open('dictionary_compact.json'))

TOKEN = '6003572502:AAHCcTNk-9OsFBif34FRwFPZUqJmPBvMme0'
BOT_USERNAME = '@dictionary_dictionary_bot'



#commands
async def start_command(update: Update , context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for choosing me, I can provide meaning for a given word")


async def help_command(update: Update , context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter a word to know the meaning(Enter a single word)")

#responds

def handle_response(text: str) -> str:
    
    word : str =  text.lower()
    possible = get_close_matches(word, data.keys(),n = 3) # n default value = 3
    
    if word in data:
        sentences = re.split(r'(?<=[.!?])\s+', data[word])
        
        # Initialize variables
        result = ''
        word_count = 0
        
        # Iterate through sentences until reaching the word limit
        for sentence in sentences:
            words = sentence.split()
            word_count += len(words)
            
            # Add the sentence to the result
            result += sentence + ' '
            
            # Check if the word limit is reached
            if word_count >= max_words:
                break
        
        return result.strip()
    # if word in data:
    #     match = re.search(r'(.*?)\bfinal clause')
    #     return data[word]
    elif len(possible) > 0:
        return f"Word not found! Try these {possible} :"
    else:
        return 'Word does not exist!'
    
async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message_type :str = update.message.chat.type        #To get the type of message mode(group or private)
    text: str = update.message.text

    #for debug
    print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text: 
            new_text : str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot: ",response)
    await update.message.reply_text(response)

    #to identify error

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused the error {context.error}')




if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    print("Starting bot")
    #commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))

    #message
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #error
    app.add_error_handler(error)

    print("Polling")
    #time period to check new messages
    app.run_polling(poll_interval=3)
