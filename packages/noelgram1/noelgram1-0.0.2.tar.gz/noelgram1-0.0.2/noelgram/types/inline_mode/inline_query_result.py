#  Noelgram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Noelgram.
#
#  Noelgram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Noelgram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Noelgram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import noelgram
from noelgram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~noelgram.types.InlineQueryResultCachedAudio`
    - :obj:`~noelgram.types.InlineQueryResultCachedDocument`
    - :obj:`~noelgram.types.InlineQueryResultCachedAnimation`
    - :obj:`~noelgram.types.InlineQueryResultCachedPhoto`
    - :obj:`~noelgram.types.InlineQueryResultCachedSticker`
    - :obj:`~noelgram.types.InlineQueryResultCachedVideo`
    - :obj:`~noelgram.types.InlineQueryResultCachedVoice`
    - :obj:`~noelgram.types.InlineQueryResultArticle`
    - :obj:`~noelgram.types.InlineQueryResultAudio`
    - :obj:`~noelgram.types.InlineQueryResultContact`
    - :obj:`~noelgram.types.InlineQueryResultDocument`
    - :obj:`~noelgram.types.InlineQueryResultAnimation`
    - :obj:`~noelgram.types.InlineQueryResultLocation`
    - :obj:`~noelgram.types.InlineQueryResultPhoto`
    - :obj:`~noelgram.types.InlineQueryResultVenue`
    - :obj:`~noelgram.types.InlineQueryResultVideo`
    - :obj:`~noelgram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "noelgram.Client"):
        pass
