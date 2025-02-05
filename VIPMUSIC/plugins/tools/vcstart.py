from typing import List, Optional, Union

from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import ChatPrivileges, Message

from VIPMUSIC import app
from VIPMUSIC.core.call import VIP
from VIPMUSIC.utils.database import *
from VIPMUSIC.utils.database import set_loop

other_filters = filters.group & ~filters.via_bot & ~filters.forwarded
other_filters2 = filters.private & ~filters.via_bot & ~filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands, "")


@app.on_message(filters.video_chat_started & filters.group)
async def brah(_, msg):
    chat_id = msg.chat.id
    try:
        await msg.reply("**😉𝑺𝒕𝒂𝒓𝒕𝒆𝒅 𝒕𝒉𝒆 𝒗𝒊𝒅𝒆𝒐 𝒄𝒉𝒂𝒕... 𝒃𝒖𝒕 𝑰 𝒄𝒂𝒏’𝒕 𝒔𝒕𝒐𝒑 𝒔𝒕𝒂𝒓𝒊𝒏𝒈 𝒂𝒕 𝒚𝒐𝒖!❤️‍🩹**")
        await VIP.st_stream(chat_id)
        await set_loop(chat_id, 0)
    except Exception as e:
        return await msg.reply(f"**Error {e}**")


################################################
async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    assistant = await get_assistant(message.chat.id)
    chat_peer = await assistant.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await assistant.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await assistant.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await app.send_message(f"𝑽𝒐𝒊𝒄𝒆 𝒄𝒉𝒂𝒕’𝒔 𝒈𝒐𝒏𝒆? 𝑮𝒖𝒆𝒔𝒔 𝒊𝒕’𝒔 𝒋𝒖𝒔𝒕 𝒎𝒆 𝒂𝒏𝒅 𝒎𝒚 𝒕𝒉𝒐𝒖𝒈𝒉𝒕𝒔... 𝒔𝒄𝒂𝒓𝒚!** {err_msg}")
    return False


@app.on_message(filters.command(["vcstart", "startvc"], ["/", "!"]))
async def start_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "𝑬𝒓𝒓𝒐𝒓 𝑾𝒊𝒕𝒉 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕")
        return
    msg = await app.send_message(chat_id, "𝑽𝒐𝒊𝒄𝒆 𝒄𝒉𝒂𝒕 𝒔𝒕𝒂𝒓𝒕𝒊𝒏𝒈! 𝑳𝒆𝒕’𝒔 𝒔𝒆𝒆 𝒘𝒉𝒐 𝒇𝒐𝒓𝒈𝒆𝒕𝒔 𝒕𝒐 𝒖𝒏𝒎𝒖𝒕𝒆 𝒇𝒊𝒓𝒔𝒕!..")
    try:
        peer = await assistant.resolve_peer(chat_id)
        await assistant.invoke(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=assistant.rnd_id() // 9000000000,
            )
        )
        await msg.edit_text("𝑽𝒐𝒊𝒄𝒆 𝒄𝒉𝒂𝒕’𝒔 𝒍𝒊𝒗𝒆, 𝒃𝒖𝒕 𝑰 𝒕𝒉𝒊𝒏𝒌 𝑰’𝒎 𝒕𝒉𝒆 𝒐𝒏𝒆 𝒘𝒉𝒐’𝒔 𝒏𝒆𝒓𝒗𝒐𝒖𝒔 𝒏𝒐𝒘!")
    except ChatAdminRequired:
        try:
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=True,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            peer = await assistant.resolve_peer(chat_id)
            await assistant.invoke(
                CreateGroupCall(
                    peer=InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    ),
                    random_id=assistant.rnd_id() // 9000000000,
                )
            )
            await app.promote_chat_member(
                chat_id,
                assid,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                ),
            )
            await msg.edit_text("𝑽𝒐𝒊𝒄𝒆 𝒄𝒉𝒂𝒕’𝒔 𝒍𝒊𝒗𝒆, 𝒃𝒖𝒕 𝑰 𝒕𝒉𝒊𝒏𝒌 𝑰’𝒎 𝒕𝒉𝒆 𝒐𝒏𝒆 𝒘𝒉𝒐’𝒔 𝒏𝒆𝒓𝒗𝒐𝒖𝒔 𝒏𝒐𝒘!")
            await VIP.st_stream(chat_id)
            await set_loop(chat_id, 0)
        except:
            await msg.edit_text("𝑮𝒊𝒗𝒆 𝒕𝒉𝒆 𝒃𝒐𝒕 𝒂𝒍𝒍 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏 𝒂𝒏𝒅 𝒕𝒓𝒚 𝒂𝒈𝒂𝒊𝒏 ⚡")


@app.on_message(filters.command(["vcend", "endvc"], ["/", "!"]))
async def stop_group_call(c: Client, m: Message):
    chat_id = m.chat.id
    assistant = await get_assistant(chat_id)
    ass = await assistant.get_me()
    assid = ass.id
    if assistant is None:
        await app.send_message(chat_id, "𝑬𝒓𝒓𝒐𝒓 𝑾𝒊𝒕𝒉 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕")
        return
    msg = await app.send_message(chat_id, "ᴄʟᴏꜱɪɴɢ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ..")
    try:
        if not (
            group_call := (
                await get_group_call(
                    assistant, m, err_msg=", ɢʀᴏᴜᴘ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴅᴇᴅ"
                )
            )
        ):
            return
        await assistant.invoke(DiscardGroupCall(call=group_call))
        await msg.edit_text("𝑬𝒏𝒅𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒗𝒐𝒊𝒄𝒆 𝒄𝒐𝒏𝒗𝒆𝒓𝒔𝒂𝒕𝒊𝒐𝒏 𝒏𝒐𝒘~!")
    except Exception as e:
        if "GROUPCALL_FORBIDDEN" in str(e):
            try:
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=True,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
                )
                if not (
                    group_call := (
                        await get_group_call(
                            assistant, m, err_msg=", 𝑻𝒉𝒆 𝒈𝒓𝒐𝒖𝒑 𝒗𝒐𝒊𝒄𝒆 𝒄𝒉𝒂𝒕 𝒉𝒂𝒔 𝒂𝒍𝒓𝒆𝒂𝒅𝒚 𝒃𝒆𝒆𝒏 𝒄𝒐𝒏𝒄𝒍𝒖𝒅𝒆𝒅"
                        )
                    )
                ):
                    return
                await assistant.invoke(DiscardGroupCall(call=group_call))
                await app.promote_chat_member(
                    chat_id,
                    assid,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
                )
                await msg.edit_text("𝑬𝒏𝒅𝒊𝒏𝒈 𝒕𝒉𝒊𝒔 𝒗𝒐𝒊𝒄𝒆 𝒄𝒐𝒏𝒗𝒆𝒓𝒔𝒂𝒕𝒊𝒐𝒏 𝒏𝒐𝒘~!")
                await VIP.st_stream(chat_id)
                await set_loop(chat_id, 0)
            except:
                await msg.edit_text("𝑮𝒊𝒗𝒆 𝒕𝒉𝒆 𝒃𝒐𝒕 𝒂𝒍𝒍 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏 𝒂𝒏𝒅 𝒕𝒓𝒚 𝒂𝒈𝒂𝒊𝒏")
