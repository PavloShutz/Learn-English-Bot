from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_commands = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Show users", callback_data="show_users"),
            InlineKeyboardButton(text="Add question", callback_data="add_question")
        ]
    ]
)

user_get_dictionary_commands = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отримати словник", callback_data="get_dictionary"),
            InlineKeyboardButton(text="Ні, я ще занесу слова)", callback_data="cancel")
        ]
    ]
)
