#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import os
import asyncio
import time
import sys
import psutil

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from bot import LOGGER, Config
from bot.database.database import Database
from bot.helpers.utils import humanbytes, convert_size


logger = LOGGER(__name__)
db = Database()


@Client.on_message(filters.command(["start"]))
async def start (bot, update):
    
    await update.reply_text("Bot Started..! And its Up and Running..!")


@Client.on_message(filters.private & filters.command(["help"]) & filters.user(Config.AUTH_USERS))
async def help(bot, update):
    
    await update.reply_text(
        "Avaliable Commands:\n\n"\
        "/start - Check if bot alive\n"\
        "/help - Show this menu\n\n" + \
        
        ("/stats - Show bot statistics\n"\
        "/restart - Restart the bot\n"\
        "/logs - Get bot logs\n\n" if update.from_user.id in Config.AUTH_USERS else "" )+ \
            
        ("/add - Add user to database\n"\
        "/remove - Remove user from database\n"\
        "/tireusers - List all users in database\n\n" if update.from_user.id in Config.AUTH_USERS else "" )+ \
        
        "/addsource - Add a source to the bot\n"\
        "/delsource - Remove a source from the bot\n"\
        "/listsources - List all sources in the bot\n\n"\
        
        "/id - Get your Telegram ID\n"
    )


@Client.on_message(filters.private & filters.command(["stats"]) & filters.user(Config.AUTH_USERS))
async def stats(bot, update):


    msg = await bot.send_message(
        chat_id=update.chat.id,
        text="__Processing...__",
        parse_mode=enums.ParseMode.MARKDOWN
    )

    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(
        time.time() - Config.BOT_START_TIME))
    cpu_usage = psutil.cpu_percent()

    memory = psutil.virtual_memory()
    storage = psutil.disk_usage('/')

    memory_stats = f"RAM Usage: {convert_size(memory.used)} / {convert_size(memory.total)} ({memory.percent}%)"
    storage_stats = f"Storage Usage: {convert_size(storage.used)} / {convert_size(storage.total)} ({storage.percent}%)"


    size = await db.get_db_size()
    free = 536870912 - size
    size = humanbytes(size)
    free = humanbytes(free)


    ms_g = f"<b><u>Bot Stats</b></u>\n" \
        f"<code>Uptime: {currentTime}</code>\n"\
        f"<code>CPU Usage: {cpu_usage}%</code>\n"\
        f"<code>{memory_stats}</code>\n"\
        f"<code>{storage_stats}</code>\n\n" \
        f"<b><u>Mongodb Stats</b></u>\n"\
        f"<b>᚛› Used Storage : <code>{size}</code></b>\n"\
        f"<b>᚛› Free Storage : <code>{free}</code></b>"

    await msg.edit_text(
        text=ms_g,
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.private & filters.command(["restart"]) & filters.user(Config.AUTH_USERS))
async def restart(bot, update):

    b = await bot.send_message(
        chat_id=update.chat.id,
        text="__Restarting.....__",
        parse_mode=enums.ParseMode.MARKDOWN
    )
    await asyncio.sleep(3)
    await b.delete()
    os.system("git pull")
    os.remove("logs.txt")
    os.execl(sys.executable, sys.executable, "-m", "bot")


@Client.on_message(filters.command(['logs']) & filters.user(Config.AUTH_USERS))
async def send_logs(_, m):
    await m.reply_document(
        "logs.txt",
        caption='Logs'
    )

