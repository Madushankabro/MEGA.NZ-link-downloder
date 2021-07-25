"""
Mega.nz downloader bot
Copyright (C) 2021 @ImJanindu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import logging
from pyrogram import filters, Client, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mega import Mega
from sample_config import Config

# mega client
mega = Mega()
m = mega.login()

# location
LOCATION = "./"

# logging
bot = Client(
   "MegaNz",
   api_id=Config.API_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.BOT_TOKEN,
)

# start msg
@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
   user = message.from_user.mention
   return await message.reply_text(f"""Hey {user}, I am **Mega-Nz Bot** ✨

I can download mega.nz links & upload to Telegram 💥
Give me a mega.nz link to start download 🚿""",
   reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Source Code 💻", url="https://github.com/ImJanindu/MegaNz-Bot")]]))

# mega download
@bot.on_message(filters.regex(pattern="https://mega.nz/") & filters.private)
async def meganz(_, message):
    input = message.text
    user = message.from_user.mention
    msg = await message.reply_text("📥 `Downloading...`")
    try:
        file = m.download_url(input, LOCATION)
    except Exception as e:
        print(str(e))
        return await msg.edit("❌ `Invalid Link.`")
    await msg.edit("📤 `Uploading...`")
    cap = f"✨ `Uploaded By:` {user} \n💻 `Bot By:` @Infinity_Bots"
    await bot.send_document(message.chat.id, file, caption=cap)
    await msg.delete()
    os.remove(file)


bot.start()
idle()
