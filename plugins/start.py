from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from DB.admin import Admin
from helpers.inlin import inline_keyboard,inline_keyboard2
from helpers.worker import start_worker
import os
admin = Admin()
start_text = """
Hey there! 👋

I'm a specialized bot designed to help manage and automate tasks. I'm currently configured to only respond to the bot owner.

Use /start to begin interacting with me.
"""

@Client.on_message(filters.command("start"))
async def start(client, message):



    await message.reply(start_text, reply_markup=inline_keyboard)


@Client.on_callback_query(filters.regex("^worker$"))
async def worker_callback(client, callback_query):
    if admin.get_worker():
        admin.update_worker(False)
        await callback_query.answer("Worker is disabled", show_alert=True)
    else:
        await callback_query.message.edit("Worker is enabled\nNow starting the service...", reply_markup=inline_keyboard2)
        admin.update_worker(True)
        await start_worker(callback_query.message, client)






