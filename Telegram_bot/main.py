from aiogram import Bot, Dispatcher, types, executor
import logging
import requests
import time
import sqlite3
import os

TOKEN = "6181328790:AAEzB9IkPHGq6AC0CqzD43DVuQm7_DHRsnE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

users = {}
review_tasks = {'1A': 4, '1G': 10, '2A': 16, '2I': 24, '3A': 28, '3C': 30,
                '4A': 39, '4F': 44, '5H': 63, '5K': 66, '5O': 70}

sheet_id = "1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU"
api_key = "AIzaSyBoU9ues1BX8wt6LfdyNedQLxOCz7hOCWk"

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id)")
    connect.commit()

    user_id = message.from_user.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")

    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO login_id (id) VALUES ({user_id});")
        connect.commit()
        user_full_name = message.from_user.full_name
        logging.info(f"{user_id=} {user_full_name=} {time.asctime()}")
        await message.reply(f"Привет, {user_full_name}! Введи свое ФИО")
    else:
        await message.reply("Привет, а я тебя помню!")


@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    user_id = message.from_user.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {user_id}")
    connect.commit()
    await message.reply("Тебя больше нет в базе:(\n"
                        "Для того чтобы вернутся пиши /start.")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Привет, я расскажу тебе о твоих успехах в алгоритмах и структурах данных!")


@dp.message_handler(commands=['mark'])
async def get_mark(message: types.Message):
    sheet_name = "Итого"
    all_table_ranges = "A1:J132"
    first_req = requests.get(
        f"https://sheets.googleapis.com/v4/spreadsheets/1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU/"
        f"values/{sheet_name}!{all_table_ranges}?key={api_key}"
    )

    limits_table_ranges = "P5:W7"
    third_req = requests.get(
        f"https://sheets.googleapis.com/v4/spreadsheets/1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU/"
        f"values/{sheet_name}!{limits_table_ranges}?key={api_key}"
    )

    all_table_data = first_req.json()
    limits_table_data = third_req.json()

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")

    data = cursor.fetchone()

    if data is None:
        raise Exception

    index_in_table = users[data]
    print(limits_table_data['values'])
    final_mark = all_table_data['values'][index_in_table][-1]
    mark = int(all_table_data['values'][index_in_table][4])

    contest_mark = all_table_data['values'][index_in_table][6]
    new_contest_mark = float_cast(contest_mark)

    if mark < 9:
        limit = int(limits_table_data['values'][2][mark - 1])
        difference = int(limit - new_contest_mark)

        ending = "баллов"

        if difference % 10 == 1:
            ending = "балл"
        elif 1 < difference % 10 < 5:
            ending = "балла"

        await message.reply(f"На данный момент твоя итоговая оценка {final_mark}.\n"
                            f"Балл за контесты {all_table_data['values'][index_in_table][4]}.\n"
                            f"Оценка за контесты {all_table_data['values'][index_in_table][5]}.\n"
                            f"Балл за теорию {all_table_data['values'][index_in_table][6]}.\n"
                            f"Балл от семинариста {all_table_data['values'][index_in_table][7]}.\n"
                            f"Для оценки за контесты {mark + 1} необходимо набрать {difference} {ending}.")
    else:
        await message.reply(f"На данный момент твоя итоговая оценка {mark}.\n"
                            f"Балл за контесты {all_table_data['values'][index_in_table][4]}.\n"
                            f"Оценка за контесты {all_table_data['values'][index_in_table][5]}.\n"
                            f"Балл за теорию {all_table_data['values'][index_in_table][6]}.\n"
                            f"Балл от семинариста {all_table_data['values'][index_in_table][7]}.\n"
                            f"Поздравляю! У тебя максимальный балл за контесты.")
#    except Exception:
#       await message.reply("Тебя нет в базе:(")


