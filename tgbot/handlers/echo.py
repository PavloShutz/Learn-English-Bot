import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.misc import UserLearning
from tgbot.services.parser import main


async def send_learning_materials(message: types.Message):
    for item in await main():
        await message.answer(text=f"<b>{item['text']}</b>\n\n<b>Посилання</b>: {item['link']}")
        time.sleep(3)


async def add_new_word(message: types.Message):
    await message.answer("Будь-ласка, відправ мені слово, яке ти хочеш записати.")
    await UserLearning.add_word.set()


async def add_definition_to_word(message: types.Message, state: FSMContext):
    await state.set_data({'word': message.text})
    await message.answer("Додай визначення для цього слова.")
    await UserLearning.add_definition_to_word.set()


async def add_word_to_dictionary(message: types.Message, state: FSMContext):
    await state.update_data({'definition': message.text})
    await message.answer(text=f"Додано слово:\n{await state.get_data()}")
    await state.finish()


def register_echo(dp: Dispatcher):
    dp.register_message_handler(send_learning_materials, commands=['learn'])
    dp.register_message_handler(add_new_word, commands=['add_new_word'])
    dp.register_message_handler(add_definition_to_word, state=UserLearning.add_word)
    dp.register_message_handler(add_word_to_dictionary, state=UserLearning.add_definition_to_word)
