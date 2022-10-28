from aiogram.dispatcher.filters.state import State, StatesGroup


class UserLearning(StatesGroup):
    add_word = State()
    add_definition_to_word = State()
