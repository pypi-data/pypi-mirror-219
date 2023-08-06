from copy import deepcopy


class Group:
    """Represents a TG Group

    Attributes
    ----------
    id: :class:`int`
        Id of group, positive int
    name: :class:`str`
        Display name of the group
    screen_name: :class:`str`
        Screen name of the group (link part after vk.com/)
    is_closed: :class:`bool`
        ``True`` if group is closed
    type: :class:`str`
        Can be either `event`, `group` or `page` depending on group type
    photo: :class:`dict`
        Has group photo urls with different sizes
    """

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.is_bot = data.get('is_bot')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name') if 'last_name' in data else None
        self.username = data.get('username') if 'username' in data else None
        self.language_code = data.get('language_code') if 'language_code' in data else None
        self.is_premium = data.get('is_premium') if 'is_premium' in data else False
        self.added_to_attachment_menu = data.get('added_to_attachment_menu') if 'added_to_attachment_menu' in data else False
        self.can_join_groups = data.get('can_join_groups') if 'can_join_groups' in data else False
        self.can_read_all_group_messages = data.get('can_read_all_group_messages') if 'can_read_all_group_messages' in data else False
        self.supports_inline_queries = data.get('supports_inline_queries') if 'supports_inline_queries' in data else False

class Comments:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.count = data.get('count')
        self.can_post = data.get('can_post')
        self.groups_can_post = data.get('groups_can_post')
        self.can_close = data.get('can_close')
        self.can_open = data.get('can_open')


class Likes:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.count = data.get('count')
        self.user_likes = data.get('user_likes')
        self.can_like = data.get('can_like')
        self.can_publish = data.get('can_publish')


class Reposts:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.count = data.get('count')
        self.user_reposted = data.get('user_reposted')


class Views:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.count = data.get('count')


class Geo:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.type = data.get('type')
        self.coordinates = data.get('coordinates')
        self.place = data.get('place')


class Thread:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.count = data.get('count')
        self.items = data.get('items')
        self.can_post = data.get('can_post')
        self.show_reply_button = data.get('show_reply_button')
        self.groups_can_post = data.get('groups_can_post')


class WallComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.reply_to_user = data.get('reply_to_user')
        self.reply_to_comment = data.get('reply_to_comment')
        self.attachments = data.get('attachments')
        self.parents_stack = data.get('parents_stack')
        self.thread = Thread(data.get('thread', {}))
        self.post_id = data.get('post_id')
        self.post_owner_id = data.get('post_owner_id')


class DeletedWallComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.owner_id = data.get('owner_id')
        self.id = data.get('id')
        self.deleter_id = data.get('deleter_id')
        self.post_id = data.get('post_id')


class MarketComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.reply_to_user = data.get('reply_to_user')
        self.reply_to_comment = data.get('reply_to_comment')
        self.attachments = data.get('attachments')
        self.parents_stack = data.get('parents_stack')
        self.thread = Thread(data.get('thread', {}))
        self.market_owner_id = data.get('market_owner_id')
        self.item_id = data.get('item_id')


class DeletedMarketComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.owner_id = data.get('owner_id')
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.deleter_id = data.get('deleter_id')
        self.item_id = data.get('item_id')


class VideoComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.reply_to_user = data.get('reply_to_user')
        self.reply_to_comment = data.get('reply_to_comment')
        self.attachments = data.get('attachments')
        self.parents_stack = data.get('parents_stack')
        self.thread = Thread(data.get('thread', {}))
        self.video_id = data.get('video_id')
        self.video_owner_id = data.get('video_owner_id')


class DeletedVideoComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.owner_id = data.get('owner_id')
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.deleter_id = data.get('deleter_id')
        self.video_id = data.get('video_id')


class PhotoComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.reply_to_user = data.get('reply_to_user')
        self.reply_to_comment = data.get('reply_to_comment')
        self.attachments = data.get('attachments')
        self.parents_stack = data.get('parents_stack')
        self.thread = Thread(data.get('thread', {}))
        self.photo_id = data.get('photo_id')
        self.photo_owner_id = data.get('photo_owner_id')


class DeletedPhotoComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.owner_id = data.get('owner_id')
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.deleter_id = data.get('deleter_id')
        self.photo_id = data.get('photo_id')


class Post:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.owner_id = data.get('owner_id')
        self.date = data.get('date')
        self.marked_as_ads = data.get('marked_as_ads')
        self.post_type = data.get('post_type')
        self.text = data.get('text')
        self.can_pin = data.get('can_pin')
        self.can_edit = data.get('can_edit')
        self.created_by = data.get('created_by')
        self.can_delete = data.get('can_delete')
        self.comments = Comments(data.get('comments', {}))
        self.is_favorite = data.get('is_favorite')
        self.likes = Likes(data.get('likes', {}))
        self.reposts = Reposts(data.get('reposts', {}))
        self.views = Views(data.get('views', {}))
        self.attachments = data.get('attachments')
        self.geo = Geo(data.get('geo', {}))
        self.signer_id = data.get('signer_id')
        self.copy_history = data.get('copy_history')
        self.is_pinned = data.get('is_pinned')
        self.postponed_id = data.get('postponed_id')


class BoardComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.id = data.get('id')
        self.from_id = data.get('from_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.attachments = data.get('attachments')
        self.likes = Likes(data.get('likes', {}))
        self.topic_id = data.get('topic_id')
        self.topic_owner_id = data.get('topic_owner_id')


class DeletedBoardComment:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.topic_owner_id = data.get('topic_owner_id')
        self.topic_id = data.get('topic_id')
        self.id = data.get('id')


class PollVote:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.owner_id = data.get('owner_id')
        self.poll_id = data.get('poll_id')
        self.option_id = data.get('option_id')
        self.user_id = data.get('user_id')


class OfficersEdit:

    def __init__(self, data):
        self._unpack(data)

    def _unpack(self, data):
        self.admin_id = data.get('admin_id')
        self.user_id = data.get('user_id')
        self.level_old = data.get('level_old')
        self.level_new = data.get('level_new')
