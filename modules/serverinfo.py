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

__version__ = (1, 2, 0)

import psutil
import platform
import time
import io
from datetime import timedelta
from .. import loader, utils

loader.require("matplotlib")

import matplotlib.pyplot as plt

@loader.tds
class ServerInfoMod(loader.Module):
    """Shows information about the server where the userbot is running"""

    strings = {
        "name": "ServerInfo",
        "caption": "<b>Uptime:</b> <code>{uptime_str}</code>",
        "cpu_title": "┎ <b>CPU</b>",
        "cpu_model": "┣ <b>Model:</b> <code>{cpu_name}</code>",
        "cpu_cores": "┣ <b>Cores:</b> <code>{cpu_cores}</code>",
        "cpu_load": "┗ <b>Load:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>",
        "mem_title": "┎ <b>Memory</b>",
        "mem_ram": "┣ <b>RAM:</b> <code>{used_ram:.2f}/{total_ram:.2f} GB</code>",
        "mem_disk": "┗ <b>Disk:</b> <code>{used_disk:.2f} GB (Free: {free_disk:.2f} GB)</code>",
        "net_title": "┎ <b>Network</b>",
        "net_traffic": "┗ <b>Traffic:</b> <code>↓ {net_down:.2f} GB / ↑ {net_up:.2f} GB</code>",
        "sys_title": "┎ <b>System</b>",
        "sys_os": "┣ <b>OS:</b> <code>{os_info}</code>",
        "sys_python": "┣ <b>Python:</b> <code>{python_ver}</code>",
        "sys_uptime": "┗ <b>Uptime:</b> <code>{uptime_str}</code>",
        "btn_graph": "📊 График",
        "btn_text": "📝 Текст",
        "graph_title": "Server Load",
        "graph_y_label": "Usage (%)",
    }
    
    strings_ru = {
        "_cls_doc": "Показывает информацию о сервере, на котором запущен юзербот",
        "_cmd_doc_serverinfo": "Показать информацию о сервере",
        "caption": "<b>Аптайм:</b> <code>{uptime_str}</code>",
        "cpu_title": "┎ <b>Процессор</b>",
        "cpu_model": "┣ <b>Модель:</b> <code>{cpu_name}</code>",
        "cpu_cores": "┣ <b>Ядра:</b> <code>{cpu_cores}</code>",
        "cpu_load": "┗ <b>Нагрузка:</b> <code>{cpu_bar} {cpu_load:.1f}%</code>",
        "mem_title": "┎ <b>Память</b>",
        "mem_ram": "┣ <b>ОЗУ:</b> <code>{used_ram:.2f}/{total_ram:.2f} ГБ</code>",
        "mem_disk": "┗ <b>Диск:</b> <code>{used_disk:.2f} ГБ (Свободно: {free_disk:.2f} ГБ)</code>",
        "net_title": "┎ <b>Сеть</b>",
        "net_traffic": "┗ <b>Трафик:</b> <code>↓ {net_down:.2f} ГБ / ↑ {net_up:.2f} ГБ</code>",
        "sys_title": "┎ <b>Система</b>",
        "sys_os": "┣ <b>ОС:</b> <code>{os_info}</code>",
        "sys_python": "┣ <b>Python:</b> <code>{python_ver}</code>",
        "sys_uptime": "┗ <b>Аптайм:</b> <code>{uptime_str}</code>",
        "btn_graph": "📊 График",
        "btn_text": "📝 Текст",
        "graph_title": "Нагрузка на сервер",
        "graph_y_label": "Использование (%)",
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
        
        bar = lambda p, w=10: '█' * int(p * w / 100) + '▒' * (w - int(p * w / 100))
        s["cpu_bar"] = bar(s["cpu_load"])
        return s

    async def get_text_view(self, stats):
        return (
            f'{self.strings("cpu_title")}\n'
            f'{self.strings("cpu_model").format(**stats)}\n'
            f'{self.strings("cpu_cores").format(**stats)}\n'
            f'{self.strings("cpu_load").format(**stats)}\n\n'
            f'{self.strings("mem_title")}\n'
            f'{self.strings("mem_ram").format(**stats)}\n'
            f'{self.strings("mem_disk").format(**stats)}\n\n'
            f'{self.strings("net_title")}\n'
            f'{self.strings("net_traffic").format(**stats)}\n\n'
            f'{self.strings("sys_title")}\n'
            f'{self.strings("sys_os").format(**stats)}\n'
            f'{self.strings("sys_python").format(**stats)}\n'
            f'{self.strings("sys_uptime").format(**stats)}'
        )

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
        stats = await self.get_stats()
        text = await self.get_text_view(stats)
        
        await self.inline.form(
            message=message,
            text=text,
            reply_markup=[[{"text": self.strings("btn_graph"), "callback": self.toggle_view, "data": "graph"}]],
        )

    async def toggle_view(self, call):
        view_type = call.data
        stats = await self.get_stats()

        if view_type == "graph":
            graph_image = await self.create_graph(stats)
            caption = self.strings("caption").format(**stats)
            btn_data = "text"
            btn_text = self.strings("btn_text")
            
            await call.edit(
                text=caption, 
                file=graph_image, 
                reply_markup=[[{"text": btn_text, "callback": self.toggle_view, "data": btn_data}]]
            )
        else:
            text = await self.get_text_view(stats)
            btn_data = "graph"
            btn_text = self.strings("btn_graph")
            
            await call.edit(
                text=text,
                file=None,
                reply_markup=[[{"text": btn_text, "callback": self.toggle_view, "data": btn_data}]]
            )
