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

import asyncio
from datetime import datetime, timedelta
from typing import Union

import pyrogram

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from pytgcalls.types.stream import StreamAudioEnded



autoend = {}
counter = {}
AUTO_END_TIME = 3

class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class MetaCall:
    queue = {}
    
    def __init__(self: "pyrogram.Client"):
        try:
            x = self.get_ubot()
        except:
            pass
        self.asst = pyrogram.Client(
            name=x['user_id'],
            api_id=x['api_id'],
            api_hash=x['api_hash'],
            session_string=x['session_string'],
        )
        self.call = PyTgCalls(
            self.asst,
            cache_duration=100,
        )

    def add_to_queue(self, chat_id, songname, link, ref, type, quality):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.append([songname, link, ref, type, quality])
            return int(len(chat_queue) - 1)
        self.queue[chat_id] = [[songname, link, ref, type, quality]]
    
    def get_queue(self, chat_id):
        if chat_id in self.queue:
            return self.queue[chat_id]
        return 0
    
    def pop_an_item(self, chat_id):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.pop(0)
            return 1
        return 0
    
    def clear_queue(self, chat_id: int):
        if chat_id in self.queue:
            self.queue.pop(chat_id)
            return 1
        return 0
    
    async def skip_current_song(self, chat_id: int):
        if chat_id not in self.queue:
            return 0
        chat_queue = self.get_queue(chat_id)
        if len(chat_queue) == 1:
            await self.call.leave_group_call(chat_id)
            self.clear_queue(chat_id)
            return 1
        songname = chat_queue[1][0]
        url = chat_queue[1][1]
        link = chat_queue[1][2]
        type = chat_queue[1][3]
        RESOLUSI = chat_queue[1][4]
        if type == "Audio":
            await self.call.change_stream(
                chat_id,
                AudioPiped(
                    url,
                    HighQualityAudio(),
                ),
            )
        elif type == "Video":
            if RESOLUSI == 720:
                hm = HighQualityVideo()
            elif RESOLUSI == 480:
                hm = MediumQualityVideo()
            elif RESOLUSI == 360:
                hm = LowQualityVideo()
            await self.call.change_stream(
                chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
            )
        self.pop_an_item(chat_id)
        return [songname, link, type]

    async def skip_item(self, chat_id, h):
        if chat_id in self.queue:
            chat_queue = self.get_queue(chat_id)
            try:
                x = int(h)
                songname = chat_queue[x][0]
                chat_queue.pop(x)
                return songname
            except Exception as e:
                print(e)
                return 0
        else:
            return 0

    async def start_call(self):
        await self.call.start()

    async def decorators(self):
        @self.call.on_stream_end()
        async def stream_end_handler(_, u: Update):
            chat_id = u.chat_id
            print(chat_id)
            await self.skip_current_song(chat_id)

        @self.call.on_closed_voice_chat()
        async def closedvc(_, chat_id: int):
            if chat_id in self.queue:
                self.clear_queue(chat_id)

        @self.call.on_left()
        async def leftvc(_, chat_id: int):
            if chat_id in self.queue:
                self.clear_queue(chat_id)

        @self.call.on_kicked()
        async def kickedvc(_, chat_id: int):
            if chat_id in self.queue:
                self.clear_queue(chat_id)

        @self.call.on_participants_change()
        async def participants_change_handler(client, update: Update):
            if not isinstance(
                update, JoinedGroupCallParticipant
            ) and not isinstance(update, LeftGroupCallParticipant):
                return
            chat_id = update.chat_id
            users = counter.get(chat_id)
            if not users:
                try:
                    got = len(await client.get_participants(chat_id))
                except:
                    return
                counter[chat_id] = got
                if got == 1:
                    autoend[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                autoend[chat_id] = {}
            else:
                final = (
                    users + 1
                    if isinstance(update, JoinedGroupCallParticipant)
                    else users - 1
                )
                counter[chat_id] = final
                if final == 1:
                    autoend[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                autoend[chat_id] = {}
