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

__version__ = (1, 0, 5)

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
        "server_info_title": "<b>Server Information</b>",
        "cpu_title": "┎ <b>CPU</b>",
        "cpu_model": "┣ <b>Model:</b> <code>{cpu_name}</code>",
        "cpu_cores": "┣ <b>Cores:</b> <code>{cpu_cores}</code>",
        "cpu_load": "┗ <b>Load:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>",
        "mem_title": "┎ <b>Memory</b>",
        "mem_ram": "┣ <b>RAM:</b> <code>{ram_bar} {used_ram:.2f}/{total_ram:.2f} GB</code>",
        "mem_disk": "┗ <b>Disk:</b> <code>{disk_bar} {used_disk:.2f}/{total_disk:.2f} GB (Free: {free_disk:.2f} GB)</code>",
        "net_title": "┎ <b>Network</b>",
        "net_traffic": "┗ <b>Traffic:</b> <code>↓ {net_down:.2f} GB / ↑ {net_up:.2f} GB</code>",
        "sys_title": "┎ <b>System</b>",
        "sys_os": "┣ <b>OS:</b> <code>{os_info}</code>",
        "sys_python": "┣ <b>Python:</b> <code>{python_ver}</code>",
        "sys_uptime": "┗ <b>Uptime:</b> <code>{uptime_str}</code>",
    }
    
    strings_ru = {
        "_cls_doc": "Показывает информацию о сервере, на котором запущен юзербот",
        "_cmd_doc_serverinfo": "Показать информацию о сервере",
        "server_info_title": "<b>Информация о сервере</b>",
        "cpu_title": "┎ <b>Процессор</b>",
        "cpu_model": "┣ <b>Модель:</b> <code>{cpu_name}</code>",
        "cpu_cores": "┣ <b>Ядра:</b> <code>{cpu_cores}</code>",
        "cpu_load": "┗ <b>Нагрузка:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>",
        "mem_title": "┎ <b>Память</b>",
        "mem_ram": "┣ <b>ОЗУ:</b> <code>{ram_bar} {used_ram:.2f}/{total_ram:.2f} ГБ</code>",
        "mem_disk": "┗ <b>Диск:</b> <code>{disk_bar} {used_disk:.2f}/{total_disk:.2f} ГБ (Свободно: {free_disk:.2f} ГБ)</code>",
        "net_title": "┎ <b>Сеть</b>",
        "net_traffic": "┗ <b>Трафик:</b> <code>↓ {net_down:.2f} ГБ / ↑ {net_up:.2f} ГБ</code>",
        "sys_title": "┎ <b>Система</b>",
        "sys_os": "┣ <b>ОС:</b> <code>{os_info}</code>",
        "sys_python": "┣ <b>Python:</b> <code>{python_ver}</code>",
        "sys_uptime": "┗ <b>Аптайм:</b> <code>{uptime_str}</code>",
    }
    
    @loader.command(
        ru_doc="Показать информацию о сервере"
    )
    async def serverinfo(self, message):
        """Show server info"""
        cpu_load = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_name = "Unknown"
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                     if "model name" in line:
                         cpu_name = line.split(":", 1)[1].strip()
                         break
        except:
            cpu_name = platform.processor() or "Unknown"

        ram = psutil.virtual_memory()
        total_ram = ram.total / 1024 ** 3
        used_ram = ram.used / 1024 ** 3

        disk = psutil.disk_usage('/')
        total_disk = disk.total / 1024 ** 3
        used_disk = disk.used / 1024 ** 3
        free_disk = disk.free / 1024 ** 3

        net = psutil.net_io_counters()
        net_down = net.bytes_recv / 1024 ** 3
        net_up = net.bytes_sent / 1024 ** 3

        os_info = platform.platform()
        python_ver = platform.python_version()

        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        days = int(uptime // (24 * 3600))
        time_part = timedelta(seconds=int(uptime % (24 * 3600)))

        if days:
            if 11 <= days % 100 <= 19:
                day_word = "дней"
            elif days % 10 == 1:
                day_word = "день"
            elif 2 <= days % 10 <= 4:
                day_word = "дня"
            else:
                day_word = "дней"
            uptime_str = f"{days} {day_word}, {time_part}"
        else:
            uptime_str = str(time_part)

        bar = lambda p, w=10: '█' * int(p * w // 100) + '▒' * (w - int(p * w // 100))
        cpu_bar = bar(cpu_load)
        ram_bar = bar(used_ram / total_ram * 100)
        disk_bar = bar(used_disk / total_disk * 100)

        reply = (
            f'{self.strings("server_info_title")}\n\n'
            f'{self.strings("cpu_title")}\n'
            f'{self.strings("cpu_model").format(cpu_name=cpu_name)}\n'
            f'{self.strings("cpu_cores").format(cpu_cores=cpu_cores)}\n'
            f'{self.strings("cpu_load").format(cpu_bar=cpu_bar, cpu_load=cpu_load)}\n\n'
            f'{self.strings("mem_title")}\n'
            f'{self.strings("mem_ram").format(ram_bar=ram_bar, used_ram=used_ram, total_ram=total_ram)}\n'
            f'{self.strings("mem_disk").format(disk_bar=disk_bar, used_disk=used_disk, total_disk=total_disk, free_disk=free_disk)}\n\n'
            f'{self.strings("net_title")}\n'
            f'{self.strings("net_traffic").format(net_down=net_down, net_up=net_up)}\n\n'
            f'{self.strings("sys_title")}\n'
            f'{self.strings("sys_os").format(os_info=os_info)}\n'
            f'{self.strings("sys_python").format(python_ver=python_ver)}\n'
            f'{self.strings("sys_uptime").format(uptime_str=uptime_str)}'
        )

        await utils.answer(message, reply)
