import config
from telebot import types, TeleBot
from email_addres import email, sverka_reg, register, post
from datetime import datetime

bot = TeleBot(config.TOKEN) #Тоукен телеграма
reg_email = {} # Словарь для почты
reg_email.update(sverka_reg()) # Добовление в словарь ранее зарегистрированных пользователей
print(reg_email)
subject_user = {} #Словарь для темы в письме
stop_send = {}
now = datetime.utcnow().strftime('%Y-%m-%d')

@bot.message_handler(commands=['start'], content_types=['text'])
def handler_text(message):  #Главное меню
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Отправить заявку в Service desk')
    user_markup.row('Выбрать тему')
    bot.send_message(message.from_user.id, 'Вас приветствует первый бот КМФ', reply_markup=user_markup)
    if message.from_user.id not in reg_email:
        bot.send_message(message.chat.id, f"Зарегистрируйте ваш почтовый адресс KMF!!!")
        sent = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(sent, save_link)
    if message.from_user.id not in stop_send.keys():
        add_limit = {message.from_user.id: [now, 0]}
        stop_send.update(add_limit)

@bot.message_handler(commands=['stop'])
def handler_text(message):
    hide_marup = types.ReplyKeyboardMarkup(True, True)
    bot.send_message(message.from_user.id, 'Пока'.encode('utf-8'), reply_markup=hide_marup)

@bot.message_handler(content_types=['text', "photo"])
def read_answer(message): #Основные условия
    if message.text == "Новый адрес":
        sent = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(sent, save_link)
    if message.from_user.id not in stop_send.keys():
        add_limit = {message.from_user.id: [now, 0]}
        stop_send.update(add_limit)
    elif stop_send[message.from_user.id][0] != now:
        stop_send[message.from_user.id][1] = 0
        stop_send[message.from_user.id][0] = now
    if message.from_user.id in reg_email and message.from_user.id not in subject_user \
            or message.text == "Выбрать тему":
        keyboard = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Терминал оплаты", callback_data="BOT_SHF_TO")
        item2 = types.InlineKeyboardButton(text="ЭО", callback_data="BOT_SHF_EO")
        item3 = types.InlineKeyboardButton(text="ПК", callback_data="BOT_SHF_ws")
        item4 = types.InlineKeyboardButton(text="Планшет", callback_data="BOT_SHF_tab")
        keyboard.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Выберите тему заявки", reply_markup=keyboard)
    elif message.text == "Отправить заявку в Service desk":

        if message.from_user.id in reg_email.keys():
            if message.from_user.id in subject_user.keys():
                if stop_send[message.from_user.id][1] != 10:
                    stop_send[message.from_user.id][1] += 1
                    sd_send = bot.send_message(message.chat.id, "Вы может описать проблему и отпраить заявку в СД:")
                    bot.register_next_step_handler(sd_send, sd)
                else:
                    bot.send_message(message.chat.id, f"Вы не можете отправить более 10 "
                                                      f"заявок в день через Telegram Bot")
            else:
                bot.send_message(message.chat.id, "Выбрать тему")
        else:
            bot.send_message(message.chat.id, f"Зарегистрируйте выаш почтовый адресс KMF!!!")
            sent = bot.send_message(message.chat.id, "Введите email:")
            bot.register_next_step_handler(sent, save_link)
    elif message.content_type == 'photo' and message.from_user.id not in reg_email:
        sent = bot.send_message(message.chat.id, "По фото я не могу распознать вашь адрес.\nВведите email:")
        bot.register_next_step_handler(sent, save_link)
    else:
        if message.from_user.id in reg_email.keys():
            bot.send_message(message.chat.id, "Вы зарегистрировали вашь Email можете подать заявку. Нажмите "
                                              f"/start для вызова меню")
            print(reg_email)
        else:
            bot.send_message(message.chat.id, f"Зарегистрируйте выаш почтовый адресс KMF!!!")
            sent = bot.send_message(message.chat.id, "Введите email:")
            bot.register_next_step_handler(sent, save_link)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def save_link(message):   # Регистрация ID и почты в фаил и временый документ
    if message.content_type == 'text':
        my_link = message.text
        if email(message.text):
            add_email = {message.from_user.id: my_link}
            register(f'{message.from_user.id}: {my_link.lower()}')
            reg_email.update(add_email)
            bot.send_message(message.chat.id, f"Сохранил: {my_link} \nНажмите /strat для вызова меню")
        else:
            bot.send_message(message.chat.id, f"Вы ввели е-mail адрес с ошибкой или его нет "
                                              f"в списке разрешонных для ШФ")

@bot.callback_query_handler(func=lambda c:True)
def inline(callback):   # Выбор темы
    if callback.data == "BOT_SHF_TO" or callback.data == "BOT_SHF_EO" \
            or callback.data == "BOT_SHF_pk" or callback.data == "BOT_SHF_tab":
        save_subject = {callback.from_user.id: callback.data}
        subject_user.update(save_subject)
    else:
        save_subject = {callback.from_user.id: None}
        subject_user.update(save_subject)

@bot.message_handler(func=lambda message: True, content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def sd(message):   # Определение формата сообщения
    from_addr = reg_email[message.from_user.id]
    try:
        if message.content_type == 'photo':
            text_photo = message.caption
            id_photo = message.photo[2].file_id
            file_info = bot.get_file(id_photo)
            print(f'http://api.telegram.org/file/bot{config.TOKEN}/{file_info.file_path}')  # Выводим ссылку на файл

            if text_photo is None:
                bot.send_message(message.chat.id, f"Фото должно содержать комментарий об ошибке, без комментария "
                                                  f"к фото содержащих описание проблемы заявка не будет отправлена.")
            else:
                subject = subject_user[message.from_user.id]
                path = f'http://api.telegram.org/file/bot{config.TOKEN}/{file_info.file_path}'
                post(from_addr, subject, text_photo, path)
                bot.send_message(message.chat.id, f"Ваша заявка успешна отправлена с адреса: {from_addr}")
        elif message.content_type == 'text' and message.text != "Отправить заявку в Service desk" and message.text != \
                "Выбрать тему":
            subject = subject_user[message.from_user.id]
            path = None
            body_text = message.text
            post(from_addr, subject, body_text, path)
            bot.send_message(message.chat.id, f"Ваша заявка успешна отправлена с адреса: {from_addr}")
        else:
            bot.send_message(message.chat.id, f"Данный формат заявки не допустим или не коректно описали тему")
    except Exception as err:
        print("Произошла ошибка:\n", err)

bot.polling(none_stop=True)

