import asyncio
import enum
import sys
import textwrap
import traceback
import typing
from typing import TypeVar

import aiohttp

from tg_botting.exceptions import TGException, TGApiError, BadArgument
from tg_botting.general import convert_params
from tg_botting.message import Chat, Message, CallbackQuery
from tg_botting.objects import get_chat_member, MessageEntity, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from tg_botting.user import User
from tg_botting.utils import to_json, maybe_coroutine

String = TypeVar('String', bound=str)
Integer = TypeVar('Integer', bound=int)
Float = TypeVar('Float', bound=float)
Boolean = TypeVar('Boolean', bound=bool)
T = TypeVar('T')

class UserMessageFlags(enum.IntFlag):
    Unread = 1,
    Outbox = 2,
    Replied = 4,
    Important = 8,
    Chat = 16,
    Friends = 32,
    Spam = 64,
    Deleted = 128,
    Fixed = 256,
    Media = 512,
    Hidden = 65536,
    DeleteForAll = 131072,
    NotDelivered = 262144


class _ClientEventTask(asyncio.Task):
    def __init__(self, original_coro, event_name, coro, *, loop):
        super().__init__(coro, loop=loop)
        self.__event_name = event_name
        self.__original_coro = original_coro

    def __repr__(self):
        info = [
            ('state', self._state.lower()),
            ('event', self.__event_name),
            ('coro', repr(self.__original_coro)),
        ]
        if self._exception is not None:
            info.append(('exception', repr(self._exception)))
        return '<ClientEventTask {}>'.format(' '.join('%s=%s' % t for t in info))


