# -*- coding: utf-8 -*- (test info)

# *          __  __ _             __  __           _       _
# *         |  \/  (_)_   _ _   _|  \/  | ___   __| |_   _| | ___  ___
# *         | |\/| | | | | | | | | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
# *         | |  | | | |_| | |_| | |  | | (_) | (_| | |_| | |  __/\__ \
# *         |_|  |_|_|\__, |\__,_|_|  |_|\___/ \__,_|\__,_|_|\___||___/
# *                   |___/
# *
# *       ╔════════════════════════════════════════════════════════════╗
# *       ║ © Copyright 2025, miyumodules
# *       ║
# *       ║ 🔒 Licensed under the GNU AGPLv3
# *       ║    https://www.gnu.org/licenses/agpl-3.0.html
# *       ║
# *       ║ ⛔️ You CANNOT edit or distribute this file without direct
# *       ║    permission from the author.
# *       ╚════════════════════════════════════════════════════════════╝

# Name: UserInfo
# Author: miyumodules
# Commands:
# .uinfo
# scope: hikka_only
# meta developer: @miyumodules
# meta pic: https://github.com/d4s4n/miyumodules/blob/main/assets/pfp.png?raw=true
# meta banner: https://github.com/d4s4n/miyumodules/blob/main/assets/banner.png?raw=true

__version__ = (1, 0, 4)

import datetime
import bisect
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User
from .. import loader, utils

REG_DATES = {
    1: 1375315200, 10000000: 1389484800, 100000000: 1444435200,
    200000000: 1467417600, 300000000: 1489622400, 400000000: 1512000000,
    500000000: 1524960000, 700000000: 1546473600, 1000000000: 1569024000,
    1500000000: 1604448000, 2147483647: 1624579200, 3000000000: 1635206400,
    4000000000: 1645401600, 5000000000: 1657929600, 6000000000: 1680307200,
    7000000000: 1714608000
}
KNOWN_IDS = sorted(REG_DATES.keys())

def get_reg_date(uid: int) -> datetime.datetime:
    idx = bisect.bisect_right(KNOWN_IDS, uid)

    if idx == 0: id1, id2 = KNOWN_IDS[0], KNOWN_IDS[1]
    elif idx >= len(KNOWN_IDS): id1, id2 = KNOWN_IDS[-2], KNOWN_IDS[-1]
    else: id1, id2 = KNOWN_IDS[idx - 1], KNOWN_IDS[idx]

    ts1, ts2 = REG_DATES[id1], REG_DATES[id2]
    id_diff, time_diff = id2 - id1, ts2 - ts1

    if not id_diff: reg_ts = ts1
    else:
        ratio = (uid - id1) / id_diff
        reg_ts = ts1 + (time_diff * ratio)
        
    return datetime.datetime.fromtimestamp(reg_ts, tz=datetime.timezone.utc)


