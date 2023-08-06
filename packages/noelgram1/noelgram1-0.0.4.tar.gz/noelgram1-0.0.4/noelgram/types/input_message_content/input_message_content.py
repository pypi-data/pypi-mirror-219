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

import noelgram

from ..object import Object

"""- :obj:`~noelgram.types.InputLocationMessageContent`
    - :obj:`~noelgram.types.InputVenueMessageContent`
    - :obj:`~noelgram.types.InputContactMessageContent`"""


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Noelgram currently supports the following types:

    - :obj:`~noelgram.types.InputTextMessageContent`
    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "noelgram.Client", reply_markup):
        raise NotImplementedError
