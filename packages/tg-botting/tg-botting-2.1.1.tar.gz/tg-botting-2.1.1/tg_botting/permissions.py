from copy import deepcopy


class ChatPermissions:

    def __init__(self, data):
        self.original_data = deepcopy(data)
        self._unpack(data)

    def _unpack(self, data):
        self.can_send_messages = data.get('can_send_messages') if "can_send_messages" in data else False
        self.can_send_audios = data.get('can_send_audios') if "can_send_audios" in data else False
        self.can_send_documents = data.get('can_send_documents') if "can_send_documents" in data else False
        self.can_send_photos = data.get('can_send_photos') if "can_send_photos" in data else False
        self.can_send_videos = data.get('can_send_videos') if "can_send_videos" in data else False
        self.can_send_video_notes = data.get('can_send_video_notes') if "can_send_video_notes" in data else False
        self.can_send_voice_notes = data.get('can_send_voice_notes') if "can_send_voice_notes" in data else False
        self.can_send_polls = data.get('can_send_polls') if "can_send_polls" in data else False
        self.can_send_other_messages = data.get(
            'can_send_other_messages') if "can_send_other_messages" in data else False
        self.can_add_web_page_previews = data.get(
            'can_add_web_page_previews') if "can_add_web_page_previews" in data else False
        self.can_change_info = data.get('can_change_info') if "can_change_info" in data else False
        self.can_invite_users = data.get('can_invite_users') if "can_invite_users" in data else False
        self.can_pin_messages = data.get('can_pin_messages') if "can_pin_messages" in data else False
        self.can_manage_topics = data.get('can_manage_topics') if "can_manage_topics" in data else False

    @classmethod
    def create(cls, can_send_messages=False, can_send_audios=False,
               can_send_documents=False, can_send_photos=False,
               can_send_videos=False, can_send_video_notes=False,
               can_send_voice_notes=False, can_send_polls=False,
               can_send_other_messages=False, can_add_web_page_previews=False,
               can_change_info=False, can_invite_users=False,
               can_pin_messages=False, can_manage_topics=False):
        data = {
            "can_send_messages": can_send_messages,
            "can_send_audios": can_send_audios,
            "can_send_documents": can_send_documents,
            "can_send_photos": can_send_photos,
            "can_send_videos": can_send_videos,
            "can_send_video_notes": can_send_video_notes,
            "can_send_voice_notes": can_send_voice_notes,
            "can_send_polls": can_send_polls,
            "can_send_other_messages": can_send_other_messages,
            "can_add_web_page_previews": can_add_web_page_previews,
            "can_change_info": can_change_info,
            "can_invite_users": can_invite_users,
            "can_pin_messages": can_pin_messages,
            "can_manage_topics": can_manage_topics
        }
        return cls(data)
