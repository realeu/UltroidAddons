# Inline alive for Ultroid
# Made By @e3ris & Edited By @xdune 😌


import time
import sys
import shutil
from random import choice
from datetime import datetime as dt
from telethon.events import CallbackQuery, InlineQuery

from pyUltroid.version import __version__ as UltVer
from telethon import __version__, events, Button
from telethon.errors import (
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import *

EMOJIX = "🦋"
DEFAULT_PIC = "https://telegra.ph/file/804a8f326f02c5b8506b4.jpg"


@ultroid_cmd(
    pattern="ialive",
    ignore_dualmode=True,   
)
async def inlive(ialive):
    "Inline Alive"
    if ialive.fwd_from:
        return
    here = ialive.chat_id
    e3 = await eor(ialive, "`Processing ...`")
    uptime = time_formatter((time.time() - start_time) * 1000)
    py_vrsn = sys.version.split(' ')[0]
    
    header_text = udB.get("IALIVE_TEXT") 
    # Title
    if not header_text:
        header_text = "Ultroid is Up and Running Master!"

    em_ = udB.get("IALIVE_EMOJI")
    # emoji
    em_ = choice(em_.split()) if em_ else EMOJIX

    msg = f"**{header_text}**"\n\n
    msg += f"{em_} **Owner :**` {OWNER_NAME}`"\n
    msg += f"{em_} **Ultroid Version :**` {ultroid_version}`"\n
    msg += f"{em_} **Uptime :**` {uptime}`"\n
    msg += f"{em_} **Telethon :**` {__version__}`"\n
    msg += f"{em_} **Python :**` {py_vrsn}`"

    reply_to = ialive.reply_to_msg_id if ialive.is_reply else None

    query = await ultroid_bot.inline_query(
        bot=asst.me.username,
        query=f"Ialive_ {msg}",
        entity=here,
    )
    try:
        await query[0].click(
            hide_via=True,
            reply_to=reply_to,
        )
        await e3.delete()
    except (ChatSendInlineForbiddenError, ChatSendMediaForbiddenError):
        return await e3.edit(msg)
    except Exception as ex:
        return await eod(e3, f"`{ex}`")
        

@asst.on(InlineQuery(pattern=r"Ialive_"))
async def i_alive(event):
    user_ = event.query.user_id
    sudo = udB.get("SUDOS").split()
    sudo.append(str(ultroid.me.id))
    if str(user_) not in sudo:
        return
    text = event.text

    pic = udB.get("IALIVE_PIC")
    photo_ = choice(pic.split()) if pic else DEFAULT_PIC

    uname = ultroid.me.username
    owner = (
        f"https://telegram.me/{uname}"
        if uname
        else f"tg://openmessage?user_id={ultroid.me.id}"
    )
    button = [
        [
            Button.url("Repo", url="https://github.com/TeamUltroid/Ultroid"),
            Button.inline("Stats", data="_stats"),
            Button.url("Master", url=owner),
        ]
    ]
    art = event.builder.photo(
        text=text[8:],
        file=photo_,
        buttons=button,
        link_preview=False,
    )
    await event.answer([art])


@asst.on(CallbackQuery(data="_stats"))
async def staats(event):
    start = dt.now() # ping
    # storage
    disk = shutil.disk_usage(".")

    # addons and pmpermit
    pm_perm = udB.get("PMSETTING")
    addons = (
        "Disabled"
        if udB.get("ADDONS") == "False"
        else "Enabled"
    )   
    pmperms = (
        "Enabled"
        if pm_perm == "True"
        else "Disabled"
    )    
    end = dt.now()
    pong = (end - start).microseconds / 1000

    fyi = "🦋 Stats of My Ultroid UB! 🦋\n\n"    
    fyi += f"pyUltroid : {UltVer}\n"
    fyi += f"Ping : {pong} ms\n"
    fyi += f"Addons : {addons}\n"
    fyi += f"PM Security : {pmperms}\n"
    fyi += f"Storage : {humanbytes(disk.free)} free of {humanbytes(disk.total)}"

    await event.answer(fyi, cache_time=0, alert=True)
