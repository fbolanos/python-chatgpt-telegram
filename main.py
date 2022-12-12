import logging

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import openai

openai.api_key = "ENTER_HERE_YOUR_OPENAI_API_KEY"
telegram_bot_api_key = 'ENTER_HERE_YOUR_TELEGRAM-BOT_API_KEY'
MAX_TOKENS = 1200
TEMPERATURE = 0.7
PREVIOUS_CONTEXT_KEYWORD = '@@\n'

list_of_chat_histories = []

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TextHistory():
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.text_history = ''
        
    def check_id(self, current_chat_id):
        return self.chat_id == current_chat_id
    
    def add_to_last_message(self, chat_id, message):
        if not self.check_id(chat_id):
            return
        else:
            self.text_history += (message + '\n\n')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    b_found_chat_history = False
    for chat_obj in list_of_chat_histories:
        if chat_obj.check_id(update.effective_chat.id):
            start_message = 'A chat history object already exists for you. Converse as you normally would.'
            b_found_chat_history = True
            
    if not b_found_chat_history:
        start_message = "Created a new chat history object for you. If you wish for chatGPT to take into account the previous message, please beging your message with {}. If no {} is found then chatGPT will only use the context in your current message to respond to your query."
        
    chat_obj = TextHistory(update.effective_chat.id)
    list_of_chat_histories.append(chat_obj)
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)
    
    
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    b_found_chat_history = False
    chat_history_obj = None
    for chat_obj in list_of_chat_histories:
        if chat_obj.check_id(update.effective_chat.id):
            b_found_chat_history = True
            chat_history_obj = chat_obj
            break
    
    if not b_found_chat_history:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text='Unable to find your chat history object, please start the conversation with a \'/start\' message.'.format(PREVIOUS_CONTEXT_KEYWORD, PREVIOUS_CONTEXT_KEYWORD))
        return
    
    if PREVIOUS_CONTEXT_KEYWORD in update.message.text:
        update.message.text = update.message.text.replace(PREVIOUS_CONTEXT_KEYWORD, '')
        
        chat_history_obj.add_to_last_message(update.effective_chat.id, update.message.text)
        
        full_query = chat_history_obj.text_history
    else:
        chat_history_obj.text_history = ''
        chat_history_obj.add_to_last_message(update.effective_chat.id, update.message.text)
        full_query = chat_history_obj.text_history
        
    
    result = openai.Completion.create(model="text-davinci-003",
                                      prompt=full_query,
                                      temperature=TEMPERATURE,
                                      max_tokens=MAX_TOKENS,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0)
    
    
    prompt_response = result['choices'][0]['text']
    chat_history_obj.add_to_last_message(update.effective_chat.id, prompt_response)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=prompt_response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_bot_api_key).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
