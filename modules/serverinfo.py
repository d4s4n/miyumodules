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

__version__ = (1, 0, 1)

import psutil
import platform
import time
from datetime import timedelta
from .. import loader, utils

@loader.tds
class ServerInfoMod(loader.Module):

    strings = {
        "name": "ServerInfo"
    }

    version = "v{}.{}.{}".format(*__version__)

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        try:
            await self.inline.bot.send_message(
                "@HikkaUserbot",
                "🌙 <b>Модуль ServerInfo ({}) загружен ( ^_^)ﾉ</b>\n".format(self.version) +
                "ℹ️ Получение информации о сервере\n\n"
                "▫️ <code>.serverinfo</code> - Показать информацию о сервере\n\n"
                "🤲 Разработчик: @miyumodules"
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {str(e)}")

    async def serverinfocmd(self, message):
        try:
            cpu_load = psutil.cpu_percent(interval=1)
            cpu_cores = psutil.cpu_count(logical=False)

            cpu_name = "Неизвестно"
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_name = line.split(":")[1].strip()
                            break
            except:
                cpu_name = platform.processor() or "Неизвестно"

            ram = psutil.virtual_memory()
            total_ram = ram.total / (1024**3)
            used_ram = ram.used / (1024**3)

            disk = psutil.disk_usage('/')
            total_disk = disk.total / (1024**3)
            used_disk = disk.used / (1024**3)
            free_disk = disk.free / (1024**3)

            net = psutil.net_io_counters()
            net_down = net.bytes_recv / (1024**3)
            net_up = net.bytes_sent / (1024**3)

            os_info = platform.platform()
            python_ver = platform.python_version()

            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            days = int(uptime // (24 * 3600))
            time_part = timedelta(seconds=int(uptime % (24 * 3600)))

            uptime_str = ""
            if days > 0:
                if 11 <= days % 100 <= 19:
                    day_word = "дней"
                elif days % 10 == 1:
                    day_word = "день"
                elif 2 <= days % 10 <= 4:
                    day_word = "дня"
                else:
                    day_word = "дней"
                uptime_str += f"{days} {day_word}, "
            uptime_str += str(time_part)

            def bar(percentage, width=10):
                filled = int(width * percentage // 100)
                return '█' * filled + '▒' * (width - filled)

            cpu_bar = bar(cpu_load)
            ram_bar = bar(used_ram / total_ram * 100)
            disk_bar = bar(used_disk / total_disk * 100)

            reply = "🌙 <b>Информация о сервере</b>\n\n"
            reply += "┎ <b>⚙️ Процессор</b>\n"
            reply += f"┣ <b>Модель:</b> <code>{cpu_name}</code>\n"
            reply += f"┣ <b>Ядра:</b> <code>{cpu_cores}</code>\n"
            reply += f"┗ <b>Нагрузка:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>\n\n"
            reply += "┎ <b>📈 Память</b>\n"
            reply += f"┣ <b>ОЗУ:</b> <code>{ram_bar} {used_ram:.2f}/{total_ram:.2f} ГБ</code>\n"
            reply += f"┗ <b>Диск:</b> <code>{disk_bar} {used_disk:.2f}/{total_disk:.2f} ГБ (Свободно: {free_disk:.2f} ГБ)</code>\n\n"
            reply += "┎ <b>🌐 Сеть</b>\n"
            reply += f"┗ <b>Трафик:</b> <code>↓ {net_down:.2f} ГБ / ↑ {net_up:.2f} ГБ</code>\n\n"
            reply += "┎ <b>🛠️ Система</b>\n"
            reply += f"┣ <b>ОС:</b> <code>{os_info}</code>\n"
            reply += f"┣ <b>Python:</b> <code>{python_ver}</code>\n"
            reply += f"┗ <b>Аптайм:</b> <code>{uptime_str}</code>\n\n"
            reply += "🤲 <i>by @miyumodules</i>"

            await utils.answer(message, reply)
        except Exception as e:
            await utils.answer(message, f"Ошибка: {str(e)}")
