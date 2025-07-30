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

__version__ = (1, 1, 6)

import psutil
import platform
import time
import io
from datetime import timedelta
from .. import loader, utils

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

@loader.tds
class ServerInfoMod(loader.Module):
    """Shows information about the server where the userbot is running"""

    strings = {
        "name": "ServerInfo",
        "loading": "<i>Loading server data...</i>",
        "info_template_premium": (
            "┎ <b>CPU</b>\n"
            "┣ <emoji document_id=5172869086727635492>💻</emoji> <b>Model:</b> <code>{cpu_name}</code>\n"
            "┣ <emoji document_id=5172839378438849164>💻</emoji> <b>Cores:</b> <code>{cpu_cores}</code>\n\n"
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
        "info_template_standard": (
            "┎ <b>CPU</b>\n"
            "┣ 💻 <b>Model:</b> <code>{cpu_name}</code>\n"
            "┣ ⚙️ <b>Cores:</b> <code>{cpu_cores}</code>\n\n"
            "┎ <b>Memory</b>\n"
            "┣ 💾 <b>RAM:</b> <code>{used_ram:.2f}/{total_ram:.2f} GB</code>\n"
            "┗ 💿 <b>Disk:</b> <code>{used_disk:.2f} GB (Free: {free_disk:.2f} GB)</code>\n\n"
            "┎ <b>Network</b>\n"
            "┗ 📡 <b>Traffic:</b> <code>↓ {net_down:.2f} GB / ↑ {net_up:.2f} GB</code>\n\n"
            "┎ <b>System</b>\n"
            "┣ 🐧 <b>OS:</b> <code>{os_info}</code>\n"
            "┣ 🐍 <b>Python:</b> <code>{python_ver}</code>\n"
            "┗ ⏱ <b>Uptime:</b> <code>{uptime_str}</code>"
        ),
        "graph_title": "Server Load",
        "graph_y_label": "Usage (%)",
        "matplotlib_missing": "<b>Library <code>matplotlib</code> not installed.</b>\nInstall it with <code>.terminal pip install matplotlib</code>",
    }
    
    strings_ru = {
        "_cls_doc": "Показывает информацию о сервере, на котором запущен юзербот",
        "_cmd_doc_serverinfo": "Показать информацию о сервере",
        "loading": "<i>Собираю данные о сервере...</i>",
        "info_template_premium": (
            "┎ <b>Процессор</b>\n"
            "┣ <emoji document_id=5172869086727635492>💻</emoji> <b>Модель:</b> <code>{cpu_name}</code>\n"
            "┣ <emoji document_id=5172839378438849164>💻</emoji> <b>Ядра:</b> <code>{cpu_cores}</code>\n\n"
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
        "info_template_standard": (
            "┎ <b>Процессор</b>\n"
            "┣ 💻 <b>Модель:</b> <code>{cpu_name}</code>\n"
            "┣ ⚙️ <b>Ядра:</b> <code>{cpu_cores}</code>\n\n"
            "┎ <b>Память</b>\n"
            "┣ 💾 <b>ОЗУ:</b> <code>{used_ram:.2f}/{total_ram:.2f} ГБ</code>\n"
            "┗ 💿 <b>Диск:</b> <code>{used_disk:.2f} ГБ (Свободно: {free_disk:.2f} ГБ)</code>\n\n"
            "┎ <b>Сеть</b>\n"
            "┗ 📡 <b>Трафик:</b> <code>↓ {net_down:.2f} ГБ / ↑ {net_up:.2f} ГБ</code>\n\n"
            "┎ <b>Система</b>\n"
            "┣ 🐧 <b>ОС:</b> <code>{os_info}</code>\n"
            "┣ 🐍 <b>Python:</b> <code>{python_ver}</code>\n"
            "┗ ⏱ <b>Аптайм:</b> <code>{uptime_str}</code>"
        ),
        "graph_title": "Нагрузка на сервер",
        "graph_y_label": "Использование (%)",
        "matplotlib_missing": "<b>Библиотека <code>matplotlib</code> не установлена.</b>\nУстановите ее командой <code>.terminal pip install matplotlib</code>",
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
        s["ram_percent"] = ram.percent
        s["total_ram"] = ram.total / 1024 ** 3
        s["used_ram"] = ram.used / 1024 ** 3

        disk = psutil.disk_usage('/')
        s["disk_percent"] = disk.percent
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
        
        return s
    
    async def create_graph(self, stats):
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(6, 4))
        
        labels = ["CPU", "RAM", "Disk"]
        values = [stats["cpu_load"], stats["ram_percent"], stats["disk_percent"]]
        
        bars = ax.bar(labels, values, color=["#1f77b4", "#2ca02c", "#d62728"])
        ax.set_ylim(0, 100)
        ax.set_ylabel(self.strings("graph_y_label"))
        ax.set_title(self.strings("graph_title"))
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.1f}%', ha='center', va='bottom')

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    @loader.command(
        ru_doc="Показать информацию о сервере"
    )
    async def serverinfo(self, message):
        """Show server info"""
        if not plt:
            await utils.answer(message, self.strings("matplotlib_missing"))
            return
        
        msg = await utils.answer(message, self.strings("loading"))

        stats = await self.get_stats()
        me = await message.client.get_me()

        if me.premium or message.is_private:
            template = self.strings("info_template_premium")
        else:
            template = self.strings("info_template_standard")
        
        graph_image = await self.create_graph(stats)
        caption = template.format(**stats)
        
        await utils.answer(msg, caption, file=graph_image)