@dp.message_handler(commands=['review'])
async def get_review(message: types.Message):
    try:
        all_table_ranges = "A1:BW132"
        sheet_name = "Контесты"
        first_req = requests.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU/"
            f"values/{sheet_name}!{all_table_ranges}?key={api_key}"
        )

        all_table_data = first_req.json()

        on_check = []
        unsolved = []
        solved = []

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        user_id = message.from_user.id
        cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")

        data = cursor.fetchone()

        if data is None:
            raise Exception

        index_in_table = users[data]
        tasks_info = all_table_data['values'][index_in_table]

        for key in review_tasks.keys():
            mark = 0
            if not tasks_info[review_tasks[key]] == '':
                mark = float_cast(tasks_info[review_tasks[key]])
            if 0 < mark < 1:
                on_check.append(key)
            elif int(mark) >= 1:
                solved.append(key)
            else:
                unsolved.append(key)

        if len(solved) < 3:
            await message.reply(f"Информация о задачах на ревью.\nНа данный момент принято на ревью {len(solved)} задач.\n"
                                f"Приняты: {', '.join(solved)}\n"
                                f"Проверяются: {', '.join(on_check)}\n"
                                f"Не сделаны: {', '.join(unsolved)}\n"
                                f"Учти, что необходимо сдать минимум 3 задачи на ревью!\n"
                                )
        else:
             await message.reply(f"Информация о задачах на ревью.\nНа данный момент принято на ревью {len(solved)} задач.\n"
                                f"Приняты: {', '.join(solved)}\n"
                                f"Проверяются: {', '.join(on_check)}\n"
                                f"Не сделаны: {', '.join(unsolved)}\n"
                                )

    except Exception:
        await message.reply("Тебя нет в базе:(")


@dp.message_handler(commands=['exam'])
async def get_exam(message: types.Message):
    try:
        all_table_ranges = "A1:O132"
        sheet_name = "Экзамен"
        req = requests.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU/"
            f"values/{sheet_name}!{all_table_ranges}?key={api_key}"
        )

        all_table_data = req.json()
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        user_id = message.from_user.id
        cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")

        data = cursor.fetchone()
        index_in_table = users[data]
        exam_info = all_table_data['values'][index_in_table]

        if data is None:
            raise Exception

        date = exam_info[3]
        place = exam_info[4]
        exam_time = exam_info[5]

        await message.reply(f"Информация об экзамене.\nДата: {date}.\nАудитория: {place}.\n"
                            f"Время захода: {exam_time}.\n")

    except Exception:
        await message.reply("Тебя нет в базе:(")


@dp.message_handler()
async def get_full_name(message: types.Message):
    try:
        full_name_table_ranges = "B:B"
        second_req = requests.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/1ha9zc_2ZuPEqfI5f3V1LyTt9R9hlGw7RsoHmHDGJVvU/"
            f"values/{full_name_table_ranges}?key={api_key}"
        )
        full_names_data = second_req.json()
        index_in_table = 1000
        full_names = full_names_data['values']

        for i in range(3, len(full_names)):
            if full_names[i][0].strip() == message.text.strip():
                index_in_table = i

        if index_in_table != 1000:

            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()

            user_id = message.from_user.id
            cursor.execute(f"SELECT id FROM login_id WHERE id = {user_id}")

            data = cursor.fetchone()
            users[data] = index_in_table

        else:
            raise Exception

        await message.reply("Отлично!\n"
                            "Напиши /mark если хочешь узнать информацию о своей текущей оценке.\n"
                            "/review для информации о задачах на ревью.\n"
                            "/exam - информации об экзамене.")

    except Exception:
        await message.reply("Тебя нет в списке! Проверь правильность ввода ФИО.\n"
                            "Учти, что вводить нужно также, как и при заполнении формы.")


def float_cast(num: str) -> float:
    new_num = ""
    for i in range(len(num)):
        if not num[i] == ',':
            new_num += num[i]
        else:
            new_num += '.'

    return float(new_num)


if __name__ == '__main__':
    executor.start_polling(dp)