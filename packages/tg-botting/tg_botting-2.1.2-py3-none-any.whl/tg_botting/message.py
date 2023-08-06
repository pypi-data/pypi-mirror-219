import ctypes
import json
from copy import deepcopy
from datetime import datetime
from random import randint

from tg_botting.abstract import Messageable
from tg_botting.exceptions import TGApiError
from tg_botting.objects import Animation, Audio, Document, PhotoSize, Sticker, Video, VideoNote, Voice, Contact, \
    Dice, MessageEntity, Game, Poll, Venue, Location, MessageAutoDeleteTimerChanged, Invoice, SuccessfulPayment, \
    UserShared, ChatShared, WriteAccessAllowed, PassportData, ProximityAlertTriggered, ForumTopicReopened, \
    ForumTopicClosed, ForumTopicEdited, ForumTopicCreated, GeneralForumTopicHidden, GeneralForumTopicUnhidden, \
    VideoChatScheduled, VideoChatStarted, VideoChatEnded, VideoChatParticipantsInvited, WebAppData, \
    InlineKeyboardMarkup, ChatPhoto, ChatLocation, ChatInviteLink, get_params_from_class, get_chat_member
from tg_botting.permissions import ChatPermissions
from tg_botting.user import User


class ChatMemberUpdated:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.chat = Chat(data.get('chat'))
        self.from_ = User(data.get('from'))
        self.date = data.get('date')
        self.old_chat_member = get_chat_member(data.get('old_chat_member'))
        self.new_chat_member = get_chat_member(data.get('new_chat_member'))
        self.invite_link = ChatInviteLink(data.get('invite_link')) if data.get('invite_link',
                                                                               None) is not None else None
        self.via_chat_folder_invite_link = data.get('via_chat_folder_invite_link', None)


class ChatJoinRequest:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.chat = Chat(data.get('chat'))
        self.from_ = User(data.get('from'))
        self.user_chat_id = data.get('user_chat_id')
        self.date = data.get('date')
        self.bio = data.get('bio', None)
        self.invite_link = ChatInviteLink(data.get('invite_link')) if data.get('invite_link',
                                                                               None) is not None else None


class Chat:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.type = data.get('type')
        self.title = data.get('title') if "title" in data else ""
        self.username = data.get('username') if "username" in data else None
        self.first_name = data.get('first_name') if "first_name" in data else None
        self.last_name = data.get('last_name') if "last_name" in data else None
        self.is_forum = data.get('is_forum') if "is_forum" in data else False
        self.photo = ChatPhoto(data.get('photo')) if "photo" in data else None
        self.active_usernames = [r for r in data.get('active_usernames')] if "active_usernames" in data else []
        self.emoji_status_custom_emoji_id = data.get(
            "emoji_status_custom_emoji_id") if 'emoji_status_custom_emoji_id' in data else None
        self.bio = data.get("bio") if 'bio' in data else None
        self.has_private_forwards = data.get("has_private_forwards") if 'has_private_forwards' in data else False
        self.has_restricted_voice_and_video_messages = data.get(
            "has_restricted_voice_and_video_messages") if 'has_restricted_voice_and_video_messages' in data else False
        self.join_to_send_messages = data.get("join_to_send_messages") if 'join_to_send_messages' in data else False
        self.join_by_request = data.get("join_by_request") if 'join_by_request' in data else False
        self.description = data.get("description") if 'description' in data else None
        self.invite_link = data.get("invite_link") if 'invite_link' in data else None
        self.pinned_message = Message(data.get("pinned_message")) if 'pinned_message' in data else None
        self.permissions = ChatPermissions(data.get("permissions")) if 'permissions' in data else None
        self.slow_mode_delay = data.get("slow_mode_delay") if 'slow_mode_delay' in data else None
        self.message_auto_delete_time = data.get(
            "message_auto_delete_time") if 'message_auto_delete_time' in data else None
        self.has_aggressive_anti_spam_enabled = data.get(
            "has_aggressive_anti_spam_enabled") if 'has_aggressive_anti_spam_enabled' in data else False
        self.has_hidden_members = data.get("has_hidden_members") if 'has_hidden_members' in data else False
        self.has_protected_content = data.get("has_protected_content") if 'has_protected_content' in data else False
        self.sticker_set_name = data.get("sticker_set_name") if 'sticker_set_name' in data else None
        self.can_set_sticker_set = data.get("can_set_sticker_set") if 'can_set_sticker_set' in data else False
        self.linked_chat_id = data.get("linked_chat_id") if 'linked_chat_id' in data else None
        self.location = ChatLocation(data.get("location")) if 'location' in data else None

    @property
    def dict(self):
        data = get_params_from_class(self.__dict__, "original_data")
        return data


