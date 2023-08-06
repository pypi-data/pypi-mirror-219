# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import pyrogram

from pyrogram.filters import SUDOERS
from pyrogram.storage import MongoDB


class Sudoers:
    async def add_sudo(self: "pyrogram.Client", user, nama):
        sudoersdb = self.mongo_async.sudoers
        cek = await sudoersdb.find_one({"user_id": self.me.id, "user": user})
        if cek:
            await sudoersdb.update_one(
                {"user_id": self.me.id},
                {
                    "$set": {
                        "user": user,
                        "nama": nama,
                    }
                },
            )
        else:
            await sudoersdb.insert_one({"user_id": self.me.id, "user": user, "nama": nama})


    async def del_sudo(self: "pyrogram.Client", user):
        sudoersdb = self.mongo_async.sudoers
        await sudoersdb.delete_one({"user_id": self.me.id, "user": user})


    async def get_all_sudo(self: "pyrogram.Client"):
        sudoersdb = self.mongo_async.sudoers
        r = [jo async for jo in sudoersdb.find({"user_id": self.me.id})]
        if r:
            return r
        else:
            return False

    async def sudo(self: "pyrogram.Client"):
        global SUDOERS
        
        try:
            for x in await self.get_all_sudo():
                SUDOERS.add(x['user'])
            print(f"Sudoers {self.me.first_name} Loaded.")
        except TypeError:
            print(f"Sudoers {self.me.first_name} Loaded.")
