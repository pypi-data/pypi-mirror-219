from tg_botting.abstract import Messageable
from tg_botting.utils import get_params_from_class,get_params_from_func


class User(Messageable):
    async def _get_conversation(self):
        return self.id

    def __init__(self,data):
        self.original_data = data
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.is_bot = data.get('is_bot')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name') if "last_name" in data else ""
        self.username = data.get('username') if "username" in data else None
        self.language_code = data.get('language_code') if "language_code" in data else None
        self.is_premium = data.get('is_premium') if "is_premium" in data else False
        self.added_to_attachment_menu = data.get('added_to_attachment_menu') if "added_to_attachment_menu" in data else False
        self.can_join_groups = data.get('can_join_groups') if "can_join_groups" in data else False
        self.can_read_all_group_messages = data.get('can_read_all_group_messages') if "can_read_all_group_messages" in data else False
        self.supports_inline_queries = data.get('supports_inline_queries') if "supports_inline_queries" in data else False


    @property
    def mention(self,style=None):
        if style is None:
            return "@{}".format(self.username)
        elif style=="mardown":
            return "[{} {}](tg://user?id={})".format(self.first_name,self.last_name,self.id)
        elif style=="html":
            return "<a href=\"tg://user?id={}\">{} {}</a>".format(self.first_name,self.last_name,self.id)
        else:
            return "@{}".format(self.username) if self.username != None else self.mention("html")

    @property
    def dict(self):
        data = get_params_from_class(self.__dict__, "original_data")
        return data