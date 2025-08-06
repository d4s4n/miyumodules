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

# Name: FortInfo
# Author: miyumodules
# Commands:
# .fnnews | .fnmap | .fnitem | .fncreator | .fnaes
# scope: hikka_only
# requires: aiohttp, pillow
# meta developer: @miyumodules
# meta pic: https://github.com/d4s4n/miyumodules/blob/main/assets/pfp.png?raw=true
# meta banner: https://github.com/d4s4n/miyumodules/blob/main/assets/banner.png?raw=true

__version__ = (1, 3, 5)

import aiohttp
import asyncio
import io
import re
from datetime import datetime
from urllib.parse import quote_plus
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .. import loader, utils


@loader.tds
class FortInfoMod(loader.Module):
    strings = {
        "name": "FortInfo",
        "processing": {
            "premium": "<b><emoji document_id=5960751816084820359>⏲️</emoji> Processing...</b>",
            "standard": "<b>⏳ Processing...</b>",
        },
        "error": {
            "premium": "<b><emoji document_id=5879896690210639497>💥</emoji> Error:</b> <code>{error}</code>",
            "standard": "<b>💥 Error:</b> <code>{error}</code>",
        },
        "news_url": "https://fortnite-api.com/v2/news/br?language=en",
        "map_url": "https://fortnite-api.com/v1/map?language=en",
        "item_search_url": "https://fortnite-api.com/v2/cosmetics/br/search/all?name={query}&language=en",
        "creator_code_url": "https://fortnite-api.com/v2/creatorcode?name={query}",
        "aes_url": "https://fortnite-api.com/v2/aes",
        "news_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>🗞</emoji> {title}</b>\n\n<i>{body}</i>",
            "standard": "<b>🗞 {title}</b>\n\n<i>{body}</i>",
        },
        "no_news": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> No news found.</b>",
            "standard": "<b>⚠️ No news found.</b>",
        },
        "map_caption": {
            "premium": "<b><emoji document_id=5883955653348692941>🗺️</emoji> Current map for {date}</b>\n\n<i>This map shows the names of locations for the current Fortnite season.</i>",
            "standard": "<b>🗺️ Current map for {date}</b>\n\n<i>This map shows the names of locations for the current Fortnite season.</i>",
        },
        "no_map": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Map not available.</b>",
            "standard": "<b>⚠️ Map not available.</b>",
        },
        "no_item_arg": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> You need to provide an item name.</b>",
            "standard": "<b>⚠️ You need to provide an item name.</b>",
        },
        "russian_input_warning": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Please use English for item search.</b>",
            "standard": "<b>⚠️ Please use English for item search.</b>",
        },
        "item_not_found": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Item not found.</b>",
            "standard": "<b>⚠️ Item not found.</b>",
        },
        "item_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> {name} ({rarity})</b>\n"
            "<i>{description}</i>\n\n"
            "<b><emoji document_id=5877332341331857066>📁</emoji> Set:</b> <code>{set_name}</code>\n"
            "<b><emoji document_id=5956561916573782596>📄</emoji> Type:</b> <code>{type}</code>\n"
            "<b><emoji document_id=5988023995125993550>🛠</emoji> ID:</b> <code>{id}</code>",
            "standard": "<b>✨ {name} ({rarity})</b>\n"
            "<i>{description}</i>\n\n"
            "<b>🗃 Set:</b> <code>{set_name}</code>\n"
            "<b>📋 Type:</b> <code>{type}</code>\n"
            "<b>🆔 ID:</b> <code>{id}</code>",
        },
        "no_creator_code_arg": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> You need to provide a creator code.</b>",
            "standard": "<b>⚠️ You need to provide a creator code.</b>",
        },
        "creator_not_found": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Creator code not found.</b>",
            "standard": "<b>⚠️ Creator code not found.</b>",
        },
        "creator_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> Creator Code Info</b>\n\n<b><emoji document_id=6005570495603282482>🔑</emoji> Code:</b> <code>{code}</code>\n<b><emoji document_id=5908808657700655253>🙋</emoji> Account:</b> <code>{account_name}</code>\n<b><emoji document_id=5931409969613116639>🛡</emoji> Status:</b> <code>{status}</code>",
            "standard": "<b>✨ Creator Code Info</b>\n\n<b>👨‍💻 Code:</b> <code>{code}</code>\n<b>👤 Account:</b> <code>{account_name}</code>\n<b>ℹ️ Status:</b> <code>{status}</code>",
        },
        "creator_status_active": "Active",
        "creator_status_inactive": "Inactive",
        "no_aes_data": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> AES key data not found.</b>",
            "standard": "<b>⚠️ AES key data not found.</b>",
        },
        "aes_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> AES Key Info</b>\n\n<b><emoji document_id=6005570495603282482>🔑</emoji> Main Key:</b> <code>{main_key}</code>\n<b><emoji document_id=5877307202888273539>📥</emoji> Build:</b> <code>{build}</code>\n<b><emoji document_id=5845943483382110702>🔄</emoji> Updated:</b> <code>{updated}</code>\n<b><emoji document_id=5874960879434338403>🔎</emoji> Dynamic Keys:</b> <code>{dynamic_keys}</code>",
            "standard": "<b>✨ AES Key Info</b>\n\n<b>🔑 Main Key:</b> <code>{main_key}</code>\n<b>📦 Build:</b> <code>{build}</code>\n<b>📅 Updated:</b> <code>{updated}</code>\n<b>🔒 Dynamic Keys:</b> <code>{dynamic_keys}</code>",
        },
        "not_available": "N/A",
        "months": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    }

    strings_ru = {
        "_cls_doc": "Предоставляет публичную информацию по Fortnite (новости, карта, предметы, коды автора, AES-ключи)",
        "_cmd_doc_fnnews": "- Показать последние новости",
        "_cmd_doc_fnmap": "- Показать актуальную карту",
        "_cmd_doc_fnitem": "<название> - Найти информацию о предмете",
        "_cmd_doc_fncreator": "<код> - Показать информацию о коде автора",
        "_cmd_doc_fnaes": "- Показать информацию о текущем AES-ключе",
        "processing": {
            "premium": "<b><emoji document_id=5960751816084820359>⏲️</emoji> Обработка...</b>",
            "standard": "<b>⏳ Обработка...</b>",
        },
        "error": {
            "premium": "<b><emoji document_id=5879896690210639497>💥</emoji> Ошибка:</b> <code>{error}</code>",
            "standard": "<b>💥 Ошибка:</b> <code>{error}</code>",
        },
        "news_url": "https://fortnite-api.com/v2/news/br?language=ru",
        "map_url": "https://fortnite-api.com/v1/map?language=ru",
        "item_search_url": "https://fortnite-api.com/v2/cosmetics/br/search/all?name={query}&language=ru",
        "creator_code_url": "https://fortnite-api.com/v2/creatorcode?name={query}",
        "aes_url": "https://fortnite-api.com/v2/aes",
        "news_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>🗞</emoji> {title}</b>\n\n<i>{body}</i>",
            "standard": "<b>🗞 {title}</b>\n\n<i>{body}</i>",
        },
        "no_news": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Новости не найдены.</b>",
            "standard": "<b>⚠️ Новости не найдены.</b>",
        },
        "map_caption": {
            "premium": "<b><emoji document_id=5883955653348692941>🗺️</emoji> Актуальная карта на {date}</b>\n\n<i>На карте указаны названия локаций текущего сезона Fortnite.</i>",
            "standard": "<b>🗺️ Актуальная карта на {date}</b>\n\n<i>На карте указаны названия локаций текущего сезона Fortnite.</i>",
        },
        "no_map": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Карта недоступна.</b>",
            "standard": "<b>⚠️ Карта недоступна.</b>",
        },
        "no_item_arg": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Нужно указать название предмета.</b>",
            "standard": "<b>⚠️ Нужно указать название предмета.</b>",
        },
        "russian_input_warning": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Пожалуйста, используйте английский язык для поиска предметов.</b>",
            "standard": "<b>⚠️ Пожалуйста, используйте английский язык для поиска предметов.</b>",
        },
        "item_not_found": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Предмет не найден.</b>",
            "standard": "<b>⚠️ Предмет не найден.</b>",
        },
        "item_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> {name} ({rarity})</b>\n"
            "<i>{description}</i>\n\n"
            "<b><emoji document_id=5877332341331857066>📁</emoji> Набор:</b> <code>{set_name}</code>\n"
            "<b><emoji document_id=5956561916573782596>📄</emoji> Тип:</b> <code>{type}</code>\n"
            "<b><emoji document_id=5988023995125993550>🛠</emoji> ID:</b> <code>{id}</code>",
            "standard": "<b>✨ {name} ({rarity})</b>\n"
            "<i>{description}</i>\n\n"
            "<b>🗃 Набор:</b> <code>{set_name}</code>\n"
            "<b>📋 Тип:</b> <code>{type}</code>\n"
            "<b>🆔 ID:</b> <code>{id}</code>",
        },
        "no_creator_code_arg": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Нужно указать код автора.</b>",
            "standard": "<b>⚠️ Нужно указать код автора.</b>",
        },
        "creator_not_found": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Код автора не найден.</b>",
            "standard": "<b>⚠️ Код автора не найден.</b>",
        },
        "creator_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> Информация о коде автора</b>\n\n<b><emoji document_id=6005570495603282482>🔑</emoji> Код:</b> <code>{code}</code>\n<b><emoji document_id=5908808657700655253>🙋</emoji> Аккаунт:</b> <code>{account_name}</code>\n<b><emoji document_id=5931409969613116639>🛡</emoji> Статус:</b> <code>{status}</code>",
            "standard": "<b>✨ Информация о коде автора</b>\n\n<b>👨‍💻 Код:</b> <code>{code}</code>\n<b>👤 Аккаунт:</b> <code>{account_name}</code>\n<b>ℹ️ Статус:</b> <code>{status}</code>",
        },
        "creator_status_active": "Активен",
        "creator_status_inactive": "Неактивен",
        "no_aes_data": {
            "premium": "<b><emoji document_id=5881702736843511327>⚠️</emoji> Данные об AES-ключе не найдены.</b>",
            "standard": "<b>⚠️ Данные об AES-ключе не найдены.</b>",
        },
        "aes_caption": {
            "premium": "<b><emoji document_id=5958376256788502078>✨</emoji> Информация об AES-ключе</b>\n\n<b><emoji document_id=6005570495603282482>🔑</emoji> Главный ключ:</b> <code>{main_key}</code>\n<b><emoji document_id=5877307202888273539>📥</emoji> Сборка:</b> <code>{build}</code>\n<b><emoji document_id=5845943483382110702>🔄</emoji> Обновлено:</b> <code>{updated}</code>\n<b><emoji document_id=5874960879434338403>🔎</emoji> Динамические ключи:</b> <code>{dynamic_keys}</code>",
            "standard": "<b>✨ Информация об AES-ключе</b>\n\n<b>🔑 Главный ключ:</b> <code>{main_key}</code>\n<b>📦 Сборка:</b> <code>{build}</code>\n<b>📅 Обновлено:</b> <code>{updated}</code>\n<b>🔒 Динамические ключи:</b> <code>{dynamic_keys}</code>",
        },
        "not_available": "Н/Д",
        "months": [
            "Января",
            "Февраля",
            "Марта",
            "Апреля",
            "Мая",
            "Июня",
            "Июля",
            "Августа",
            "Сентября",
            "Октября",
            "Ноября",
            "Декабря",
        ],
    }

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.rarity_colors = {
            "common": (120, 120, 120),
            "uncommon": (0, 170, 0),
            "rare": (0, 170, 255),
            "epic": (170, 0, 255),
            "legendary": (255, 170, 0),
            "mythic": (255, 215, 0),
            "icon": (0, 255, 255),
            "starwars": (255, 255, 255),
            "marvel": (255, 0, 0),
            "dc": (100, 100, 255),
            "dark": (255, 0, 255),
            "lava": (255, 100, 0),
            "slurp": (0, 255, 170),
            "frozen": (0, 200, 255),
            "gaminglegends": (128, 0, 128),
        }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.font_watermark = ImageFont.load_default()

    async def on_unload(self):
        await self.session.close()

    async def get_style(self, message):
        me = await self.client.get_me()
        is_premium = me.premium or message.is_private
        return "premium" if is_premium else "standard"

    async def api_request(self, url, headers=None):
        try:
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 404:
                    return None
                resp.raise_for_status()
                if "application/json" in resp.headers.get("Content-Type", ""):
                    data = await resp.json()
                    return data.get("data", data)
                return await resp.read()
        except aiohttp.ClientError:
            return None

    def format_date(self, date_obj):
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings
        months = strings_to_use["months"]
        return f"{date_obj.day} {months[date_obj.month - 1]} {date_obj.year}"

    def create_gradient(self, color, W, H):
        start_color = tuple(c // 2 for c in color)
        gradient = Image.new("RGBA", (1, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        for y in range(H):
            inter_color = tuple(
                int(start_color[i] + (color[i] - start_color[i]) * (y / H))
                for i in range(3)
            )
            draw.point((0, y), fill=inter_color)
        return gradient.resize((W, H))

    def create_glow(self, image, blur_radius=20, color=(255, 255, 255, 80)):
        mask = image.split()[-1]
        glow_mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        glow_image = Image.new("RGBA", image.size, color)
        glow_image.putalpha(glow_mask)
        return Image.alpha_composite(glow_image, image)

    async def create_item_image(self, item):
        W, H = 1024, 1024

        img_url = item.get("images", {}).get("featured") or item.get("images", {}).get(
            "icon"
        )
        async with self.session.get(img_url) as resp:
            item_img_data = await resp.read()
            item_img = Image.open(io.BytesIO(item_img_data)).convert("RGBA")

        rarity = item.get("rarity", {}).get("value", "common").lower()
        bg_color = self.rarity_colors.get(rarity, (120, 120, 120))
        bg = self.create_gradient(bg_color, W, H)

        text = "MiyuModules"
        text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        font_size = 50
        font = ImageFont.load_default()
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = (
            text_bbox[2] - text_bbox[0],
            text_bbox[3] - text_bbox[1],
        )

        for y in range(-text_height, H, text_height * 2):
            for x in range(-text_width, W, text_width * 2):
                draw.text(
                    (x, y),
                    text,
                    font=font,
                    fill=(255, 255, 255, 20),
                )

        bg.paste(text_layer, (0, 0), text_layer)

        item_with_glow = await asyncio.to_thread(self.create_glow, item_img)
        item_with_glow.thumbnail((W - 80, H - 80))

        bg.paste(
            item_with_glow,
            ((W - item_with_glow.width) // 2, (H - item_with_glow.height) // 2),
            item_with_glow,
        )

        buffer = io.BytesIO()
        await asyncio.to_thread(bg.save, buffer, "PNG")
        buffer.name = "item_image.png"
        buffer.seek(0)
        return buffer

    @loader.command(
        aliases=["fitem"], ru_doc="<название> - Найти информацию о предмете"
    )
    async def fnitem(self, message):
        style = await self.get_style(message)
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings

        query = utils.get_args_raw(message)

        if not query:
            await utils.answer(message, strings_to_use["no_item_arg"][style])
            return

        if re.search("[а-яА-Я]", query):
            await utils.answer(message, strings_to_use["russian_input_warning"][style])
            return

        msg = await utils.answer(message, strings_to_use["processing"][style])
        url = strings_to_use["item_search_url"].format(query=quote_plus(query))
        data = await self.api_request(url)

        if not data:
            await utils.answer(msg, strings_to_use["item_not_found"][style])
            return

        item = data[0] if isinstance(data, list) else data
        image_buffer = await self.create_item_image(item)

        not_avail = strings_to_use["not_available"]
        set_name = item.get("set", {}).get("text", not_avail)
        if lang == "ru" and set_name.startswith("Part of the "):
            set_name = set_name.split("Part of the ")[-1].strip()

        type_translations = {
            "outfit": "Скин",
            "pickaxe": "Кирка",
            "emote": "Эмоция",
            "glider": "Дельтаплан",
            "wrap": "Обёртка",
            "spray": "Граффити",
            "emoji": "Эмодзи",
            "backpack": "Рюкзак",
            "loadingscreen": "Экран загрузки",
            "contrail": "След",
            "music": "Музыка",
            "bundle": "Набор",
        }
        item_type = item.get("type", {}).get("displayValue", not_avail)
        if lang == "ru":
            item_type_key = item.get("type", {}).get("value", "").lower()
            item_type = type_translations.get(item_type_key, item_type)

        caption = strings_to_use["item_caption"][style].format(
            name=utils.escape_html(item.get("name", not_avail)),
            rarity=utils.escape_html(
                item.get("rarity", {}).get("displayValue", not_avail)
            ),
            description=utils.escape_html(item.get("description", not_avail)),
            set_name=utils.escape_html(set_name),
            type=utils.escape_html(item_type),
            id=utils.escape_html(item.get("id", not_avail)),
        )

        await self.client.send_file(
            message.peer_id,
            file=image_buffer,
            caption=caption,
            reply_to=message.reply_to_msg_id,
        )
        await msg.delete()

    @loader.command(aliases=["fnc"], ru_doc="<код> - Показать информацию о коде автора")
    async def fncreator(self, message):
        style = await self.get_style(message)
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings

        code = utils.get_args_raw(message)

        if not code:
            await utils.answer(message, strings_to_use["no_creator_code_arg"][style])
            return

        msg = await utils.answer(message, strings_to_use["processing"][style])
        url = strings_to_use["creator_code_url"].format(query=quote_plus(code))
        data = await self.api_request(url)

        if not data or not data.get("account"):
            await utils.answer(msg, strings_to_use["creator_not_found"][style])
            return

        status_key = (
            "creator_status_active"
            if data.get("status") == "ACTIVE"
            else "creator_status_inactive"
        )
        status_text = strings_to_use[status_key]
        not_avail = strings_to_use["not_available"]
        account_name = data.get("account", {}).get("name") or not_avail

        text = strings_to_use["creator_caption"][style].format(
            code=utils.escape_html(data.get("code") or not_avail),
            account_name=utils.escape_html(account_name),
            status=utils.escape_html(status_text),
        )

        await utils.answer(msg, text)

    @loader.command(aliases=["fnews"], ru_doc="- Показать последние новости")
    async def fnnews(self, message):
        style = await self.get_style(message)
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings

        msg = await utils.answer(message, strings_to_use["processing"][style])
        url = strings_to_use["news_url"]
        data = await self.api_request(url)

        if not (news := data.get("motds")):
            await utils.answer(msg, strings_to_use["no_news"][style])
            return

        latest = news[0]
        not_avail = strings_to_use["not_available"]
        caption = strings_to_use["news_caption"][style].format(
            title=utils.escape_html(latest.get("title", not_avail)),
            body=utils.escape_html(latest.get("body", not_avail)),
        )

        if image_url := latest.get("image"):
            img = await self.api_request(image_url)
            await self.client.send_file(
                message.peer_id,
                file=img,
                caption=caption,
                reply_to=message.reply_to_msg_id,
            )
            await msg.delete()
        else:
            await utils.answer(msg, caption)

    @loader.command(aliases=["fmap"], ru_doc="- Показать актуальную карту")
    async def fnmap(self, message):
        style = await self.get_style(message)
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings

        msg = await utils.answer(message, strings_to_use["processing"][style])
        url = strings_to_use["map_url"]
        data = await self.api_request(url)

        if not (map_url := data.get("images", {}).get("pois")):
            await utils.answer(msg, strings_to_use["no_map"][style])
            return

        img = await self.api_request(map_url)
        today_str = self.format_date(datetime.now())

        caption = strings_to_use["map_caption"][style].format(date=today_str)
        await self.client.send_file(
            message.peer_id, file=img, caption=caption, reply_to=message.reply_to_msg_id
        )
        await msg.delete()

    @loader.command(
        aliases=["faes"], ru_doc="- Показать информацию о текущем AES-ключе"
    )
    async def fnaes(self, message):
        style = await self.get_style(message)
        lang = self.db.get("hikka", "lang", "en")
        strings_to_use = self.strings_ru if lang == "ru" else self.strings

        msg = await utils.answer(message, strings_to_use["processing"][style])
        url = strings_to_use["aes_url"]
        data = await self.api_request(url)

        if not data:
            await utils.answer(msg, strings_to_use["no_aes_data"][style])
            return

        not_avail = strings_to_use["not_available"]
        updated_str = data.get("updated", not_avail)

        if updated_str != not_avail:
            try:
                updated_date = datetime.strptime(updated_str, "%Y-%m-%dT%H:%M:%SZ")
                updated_str = self.format_date(updated_date)
            except ValueError:
                pass

        dynamic_keys = data.get("dynamicKeys", [])
        dynamic_keys_str = (
            ", ".join([key.get("key", not_avail) for key in dynamic_keys]) or not_avail
        )

        text = strings_to_use["aes_caption"][style].format(
            main_key=utils.escape_html(data.get("mainKey", not_avail)),
            build=utils.escape_html(data.get("build", not_avail)),
            updated=utils.escape_html(updated_str),
            dynamic_keys=utils.escape_html(dynamic_keys_str),
        )

        await utils.answer(msg, text)
