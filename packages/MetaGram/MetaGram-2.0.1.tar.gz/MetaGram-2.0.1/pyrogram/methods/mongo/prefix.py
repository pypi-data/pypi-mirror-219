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


class Prefix:
    def set_prefix(self: "pyrogram.Client", handler):
        hndlrdb = self.mongo_sync.prefix
        user_id = self.me.id
        cek = hndlrdb.find_one({"user_id": user_id})
        if cek:
            hndlrdb.update_one({"user_id": user_id}, {"$set": {"hndlr": handler.split(' ')}})
        else:
            hndlrdb.insert_one(
                {
                    "user_id": user_id,
                    "hndlr": handler
                }
            )

    def set_prefix_user(self: "pyrogram.Client", user_id, handler):
        """- For Bot Setting Prefix User Id"""
        hndlrdb = self.mongo_sync.prefix
        cek = hndlrdb.find_one({"user_id": user_id})
        if cek:
            hndlrdb.update_one({"user_id": user_id}, {"$set": {"hndlr": handler.split(' ')}})
        else:
            hndlrdb.insert_one(
                {
                    "user_id": user_id,
                    "hndlr": handler
                }
            )

    def del_prefix(self: "pyrogram.Client"):
        hndlrdb = self.mongo_sync.prefix
        hndlrdb.update_one({"user_id": self.me.id}, {"$set": {"hndlr": [".", "!", "*", "^", "-", "?"]}})

    def get_prefix(self: "pyrogram.Client"):
        hndlrdb = self.mongo_sync.prefix
        x = hndlrdb.find_one({'user_id': self.me.id})
        return x['hndlr']
        #if x:
        #    return x['hndlr']
        #else:
        #    return [".", "!", "*", "^", "-", "?"]

    def get_prefix_user(self: "pyrogram.Client", user_id):
        hndlrdb = self.mongo_sync.prefix
        x = hndlrdb.find_one({'user_id': user_id})
        return x['hndlr']
        #if x:
        #    return x['hndlr']
        #else:
        #    return [".", "!", "*", "^", "-", "?"]
