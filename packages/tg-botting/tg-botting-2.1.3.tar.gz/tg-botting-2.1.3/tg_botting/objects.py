import json
from copy import deepcopy
from datetime import datetime

from tg_botting.user import User
from tg_botting.utils import get_params_from_func, get_params_from_class


def get_chat_member(response):
    chatMember = ChatMember(response)
    if chatMember.status == 'creator':
        return ChatMemberOwner(response)
    elif chatMember.status == 'administrator':
        return ChatMemberAdministrator(response)
    elif chatMember.status == 'member':
        return ChatMemberMember(response)
    elif chatMember.status == 'restricted':
        return ChatMemberRestricted(response)
    elif chatMember.status == 'left':
        return ChatMemberLeft(response)
    elif chatMember.status == 'kicked':
        return ChatMemberBanned(response)
    return chatMember


class ChatPhoto:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.small_file_id = data.get('small_file_id')
        self.small_file_unique_id = data.get('small_file_unique_id')
        self.big_file_id = data.get('big_file_id')
        self.big_file_unique_id = data.get('big_file_unique_id')


class Location:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.longitude = data.get('longitude')
        self.latitude = data.get('latitude')
        self.horizontal_accuracy = data.get('horizontal_accuracy') if 'horizontal_accuracy' in data else 0
        self.live_period = data.get('live_period') if 'live_period' in data else 0
        self.heading = data.get('heading') if 'heading' in data else 0
        self.proximity_alert_radius = data.get('proximity_alert_radius') if 'proximity_alert_radius' in data else 0


class ChatLocation:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.location = Location(data.get("location"))
        self.address = data.get("address")


class File:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self.__unpack(data)

    def __unpack(self, data):
        self.file_id = data.get('file_id')
        self.file_unique_id = data.get('file_unique_id')
        self.width = data.get('width') if 'widht' in data else None
        self.height = data.get('height') if 'height' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None
        self.file_path = data.get('file_path') if 'file_path' in data else None


class PhotoSize(File):

    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.file_size = data.get('file_size') if 'file_size' in data else None


class Animation(File):

    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.duration = data.get('duration')
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None
        self.file_name = data.get('file_name') if 'file_name' in data else None
        self.mime_type = data.get('mime_type') if 'mime_type' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None


class Audio(File):

    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.duration = data.get('duration')
        self.performer = data.get('performer') if 'performer' in data else None
        self.title = data.get('title') if 'title' in data else None
        self.file_name = data.get('file_name') if 'file_name' in data else None
        self.mime_type = data.get('mime_type') if 'mime_type' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None


