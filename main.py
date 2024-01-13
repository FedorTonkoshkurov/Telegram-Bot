import datetime
import telebot
import random

bot = telebot.TeleBot('Telegram Bot API Key')

tasks = {}
task_names = {}
task_name = ''
task_date = ''
task_id = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, '''
    Привет! Я telegram бот планировщик задач.
    Список команд:
    /newtask - создать задачу
    /viewtasks - посмотреть задачи
    /deltask - удалить задачу
    ''')


@bot.message_handler(commands=['newtask'])
def get_task_name(message):
    global task_name
    bot.send_message(message.from_user.id, 'Введите название задачи: ')
    bot.register_next_step_handler(message, get_task_date)


def get_task_date(message):
    global task_name, task_date
    task_name = message.text
    bot.send_message(message.from_user.id, 'Введите дату задачи в формате ГГГГ-ММ-ДД: ')
    bot.register_next_step_handler(message, check_date)


def check_date(message):
    global task_date
    date_text = message.text
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        task_date = date_text
        create_task(message)
    except ValueError:
        bot.send_message(message.from_user.id, 'Дата некорректна, попробуйте ещё раз')
        bot.register_next_step_handler(message, check_date)


def create_task(message):
    global task_id
    task_id = random.randint(1000, 9999)
    if task_id not in tasks:
        tasks[task_id] = task_date
        task_names[task_id] = task_name
        bot.send_message(message.from_user.id, 'Задача успешно создана!')
    else:
        create_task(message)


@bot.message_handler(commands=['viewtasks'])
def view_tasks(message):
    global task_id
    global task_date
    if tasks:
        for task_id, task_date in tasks.items():
            bot.send_message(message.from_user.id, f" {task_names[task_id]}: {task_date}")
    else:
        bot.send_message(message.from_user.id, 'У вас ещё нет ни одной задачи.')


if __name__ == '__main__':
    bot.infinity_polling()
