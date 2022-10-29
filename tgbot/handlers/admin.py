from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.misc import AddQuestion
from tgbot.services.repository import Repo
from tgbot.keyboards.inline import admin_commands


async def admin_start(message: types.Message, repo: Repo):
    await message.reply("Hello, admin!", reply_markup=admin_commands)
    await repo.add_user(message.from_user.id, message.from_user.full_name)


async def admin_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer_sticker('CAACAgIAAxkBAAEOuT1jXTuKPkow32aMKG5wfsKHRifF5AAC1wAD9wLIDx-GnSrVbtclKgQ')
    await message.reply(text="Your last action was canceled.")


async def add_question(callback: types.CallbackQuery):
    await callback.message.answer(text="Please, add question title.")
    await AddQuestion.add_question.set()


async def provide_first_answer(message: types.Message, state: FSMContext):
    await state.set_data({'title': message.text})
    await message.answer(text="Add first answer")
    await AddQuestion.add_first_answer.set()


async def provide_second_answer(message: types.Message, state: FSMContext):
    await state.update_data({'first_answer': message.text})
    await message.answer(text="Add second answer")
    await AddQuestion.add_second_answer.set()


async def provide_third_answer(message: types.Message, state: FSMContext):
    await state.update_data({'second_answer': message.text})
    await message.answer(text="Add third answer")
    await AddQuestion.add_third_answer.set()


async def provide_fourth_answer(message: types.Message, state: FSMContext):
    await state.update_data({'third_answer': message.text})
    await message.answer(text="Add fourth answer")
    await AddQuestion.add_fourth_answer.set()


async def provide_correct_answer(message: types.Message, state: FSMContext):
    await state.update_data({'fourth_answer': message.text})
    await message.answer(text="Now, provide correct answer id.")
    await AddQuestion.provide_correct_answer_id.set()


async def add_question_data_to_database(message: types.Message, state: FSMContext, repo: Repo):
    await state.update_data({'correct_id': int(message.text)})
    data = await state.get_data()
    await message.answer(text=f"Here you got it:\n{data}")
    await repo.add_question(data['title'])
    question_id = await repo.select_question_id(data['title'])
    answer_titles = ('first_answer', 'second_answer', 'third_answer', 'fourth_answer')
    for item in answer_titles:
        if answer_titles.index(item) + 1 == data['correct_id']:
            await repo.add_answer(data[item], question_id, True)
            continue
        await repo.add_answer(data[item], question_id, False)
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEOuFhjXQL9p_zytfYlisCzIG0eSkFsfAAC_gADVp29CtoEYTAu-df_KgQ')
    await message.answer(text="Question added successfully!")
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(admin_cancel, commands=['cancel'], state="*")

    # commands for admin only
    dp.register_callback_query_handler(add_question, text='add_question', is_admin=True)
    dp.register_message_handler(provide_first_answer, state=AddQuestion.add_question)
    dp.register_message_handler(provide_second_answer, state=AddQuestion.add_first_answer)
    dp.register_message_handler(provide_third_answer, state=AddQuestion.add_second_answer)
    dp.register_message_handler(provide_fourth_answer, state=AddQuestion.add_third_answer)
    dp.register_message_handler(provide_correct_answer, state=AddQuestion.add_fourth_answer)
    dp.register_message_handler(add_question_data_to_database, text=('1', '2', '3', '4'),
                                state=AddQuestion.provide_correct_answer_id)
