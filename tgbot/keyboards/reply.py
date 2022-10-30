from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_provide_phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Відправ мені свій телефон для завершення реєстрації.", request_contact=True)
        ]
    ],
    one_time_keyboard=True
)
