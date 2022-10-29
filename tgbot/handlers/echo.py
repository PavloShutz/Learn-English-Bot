import time
from random import shuffle, randint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.misc import UserLearning
from tgbot.services.parser import main
from tgbot.services.repository import Repo


def _get_key(input_dict: dict, value):
    """Return key if val == value, else None is returned."""
    for key, val in input_dict.items():
        if val == value:
            return key
    return None


async def start_polling(message: types.Message, repo: Repo):
    if await repo.user_in_table(message.from_user.id):
        data = await repo.get_poll_data(randint(1, await repo.get_amount_of_questions()))
        question = data[0]
        answers = [answer for a in data[1] for answer in a.keys()]
        shuffle(answers)
        correct_id = answers.index([_get_key(i, True) for i in data[1] if _get_key(i, True)][0])
        await message.answer_poll(
            question=question,
            options=answers,
            type='quiz',
            correct_option_id=correct_id,
            is_anonymous=False,  # this argument is required!
        )
    else:
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEOuRtjXTGQBCCOkxXpdIbU-n0t9LZlEwAC-gADVp29Ckfe-pdxdHEBKgQ')
        await message.reply(text="Будь-ласка, зареєструйтесь, відправивши /start!")


async def send_learning_materials(message: types.Message):
    for item in await main():
        await message.answer(text=f"<b>{item['text']}</b>\n\n<b>Посилання</b>: {item['link']}")
        time.sleep(3)


async def add_new_word(message: types.Message):
    """User adds word to his dictionary."""
    await message.answer("📝 Будь-ласка, відправ мені слово, яке ти хочеш записати.")
    await UserLearning.add_word.set()


async def add_definition_to_word(message: types.Message, state: FSMContext):
    await state.set_data({'word': message.text})
    await message.answer("🌐 Додай визначення для цього слова.")
    await UserLearning.add_definition_to_word.set()


async def add_word_to_dictionary(message: types.Message, state: FSMContext, repo: Repo):
    await state.update_data({'definition': message.text})
    word_data = await state.get_data()
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEOuP1jXS4_QitLTI8OFZeMi8qshwHUUAAC3AAD9wLID1DYvAZ7vfB8KgQ')
    time.sleep(1)
    await message.answer(
        text=f"Додано слово: <b>{word_data['word']}</b>\nВизначення: <b>{word_data['definition']}</b>"
    )
    await repo.add_word_to_dictionary(word_data['word'], word_data['definition'])
    await state.finish()


def register_echo(dp: Dispatcher):
    # default commands for every user
    dp.register_message_handler(start_polling, commands=['start_polling'])
    dp.register_message_handler(send_learning_materials, commands=['learn'])
    dp.register_message_handler(add_new_word, commands=['add_new_word'])
    dp.register_message_handler(add_definition_to_word, state=UserLearning.add_word)
    dp.register_message_handler(add_word_to_dictionary, state=UserLearning.add_definition_to_word)
