from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os

bot = TeleBot("7485312827:AAGI7KoGkPfBCUreZFiaHqA69zBymg6BFJc")
admin = "6150504681"

@bot.message_handler(commands=['start', 'help'])
def reaction_to_start(message: Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name

    if message.text == "/start":
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✉️ Murojaat yuborish", callback_data="murojaat"), InlineKeyboardButton("Yopish", callback_data="yopish"))

        bot.send_message(chat_id, f"👋 <b>Assalomu alaykum {first_name}</b>\n\nQuyidagilardan birini tanlang:", parse_mode='html', reply_markup=markup)
    elif message.text == "/help":
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📝 Loyihalar", callback_data="loyiha"),
            InlineKeyboardButton("◀️ Orqaga", callback_data="menu")
        )

        bot.send_message(chat_id, f"👇 <b>Quyidagilardan birini tanlang:</b>", parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    first_name = call.message.chat.first_name
    data = call.data.split("=")

    if call.data == "loyiha":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("◀️ Orqaga", callback_data="back"))

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="⏱️ <b>Yuklanmoqda...</b>", parse_mode='html')
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"<b>Hozirda mavjud bo'lgan loyihalar:</b>\n\n• @byOpenAIBot\n• @byBusinessBot", parse_mode='html', reply_markup=markup)

    elif call.data == "murojaat":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("◀️ Orqaga", callback_data="menu"))

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"📝 <b>Murojaat matnini kiriting:</b>", parse_mode='html', reply_markup=markup)
        with open(f"{chat_id}.txt", mode='w', encoding='utf-8') as file:
            file.write("murojaat")

    elif call.data == "back":
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📝 Loyihalar", callback_data="loyiha"),
            InlineKeyboardButton("◀️ Orqaga", callback_data="menu")
        )

        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=f"👇 <b>Quyidagilardan birini tanlang:</b>", parse_mode='html', reply_markup=markup)

    elif call.data == "menu":
        markup = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✉️ Murojaat yuborish", callback_data="murojaat"), InlineKeyboardButton("Yopish", callback_data="yopish"))

        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=f"👋 <b>Assalomu alaykum {first_name}</b>\n\nQuyidagilardan birini tanlang:", parse_mode='html', reply_markup=markup)

        try:
            os.remove(f"{chat_id}.txt")
        except FileNotFoundError:
            pass

    elif call.data == "yopish":
        bot.answer_callback_query(call.id, "Bo'lim yopildi!", False)
        bot.delete_message(chat_id=chat_id, message_id=message_id)

        try:
            os.remove(f"{chat_id}.txt")
        except FileNotFoundError:
            pass

    elif len(data) == 2 and data[0] == "javob":
        id = data[1]
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("◀️ Orqaga", callback_data="menu"))

        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=f"📝 <b>Javob matnini kiriting:</b>", parse_mode='html', reply_markup=markup)

        with open(f"{chat_id}.txt", mode='w', encoding='utf-8') as file:
            file.write(f"javob={id}")

@bot.message_handler(func=lambda message: True)
def step(message: Message):
    chat_id = message.chat.id
    from_id = message.from_user.id
    message_id = message.message_id

    try:
        with open(f"{chat_id}.txt", 'r', encoding='utf-8') as file:
            content = file.read().strip()

        back = InlineKeyboardMarkup().add(InlineKeyboardButton("◀️ Orqaga", callback_data="menu"))

        if content == "murojaat":
            javob = InlineKeyboardMarkup().add(InlineKeyboardButton("📝 Javob yozish", callback_data=f"javob={chat_id}"))

            bot.send_message(chat_id, f"✅ <b>Murojaatingiz muvaffaqiyatli yuborildi!</b>", parse_mode='html', reply_markup=back)
            bot.forward_message(chat_id=admin, from_chat_id=from_id, message_id=message_id)
            bot.send_message(admin, f"👇 <b>Javob yozish uchun quyidagi tugmadan foydalanishingiz mumkin!</b>", parse_mode='html', reply_markup=javob)
            os.remove(f"{chat_id}.txt")

        elif content.startswith("javob="):
            id = content.split("=")[1]

            bot.send_message(id, message.text, parse_mode='html')
            bot.send_message(chat_id, f"✅ <b>Javobingiz foydalanuvchiga yuborildi!</b>", parse_mode='html', reply_markup=back)
            os.remove(f"{chat_id}.txt")
    except FileNotFoundError:
        pass

bot.infinity_polling()
