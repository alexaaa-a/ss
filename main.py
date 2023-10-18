import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6612935089:AAGvn3O2QDztCTwgtQMFzIA89LBEOl-pxls",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Опрос"  # Можно менять текст
text_button_1 = "Интересуюсь на любительском уровне"  # Можно менять текст
text_button_2 = "Хочу развить до разговорного языка"  # Можно менять текст
text_button_3 = "Хочу оценить свои способности"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Это бот для изучения английского языка!',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Отлично! *На каком этапе изучения Вы находитесь?*')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! [Начало изучения](https://youtu.be/wXsonoRfBVU)')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за  обращение!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Делюсь ссылкой важного сайта!](https://puzzle-english.com/directory/talk-english)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Речевые шаблоны — важная часть разговорного английского](https://langformula.ru/english-phrases/)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[Давай проверим твой уровень!](https://magazine.skyeng.ru/englishlevel-test-profession-new/?product=type-skyeng_test%7Cname-englishlevel&source_type=context&manager=0105&workflow=special-projects&service=english&study=individual&utm_medium=search&utm_source=yandex&utm_campaign=skyeng_yandex_search_free_worldwide_ru%7Ccpid-95834483&utm_term=gid-5283847132%7Ck-уровни%20английского%20языка%20тест-47086606968-none%7Cpos-premium_2%7C47086606968&utm_content=adid-15123527338%7Cdev-desktop%7Cloc-Стерлитамак%7Clid-11116&yclid=4068744886617374719)",
                     reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()