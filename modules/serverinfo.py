# *          __  __ _             __  __           _       _
# *         |  \/  (_)_   _ _   _|  \/  | ___   __| |_   _| | ___  ___
# *         | |\/| | | | | | | | | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
# *         | |  | | | |_| | |_| | |  | | (_) | (_| | |_| | |  __/\__ \
# *         |_|  |_|_|\__, |\__,_|_|  |_|\___/ \__,_|\__,_|_|\___||___/
# *                   |___/
# *
# *                          © Copyright 2025
# *
# *                      https://t.me/miyumodules
# *
# * 🔒 Code is licensed under GNU AGPLv3
# * 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# * ⛔️ You CANNOT edit this file without direct permission from the author.
# * ⛔️ You CANNOT distribute this file if you have modified it without the direct permission of the author.

# Name: ServerInfo
# Author: miyumodules
# Commands:
# .serverinfo
# scope: hikka_only
# meta developer: @miyumodules

# meta pic: https://github.com/d4s4n/miyumodules/blob/main/assets/pfp.png?raw=true
# meta banner: https://github.com/d4s4n/miyumodules/blob/main/assets/banner.png?raw=true

__version__ = (1, 1, 5)

import psutil
import platform
import time
from datetime import timedelta
from .. import loader, utils

@loader.tds
class ServerInfoMod(loader.Module):
    """Shows information about the server where the userbot is running"""

    strings = {
        "name": "ServerInfo",
        "info_template": (
            "┎ <b>CPU</b>\n"
            "┣ <emoji document_id=5172869086727635492>💻</emoji> <b>Model:</b> <code>{cpu_name}</code>\n"
            "┣ <emoji document_id=5172839378438849164>💻</emoji> <b>Cores:</b> <code>{cpu_cores}</code>\n"
            "┗ <emoji document_id=5174983383163339593>💻</emoji> <b>Load:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>\n\n"
            "┎ <b>Memory</b>\n"
            "┣ <emoji document_id=5174693704799093859>💻</emoji> <b>RAM:</b> <code>{used_ram:.2f}/{total_ram:.2f} GB</code>\n"
            "┗ <emoji document_id=5175135107178038706>💻</emoji> <b>Disk:</b> <code>{used_disk:.2f} GB (Free: {free_disk:.2f} GB)</code>\n\n"
            "┎ <b>Network</b>\n"
            "┗ <emoji document_id=5175152196852908642>💻</emoji> <b>Traffic:</b> <code>↓ {net_down:.2f} GB / ↑ {net_up:.2f} GB</code>\n\n"
            "┎ <b>System</b>\n"
            "┣ <emoji document_id=5275996452709998361>👩‍💻</emoji> <b>OS:</b> <code>{os_info}</code>\n"
            "┣ <emoji document_id=5276529733029339480>👩‍💻</emoji> <b>Python:</b> <code>{python_ver}</code>\n"
            "┗ <emoji document_id=5172533495162995360>💻</emoji> <b>Uptime:</b> <code>{uptime_str}</code>"
        ),
    }
    
    strings_ru = {
        "_cls_doc": "Показывает информацию о сервере, на котором запущен юзербот",
        "_cmd_doc_serverinfo": "Показать информацию о сервере",
        "info_template": (
            "┎ <b>Процессор</b>\n"
            "┣ <emoji document_id=5172869086727635492>💻</emoji> <b>Модель:</b> <code>{cpu_name}</code>\n"
            "┣ <emoji document_id=5172839378438849164>💻</emoji> <b>Ядра:</b> <code>{cpu_cores}</code>\n"
            "┗ <emoji document_id=5174983383163339593>💻</emoji> <b>Нагрузка:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>\n\n"
            "┎ <b>Память</b>\n"
            "┣ <emoji document_id=5174693704799093859>💻</emoji> <b>ОЗУ:</b> <code>{used_ram:.2f}/{total_ram:.2f} ГБ</code>\n"
            "┗ <emoji document_id=5175135107178038706>💻</emoji> <b>Диск:</b> <code>{used_disk:.2f} ГБ (Свободно: {free_disk:.2f} ГБ)</code>\n\n"
            "┎ <b>Сеть</b>\n"
            "┗ <emoji document_id=5175152196852908642>💻</emoji> <b>Трафик:</b> <code>↓ {net_down:.2f} ГБ / ↑ {net_up:.2f} ГБ</code>\n\n"
            "┎ <b>Система</b>\n"
            "┣ <emoji document_id=5275996452709998361>👩‍💻</emoji> <b>ОС:</b> <code>{os_info}</code>\n"
            "┣ <emoji document_id=5276529733029339480>👩‍💻</emoji> <b>Python:</b> <code>{python_ver}</code>\n"
            "┗ <emoji document_id=5172533495162995360>💻</emoji> <b>Аптайм:</b> <code>{uptime_str}</code>"
        ),
    }

    async def get_stats(self):
        s = {}
        s["cpu_load"] = psutil.cpu_percent(interval=0.5)
        s["cpu_cores"] = psutil.cpu_count(logical=False)
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        s["cpu_name"] = line.split(":", 1)[1].strip()
                        break
        except:
            s["cpu_name"] = platform.processor() or "Unknown"

        ram = psutil.virtual_memory()
        s["total_ram"] = ram.total / 1024 ** 3
        s["used_ram"] = ram.used / 1024 ** 3

        disk = psutil.disk_usage('/')
        s["total_disk"] = disk.total / 1024 ** 3
        s["used_disk"] = disk.used / 1024 ** 3
        s["free_disk"] = disk.free / 1024 ** 3

        net = psutil.net_io_counters()
        s["net_down"] = net.bytes_recv / 1024 ** 3
        s["net_up"] = net.bytes_sent / 1024 ** 3

        s["os_info"] = platform.platform()
        s["python_ver"] = platform.python_version()

        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        days = int(uptime // (24 * 3600))
        time_part = timedelta(seconds=int(uptime % (24 * 3600)))

        if days:
            day_word = "дней"
            if not (11 <= days % 100 <= 19):
                if days % 10 == 1: day_word = "день"
                elif 2 <= days % 10 <= 4: day_word = "дня"
            s["uptime_str"] = f"{days} {day_word}, {time_part}"
        else:
            s["uptime_str"] = str(time_part)
        
        bar = lambda p, w=10: '█' * int(p * w / 100) + '▒' * (w - int(p * w / 100))
        s["cpu_bar"] = bar(s["cpu_load"])
        return s

    @loader.command(
        ru_doc="Показать информацию о сервере"
    )
    async def serverinfo(self, message):
        """Show server info"""
        stats = await self.get_stats()
        text = self.strings("info_template").format(**stats)
        await utils.answer(message, text)