class Client:
    def __init__(self, **kwargs):
        self.force = kwargs.get('force', False)
        self.lang = kwargs.get('lang', None)
        self.loop = asyncio.get_event_loop()
        self.group = None
        self.user = None
        self.key = None
        self.server = None
        self._listeners = {}
        timeout = aiohttp.ClientTimeout(total=100, connect=10)
        user_agent = kwargs.get('user_agent', None)
        if user_agent:
            headers = {
                'User-Agent': user_agent
            }
            self.session = kwargs.get('session', aiohttp.ClientSession(timeout=timeout, headers=headers))
        else:
            self.session = kwargs.get('session', aiohttp.ClientSession(timeout=timeout))
        self._all_events = ['message_new', 'sticker' 'message_event', 'message_reply', 'message_allow',
                            'message_deny',
                            'message_edit', 'message_typing_state', 'photo_new', 'audio_new', 'video_new',
                            'wall_reply_new', 'wall_reply_edit', 'wall_reply_delete', 'wall_reply_restore',
                            'wall_post_new', 'wall_repost', 'board_post_new', 'board_post_edit', 'board_post_restore',
                            'board_post_delete', 'photo_comment_new', 'photo_comment_edit', 'photo_comment_delete',
                            'photo_comment_restore', 'video_comment_new', 'video_comment_edit', 'video_comment_delete',
                            'video_comment_restore', 'market_comment_new', 'market_comment_edit',
                            'market_comment_delete', 'market_comment_restore', 'poll_vote_new', 'group_join',
                            'group_leave', 'group_change_settings', 'group_change_photo', 'group_officers_edit',
                            'user_block', 'user_unblock']
        self.extra_events = []
        self.token = None
        self.user_token = None
        self.event_handlers = {
            'callback_query': self.handle_callback_query,
            'message_reply': self.handle_message_reply,
            'message_edit': self.handle_message_edit,
            'sticker': self.handle_sticker_new,
            # 'message_typing_state': self.handle_message_typing_state,
            # 'message_allow': self.handle_message_allow,
            # 'message_deny': self.handle_message_allow,
            # 'photo_new': self.handle_photo_new,
            # 'photo_comment_new': self.handle_photo_comment_new,
            # 'photo_comment_edit': self.handle_photo_comment_new,
            # 'photo_comment_restore': self.handle_photo_comment_new,
            # 'photo_comment_delete': self.handle_photo_comment_delete,
            # 'audio_new': self.handle_audio_new,
            # 'video_new': self.handle_video_new,
            # 'video_comment_new': self.handle_video_comment_new,
            # 'video_comment_edit': self.handle_video_comment_new,
            # 'video_comment_restore': self.handle_video_comment_new,
            # 'video_comment_delete': self.handle_video_comment_delete,
            # 'wall_post_new': self.handle_wall_post_new,
            # 'wall_repost': self.handle_wall_post_new,
            # 'wall_reply_new': self.handle_wall_reply_new,
            # 'wall_reply_edit': self.handle_wall_reply_new,
            # 'wall_reply_restore': self.handle_wall_reply_new,
            # 'wall_reply_delete': self.handle_wall_reply_delete,
            # 'board_post_new': self.handle_board_post_new,
            # 'board_post_edit': self.handle_board_post_new,
            # 'board_post_restore': self.handle_board_post_new,
            # 'board_post_delete': self.handle_board_post_delete,
            # 'market_comment_new': self.handle_market_comment_new,
            # 'market_comment_edit': self.handle_market_comment_new,
            # 'market_comment_restore': self.handle_market_comment_new,
            # 'market_comment_delete': self.handle_market_comment_delete,
            # 'group_leave': self.handle_group_leave,
            # 'group_join': self.handle_group_join,
            # 'user_block': self.handle_user_block,
            # 'user_unblock': self.handle_user_unblock,
            # 'poll_vote_new': self.handle_poll_vote_new,
            # 'group_officers_edit': self.handle_group_officers_edit,
        }

    def Payload(self, **kwargs):
        kwargs['access_token'] = self.token
        return kwargs

    def UserPayload(self, **kwargs):
        if not self.user_token:
            raise TGException('User Token not attached. Use Bot.attach_user_token to attach it.')
        kwargs['access_token'] = self.user_token
        return kwargs

    class botCommandException(Exception):
        pass

    def wait_for(self, event, *, check=None, timeout=None):
        """|coro|

        Waits for an event to be dispatched.

        This could be used to wait for a user to reply to a message or to edit a message in a self-containedway.

        The ``timeout`` parameter is passed onto :func:`asyncio.wait_for`. By default,
        it does not timeout. Note that this does propagate the
        :exc:`asyncio.TimeoutError` for you in case of timeout and is provided for
        ease of use.

        In case the event returns multiple arguments, a :class:`tuple` containing those
        arguments is returned instead. Please check the
        :ref:`documentation <vk_api_events>` for a list of events and their
        parameters.

        This function returns the **first event that meets the requirements**.

        Examples
        ---------
        Waiting for a user reply: ::

            @bot.command()
            async def greet(ctx):
                await ctx.send('Say hello!')
                def check(m):
                    return m.text == 'hello' and m.from_id == ctx.from_id
                msg = await bot.wait_for('message_new', check=check)
                await ctx.send('Hello {.from_id}!'.format(msg))

        Parameters
        ------------
        event: :class:`str`
            The event name, similar to the :ref:`event reference <vk_api_events>`,
            but without the ``on_`` prefix, to wait for.
        check: Optional[Callable[..., :class:`bool`]]
            A predicate to check what to wait for. The arguments must meet the
            parameters of the event being waited for.
        timeout: Optional[:class:`float`]
            The number of seconds to wait before timing out and raising
            :exc:`asyncio.TimeoutError`.

        Raises
        -------
        asyncio.TimeoutError
            If a timeout is provided and it was reached.

        Returns
        --------
        Any
            Returns no arguments, a single argument, or a :class:`tuple` of multiple
            arguments that mirrors the parameters passed in the
            :ref:`event reference <vk_api_events>`.
        """

        future = self.loop.create_future()
        if check is None:
            def _check(*_):
                return True

            check = _check

        ev = event.lower()
        try:
            listeners = self._listeners[ev]
        except KeyError:
            listeners = []
            self._listeners[ev] = listeners

        listeners.append((future, check))
        return asyncio.wait_for(future, timeout)

    async def general_request(self, url, post=False, **params):
        params = convert_params(params)
        for tries in range(5):
            try:
                req = self.session.post(url, data=params) if post else self.session.get(url, params=params)
                async with req as r:
                    if r.content_type == 'application/json':
                        return await r.json()
                    return await r.text()
            except Exception as e:
                print('Got exception in request: {}\nRetrying in {} seconds'.format(e, tries * 2 + 1), file=sys.stderr)
                await asyncio.sleep(tries * 2 + 1)

    async def _tg_request(self, method, post, calln=1, **kwargs):
        if calln > 10:
            raise TGApiError('TG API call failed after 10 retries')
        for param in kwargs:
            if isinstance(kwargs[param], (list, tuple)):
                kwargs[param] = ','.join(map(str, kwargs[param]))
            elif isinstance(kwargs[param], dict):
                kwargs[param] = to_json(kwargs[param])
        res = await self.general_request('https://api.telegram.org/bot{}/{}'.format(kwargs['access_token'], method),
                                         post=post,
                                         **kwargs)
        if isinstance(res, str):
            await asyncio.sleep(0.1)
            return await self._tg_request(method, post, calln + 1, **kwargs)
        error = res.get('error', None)
        if error and error.get('error_code', None) == 6:
            await asyncio.sleep(1)
            return await self._tg_request(method, post, calln + 1, **kwargs)
        elif error and error.get('error_code', None) == 10 and 'could not check access_token now' in error.get(
                'error_msg', ''):
            await asyncio.sleep(0.1)
            return await self._tg_request(method, post, calln + 1, **kwargs)
        return res

    async def tg_request(self, method, post=True, **kwargs):
        return await self._tg_request(method, post, **self.Payload(**kwargs))

    async def user_tg_request(self, method, post=True, **kwargs):
        return await self._tg_request(method, post, **self.UserPayload(**kwargs))

    async def get_me(self):
        user = await self.tg_request('getMe')
        if user.get('ok') != True:
            raise TGApiError('[{error_code}] {description}'.format(**user))
        user = user.get('result')
        return User(user)

    async def get_chat(self, chat_id):
        groups = await self.tg_request('getChat', chat_id=chat_id)
        if groups.get('ok') != True:
            raise TGApiError('[{error_code}] {description}'.format(**groups))
        chat = groups.get('result')
        return Chat(chat)

    async def get_chat_member(self, chat_id, user_id):
        user = await self.tg_request("getChatMember", chat_id=chat_id, user_id=user_id)
        if user.get('ok') != True:
            raise TGApiError('[{error_code}] {description}'.format(**user))
        response = user.get('result')
        return get_chat_member(response)

    def build_msg(self, msg):
        res = Message(msg)
        res.bot = self
        return res

    def generate_link(self, method: str):
        return f'https://api.telegram.org/bot{self.token}/{method}'

    async def longpoll(self, offset=None):
        if offset is None:
            offset = 0
        payload = {'offset': offset + 1}
        try:
            res = await self.general_request(self.generate_link("getUpdates"), **payload)
        except asyncio.TimeoutError:
            return offset, []
        if res['ok'] is False:
            offset = 0
        elif len(res['result']) != 0:
            offset = res['result'][len(res['result']) - 1]['update_id']
        updates = res['result']
        return offset, updates

    def handle_message(self, message):
        msg = self.build_msg(message)

        action = None
        if msg.sticker is not None:
            action = "sticker_new"
        elif msg.audio is not None:
            action = "audio_new"
        elif msg.video is not None:
            action = "video_new"
        elif msg.video_note is not None:
            action = "video_note_new"
        elif msg.voice is not None:
            action = "voice_new"
        elif msg.poll is not None:
            action = "poll_new"
        elif msg.left_chat_member is not None:
            action = "chat_member_left"
        elif msg.photo is not None:
            action = "photo_new"
        elif msg.new_chat_members is not None:
            action = 'new_chat_members'
        elif msg.successful_payment is not None:
            action = "successful_payment"

        if action is not None:
            return self.dispatch(action, msg)

        return self.dispatch('message_new', msg)

    def handle_callback_query(self, t, obj):
        event = CallbackQuery(obj)
        event.bot = self
        return self.dispatch(t, event)

    def handle_sticker_new(self, t, obj):
        msg = self.build_msg(obj)
        return self.dispatch(t, msg)

    def handle_message_reply(self, t, obj):
        msg = self.build_msg(obj)
        return self.dispatch(t, msg)

    def handle_message_edit(self, t, obj):
        msg = self.build_msg(obj)
        return self.dispatch(t, msg)

    def handle_custom_classes(self, t, obj, update):
        names = t.split("_")
        name = [r.title() for r in names]
        class_name = ''.join(name)

        if class_name not in globals():
            return self.dispatch('unknown', update)

        klass = globals()[class_name]
        instance = klass(obj)
        return self.dispatch(t, instance)

    def handle_update(self, update):
        update.pop('update_id')
        t = list(update.keys())[0]
        obj = update[t]
        on_t = 'on_{}'.format(t)
        used = (t in self._listeners and self._listeners[t]) or (on_t in self.extra_events and self.extra_events[on_t])
        unknown_used = ('unknown' in self._listeners and self._listeners['unknown']) or (
                'on_unknown' in self.extra_events and self.extra_events['on_unknown'])
        if t == 'message':
            return self.handle_message(obj)
        elif t in ['inline_query', 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query',
                   'poll',
                   'poll_answer', 'my_chat_member', 'chat_member', 'chat_join_request']:
            return self.handle_custom_classes(t, obj, update)
        elif t in self.event_handlers and used:
            return self.loop.create_task(maybe_coroutine(self.event_handlers[t], t, obj))
        elif t not in self.event_handlers and unknown_used:
            return self.dispatch('unknown', update)

    def dispatch(self, event, *args, **kwargs):
        method = 'on_' + event
        listeners = self._listeners.get(event)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as exc:
                    future.set_exception(exc)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)

            if len(removed) == len(listeners):
                self._listeners.pop(event)
            else:
                for idx in reversed(removed):
                    del listeners[idx]

        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._schedule_event(coro, method, *args, **kwargs)

    async def on_error(self, event_method, *args, **kwargs):
        print('Ignoring exception in {}'.format(event_method), file=sys.stderr)
        traceback.print_exc()

    async def send_photo(self,
                         chat_id: typing.Union[Integer],
                         photo: typing.Union[String],
                         caption: typing.Optional[String] = None,
                         parse_mode: typing.Optional[String] = None,
                         caption_entities: typing.Optional[typing.List[MessageEntity]] = None,
                         message_thread_id: typing.Optional[Integer] = None,
                         disable_notification: typing.Optional[Boolean] = None,
                         protect_content: typing.Optional[Boolean] = None,
                         reply_to_message_id: typing.Optional[Integer] = None,
                         allow_sending_without_reply: typing.Optional[Boolean] = None,
                         reply_markup: typing.Union[InlineKeyboardMarkup,
                         ReplyKeyboardMarkup,
                         ReplyKeyboardRemove,
                         None] = None,
                         has_spoiler: typing.Optional[Boolean] = None,
                         ) -> Message:
        reply_markup = reply_markup.dict if reply_markup is not None else None
        caption_entities = [r.dict for r in caption_entities] if caption_entities else None
        data = {
            'chat_id':chat_id,
            'photo':photo,
            'caption':caption,
            'parse_mode':parse_mode,
            'caption_entities':caption_entities,
            'message_thread_id':message_thread_id,
            'disable_notification':disable_notification,
            'protect_content':protect_content,
            'reply_to_message_id':reply_to_message_id,
            'allow_sending_without_reply':allow_sending_without_reply,
            'reply_markup':reply_markup,
            'has_spoiler':has_spoiler
        }

        result = await self.tg_request('dendPhoto', True, **data)
        return result

    @staticmethod
    def prepare_file(payload, files, key, file):
        if isinstance(file, str):
            payload[key] = file
        elif file is not None:
            files[key] = file

    async def _run_event(self, coro, event_name, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass

    def _schedule_event(self, coro, event_name, *args, **kwargs):
        wrapped = self._run_event(coro, event_name, *args, **kwargs)
        return _ClientEventTask(original_coro=coro, event_name=event_name, coro=wrapped, loop=self.loop)

    async def send_message(self, chat_id, text, message_thread_id=None, parse_mode=None, disable_web_page_preview=None,
                           disable_notification=None, entities=None,
                           protect_content=None, reply_to_message_id=None, allow_sending_without_reply=None,
                           reply_markup=None, **kwargs):
        as_user = kwargs.pop('as_user', False)
        if kwargs:
            print('Unknown parameters passed to send_message: {}'.format(', '.join(kwargs.keys())), file=sys.stderr)
            raise BadArgument
        if len(text) > 4096:
            w = textwrap.TextWrapper(width=4096, replace_whitespace=False)
            messages = w.wrap(text)
            for message in messages[:-1]:
                await self.send_message(chat_id, message, **kwargs)
            return await self.send_message(chat_id, messages[-1], message_thread_id=message_thread_id,
                                           parse_mode=parse_mode,
                                           entities=entities, disable_web_page_preview=disable_web_page_preview,
                                           disable_notification=disable_notification,
                                           protect_content=protect_content, reply_to_message_id=reply_to_message_id,
                                           allow_sending_without_reply=allow_sending_without_reply,
                                           reply_markup=reply_markup, **kwargs)
        params = {'chat_id': chat_id,
                  'text': text,
                  'message_thread_id': message_thread_id,
                  'parse_mode': parse_mode,
                  'entities': [r.dict for r in entities] if entities else None,
                  'disable_web_page_preview': disable_web_page_preview,
                  'disable_notification': disable_notification,
                  'protect_content': protect_content,
                  'reply_to_message_id': reply_to_message_id,
                  'allow_sending_without_reply': allow_sending_without_reply,
                  'reply_markup': reply_markup.dict if reply_markup else None,
                  }
        res = await self.tg_request('sendMessage', **params)
        # if not as_user else await self.user_vk_request(
        # 'messages.send', **params)
        if res.get('ok') != True:
            if res.get('error_code') == 9:
                await asyncio.sleep(1)
                return await self.send_message(chat_id, text, message_thread_id=message_thread_id,
                                               parse_mode=parse_mode,
                                               entities=entities, disable_web_page_preview=disable_web_page_preview,
                                               disable_notification=disable_notification,
                                               protect_content=protect_content, reply_to_message_id=reply_to_message_id,
                                               allow_sending_without_reply=allow_sending_without_reply,
                                               reply_markup=reply_markup, **kwargs)
            raise TGApiError('[{error_code}] {description}'.format(**res))
        if self.is_group and not as_user:
            params['from'] = self.group.dict
            params['message_id'] = res['result']['message_id']
            params['chat']  = res['result']['chat']
        else:
            pass
            # params['from_id'] = self.user.id
            # params['id'] = res['response']
        return self.build_msg(params)

    async def add_user_token(self, token):
        await self.attach_user_token(token)

    async def _run(self):
        self.is_group = True
        self.group = await self.get_me()
        self.dispatch('ready')
        updates = []
        offset = None
        while True:
            try:
                lp = self.loop.create_task(self.longpoll(offset))
                for update in updates:
                    self.handle_update(update)
                offset, updates = await lp
            except Exception as e:
                if self.use_stack_trace:
                    traceback.print_exc(file=sys.stderr)
                print('Ignoring exception in longpoll cycle:\n{}'.format(e), file=sys.stderr)
                offset+=1

    def run(self, token, user_id=None, user_hash=None):
        self.use_stack_trace = False
        self.token = token
        self.user_id = user_id
        self.user_hash = user_hash
        self.loop.create_task(self._run())
        self.loop.run_forever()

# class UserClient(Client):
#
#     def __init__(self, **kwargs):
#         user_agent = kwargs.get('user_agent',
#                                 'KateMobileAndroid/52.1 lite-445 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)')
#         kwargs.setdefault('user_agent', user_agent)
#         super().__init__(**kwargs)
#
#     async def build_user_msg(self, msg):
#         res = UserMessage(msg)
#         if res.attachments:
#             res.attachments = await get_user_attachments(res.attachments)
#         res.bot = self
#         return res
#
#     async def get_user_longpoll(self):
#         res = await self.vk_request('messages.getLongPollServer', group_id=self.group.id, lp_version=3)
#         error = res.get('error', None)
#         if error and error['error_code'] == 15:
#             raise LoginError('User has no access to messages API. Try generating token with vk_botting.auth methods')
#         elif error:
#             raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
#         self.key = res['response']['key']
#         server = res['response']['server'].replace(r'\/', '/')
#         self.server = 'https://{}'.format(server)
#         ts = res['response']['ts']
#         return ts
#
#     async def longpoll(self, ts):
#         payload = {'key': self.key,
#                    'act': 'a_check',
#                    'ts': ts,
#                    'wait': '10'}
#         if not self.is_group:
#             payload['mode'] = 10
#         try:
#             res = await self.general_request(self.server, **payload)
#         except asyncio.TimeoutError:
#             return ts, []
#         if 'ts' not in res.keys() or 'failed' in res.keys():
#             ts = await self.get_user_longpoll()
#         else:
#             ts = res['ts']
#         updates = res.get('updates', [])
#         return ts, updates
#
#     async def handle_user_update(self, update):
#         t = update.pop(0)
#         if t == 4:
#             data = {
#                 'id': update.pop(0),
#                 'flags': UserMessageFlags(update.pop(0)),
#                 'peer_id': update.pop(0),
#                 'date': update.pop(0),
#                 'text': update.pop(1),
#                 'attachments': update.pop(1)
#             }
#             data['from_id'] = data['attachments'].pop('from', data['peer_id'])
#             msg = await self.build_user_msg(data)
#             return self.dispatch('message_new', msg)
#         elif 'on_unknown' in self.extra_events:
#             return self.dispatch('unknown', update)
#
#     async def _run(self):
#         # if owner_id and owner_id.__class__ is not int:
#         #     raise TypeError('Owner_id must be positive integer, not {0.__class__.__name__}'.format(owner_id))
#         # if owner_id and owner_id < 0:
#         #     raise TGApiError('Owner_id must be positive integer')
#         # user = await self.get_own_page()
#         # if isinstance(user, User):
#         self.is_group = False
#         self.group = Group({})
#         # self.user = user
#         ts = await self.get_user_longpoll()
#         self.dispatch('ready')
#         updates = []
#         while True:
#             try:
#                 lp = self.loop.create_task(self.longpoll(ts))
#                 for update in updates:
#                     self.loop.create_task(self.handle_user_update(update))
#                 ts, updates = await lp
#             except Exception as e:
#                 print('Ignoring exception in longpoll cycle:\n{}'.format(e), file=sys.stderr)
#                 ts = await self.get_user_longpoll()
#         # raise LoginError('Group token passed to user client')
#
#     def run(self, token, owner_id=None):
#         """A blocking call that abstracts away the event loop
#         initialisation from you.
#
#         .. warning::
#             This function must be the last function to call due to the fact that it
#             is blocking. That means that registration of events or anything being
#             called after this function call will not execute until it returns.
#
#         Parameters
#         ----------
#         token: :class:`str`
#             Bot token. Should be group token or user token with access to group
#         owner_id: :class:`int`
#             Should only be passed alongside user token. Owner id of group to connect to
#         """
#         self.token = token
#         self.user_token = token
#         self.loop.create_task(self._run(owner_id))
#         self.loop.run_forever()
