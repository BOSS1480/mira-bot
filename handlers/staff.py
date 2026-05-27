\"""
Staff management handlers - promote, demote, staff list
"""
from pyrogram import Client, filters
from pyrogram.types import Message

# Promote command
@Client.on_message(filters.command("promote") & filters.group)
async def promote_handler(client: Client, message: Message):
    """Promote a user to admin"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    
    # Check if user is creator
    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status != "creator":
            await message.reply("🚫 Only the group creator can promote users!")
            return
    except:
        return
    
    # Get user to promote
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=False,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_video_chats=True
        )
        await message.reply(f"✅ {user_name} promoted to admin!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Demote command
@Client.on_message(filters.command("demote") & filters.group)
async def demote_handler(client: Client, message: Message):
    """Demote an admin"""
    if not message.from_user:
        return
    
    chat_id = message.chat.id
    
    # Check if user is creator
    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status != "creator":
            await message.reply("🚫 Only the group creator can demote users!")
            return
    except:
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name or "User"
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user_name = "User"
        except:
            await message.reply("Invalid user ID")
            return
    else:
        await message.reply("Reply to a user or provide user ID")
        return
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_video_chats=False
        )
        await message.reply(f"✅ {user_name} demoted from admin!")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Staff command
@Client.on_message(filters.command("staff") & filters.group)
async def staff_handler(client: Client, message: Message):
    """List all admins"""
    chat_id = message.chat.id
    
    try:
        admins = await client.get_chat_administrators(chat_id)
        
        text = "👥 *Staff:*\n\n"
        for admin in admins:
            name = admin.user.first_name or "Unknown"
            if admin.status == "creator":
                text += f"👑 {name} (Creator)\n"
            else:
                text += f"⭐ {name} (Admin)\n"
        
        await message.reply(text)
    except Exception as e:
        await message.reply(f"Error: {e}")