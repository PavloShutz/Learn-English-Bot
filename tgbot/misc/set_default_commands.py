from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Вивести довідку"),
            types.BotCommand("add_new_word", "Додати нове слово до словнику"),
            types.BotCommand("learn", "Отримати матеріали для вивчення")
        ]
    )
