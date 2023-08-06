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

from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)

audio = {}
video = {}


class BitRate:
    async def save_audio_bitrate(self: "pyrogram.Client", chat_id: int, bitrate: str):
        audio[chat_id] = bitrate


    async def save_video_bitrate(self: "pyrogram.Client", chat_id: int, bitrate: str):
        video[chat_id] = bitrate


    async def get_aud_bit_name(self: "pyrogram.Client", chat_id: int) -> str:
        mode = audio.get(chat_id)
        if not mode:
            return "High"
        return mode


    async def get_vid_bit_name(self: "pyrogram.Client", chat_id: int) -> str:
        mode = video.get(chat_id)
        if not mode:
            return "Medium"
        return mode


    async def get_audio_bitrate(self: "pyrogram.Client", chat_id: int) -> str:
        mode = audio.get(chat_id)
        if not mode:
            return MediumQualityAudio()
        if str(mode) == "High":
            return HighQualityAudio()
        elif str(mode) == "Medium":
            return MediumQualityAudio()
        elif str(mode) == "Low":
            return LowQualityAudio()


    async def get_video_bitrate(self: "pyrogram.Client", chat_id: int) -> str:
        mode = video.get(chat_id)
        if not mode:
            return MediumQualityVideo()
        if str(mode) == "High":
            return HighQualityVideo()
        elif str(mode) == "Medium":
            return MediumQualityVideo()
        elif str(mode) == "Low":
            return LowQualityVideo()