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

# Name: Standoff2Decryptor
# Author: miyumodules
# Commands:
# .decmeta
# scope: hikka_only
# meta developer: @miyumodules
# meta pic: https://github.com/d4s4n/miyumodules/blob/main/assets/pfp.png?raw=true
# meta banner: https://github.com/d4s4n/miyumodules/blob/main/assets/banner.png?raw=true

__version__ = (1, 0, 5)

import os
import struct
import shutil
import uuid
import asyncio
import logging
from .. import loader, utils

try:
    from elftools.elf.elffile import ELFFile
except ImportError:
    ELFFile = None

logger = logging.getLogger(__name__)


@loader.tds
class Standoff2DecryptorMod(loader.Module):
    """Standoff 2 metadata decryptor. Based on https://github.com/Michel-M-code/Metadata-Decryptor/ script."""

    strings = {
        "name": "Standoff2Decryptor",
        "no_lib": "<b>[SO2Decryptor]</b> Core library <code>pyelftools</code> is not installed.\nInstall it with <code>.terminal pip install pyelftools</code>",
        "already_running": "<b>[SO2Decryptor]</b> A decryption process is already running. Please wait.",
        "decrypting_premium": "<emoji document_id=5210924223093244222>🔬</emoji> <b>Decrypting metadata...</b>",
        "no_file_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>You must reply to or attach a <code>libunity.so</code> file.</b>",
        "not_elf_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>The provided file is not a valid ELF file.</b>",
        "downloading_premium": "<emoji document_id=5210924223093244222>🔬</emoji> <b>File detected. Downloading...</b>",
        "success_premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Metadata decrypted successfully!</b>",
        "fail_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>An error occurred.</b>\n<code>{e}</code>",
        "no_candidates_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Error: No metadata pointer candidates found.</b>",
        "decrypting_standard": "🔬 <b>Decrypting metadata...</b>",
        "no_file_standard": "❌ <b>You must reply to or attach a <code>libunity.so</code> file.</b>",
        "not_elf_standard": "❌ <b>The provided file is not a valid ELF file.</b>",
        "downloading_standard": "🔬 <b>File detected. Downloading...</b>",
        "success_standard": "✅ <b>Metadata decrypted successfully!</b>",
        "fail_standard": "❌ <b>An error occurred.</b>\n<code>{e}</code>",
        "no_candidates_standard": "❌ <b>Error: No metadata pointer candidates found.</b>",
    }

    strings_ru = {
        "_cls_doc": "Дешифратор metadata для Standoff 2. На основе скрипта от https://github.com/Michel-M-code/Metadata-Decryptor/",
        "_cmd_doc_decmeta": "<ответом на файл / с файлом> - Расшифровать libunity.so",
        "no_lib": "<b>[SO2Decryptor]</b> Библиотека <code>pyelftools</code> не установлена.\nУстановите ее командой <code>.terminal pip install pyelftools</code>",
        "already_running": "<b>[SO2Decryptor]</b> Процесс дешифровки уже запущен. Пожалуйста, подождите.",
        "decrypting_premium": "<emoji document_id=5210924223093244222>🔬</emoji> <b>Расшифровываю метаданные...</b>",
        "no_file_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Вы должны ответить на сообщение с файлом <code>libunity.so</code> или прикрепить его.</b>",
        "not_elf_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Прикрепленный файл не является ELF файлом.</b>",
        "downloading_premium": "<emoji document_id=5210924223093244222>🔬</emoji> <b>Файл найден. Скачиваю...</b>",
        "success_premium": "<emoji document_id=5287692511945437157>✅</emoji> <b>Метаданные успешно расшифрованы!</b>",
        "fail_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Произошла ошибка.</b>\n<code>{e}</code>",
        "no_candidates_premium": "<emoji document_id=5287611315588707430>❌</emoji> <b>Ошибка: Не найдены кандидаты на указатель метаданных.</b>",
        "decrypting_standard": "🔬 <b>Расшифровываю метаданные...</b>",
        "no_file_standard": "❌ <b>Вы должны ответить на сообщение с файлом <code>libunity.so</code> или прикрепить его.</b>",
        "not_elf_standard": "❌ <b>Прикрепленный файл не является ELF файлом.</b>",
        "downloading_standard": "🔬 <b>Файл найден. Скачиваю...</b>",
        "success_standard": "✅ <b>Метаданные успешно расшифрованы!</b>",
        "fail_standard": "❌ <b>Произошла ошибка.</b>\n<code>{e}</code>",
        "no_candidates_standard": "❌ <b>Ошибка: Не найдены кандидаты на указатель метаданных.</b>",
    }

    def __init__(self):
        self.is_busy = False

    @loader.command(ru_doc="<ответом на файл / с файлом> - Расшифровать libunity.so")
    async def decmeta(self, message):
        if self.is_busy:
            await utils.answer(message, self.strings("already_running"))
            return

        if not ELFFile:
            await utils.answer(message, self.strings("no_lib"))
            return

        me = await message.client.get_me()
        use_prem = me.premium or message.is_private

        reply = await message.get_reply_message()
        target_msg = reply if reply and reply.file else message

        if (
            not target_msg
            or not target_msg.file
            or not getattr(target_msg.file, "name", "").endswith(".so")
        ):
            await utils.answer(
                message,
                self.strings("no_file_premium" if use_prem else "no_file_standard"),
            )
            return

        tmp_dir = None
        self.is_busy = True

        try:
            msg = await utils.answer(
                message,
                self.strings(
                    "downloading_premium" if use_prem else "downloading_standard"
                ),
            )

            tmp_dir = f"tmp_decrypt_{uuid.uuid4()}"
            os.makedirs(tmp_dir, exist_ok=True)
            lib_path = os.path.join(tmp_dir, "libunity.so")

            await self.client.download_media(target_msg, lib_path)

            with open(lib_path, "rb") as f:
                if f.read(4) != b"\x7fELF":
                    await utils.answer(
                        msg,
                        self.strings(
                            "not_elf_premium" if use_prem else "not_elf_standard"
                        ),
                    )
                    return

            await utils.answer(
                msg,
                self.strings(
                    "decrypting_premium" if use_prem else "decrypting_standard"
                ),
            )

            loop = asyncio.get_running_loop()
            decrypted_data = await loop.run_in_executor(
                None, self.run_decryptor, lib_path
            )

            if decrypted_data:
                out_path = os.path.join(tmp_dir, "decrypted-metadata.dat")
                with open(out_path, "wb") as f:
                    f.write(decrypted_data)

                await self.client.send_file(
                    message.chat_id,
                    out_path,
                    caption=self.strings(
                        "success_premium" if use_prem else "success_standard"
                    ),
                )
                if msg.out:
                    await msg.delete()

            else:
                await utils.answer(
                    msg,
                    self.strings(
                        "no_candidates_premium"
                        if use_prem
                        else "no_candidates_standard"
                    ),
                )

        except Exception as e:
            logger.exception("Decryption failed")
            if "msg" in locals():
                await utils.answer(
                    msg,
                    self.strings(
                        "fail_premium" if use_prem else "fail_standard"
                    ).format(e=e),
                )
        finally:
            self.is_busy = False
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    def run_decryptor(self, lib_path):
        lib = open(lib_path, "rb")
        elf = ELFFile(lib)
        is64bit = elf.get_machine_arch() == "AArch64"

        segments = [
            (s["p_vaddr"], s["p_vaddr"] + s["p_memsz"], s["p_offset"])
            for s in elf.iter_segments()
            if s["p_type"] == "PT_LOAD"
        ]

        def find_offset(va):
            for start, end, offset in segments:
                if start <= va < end:
                    return va - start + offset
            return None

        data_section = elf.get_section_by_name(".data")

        relocs = []
        for section in elf.iter_sections():
            if section.header["sh_type"] not in ("SHT_REL", "SHT_RELA"):
                continue
            for rel in section.iter_relocations():
                addr = rel["r_offset"]
                if not (
                    data_section.header["sh_addr"]
                    <= addr
                    < data_section.header["sh_addr"] + data_section.header["sh_size"]
                ):
                    continue

                ptr = rel.get("r_addend", 0) if is64bit else 0
                if not is64bit:
                    offset = find_offset(addr)
                    if offset is not None:
                        lib.seek(offset)
                        ptr = struct.unpack("<I", lib.read(4))[0]

                if ptr != 0:
                    relocs.append(ptr)

        candidates = []
        for addr in relocs:
            offset = find_offset(addr - 4)
            if offset is None:
                continue
            lib.seek(offset)
            if lib.read(12) == b"\x81\x80\x80\x3B\0\0\0\0\0\0\0\0":
                candidates.append(addr)

        if not candidates:
            return None

        meta_offset = find_offset(candidates[0])
        if meta_offset is None:
            return None

        lib.seek(meta_offset)
        meta_data = lib.read(50_000_000)
        idx = meta_data.find(b"\x00" * 256)
        if idx != -1:
            idx += (4 - idx % 4) % 4
            meta_data = meta_data[:idx]

        self.meta = meta_data
        self.offsets = []
        self.new_meta = bytearray(
            b"\xAF\x1B\xB1\xFA\x1F\0\0\0\0\x01\00\00" + b"\0" * 244
        )
        self.pos = 0

        fields = [
            struct.unpack("<I", meta_data[i : i + 4])[0] for i in range(8, 256, 4)
        ]

        offset_candidates = sorted(
            list(
                set(
                    [
                        f
                        for f in fields
                        if f % 4 == 0
                        and len(meta_data) > f > 0
                        and meta_data[f - 4 : f] == b"\0\0\0\0"
                    ]
                )
            )
        )

        for offset_val in offset_candidates:
            found = False
            if any(o[0] == offset_val for o in self.offsets):
                continue

            for field in fields:
                if field != offset_val and field != 0 and field < len(meta_data) / 3:
                    for next_offset in offset_candidates:
                        if any(o[0] == field for o in self.offsets):
                            continue
                        if (
                            -4 <= field + offset_val - next_offset <= 4
                            and offset_val != next_offset
                        ):
                            self.offsets.append((offset_val, field))
                            found = True
                            break
                    if found:
                        break
            if not found and (
                offset_val > len(meta_data) / 2
                or (self.offsets and sum(self.offsets[-1]) == offset_val - 4)
            ):
                next_offset_val = (
                    offset_candidates[offset_candidates.index(offset_val) + 1]
                    if offset_val in offset_candidates
                    else len(meta_data)
                )
                self.offsets.append((offset_val, next_offset_val - offset_val - 4))

        self.offsets = sorted(list(set(self.offsets)), key=lambda item: item[0])

        self.run_heuristic(
            lambda e: e[0][1] == e[0][1]
            and all(e[i][1] == e[i - 1][1] + e[i - 1][0] for i in range(1, len(e))),
            "<II",
            True,
            None,
        )
        self.run_heuristic(None, "<II", True, b"\x00\x00\x00\x01\x09\x00\x00\x01")
        self.run_heuristic(None, "<II", True, b"Assembly-CSharp\0")
        self.run_heuristic(
            lambda e: all(a < len(e) and r < len(e) for _, _, a, r, _, _ in e),
            "<IIIIII",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(t & 0xFF000000 == 0x17000000 for _, _, _, _, t in e),
            "<IIIII",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(
                t & 0xFF000000 == 0x06000000 for _, _, _, _, _, _, t, _, _, _, _ in e
            ),
            "<IIIIIIIHHHH",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(e[i][0] > e[i - 1][0] for i in range(1, len(e))),
            "<III",
            True,
            None,
        )
        self.run_heuristic(
            lambda e: all(e[i][0] > e[i - 1][0] for i in range(1, len(e))),
            "<III",
            False,
            None,
        )
        self.run_heuristic(None, "<III", False, b"<color=#E9AF4D>{0}</color>")
        self.run_heuristic(
            lambda e: all(e[i][0] > e[i - 1][0] for i in range(1, len(e))),
            "<III",
            True,
            None,
        )
        self.run_heuristic(
            lambda e: all(t & 0xFF000000 == 0x08000000 for _, t, _ in e),
            "<III",
            True,
            None,
        )
        self.run_heuristic(
            lambda e: all(t & 0xFF000000 == 0x04000000 for _, _, t in e),
            "<III",
            True,
            None,
        )
        self.run_heuristic(
            lambda e: all(
                c == 0 or cs == e[i - 1][2] + e[i - 1][3]
                for i, (_, _, cs, c, _, _) in enumerate(e)
                if i > 0
            ),
            "<IIHHHH",
            True,
            None,
        )
        self.run_heuristic(
            lambda e: all(1024576 > c > 256 for c in e), "<I", True, None
        )
        self.run_heuristic(
            lambda e: all(m in (0, 1) and a < 128 for _, a, m, _ in e),
            "<IIII",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: sum(1 if e[i] > e[i - 1] else -1 for i in range(1, len(e))) > 0,
            "<I",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(1024576 > c > 256 for c in e), "<I", False, None
        )
        self.run_heuristic(
            lambda e: all(i != 1 and i & 0xE0000000 == 0 for i in e), "<I", False, None
        )
        self.run_heuristic(
            lambda e: all(o < 256 and 256 < t < 65535 for t, o in e), "<II", False, None
        )
        self.run_heuristic(
            lambda e: all(en[25] & 0xFF000000 == 0x02000000 for en in e),
            "<IIIIIIIIIIIIIIIIHHHHHHHHII",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(en[7] == 1 for en in e[:-2]), "<IIIIIIIIII", False, None
        )
        self.run_heuristic(
            lambda e: all(t & 0xFF000000 == 0x20000000 for _, t, *_ in e),
            "<IIIIIIIIIIIIIIII",
            False,
            None,
        )
        self.run_heuristic(
            lambda e: all(ti > 256 and fi < 2048 for ti, fi in e), "<II", False, None
        )
        self.run_heuristic(
            lambda e: all(a < 256 for a in e) and 30 < sum(e) / len(e) < 40,
            "<I",
            False,
            None,
        )
        self.run_heuristic(None, "<I", False, b"NewFragmentBox")
        self.run_heuristic(
            lambda e: sum(2 if t & 0xFF000000 != 0 else -10 for t, _ in e) > 0,
            "<II",
            False,
            None,
        )
        self.run_heuristic(lambda e: all(256 < p < 70000 for p in e), "<I", False, None)
        self.run_heuristic(
            lambda e: all(
                s == e[i - 1][0] + e[i - 1][1] for i, (s, _) in enumerate(e) if i > 0
            ),
            "<II",
            False,
            None,
        )

        self.update_header(0)
        self.update_header(0)

        last_offset = struct.unpack("<I", self.new_meta[248:252])[0]
        self.new_meta[252:256] = struct.pack("<I", len(meta_data) - last_offset)

        return self.new_meta

    def update_header(self, size):
        self.new_meta[12 + self.pos : 16 + self.pos] = struct.pack("<I", size)
        new_size = (
            struct.unpack("<I", self.new_meta[8 + self.pos : 12 + self.pos])[0] + size
        )
        self.new_meta[16 + self.pos : 20 + self.pos] = struct.pack("<I", new_size)
        self.pos += 8

    def run_heuristic(self, callback, struct_sig, lowest_size, contains):
        found = []
        for offset, size in self.offsets:
            data = self.meta[offset : offset + size]

            if contains and contains in data:
                found.append((offset, size, data))
                break

            if not struct_sig:
                continue

            entries, valid = [], True
            try:
                step = struct.calcsize(struct_sig)
                if step == 0:
                    continue
                for i in range(0, len(data), step):
                    fields = struct.unpack_from(struct_sig, data, i)
                    entries.append(fields[0] if len(fields) == 1 else fields)
            except (struct.error, IndexError):
                valid = False

            if valid and callback and callback(entries):
                found.append((offset, size, data))

        if not found:
            return

        found.sort(key=lambda x: x[1], reverse=not lowest_size)
        try:
            self.offsets.remove(found[0][:2])
            self.update_header(found[0][1])
            self.new_meta += found[0][2]
        except (ValueError, IndexError):
            pass
