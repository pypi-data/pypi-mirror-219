import abc

from tg_botting.context_managers import Typing


class Messageable(metaclass=abc.ABCMeta):
    __slots__ = ('bot',)

    @abc.abstractmethod
    async def _get_conversation(self):
        raise NotImplementedError

    async def send(self, text, **kwargs):
        peer_id = await self._get_conversation()
        return await self.bot.send_message(peer_id, text, **kwargs)

    async def trigger_typing(self):
        peer_id = await self._get_conversation()
        res = await self.bot.vk_request('messages.setActivity', group_id=self.bot.group.id, type='typing',
                                        peer_id=peer_id)
        return res

    def typing(self):
        return Typing(self)
