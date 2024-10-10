from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.utils.helpers import escape_markdown

# ID администратора
ADMIN_CHAT_ID = 1829318372  # Замените на ваш ID администратора

# Приветственное сообщение
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Приемка квартиры", callback_data='apartment_check')],
        [InlineKeyboardButton("Взыскание с застройщика", callback_data='builder_claim')],
        [InlineKeyboardButton("Наши контакты", callback_data='contact_info')]
    ]
    message = ("Это бот-помощник юридической компании Legal Solutions GROUP.\n\n"
               "Наши услуги:\n"
               "• Приемка квартиры\n"
               "• Строительно-техническая экспертиза\n"
               "• Оценка стоимости устранения недостатков качества отделки\n"
               "• Полное юридическое сопровождение\n\n"
               "Мы гарантируем вам спокойствие и полную уверенность, что все недостатки будут устранены, "
               "либо застройщик выплатит денежную компенсацию.")
    
    if update.message:
        update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        query = update.callback_query
        query.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

# Игнорирование сообщений, если пользователь не заполняет анкету
def ignore_message(update, context):
    update.message.reply_text("Пожалуйста, используйте кнопки для взаимодействия с ботом.")

# Обработка "Приемка квартиры"
def apartment_check(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Заполнить анкету", callback_data='fill_form_apartment')],
        [InlineKeyboardButton("Наши контакты", callback_data='contact_info')],
        [InlineKeyboardButton("Главное меню", callback_data='go_to_start')]
    ]
    # Деактивировать старые кнопки
    query.edit_message_reply_markup(reply_markup=None)
    # Отправляем новое сообщение с логикой
    context.bot.send_message(chat_id=query.message.chat_id, 
                             text="Строительные эксперты компании «Легальные Решения» проверят Вашу квартиру, "
                                  "замерят площадь, выявят нарушения и составят полный перечень дефектов.")
    query.message.reply_text(text="Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))

# Обработка "Взыскание с застройщика"
def builder_claim(update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Заполнить анкету", callback_data='fill_form_builder')],
        [InlineKeyboardButton("Наши контакты", callback_data='contact_info')],
        [InlineKeyboardButton("Главное меню", callback_data='go_to_start')]
    ]
    # Деактивировать старые кнопки
    query.edit_message_reply_markup(reply_markup=None)
    # Отправляем новое сообщение с логикой
    context.bot.send_message(chat_id=query.message.chat_id, 
                             text="Если застройщик не удовлетворяет требования по устранению недостатков качества квартиры, "
                                  "дольщик вправе получить от застройщика стоимость устранения недостатков качества объекта, компенсацию морального вреда, неустойку и штраф .")
    query.message.reply_text(text="Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard))

# Начало заполнения формы
def start_form(update, context, form_type):
    query = update.callback_query
    context.user_data['form_type'] = form_type
    context.user_data['form_step'] = 1
    query.message.reply_text("Пожалуйста, укажите Ваше имя:")

# Обработка заполнения формы
def receive_form(update, context):
    if 'form_step' not in context.user_data:
        ignore_message(update, context)
        return

    form_step = context.user_data.get('form_step', 0)

    if form_step == 1:
        context.user_data['name'] = update.message.text
        context.user_data['form_step'] = 2
        update.message.reply_text("Пожалуйста, укажите Ваш номер телефона:")

    elif form_step == 2:
        context.user_data['phone'] = update.message.text
        context.user_data['form_step'] = 3
        update.message.reply_text("Пожалуйста, укажите Ваш жилой комплекс или адрес:")

    elif form_step == 3:
        context.user_data['complex'] = update.message.text
        context.user_data['form_step'] = 4
        update.message.reply_text("Пожалуйста, укажите квадратуру объекта:")

    elif form_step == 4:
        context.user_data['size'] = update.message.text
        form_data = context.user_data
        user_id = update.message.from_user.id
        message = (f"Новая анкета по запросу {form_data['form_type']} от клиента (ID: {user_id}):\n"
                   f"Имя: {form_data['name']}\nТелефон: {form_data['phone']}\n"
                   f"Жилой комплекс и адрес: {form_data['complex']}\n"
                   f"Квадратура квартиры: {form_data['size']}")

        # Отправка администратору
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

        # Сообщение пользователю
        update.message.reply_text("Спасибо за заполнение анкеты, скоро наши операторы свяжутся с Вами.")

        # Возвращение в стартовое меню
        start(update, context)

# Обработка нажатий на кнопку "Заполнить анкету" для разных сценариев
def fill_form_apartment(update, context):
    start_form(update, context, 'Приемка квартиры')

def fill_form_builder(update, context):
    start_form(update, context, 'Взыскание с застройщика')

# Контактная информация
def send_contact_info(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Главное меню", callback_data='go_to_start')]]
    query.message.reply_text(
        "Наш телефон: 8-905-509-81-71\nНаша почта: LSGROUP@internet.ru\nWhatsApp и Telegram: 8-905-509-81-71.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    # Деактивировать кнопку "Главное меню" для старых логик
    query.edit_message_reply_markup(reply_markup=None)

def contact_info(update, context):
    send_contact_info(update, context)

# Переход в главное меню
def go_to_start(update, context):
    query = update.callback_query
    # Отправляем стартовое сообщение с новыми кнопками
    start(update, context)
    # Деактивируем старые кнопки
    query.edit_message_reply_markup(reply_markup=None)

# Главная функция
def main():
    # Вставьте сюда свой токен
    updater = Updater("8167316389:AAH5mM1NGAadlsHtE1XWIJGABgyl3LTqCzc", use_context=True)

    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(apartment_check, pattern='^apartment_check$'))
    dp.add_handler(CallbackQueryHandler(builder_claim, pattern='^builder_claim$'))
    dp.add_handler(CallbackQueryHandler(fill_form_apartment, pattern='^fill_form_apartment$'))
    dp.add_handler(CallbackQueryHandler(fill_form_builder, pattern='^fill_form_builder$'))
    dp.add_handler(CallbackQueryHandler(contact_info, pattern='^contact_info$'))
    dp.add_handler(CallbackQueryHandler(go_to_start, pattern='^go_to_start$'))
    
    # Обработка сообщений для заполнения анкеты
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_form))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
