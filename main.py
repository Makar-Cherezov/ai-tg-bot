import openai
import telebot

openai.api_key = "zSrX_bnbc8hAGvfQpKHihV1wkeibkQqnVqcMZwyXHm8"
openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"

token = "5586927712:AAFhmpOYByhi18KrcVCwnywkvg0zMHiJX_A"
bot = telebot.TeleBot(token)

init_message_chain = [{'role': 'system',
                       'content': "Now act as a helpful translator with deep knowledge in English and Russian. Use formal style. Avoid repeating words. Make translated text look like a great article."},
                      {'role': 'user', 'content': 'Tell me about yourself.'}]
message_chain = init_message_chain.copy()

def get_resp(chain):
    response = openai.ChatCompletion.create(
        model='llama-2-70b-chat',
        messages=chain,
        allow_fallback=True
    )
    return response["choices"][0]["message"]['content']

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет! На генерацию ответов нужно некоторое время, не пугайся ожидания. Бот пока работает на английском, но возможно, это временно.")
    resp = get_resp(init_message_chain)
    bot.send_message(message.chat.id, resp)
    message_chain.append({'role': "assistant", 'content': resp})

@bot.message_handler(commands=['clean'])
def clean_chain(message):
    global message_chain
    message_chain.clear()
    message_chain = init_message_chain.copy()
    bot.send_message(message.chat.id, "Previous context is now being ignored.")

@bot.message_handler()
def get_prompt(message):
    bot.send_message(message.chat.id, "Hmmm, let me see...")
    message_chain.append({'role': "user", 'content': message.text})
    resp = get_resp(message_chain)
    bot.send_message(message.chat.id, resp)
    message_chain.append({'role': "assistant", 'content': resp})

bot.infinity_polling()
