

from pyrogram import Client, filters, enums, handlers
from pyrogram.types import InlineKeyboardButton, Message

from bot import Config, LOGGER
from bot.bot import app
from bot.database.database import Database


db = Database()
logger = LOGGER(__name__)


@Client.on_message(filters.command("add") & filters.user(Config.AUTH_USERS))
async def add_user_db(bot: Client, update: Message):
    
    
    if len(update.command) != 3:
        return await update.reply("Invalid Format\n<code>/add [tire lvl] [user id]</code>")
    
    tire = update.command[1]
    user_id = update.command[2]
    
    await db.remove_user(user_id)
    await db.add_user(user_id, f"Tire-{tire}")
    await db.load_tire_users()
    
    try:
        await bot.send_message(user_id, f"Your can now enjoy all the benifits of Tire-{tire}...!")
    except Exception as e:
        logger.debug(e)
        
    
    await update.reply(f"User - {user_id} has been added to Tire-{tire} sucessfully...!")
    
    
@Client.on_message(filters.command("remove") & filters.user(Config.AUTH_USERS))
async def rm_user_db(bot: Client, update: Message):
    
    if len(update.command) != 2:
        return await update.reply("Invalid Format\n<code>/remove [user id]</code>")
    
    user_id = update.command[1]
    user_info = await db.get_user_info(user_id)
    
    await db.remove_user(user_id)
    await db.load_tire_users()
    
    await bot.send_message(user_id, f"Your were removed from {user_info['tire']} as your subscription has ended...!\nPay for a new subscription to continue using the bot...!")
    
    await update.reply(f"User - {user_id} was removed sucessfully...!")
    

@Client.on_message(filters.command("tireusers") & filters.user(Config.AUTH_USERS))
async def tire_users_list(bot: Client, update: Message):
    
    tire_users = Config.TIRE_USERS
    
    text = ""
    for tire in tire_users:
        text += f"<b>{tire} | Users - {len(tire_users[tire])}</b>\n"
        for user in tire_users[tire]:
            text += f"👤 <code>{user}</code>\n"
        text += "\n"
    
    await update.reply(text=text, parse_mode=enums.ParseMode.HTML)


