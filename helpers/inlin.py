from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Start Worker", callback_data="worker")]
])

inline_keyboard2 = InlineKeyboardMarkup([
    [InlineKeyboardButton("Stop Worker", callback_data="worker")]
])

