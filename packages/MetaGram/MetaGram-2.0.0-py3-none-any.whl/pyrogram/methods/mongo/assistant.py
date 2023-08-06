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

import codecs
import pickle
import json
import pyrogram
from typing import BinaryIO

from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoMtProtoClientSet


def obj_to_str(obj):
    if not obj:
        return False
    string = (codecs.encode(pickle.dumps(obj), "base64").decode())
    return string


def str_to_obj(string: str):
    obj = (pickle.loads(codecs.decode(string.encode(), "base64")))
    return obj


class Assistant:
    def set_assistant(self: "pyrogram.Client", call_py: PyTgCalls):
        asstdb = self.mongo_sync.assistant
        asstdb.update_one(
            {"user_id": self.me.id},
            {"$set": {"calls": call_py._app}},
            upsert=True,
        )

    def del_assistant(self: "pyrogram.Client"):
        asstdb = self.mongo_sync.assistant
        return asstdb.delete_one({"user_id": self.me.id})


    async def get_assistant(self: "pyrogram.Client") -> PyTgCalls:
        for xd in self.get_ubot():
            asst = pyrogram.Client(
                **xd
            )
            if not asst.is_connected:
                await asst.start()
        return asst
        '''
        asstdb = self.mongo_sync.assistant
        call = asstdb.find_one({'user_id': self.me.id})
        if not call:
            raise NoMtProtoClientSet
        else:
            return str_to_obj(call['calls'])
        '''
    
    async def get_call_py(self: "pyrogram.Client") -> PyTgCalls:
        x = self.get_ubot()
        asst = pyrogram.Client(
            name=x['user_id'],
            api_id=x['api_id'],
            api_hash=x['api_hash'],
            session_string=x['session_string'],
        )
        if not asst.is_connected:
            await asst.start()
        call = PyTgCalls(asst, cache_duration=100)
        return call