class CallbackQuery:
    __slots__ = ('bot', 'id', 'from_', 'message', 'inline_message_id', 'chat_instance', 'data', 'game_short_name')

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_ = data.get('from')
        self.message = Message(data.get('message'))
        self.inline_message_id = data.get('inline_message_id')
        self.chat_instance = data.get('chat_instance')
        self.data = data.get('data')
        self.game_short_name = data.get('game_short_name')

    async def _answer(self, text="", show_alert=True, url=None, cache_time=None):
        data = {
            'callback_query_id': self.id,
            'text': text,
            'show_alert': show_alert
        }
        if url is not None:
            data["url"] = url
        if cache_time is not None:
            data["cache_time"] = cache_time
        res = await self.bot.tg_request('answerCallbackQuery', data)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
        return res

    async def blank_answer(self):
        return await self._answer("", False)


class Message(Messageable):

    async def _get_conversation(self):
        return self.chat.id

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.message_id = data.get('message_id')
        self.message_thread_id = data.get('message_thread_id') if "message_thread_id" in data else -1
        self.user = User(data.get("from")) if "from" in data else None
        self.sender_chat = Chat(data.get("sender_chat")) if "sender_chat" in data else None
        self.date = datetime.fromtimestamp(data.get('date', 86400))
        self.chat = Chat(data.get('chat'))
        self.forward_from_chat = Chat(data.get('forward_from_chat')) if 'forward_from_chat' in data else None
        self.message_thread_id = data.get('message_thread_id') if 'message_thread_id' in data else None
        self.forward_signature = data.get('forward_signature') if 'forward_signature' in data else None
        self.forward_sender_name = data.get('forward_sender_name') if 'forward_sender_name' in data else None
        self.forward_date = datetime.fromtimestamp(data.get('forward_date')) if 'forward_date' in data else None
        self.is_topic_message = data.get('is_topic_message') if 'is_topic_message' in data else False
        self.is_automatic_forward = data.get('is_automatic_forward') if 'is_automatic_forward' in data else False
        self.reply_to_message = Message(data.get('reply_to_message')) if 'reply_to_message' in data else None
        self.via_bot = User(data.get('via_bot')) if 'via_bot' in data else None
        self.edit_date = datetime.fromtimestamp(data.get('edit_date')) if 'edit_date' in data else None
        self.has_protected_content = data.get('has_protected_content') if 'has_protected_content' in data else False
        self.media_group_id = data.get('media_group_id') if 'media_group_id' in data else None
        self.author_signature = data.get('author_signature') if 'author_signature' in data else None
        self.text = data.get('text') if 'text' in data and data.get('text', None) is not None else None
        self.entities = [MessageEntity(r) for r in data.get('entities')] if 'entities' in data and data.get('entities',
                                                                                                            None) is not None else []
        self.animation = Animation(data.get('animation')) if 'animation' in data else None
        self.audio = Audio(data.get('audio')) if 'audio' in data else None
        self.document = Document(data.get('document')) if 'document' in data else None
        self.photo = [PhotoSize(r) for r in data.get('photo')] if 'photo' in data else None
        self.sticker = Sticker(data.get('sticker')) if 'sticker' in data else None
        self.video = Video(data.get('video')) if 'video' in data else None
        self.video_note = VideoNote(data.get('video_note')) if 'video_note' in data else None
        self.voice = Voice(data.get('voice')) if 'voice' in data else None
        self.caption = data.get('caption') if 'caption' in data else None
        self.caption_entities = [MessageEntity(r) for r in
                                 data.get('caption_entities')] if 'caption_entities' in data else None
        self.has_media_spoiler = data.get('has_media_spoiler') if 'has_media_spoiler' in data else False
        self.contact = Contact(data.get('contact')) if 'contact' in data else None
        self.dice = Dice(data.get('dice')) if 'dice' in data else None
        self.game = Game(data.get('game')) if 'game' in data else None
        self.poll = Poll(data.get('poll')) if 'poll' in data else None
        self.venue = Venue(data.get('venue')) if 'venue' in data else None
        self.location = Location(data.get('location')) if 'location' in data else None
        self.new_chat_members = [User(r) for r in data.get('new_chat_members')] if 'new_chat_members' in data else None
        self.left_chat_member = User(data.get('left_chat_member')) if 'left_chat_member' in data else None
        self.left_chat_participant = User(
            data.get('left_chat_participant')) if 'left_chat_participant' in data else None
        self.new_chat_title = data.get('new_chat_title') if 'new_chat_title' in data else None
        self.new_chat_photo = [PhotoSize(r) for r in data.get('new_chat_photo')] if 'new_chat_photo' in data else None
        self.delete_chat_photo = data.get('delete_chat_photo') if 'delete_chat_photo' in data else None
        self.group_chat_created = data.get('group_chat_created') if 'group_chat_created' in data else None
        self.supergroup_chat_created = data.get(
            'supergroup_chat_created') if 'supergroup_chat_created' in data else None
        self.channel_chat_created = data.get('channel_chat_created') if 'channel_chat_created' in data else None
        self.message_auto_delete_timer_changed = MessageAutoDeleteTimerChanged(
            data.get('message_auto_delete_timer_changed')) if 'message_auto_delete_timer_changed' in data else None
        self.migrate_to_chat_id = data.get('migrate_to_chat_id') if 'migrate_to_chat_id' in data else None
        self.migrate_from_chat_id = data.get('migrate_from_chat_id') if 'migrate_from_chat_id' in data else None
        self.pinned_message = Message(data.get('pinned_message')) if 'pinned_message' in data else None
        self.invoice = Invoice(data.get('invoice')) if 'invoice' in data else None
        self.successful_payment = SuccessfulPayment(
            data.get('successful_payment')) if 'successful_payment' in data else None
        self.user_shared = UserShared(data.get('user_shared')) if 'user_shared' in data else None
        self.chat_shared = ChatShared(data.get('chat_shared')) if 'chat_shared' in data else None
        self.connected_website = data.get('connected_website') if 'connected_website' in data else None
        self.write_access_allowed = WriteAccessAllowed(
            data.get('write_access_allowed')) if 'write_access_allowed' in data else None
        self.passport_data = PassportData(data.get('passport_data')) if 'passport_data' in data else None
        self.proximity_alert_triggered = ProximityAlertTriggered(
            data.get('proximity_alert_triggered')) if 'proximity_alert_triggered' in data else None
        self.forum_topic_created = ForumTopicCreated(
            data.get('forum_topic_created')) if 'forum_topic_created' in data else None
        self.forum_topic_edited = ForumTopicEdited(
            data.get('forum_topic_edited')) if 'forum_topic_edited' in data else None
        self.forum_topic_closed = ForumTopicClosed(
            data.get('forum_topic_closed')) if 'forum_topic_closed' in data else None
        self.forum_topic_reopened = ForumTopicReopened(
            data.get('forum_topic_reopened')) if 'forum_topic_reopened' in data else None
        self.general_forum_topic_hidden = GeneralForumTopicHidden(
            data.get('general_forum_topic_hidden')) if 'general_forum_topic_hidden' in data else None
        self.general_forum_topic_unhidden = GeneralForumTopicUnhidden(
            data.get('general_forum_topic_unhidden')) if 'general_forum_topic_unhidden' in data else None
        self.video_chat_scheduled = VideoChatScheduled(
            data.get('video_chat_scheduled')) if 'video_chat_scheduled' in data else None
        self.video_chat_started = VideoChatStarted(
            data.get('video_chat_started')) if 'video_chat_started' in data else None
        self.video_chat_ended = VideoChatEnded(data.get('video_chat_ended')) if 'video_chat_ended' in data else None
        self.video_chat_participants_invited = VideoChatParticipantsInvited(
            data.get('video_chat_participants_invited')) if 'video_chat_participants_invited' in data else None
        self.web_app_data = WebAppData(data.get('web_app_data')) if 'web_app_data' in data else None
        self.reply_markup = InlineKeyboardMarkup(data.get('reply_markup')) if 'reply_markup' in data and data.get(
            'reply_markup', None) is not None else None

    async def edit(self, text=None, *, reply_markup: InlineKeyboardMarkup = None, parse_mode: str = None,
                   entities: ctypes.Array = None, disable_web_page_preview: bool = None, message_id: int = None,
                   inline_message_id: int = None):
        params = {
            'chat_id': self.chat.id,
            'text': text
        }
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup.dict)
        if parse_mode:
            params['parse_mode'] = parse_mode
        if entities:
            params['entities'] = [r.dict for r in entities]
        if disable_web_page_preview:
            params['disable_web_page_preview'] = disable_web_page_preview
        if message_id:
            params['message_id'] = message_id
        if inline_message_id:
            params['inline_message_id'] = inline_message_id
        res = await self.bot.tg_request('editMessageText', **params)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
        return res

    async def delete(self):
        params = {
            'chat_id': self.chat.id,
            'message_id': self.message_id
        }
        res = await self.bot.tg_request('deleteMessage', **params)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))


    async def send_photo(self,chat_id: int,
                         photo:str,
                         caption: str=None,**kwargs):
        res = await self.bot.send_message(chat_id,photo,caption,*kwargs)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
        return Message(res['result'])

    async def reply(self, text, **kwargs):
        return await self.bot.send_message(text, reply_to_message_id=self.message_id,**kwargs)

    async def get_user(self):
        author = await self.bot.get_pages(self.from_id)
        return author[0]

    async def get_author(self):
        return await self.get_user()

    async def fetch_user(self):
        return await self.get_user()

    async def fetch_author(self):
        return await self.get_user()


