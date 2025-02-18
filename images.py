# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


"""
✘ Commands Available

• `{i}freepik <query> ; limit`
    search images on freepik.

• `{i}shutter <query> ; limit`
    search images on shutterstock.
"""

from random import shuffle
from urllib.request import urlopen
import os
from bs4 import BeautifulSoup as bs
from telethon.errors.rpcerrorlist import WebpageCurlFailedError
from . import *


@ultroid_cmd(pattern="freepik ?(.*)")
async def fnew_pik(event):
    match = event.pattern_match.group(1)
    limit = 5
    if not match:
        return await eor(event, "`Give Something to Search!`")
    event = await eor(event, "`...`")
    if " ; " in match:
        _ = match.split(" ; ", maxsplit=1)
        match = _[0]
        limit = int(_[1])
    match = match.replace(" ", "%20")
    content = urlopen(
        f"https://www.freepik.com/search?format=search&page=1&query={match}"
    )
    reso = bs(content, "html.parser", from_encoding="utf-8")
    con = reso.find_all("img", src=re.compile("img.freepik.com"))
    if not con:
        return await eor(event, "No Results Found!")
    shuffle(con)
    lml = [a["src"] for a in con[:limit]]
    try:
        await event.client.send_message(
            event.chat_id, f"Uploaded {len(lml)} Images!", file=lml
        )
    except WebpageCurlFailedError:
        NaN = []
        for _ in lml:
           NaN.append(await download_file(_, check_filename("freepik.png")))
           await event.client.send_message(
            event.chat_id, f"Uploaded {len(NaN)} Images!", file=NaN
            )
        [os.remove(a) for a in NaN]
    await event.delete()

@ultroid_cmd(pattern="shutter ?(.*)")
async def snew_pik(event):
    match = event.pattern_match.group(1)
    limit = 5
    if not match:
        return await eor(event, "`Give Something to Search!`")
    event = await eor(event, "`...`")
    if " ; " in match:
        _ = match.split(" ; ", maxsplit=1)
        match = _[0]
        limit = int(_[1])
    content = urlopen(
        f"https://www.shutterstock.com/search/{match.replace(' ', '+')}"
    )
    reso = bs(content, "html.parser", from_encoding="utf-8")
    con = reso.find_all("img", src=re.compile("image.shutterstock.com"))
    if not con:
        return await eor(event, "No Results Found!")
    shuffle(con)
    lml = [a["src"] for a in con[:limit]]
    try:
        await event.client.send_message(
            event.chat_id, f"Uploaded {len(lml)} Images!", file=lml
        )
    except WebpageCurlFailedError:
        NaN = []
        for _ in lml:
           NaN.append(await download_file(_, check_filename("shutter.png")))
           await event.client.send_message(
            event.chat_id, f"Uploaded {len(NaN)} Images!", file=NaN
            )
        [os.remove(a) for a in NaN]
    await event.delete()
