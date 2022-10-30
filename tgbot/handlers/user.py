from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from tgbot.keyboards.reply import user_provide_phone
from tgbot.misc import Registration
from tgbot.services.repository import Repo


async def user_start(message: Message, repo: Repo):
    if await repo.user_in_table(message.from_user.id):
        await message.answer(text="З поверненням, юзере!")
    else:
        await message.answer_sticker(sticker='CAACAgIAAxkBAAEOuQtjXTAJxrkRKaOFv9zy-Uz2QvYdXAACIgADTlzSKWF0vv5zFvwUKgQ')
        await message.reply("Привіт, юзер!", reply_markup=user_provide_phone)
        await Registration.provide_phone.set()


async def user_help(message: Message):
    faq = """
<b><u>Бот ще у розробці, деякі функції можуть працювати некоректно!</u></b>

<b>Стандартні команди для бота</b>
<code>/start</code>            <strong>Запуск бота</strong>
<code>/help</code>              <strong>Вивід довідки</strong>

<b>Навчання</b>
<code>/learn</code>                 <strong>Отримай матеріали для вивчення граматики</strong>
<code>/add_new_word</code>   <strong>З наростанням складності завдань тобі
доведеться записувати нові слова до словнику</strong>
<code>/send_me_dictionary</code>   <strong>Всі слова, записані тобою, будуть
записуватися у словник, який ти потім зможеш отримати</strong>

<b>Різне</b>
<code>/start_polling</code>   <strong>Я надішлю тобі вікторину, яку ти зможеш проходити безліч разів</strong>
"""
    await message.answer(text=faq)


async def user_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply(text="Ваша остання дія була скасована.")


async def user_provides_phone(message: Message, repo: Repo, state: FSMContext):
    await repo.add_user(message.from_user.id, message.from_user.full_name, message.contact.phone_number)
    await message.answer(text="<b>Ви успішно зареєстровані!</b>")
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(
        user_provides_phone,
        state=Registration.provide_phone,
        content_types=ContentType.CONTACT
    )
    dp.register_message_handler(user_help, commands=['help'], state="*")
    dp.register_message_handler(user_cancel, commands=['cancel'], state="*")
