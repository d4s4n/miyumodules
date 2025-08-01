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

# Name: Formatter
# Author: miyumodules
# Commands:
# .fmt | .fmtspam
# scope: hikka_only
# meta developer: @miyumodules
# meta pic: https://raw.githubusercontent.com/d4s4n/miyumodules/refs/heads/main/assets/pfp.png
# meta banner: https://raw.githubusercontent.com/d4s4n/miyumodules/refs/heads/main/assets/banner.png

__version__ = (1, 0, 8)

import time
import asyncio
import random
import re
from collections import deque
from .. import loader, utils


@loader.tds
class FormatterMod(loader.Module):
    """Automatically formats your outgoing messages with advanced spam protection"""

    strings = {
        "name": "Formatter",
        "fmt_names": {
            "mono": "Monospace",
            "bold": "Bold",
            "italic": "Italic",
            "spoiler": "Spoiler",
        },
        "example_text": "Text example",
        "set_fmt": {
            "premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Formatter set to {fmt_name}</b>\n<b>Example:</b> <i>{example}</i>",
            "standard": "✅ <b>Formatter set to {fmt_name}</b>\n<b>Example:</b> <i>{example}</i>",
        },
        "disabled": {
            "premium": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Formatter is now off</b>",
            "standard": "🗑 <b>Formatter is now off</b>",
        },
        "status_on": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Formatter is ON</b>\n<b>Mode:</b> {fmt_name}\n<b>Example:</b> <i>{example}</i>\n\n<b>Available:</b> {avail_fmts}",
            "standard": "ℹ️ <b>Formatter is ON</b>\n<b>Mode:</b> {fmt_name}\n<b>Example:</b> <i>{example}</i>\n\n<b>Available:</b> {avail_fmts}",
        },
        "status_off": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Formatter is OFF</b>\n\n<b>Available:</b> {avail_fmts}",
            "standard": "ℹ️ <b>Formatter is OFF</b>\n\n<b>Available:</b> {avail_fmts}",
        },
        "invalid_format": {
            "premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Invalid format.</b>\nAvailable: {avail_fmts}",
            "standard": "❌ <b>Invalid format.</b>\nAvailable: {avail_fmts}",
        },
        "spam_detected": "<emoji document_id=5418144562944171366>⚠️</emoji> <b>Spam detected!</b> Formatter has been disabled.",
        "spam_on": {
            "premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Spam protection is ON</b>",
            "standard": "✅ <b>Spam protection is ON</b>",
        },
        "spam_off": {
            "premium": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Spam protection is OFF</b>",
            "standard": "🗑 <b>Spam protection is OFF</b>",
        },
        "spam_status_on": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Spam protection is ON</b>",
            "standard": "ℹ️ <b>Spam protection is ON</b>",
        },
        "spam_status_off": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Spam protection is OFF</b>",
            "standard": "ℹ️ <b>Spam protection is OFF</b>",
        },
    }

    strings_ru = {
        "_cls_doc": "Автоматически форматирует ваши исходящие сообщения с продвинутой защитой от спама",
        "_cmd_doc_fmt": "<формат / off> - Установить или выключить авто-форматирование",
        "_cmd_doc_fmtspam": "<on / off> - Включить или выключить защиту от спама",
        "fmt_names": {
            "mono": "Моно",
            "bold": "Жирный",
            "italic": "Курсив",
            "spoiler": "Спойлер",
        },
        "example_text": "Пример текста",
        "set_fmt": {
            "premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Форматирование установлено на {fmt_name}</b>\n<b>Пример:</b> <i>{example}</i>",
            "standard": "✅ <b>Форматирование установлено на {fmt_name}</b>\n<b>Пример:</b> <i>{example}</i>",
        },
        "disabled": {
            "premium": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Форматирование отключено</b>",
            "standard": "🗑 <b>Форматирование отключено</b>",
        },
        "status_on": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Форматирование ВКЛЮЧЕНО</b>\n<b>Режим:</b> {fmt_name}\n<b>Пример:</b> <i>{example}</i>\n\n<b>Доступно:</b> {avail_fmts}",
            "standard": "ℹ️ <b>Форматирование ВКЛЮЧЕНО</b>\n<b>Режим:</b> {fmt_name}\n<b>Пример:</b> <i>{example}</i>\n\n<b>Доступно:</b> {avail_fmts}",
        },
        "status_off": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Форматирование ВЫКЛЮЧЕНО</b>\n\n<b>Доступно:</b> {avail_fmts}",
            "standard": "ℹ️ <b>Форматирование ВЫКЛЮЧЕНО</b>\n\n<b>Доступно:</b> {avail_fmts}",
        },
        "invalid_format": {
            "premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Неверный тип.</b>\nДоступные: {avail_fmts}",
            "standard": "❌ <b>Неверный тип.</b>\nДоступные: {avail_fmts}",
        },
        "spam_detected": "<emoji document_id=5418144562944171366>⚠️</emoji> <b>Обнаружен спам!</b> Форматирование отключено.",
        "spam_on": {
            "premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Защита от спама ВКЛЮЧЕНА</b>",
            "standard": "✅ <b>Защита от спама ВКЛЮЧЕНА</b>",
        },
        "spam_off": {
            "premium": "<emoji document_id=5879896690210639947>🗑</emoji> <b>Защита от спама ВЫКЛЮЧЕНА</b>",
            "standard": "🗑 <b>Защита от спама ВЫКЛЮЧЕНА</b>",
        },
        "spam_status_on": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Защита от спама сейчас ВКЛЮЧЕНА</b>",
            "standard": "ℹ️ <b>Защита от спама сейчас ВКЛЮЧЕНА</b>",
        },
        "spam_status_off": {
            "premium": "<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Защита от спама сейчас ВЫКЛЮЧЕНА</b>",
            "standard": "ℹ️ <b>Защита от спама сейчас ВЫКЛЮЧЕНА</b>",
        },
    }

    def __init__(self):
        self.msg_history = deque(maxlen=30)
        self.formats = {
            "mono": "<code>",
            "bold": "<b>",
            "italic": "<i>",
            "spoiler": "<tg-spoiler>",
        }
        self.aliases = {
            "mono": "mono",
            "моно": "mono",
            "bold": "bold",
            "жирный": "bold",
            "ж": "bold",
            "b": "bold",
            "italic": "italic",
            "курсив": "italic",
            "к": "italic",
            "i": "italic",
            "spoiler": "spoiler",
            "спойлер": "spoiler",
            "с": "spoiler",
            "s": "spoiler",
            "off": "off",
            "выкл": "off",
            "офф": "off",
            "on": "on",
            "вкл": "on",
        }
        self.spam_config = {
            "windows": [{"duration": 10, "limit": 15}, {"duration": 60, "limit": 30}],
            "trivial_limit": 5,
            "similarity_threshold": 6,
        }
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+"
        )

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()
        if self.db.get("Formatter", "mode", None) is None:
            self.db.set("Formatter", "mode", "off")
        if self.db.get("Formatter", "spam_protection", None) is None:
            self.db.set("Formatter", "spam_protection", True)

    def get_string(self, key, use_prem, **kwargs):
        return self.strings(key)["premium" if use_prem else "standard"].format(**kwargs)

    def get_fmt_info(self, mode):
        names = self.strings("fmt_names")
        tag = self.formats.get(mode, "")
        end_tag = f"</{tag[1:-1]}>"
        name = names.get(mode, "Unknown")
        example = f"{tag}{self.strings('example_text')}{end_tag}"
        return name, example

    def is_trivial(self, msg):
        return bool(re.match(r"^(.)\1+$", msg) or re.match(r"^(..+?)\1+$", msg))

    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        prev_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        return prev_row[-1]

    def is_similar(self, msg1, msg2):
        if self.is_trivial(msg1) or self.is_trivial(msg2):
            return False
        if self.levenshtein(msg1, msg2) < 5:
            return True
        words1, words2 = set(msg1.split()), set(msg2.split())
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return (intersection / union) > 0.4 if union > 0 else False

    def check_spam(self, text):
        now = time.time()
        self.msg_history.append({"msg": text, "time": now})
        for window in self.spam_config["windows"]:
            if (
                len(
                    [
                        m
                        for m in self.msg_history
                        if now - m["time"] <= window["duration"]
                    ]
                )
                > window["limit"]
            ):
                return True

        short_window_msgs = [
            m["msg"]
            for m in self.msg_history
            if now - m["time"] <= self.spam_config["windows"][0]["duration"]
        ]

        if len(short_window_msgs) > self.spam_config["trivial_limit"]:
            if (
                sum(1 for msg in short_window_msgs if self.is_trivial(msg))
                > self.spam_config["trivial_limit"]
            ):
                return True

        if len(short_window_msgs) > self.spam_config["similarity_threshold"]:
            similar_count = sum(
                1
                for i in range(len(short_window_msgs))
                for j in range(i + 1, len(short_window_msgs))
                if self.is_similar(short_window_msgs[i], short_window_msgs[j])
            )
            if similar_count > self.spam_config["similarity_threshold"]:
                return True
        return False

    @loader.command()
    async def fmt(self, message):
        use_prem = self.me.premium or message.is_private
        args = utils.get_args_raw(message).lower()
        mode = self.db.get("Formatter", "mode", "off")
        avail_fmts = ", ".join(f"<code>{key}</code>" for key in self.formats)

        if not args:
            if mode == "off":
                await utils.answer(
                    message,
                    self.get_string("status_off", use_prem, avail_fmts=avail_fmts),
                )
            else:
                fmt_name, example = self.get_fmt_info(mode)
                await utils.answer(
                    message,
                    self.get_string(
                        "status_on",
                        use_prem,
                        fmt_name=fmt_name,
                        example=example,
                        avail_fmts=avail_fmts,
                    ),
                )
            return

        target_mode = self.aliases.get(args)
        if not target_mode or target_mode not in self.formats and target_mode != "off":
            await utils.answer(
                message,
                self.get_string("invalid_format", use_prem, avail_fmts=avail_fmts),
            )
            return

        self.db.set("Formatter", "mode", target_mode)

        if target_mode == "off":
            await utils.answer(message, self.get_string("disabled", use_prem))
        else:
            fmt_name, example = self.get_fmt_info(target_mode)
            await utils.answer(
                message,
                self.get_string(
                    "set_fmt", use_prem, fmt_name=fmt_name, example=example
                ),
            )

    @loader.command()
    async def fmtspam(self, message):
        use_prem = self.me.premium or message.is_private
        args = utils.get_args_raw(message).lower()
        is_on = self.db.get("Formatter", "spam_protection", True)

        if not args:
            key = "spam_status_on" if is_on else "spam_status_off"
            await utils.answer(message, self.get_string(key, use_prem))
            return

        choice = self.aliases.get(args)
        if choice not in ["on", "off"]:
            await utils.answer(
                message,
                self.get_string("invalid_format", use_prem, avail_fmts="on, off"),
            )
            return

        new_state = choice == "on"
        self.db.set("Formatter", "spam_protection", new_state)

        key = "spam_on" if new_state else "spam_off"
        await utils.answer(message, self.get_string(key, use_prem))

    async def watcher(self, message):
        if not message.out or not message.text:
            return

        mode = self.db.get("Formatter", "mode", "off")
        if mode == "off":
            return

        chat = await message.get_chat()
        if (
            (message.is_channel and not message.is_group)
            or getattr(chat, "is_self", False)
            or getattr(chat, "bot", False)
        ):
            return

        text = message.text
        if text.startswith(self.get_prefix()) or text.startswith("/"):
            return

        text_without_emoji = self.emoji_pattern.sub("", text)
        if not text_without_emoji.strip():
            return

        if self.db.get("Formatter", "spam_protection", True):
            if self.check_spam(text):
                self.db.set("Formatter", "mode", "off")
                await self.client.send_message("me", self.strings("spam_detected"))
                return

        delay = random.uniform(0.1, 0.15)
        try:
            await asyncio.sleep(delay)
            tag = self.formats.get(mode)
            end_tag = f"</{tag[1:-1]}>"
            if tag:
                await message.edit(
                    f"{tag}{utils.escape_html(text)}{end_tag}", parse_mode="html"
                )
        except Exception:
            pass
