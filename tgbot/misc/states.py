from aiogram.dispatcher.filters.state import State, StatesGroup


class AnswerQuestion(StatesGroup):
    answer_question = State()


class AddQuestion(StatesGroup):
    add_question = State()
    add_first_answer = State()
    add_second_answer = State()
    add_third_answer = State()
    add_fourth_answer = State()
    provide_correct_answer_id = State()


class UserLearning(StatesGroup):
    add_word = State()
    add_definition_to_word = State()