class UserMessage(Messageable):

    async def _get_conversation(self):
        return self.peer_id

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.date = data.get('date')
        self.flags = data.get('flags')
        self.peer_id = data.get('peer_id')
        self.from_id = data.get('from_id')
        self.text = data.get('text')
        self.attachments = data.get('attachments')
        self.important = data.get('important')
        self.payload = data.get('payload')
        self.keyboard = data.get('keyboard')

    async def edit(self, message=None, *, attachment=None, keep_forward_messages='true', keep_snippets='true'):
        params = {'peer_id': self.peer_id, 'message': message, 'attachment': attachment, 'message_id': self.id,
                  'keep_forward_messages': keep_forward_messages, 'keep_snippets': keep_snippets}
        res = await self.bot.vk_request('messages.edit', **params)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
        return res

    async def reply(self, message=None, *, attachment=None, sticker_id=None, keyboard=None):
        peer_id = await self._get_conversation()
        params = {'random_id': randint(-2 ** 63, 2 ** 63 - 1), 'peer_id': peer_id, 'message': message,
                  'attachment': attachment,
                  'reply_to': self.id, 'sticker_id': sticker_id, 'keyboard': keyboard}
        res = await self.bot.vk_request('messages.send', **params)
        if 'error' in res.keys():
            raise TGApiError('[{error_code}] {error_msg}'.format(**res['error']))
        params['id'] = res['response']
        return self.bot.build_msg(params)

    async def get_user(self):
        user = await self.bot.get_pages(self.from_id)
        if user:
            return user[0]
        return None

    async def get_author(self):
        return await self.get_user()

    async def fetch_user(self):
        return await self.get_user()

    async def fetch_author(self):
        return await self.get_user()
