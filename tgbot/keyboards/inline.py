from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_commands = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Show users", callback_data="show_users"),
            InlineKeyboardButton(text="Add question", callback_data="add_question")
        ]
    ]
)
