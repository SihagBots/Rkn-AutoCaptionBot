# AutoCaptionBot by RknDeveloper
# Copyright (c) 2024 RknDeveloper
# Licensed under the MIT License
# https://github.com/RknDeveloper/Rkn-AutoCaptionBot/blob/main/LICENSE
# Please retain this credit when using or forking this code.

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!


from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant
from config import Rkn_Botz
from .database import rkn_botz

# 🧠 Membership checker used by force-sub handler
async def needs_force_sub(client: Client, message: Message) -> bool:
    if not message.from_user:
        return False

    user_id = message.from_user.id

    # Register user in DB if not already
    await rkn_botz.register_user(user_id)

    channel = (Rkn_Botz.FORCE_SUB or "").lstrip("@")
    if not channel:
        return False

    try:
        member = await client.get_chat_member(channel, user_id)
        return member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]
    except UserNotParticipant:
        return True
    except Exception:
        return False


# 📩 Handler for blocked users / unsubscribed
@Client.on_message(filters.private)
async def handle_force_sub(client: Client, message: Message):
    if not await needs_force_sub(client, message):
        return

    user_id = message.from_user.id
    chat_link = f"https://t.me/{Rkn_Botz.FORCE_SUB.lstrip('@')}"
    
    # 📢 Button UI
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔔 Join Update Channel", url=chat_link)]]
    )

    try:
        member = await client.get_chat_member(Rkn_Botz.FORCE_SUB, user_id)
        if member.status == enums.ChatMemberStatus.BANNED:
            return await message.reply_text(
                "**🚫 You are banned from using this bot.**\nContact admin if this is a mistake."
            )
    except UserNotParticipant:
        pass
    except Exception as e:
        return await message.reply_text(f"⚠️ Unexpected error: `{e}`")

    # Default reply if not joined
    return await message.reply_text(
        "**Hey buddy! 🔐 You need to join our updates channel before using me.**",
        reply_markup=button
    )
    
# ————
# End of file
# Original author: @RknDeveloperr
# GitHub: https://github.com/RknDeveloper

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!