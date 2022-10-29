from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.repository import Repo


async def user_start(message: Message, repo: Repo):
    if await repo.user_in_table(message.from_user.id):
        await message.answer(text="З поверненням, юзере!")
    else:
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEOuQtjXTAJxrkRKaOFv9zy-Uz2QvYdXAACIgADTlzSKWF0vv5zFvwUKgQ')
        await message.reply("Привіт, юзер!")
        await repo.add_user(message.from_user.id, message.from_user.full_name)


async def user_help(message: Message):
    faq = """
<b><u>Бот ще у розробці, деякі функції можуть працювати некоректно!</u></b>

<b>Стандартні команди для бота</b>
/start              Запуск бота
/help               Вивід довідки

<b>Навчання</b>
/learn              Отримати матеріали для вивчення граматики
/add_new_word   Додати нове слово до свого словника
"""
    await message.answer(text=faq)


async def user_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply(text="Your last action was canceled.")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(user_help, commands=['help'], state="*")
    dp.register_message_handler(user_cancel, commands=['cancel'], state="*")