@loader.tds
class UserInfoMod(loader.Module):
    """Shows full information about a user"""

    strings = {
        "name": "UserInfo", "processing": "<b>Processing...</b>",
        "user_not_found": "<b>User not found.</b>",
        "not_a_user": "<b>This is a channel, not a user.</b>",
        "no_bio": "Not specified",
        "info_template": {
            "premium": (
                '<b>User:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n"
                "<b>Uname:</b> <code>{username}</code>\n\n"
                "<b><emoji document_id=5958376256788502078>⭐️</emoji> Premium:</b> {premium}\n"
                "<b><emoji document_id=5879896690210639947>🗑️</emoji> Deleted:</b> {deleted}\n"
                "<b><emoji document_id=5963224093749678888>👁</emoji> Frozen:</b> {frozen}\n"
                "<b><emoji document_id=5985780596268339498>🤖</emoji> Bot:</b> {bot}\n"
                "<b><emoji document_id=5985479497586053461>🗺️</emoji> DC:</b> <code>{dc}</code>\n\n"
                "<b><emoji document_id=5985774024968379294>🖊</emoji> Reg:</b> <code>{reg_date}</code>\n\n"
                "<b><emoji document_id=6008163345885040772>🗃</emoji> Bio:</b>\n"
                "<code>{bio}</code>"
            ),
            "standard": (
                '<b>User:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n"
                "<b>Uname:</b> <code>{username}</code>\n\n"
                "<b>👑 Premium:</b> {premium}\n"
                "<b>🗑️ Deleted:</b> {deleted}\n"
                "<b>❄️ Frozen:</b> {frozen}\n"
                "<b>🤖 Bot:</b> {bot}\n"
                "<b>🗄️ DC:</b> <code>{dc}</code>\n\n"
                "<b>🗓️ Reg:</b> <code>{reg_date}</code>\n\n"
                "<b>📝 Bio:</b>\n"
                "<code>{bio}</code>"
            ),
        },
        "info_template_limited": {
            "premium": (
                '<b>User:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n\n"
                "<b><emoji document_id=5958376256788502078>⭐️</emoji> Premium:</b> {premium}\n"
                "<b><emoji document_id=5879896690210639947>🗑️</emoji> Deleted:</b> {deleted}\n"
                "<b><emoji document_id=5963224093749678888>👁</emoji> Frozen:</b> {frozen}\n"
                "<b><emoji document_id=5985780596268339498>🤖</emoji> Bot:</b> {bot}\n"
                "<b><emoji document_id=5985479497586053461>🗺️</emoji> DC:</b> <code>{dc}</code>\n\n"
                "<b><emoji document_id=5985774024968379294>🖊</emoji> Reg:</b> <code>{reg_date}</code>"
            ),
            "standard": (
                '<b>User:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n\n"
                "<b>👑 Premium:</b> {premium}\n"
                "<b>🗑️ Deleted:</b> {deleted}\n"
                "<b>❄️ Frozen:</b> {frozen}\n"
                "<b>🤖 Bot:</b> {bot}\n"
                "<b>🗄️ DC:</b> <code>{dc}</code>\n\n"
                "<b>🗓️ Reg:</b> <code>{reg_date}</code>"
            ),
        },
        "yes": "Yes", "no": "No", "not_specified": "N/A",
    }

    strings_ru = {
        "_cls_doc": "Показывает полную информацию о пользователе",
        "_cmd_doc_uinfo": "<юз/ответ/id> - Получить информацию о пользователе",
        "processing": "<b>Обработка...</b>", "user_not_found": "<b>Пользователь не найден.</b>",
        "not_a_user": "<b>Это канал, а не пользователь.</b>",
        "no_bio": "Нету",
        "months": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        "info_template": {
            "premium": (
                '<b>Пользователь:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n"
                "<b>Юз:</b> <code>{username}</code>\n\n"
                "<b><emoji document_id=5958376256788502078>⭐️</emoji> Премиум:</b> {premium}\n"
                "<b><emoji document_id=5879896690210639947>🗑️</emoji> Удален:</b> {deleted}\n"
                "<b><emoji document_id=5963224093749678888>👁</emoji> Заморожен:</b> {frozen}\n"
                "<b><emoji document_id=5985780596268339498>🤖</emoji> Бот:</b> {bot}\n"
                "<b><emoji document_id=5985479497586053461>🗺️</emoji> ДЦ:</b> <code>{dc}</code>\n\n"
                "<b><emoji document_id=5985774024968379294>🖊</emoji> Рег:</b> <code>{reg_date}</code>\n\n"
                "<b><emoji document_id=6008163345885040772>🗃</emoji> Био:</b>\n"
                "<code>{bio}</code>"
            ),
            "standard": (
                '<b>Пользователь:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n"
                "<b>Юз:</b> <code>{username}</code>\n\n"
                "<b>👑 Премиум:</b> {premium}\n"
                "<b>🗑️ Удален:</b> {deleted}\n"
                "<b>❄️ Заморожен:</b> {frozen}\n"
                "<b>🤖 Бот:</b> {bot}\n"
                "<b>🗄️ ДЦ:</b> <code>{dc}</code>\n\n"
                "<b>🗓️ Рег:</b> <code>{reg_date}</code>\n\n"
                "<b>📝 Био:</b>\n"
                "<code>{bio}</code>"
            ),
        },
        "info_template_limited": {
            "premium": (
                '<b>Пользователь:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n\n"
                "<b><emoji document_id=5958376256788502078>⭐️</emoji> Премиум:</b> {premium}\n"
                "<b><emoji document_id=5879896690210639947>🗑️</emoji> Удален:</b> {deleted}\n"
                "<b><emoji document_id=5963224093749678888>👁</emoji> Заморожен:</b> {frozen}\n"
                "<b><emoji document_id=5985780596268339498>🤖</emoji> Бот:</b> {bot}\n"
                "<b><emoji document_id=5985479497586053461>🗺️</emoji> ДЦ:</b> <code>{dc}</code>\n\n"
                "<b><emoji document_id=5985774024968379294>🖊</emoji> Рег:</b> <code>{reg_date}</code>"
            ),
            "standard": (
                '<b>Пользователь:</b> <a href="tg://user?id={id}">{name}</a>\n'
                "<b>ID:</b> <code>{id}</code>\n\n"
                "<b>👑 Премиум:</b> {premium}\n"
                "<b>🗑️ Удален:</b> {deleted}\n"
                "<b>❄️ Заморожен:</b> {frozen}\n"
                "<b>🤖 Бот:</b> {bot}\n"
                "<b>🗄️ ДЦ:</b> <code>{dc}</code>\n\n"
                "<b>🗓️ Рег:</b> <code>{reg_date}</code>"
            ),
        },
        "yes": "Да", "no": "Нет", "not_specified": "Н/Д",
    }

    def format_date(self, date_obj):
        try:
            months = self.strings("months")
            month = months[date_obj.month - 1]
            return f"{month} {date_obj.year}"
        except KeyError:
            return date_obj.strftime("%B %Y")

    @loader.command(ru_doc="<юз/ответ/id> - Получить информацию о пользователе")
    async def uinfocmd(self, message):
        """<user/reply/id> - Get full info about a user"""

        msg = await utils.answer(message, self.strings("processing"))
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None

        if args:
            try:
                lookup = int(args) if args.isdigit() else args
                user = await self.client.get_entity(lookup)
            except Exception:
                await utils.answer(msg, self.strings("user_not_found"))
                return
        elif reply:
            user = await reply.get_sender()
        else:
            user = await self.client.get_me()

        if not user:
            await utils.answer(msg, self.strings("user_not_found"))
            return

        if not isinstance(user, User):
            await utils.answer(msg, self.strings("not_a_user"))
            return

        is_deleted = user.deleted
        is_frozen = user.restricted
        is_limited = is_deleted or is_frozen

        bio = self.strings("no_bio")
        if not is_limited:
            try:
                full_user = await self.client(GetFullUserRequest(user.id))
                bio = full_user.full_user.about or self.strings("no_bio")
            except Exception:
                pass

        dc = user.photo.dc_id if user.photo else self.strings("not_specified")

        name = utils.escape_html(user.first_name or "Deleted")
        if user.last_name: name += f" {utils.escape_html(user.last_name)}"
        if len(name) > 200: name = name[:200] + "..."

        reg_date_obj = get_reg_date(user.id)
        reg_date_str = self.format_date(reg_date_obj)

        info = {
            "id": user.id, "name": name,
            "username": f"@{user.username}" if user.username else self.strings("not_specified"),
            "premium": self.strings("yes") if user.premium else self.strings("no"),
            "deleted": self.strings("yes") if is_deleted else self.strings("no"),
            "frozen": self.strings("yes") if is_frozen else self.strings("no"),
            "bot": self.strings("yes") if user.bot else self.strings("no"),
            "dc": dc, "reg_date": reg_date_str, "bio": utils.escape_html(bio),
        }

        me = await self.client.get_me()
        template_style = ("premium" if me.premium or (message.is_private and message.chat_id == me.id) else "standard")
        template_key = "info_template_limited" if is_limited else "info_template"
        template = self.strings(template_key)[template_style]
        text = template.format(**info)
        await utils.answer(msg, text)
    
    @loader.command()
    async def whoiscmd(self, message):
        await self.uinfocmd(message)

    @loader.command()
    async def userinfocmd(self, message):
        await self.uinfocmd(message)