class Document(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None
        self.file_name = data.get('file_name') if 'file_name' in data else None
        self.mime_type = data.get('mime_type') if 'mime_type' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None


class MaskPosition:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.point = data.get('point')
        self.x_shift = data.get('x_shift')
        self.y_shift = data.get('y_shift')
        self.scale = data.get('scale')


class Sticker(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.type = data.get('type')
        self.is_animated = data.get('is_animated')
        self.is_video = data.get('is_video')
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None
        self.emoji = data.get('emoji') if 'emoji' in data else None
        self.set_name = data.get('set_name') if 'set_name' in data else None
        self.premium_animation = File(data.get('premium_animation')) if 'premium_animation' in data else None
        self.mask_position = MaskPosition(data.get('mask_position')) if 'mask_position' in data else None
        self.custom_emoji_id = data.get('custom_emoji_id') if 'custom_emoji_id' in data else None
        self.needs_repainting = data.get('needs_repainting') if 'needs_repainting' in data else False
        self.file_size = data.get('file_size') if 'file_size' in data else None


class Video(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.duration = data.get('duration')
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None
        self.file_name = data.get('file_name') if 'file_name' in data else None
        self.mime_type = data.get('mime_type') if 'mime_type' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None


class VideoNote(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.length = data.get('length')
        self.duration = data.get('duration')
        self.thumbnail = PhotoSize(data.get('thumbnail')) if 'thumbnail' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None


class Voice(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.duration = data.get('duration')
        self.mime_type = data.get('mime_type') if 'mime_type' in data else None
        self.file_size = data.get('file_size') if 'file_size' in data else None


class Contact:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.phone_number = data.get('phone_number')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name') if 'last_name' in data else None
        self.user_id = data.get('user_id') if 'user_id' in data else None
        self.vcard = data.get('vcard	') if 'vcard' in data else None


class Dice:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.emoji = data.get('emoji')
        self.value = data.get('value')


class MessageEntity:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.type = data.get('type')
        self.offset = data.get('offset')
        self.length = data.get('length')
        self.url = data.get('url') if 'url' in data else None
        self.user = User(data.get('user')) if 'user' in data else None
        self.language = data.get('language') if 'language' in data else None
        self.custom_emoji_id = data.get('custom_emoji_id') if 'custom_emoji_id' in data else None

    @classmethod
    def create(cls, type, offset, lenght, url=None, user=None, language=None, custom_emoji_id=None):
        data = get_params_from_func(locals(), "data")
        return cls(data)

    @property
    def dict(self):
        data = get_params_from_class(self.__dict__, "original_data")
        return data


class Game:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.photo = [PhotoSize(r) for r in data.get('photo')]
        self.text = data.get('text') if 'text' in data else None
        self.text_entities = [MessageEntity(r) for r in data.get('text_entities')] if 'text_entities' in data else None
        self.animation = Animation(data.get('animation')) if 'animation' in data else None


class PollOption:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.text = data.get('text')
        self.voter_count = data.get('voter_count')


class Poll:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.question = data.get('question')
        self.options = [PollOption(r) for r in data.get('options')]
        self.total_voter_count = data.get('total_voter_count')
        self.is_closed = data.get('is_closed')
        self.is_anonymous = data.get('is_anonymous')
        self.type = data.get('type')
        self.allows_multiple_answers = data.get('allows_multiple_answers')
        self.correct_option_id = data.get('correct_option_id') if 'correct_option_id' in data else None
        self.explanation = data.get('explanation') if 'explanation' in data else None
        self.explanation_entities = [MessageEntity(r) for r in
                                     data.get('explanation_entities')] if 'explanation_entities' in data else None
        self.open_period = data.get('open_period') if 'open_period' in data else None
        self.close_date = data.get('close_date') if 'close_date' in data else None


class Venue:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.location = Location(data.get('location'))
        self.title = data.get('title')
        self.address = data.get('address')
        self.foursquare_id = data.get('foursquare_id') if 'foursquare_id' in data else None
        self.foursquare_type = data.get('foursquare_type') if 'foursquare_type' in data else None
        self.google_place_id = data.get('google_place_id') if 'google_place_id' in data else None
        self.google_place_type = data.get('google_place_type') if 'google_place_type' in data else None


class MessageAutoDeleteTimerChanged:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.message_auto_delete_time = data.get('message_auto_delete_time')


class Invoice:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.start_parameter = data.get('start_parameter')
        self.currency = data.get('currency')
        self.total_amount = data.get('total_amount')


class ShippingAddress:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.country_code = data.get('country_code')
        self.state = data.get('state')
        self.city = data.get('city')
        self.street_line1 = data.get('street_line1')
        self.street_line2 = data.get('street_line2')
        self.post_code = data.get('post_code')


class OrderInfo:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.name = data.get('name') if 'name' in data else None
        self.phone_number = data.get('phone_number') if 'phone_number' in data else None
        self.email = data.get('email') if 'email' in data else None
        self.shipping_address = ShippingAddress(data.get('shipping_address')) if 'shipping_address' in data else None


class SuccessfulPayment:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.currency = data.get('currency')
        self.total_amount = data.get('total_amount')
        self.invoice_payload = data.get('invoice_payload')
        self.shipping_option_id = data.get('shipping_option_id') if 'shipping_option_id' in data else None
        self.order_info = OrderInfo(data.get('order_info')) if 'order_info' in data else None
        self.telegram_payment_charge_id = data.get('telegram_payment_charge_id')
        self.provider_payment_charge_id = data.get('provider_payment_charge_id')


class UserShared:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.request_id = data.get('request_id')
        self.user_id = data.get('user_id')


class ChatShared:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.request_id = data.get('request_id')
        self.chat_id = data.get('chat_id')


class WriteAccessAllowed:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.web_app_name = data.get('web_app_name') if 'web_app_name' in data else None


class PasportFile(File):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.file_size = data.get('file_size')
        self.file_date = datetime.fromtimestamp(data.get('file_date'))


class EncryptedPassportElement:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.type = data.get('type')
        self.data = data.get('data') if 'data' in data else None
        self.phone_number = data.get('phone_number') if 'phone_number' in data else None
        self.email = data.get('email') if 'email' in data else None
        self.files = [PasportFile(r) for r in data.get('files')] if 'files' in data else None
        self.front_side = PasportFile(data.get('front_side')) if 'front_side' in data else None
        self.reverse_side = PasportFile(data.get('reverse_side')) if 'reverse_side' in data else None
        self.selfie = PasportFile(data.get('selfie')) if 'selfie' in data else None
        self.translation = [PasportFile(r) for r in data.get('translation')] if 'translation' in data else None
        self.hash = data.get('hash') if 'hash' in data else None


class EncryptedCredentials:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.data = data.get('data')
        self.hash = data.get('hash')
        self.secret = data.get('secret')


class PassportData:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.data = [EncryptedPassportElement(r) for r in data.get('data')]
        self.credentials = EncryptedCredentials(data.get('credentials'))


class ProximityAlertTriggered:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.traveler = User(data.get('traveler'))
        self.watcher = User(data.get('watcher'))
        self.distance = data.get('distance')


class ForumTopicCreated:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.name = data.get('name')
        self.icon_color = data.get('icon_color')
        self.icon_custom_emoji_id = data.get('icon_custom_emoji_id') if 'icon_custom_emoji_id' in data else None


class ForumTopicEdited:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.name = data.get('name') if 'name' in data else None
        self.icon_custom_emoji_id = data.get('icon_custom_emoji_id') if 'icon_custom_emoji_id' in data else None


class ForumTopicClosed:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class ForumTopicReopened:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class GeneralForumTopicHidden:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class GeneralForumTopicUnhidden:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class VideoChatScheduled:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.start_date = data.get('start_date') if 'start_date' in data else None


class VideoChatEnded:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class VideoChatStarted:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.duration = data.get('duration') if 'duration' in data else None


class VideoChatParticipantsInvited:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.users = [User(r) for r in data.get('users')] if 'users' in data else None


class WebAppData:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.data = data.get('data') if 'data' in data else None
        self.button_text = data.get('button_text') if 'button_text' in data else None


class WebAppInfo:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.url = data.get('url')

    @property
    def dict(self):
        return {'url':self.url}


class LoginUrl:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.url = data.get('url')
        self.forward_text = data.get('forward_text') if 'forward_text' in data else None
        self.bot_username = data.get('bot_username') if 'bot_username' in data else None
        self.request_write_access = data.get('request_write_access') if 'request_write_access' in data else False


class SwitchInlineQueryChosenChat:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.query = data.get('query') if 'query' in data else None
        self.allow_user_chats = data.get('allow_user_chats') if 'allow_user_chats' in data else None
        self.allow_bot_chats = data.get('allow_bot_chats') if 'allow_bot_chats' in data else None
        self.allow_group_chats = data.get('allow_group_chats') if 'allow_group_chats' in data else None
        self.allow_channel_chats = data.get('allow_channel_chats') if 'allow_channel_chats' in data else None


class CallbackGame:
    def __init__(self, data):
        self.original_data = deepcopy(data)


class InlineKeyboardButton:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.text = data.get('text')
        self.url = data.get('url') if 'url' in data else None
        self.callback_data = data.get('callback_data') if 'callback_data' in data else None
        self.web_app = WebAppInfo(data.get('web_app')) if 'web_app' in data else None
        self.login_url = LoginUrl(data.get('login_url')) if 'login_url' in data else None
        self.switch_inline_query = data.get('switch_inline_query') if 'switch_inline_query' in data else None
        self.switch_inline_query_current_chat = data.get(
            'switch_inline_query_current_chat') if 'switch_inline_query_current_chat' in data else None
        self.switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat(
            data.get('switch_inline_query_chosen_chat')) if 'switch_inline_query_chosen_chat' in data else None
        self.callback_game = CallbackGame(data.get('callback_game')) if 'callback_game' in data else None
        self.pay = data.get('pay') if 'pay' in data else None

    @classmethod
    def create(cls, text, url=None, callback_data=None, web_app=None,
               login_url=None, switch_inline_query=None, switch_inline_query_current_chat=None,
               switch_inline_query_chosen_chat=None, callback_game=None, pay=None):
        d = {}
        for a, b in locals().items():
            if a == 'cls' or a == 'd':
                continue
            if b != None:
                d.update({a: b})
        return cls(d)

    @property
    def dict(self):
        d_ = {}
        for a, b in self.__dict__.items():
            if a == 'original_data':
                continue
            if b is None:
                continue
            d_.update({a: b})
        return d_


class InlineKeyboardMarkup:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.inline_keyboard = [InlineKeyboardButton(r) for r in
                                data.get('inline_keyboard')] if 'inline_keyboard' in data else []

    @classmethod
    def create(cls):
        return cls({})

    def addButton(self, button: InlineKeyboardButton):
        self.inline_keyboard.append(button)

    @property
    def dict(self):
        data = {
            'inline_keyboard': [r.dict for r in self.inline_keyboard]
        }
        return data

class KeyboardButtonRequestUser:
    def __init__(self, request_id, user_is_bot=None,user_is_premium=None):
        self.request_id = request_id
        self.user_is_bot = user_is_bot
        self.user_is_premium = user_is_premium

    @property
    def dict(self):
        return self.__dict__

class ChatAdministratorRights:
    def __init__(self,is_anonymous=False,can_manage_chat=False,can_delete_messages=False,
                 can_manage_video_chats=False,can_restrict_members=False,can_promote_members=False,
                 can_change_info=False,can_invite_users=False,can_post_messages=False,
                 can_edit_messages=False,can_pin_messages=False,can_manage_topics=False):
        self.is_anonymous = is_anonymous
        self.can_manage_chat = can_manage_chat
        self.can_delete_messages = can_delete_messages
        self.can_manage_video_chats = can_manage_video_chats
        self.can_restrict_members =can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_pin_messages = can_pin_messages
        self.can_manage_topics = can_manage_topics

    @property
    def dict(self):
        return self.__dict__

class KeyboardButtonRequestChat:
    def __init__(self, request_id, chat_is_channel,chat_is_forum=None,chat_has_username=None,chat_is_created=None,
                 user_administrator_rights:ChatAdministratorRights=None,bot_administrator_rights:ChatAdministratorRights=None,
                 bot_is_member=None):
        self.request_id = request_id
        self.user_is_bot = chat_is_channel
        self.chat_is_forum = chat_is_forum
        self.chat_has_username = chat_has_username
        self.chat_is_created = chat_is_created
        self.user_administrator_rights = user_administrator_rights.dict if user_administrator_rights else None
        self.bot_administrator_rights = bot_administrator_rights.dict if bot_administrator_rights else None
        self.bot_is_member = bot_is_member

    @property
    def dict(self):
        return self.__dict__

class KeyboardButtonPollType:
    def __init__(self,type=None):
        self.type = type

    @property
    def dict(self):
        return self.__dict__

class KeyboardButton:
    def __init__(self,text,request_user:KeyboardButtonRequestUser=None,request_chat:KeyboardButtonRequestChat=None,
                 request_contact=None,request_location=None,request_poll:KeyboardButtonPollType=None,web_app:WebAppInfo=None):
        self.text = text
        self.request_user = request_user.dict if request_user else None
        self.request_chat =request_chat.dict if request_chat else None
        self.request_contact = request_contact
        self.request_location =request_location
        self.request_poll = request_poll.dict if request_poll else None
        self.web_app = web_app.dict if web_app else None

    @property
    def dict(self):
        return self.__dict__


class ReplyKeyboardMarkup:
    def __init__(self, keyboard, is_persistent=None,resize_keyboard=None,one_time_keyboard=None,
                 input_field_placeholder=None,selective=None):
        self.keyboard = [r.dict for r in keyboard]
        self.is_persistent = is_persistent
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.input_field_placeholder = input_field_placeholder
        self.selective =selective

    @property
    def dict(self):
        return self.__dict__

class ReplyKeyboardRemove:
    def __init__(self,remove_keyboard,selective=None):
        self.selective = selective
        self.remove_keyboard = remove_keyboard

    @property
    def dict(self):
        return self.__dict__

class ChatMember:
    def __init__(self, data):
        self.original_data = deepcopy(data)
        self.__unpack(data)

    def __unpack(self, data):
        self.status = data.get('status')
        self.user = User(data.get('user'))


class ChatMemberOwner(ChatMember):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.is_anonymous = data.get('is_anonymous')
        self.custom_title = data.get('custom_title') if 'custom_title' in data else None


class ChatMemberAdministrator(ChatMember):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.can_be_edited = data.get('can_be_edited')
        self.is_anonymous = data.get('is_anonymous')
        self.can_manage_chat = data.get('can_manage_chat')
        self.can_delete_messages = data.get('can_delete_messages')
        self.can_manage_video_chats = data.get('can_manage_video_chats')
        self.can_restrict_members = data.get('can_restrict_members')
        self.can_promote_members = data.get('can_promote_members')
        self.can_change_info = data.get('can_change_info')
        self.can_invite_users = data.get('can_invite_users')
        self.can_post_messages = data.get('can_post_messages')
        self.can_edit_messages = data.get('can_edit_messages')
        self.can_pin_messages = data.get('can_pin_messages')
        self.can_manage_topics = data.get('can_manage_topics')
        self.custom_title = data.get('custom_title') if 'custom_title' in data else None


class ChatMemberMember(ChatMember):
    def __init__(self, data):
        super().__init__(data)


class ChatMemberRestricted(ChatMember):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.is_member = data.get('is_member')
        self.can_send_messages = data.get('can_send_messages')
        self.can_send_audios = data.get('can_send_audios')
        self.can_send_documents = data.get('can_send_documents')
        self.can_send_photos = data.get('can_send_photos')
        self.can_send_videos = data.get('can_send_videos')
        self.can_send_video_notes = data.get('can_send_video_notes')
        self.can_send_voice_notes = data.get('can_send_voice_notes')
        self.can_send_polls = data.get('can_send_polls')
        self.can_send_other_messages = data.get('can_send_other_messages')
        self.can_add_web_page_previews = data.get('can_add_web_page_previews')
        self.can_change_info = data.get('can_change_info')
        self.can_invite_users = data.get('can_invite_users')
        self.can_pin_messages = data.get('can_pin_messages')
        self.can_manage_topics = data.get('can_manage_topics')
        self.until_date = data.get('until_date')


class ChatMemberLeft(ChatMember):
    def __init__(self, data):
        super().__init__(data)


class ChatMemberBanned(ChatMember):
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.until_date = data.get('until_date')


class InlineQuery:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_ = User(data.get('from'))
        self.query = data.get('query')
        self.offset = data.get('offset')
        self.chat_type = data.get('chat_type', None)
        self.location = Location(data.get('location')) if data.get('location', None) is not None else None


class ChosenInlineResult:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.result_id = data.get('result_id')
        self.from_ = User(data.get('from'))
        self.location = Location(data.get('location')) if data.get('location', None) is not None else None
        self.inline_message_id = data.get('inline_message_id', None)
        self.query = data.get('query', None)


class ShippingQuery:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id', None)
        self.invoice_payload = data.get('invoice_payload', None)
        self.shipping_address = ShippingAddress(data.get('shipping_address', None))
        self.from_ = User(data.get('from'))


class PreCheckoutQuery:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id', None)
        self.from_ = User(data.get('from'))
        self.currency = data.get('currency', None)
        self.total_amount = data.get('total_amount', None)
        self.invoice_payload = data.get('invoice_payload', None)
        self.shipping_option_id = data.get('shipping_option_id', None)
        self.order_info = OrderInfo(data.get('order_info', None)) if data.get('order_info', None) is not None else None


class PollAnswer:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.poll_id = data.get('poll_id', None)
        self.user = User(data.get('user', None))
        self.option_ids = [r for r in data.get('option_ids')] if data.get('option_ids', None) is not None else []


class ChatInviteLink:
    def __init__(self, data):
        super().__init__(data)
        self._unpack(data)

    def _unpack(self, data):
        self.invite_link = data.get('invite_link', None)
        self.creator = User(data.get('creator', None))
        self.creates_join_request = data.get('creates_join_request', None)
        self.is_primary = data.get('is_primary', None)
        self.is_revoked = data.get('is_revoked', None)
        self.name = data.get('name', None)
        self.expire_date = data.get('expire_date', None)
        self.member_limit = data.get('member_limit', None)
        self.pending_join_request_count = data.get('pending_join_request_count', None)
