from tg_botting.abstract import Messageable


class Context(Messageable):
    def __init__(self, **attrs):
        self.message = attrs.pop('message', None)
        self.bot = attrs.pop('bot', None)
        self.args = attrs.pop('args', [])
        self.kwargs = attrs.pop('kwargs', {})
        self.prefix = attrs.pop('prefix')
        self.command = attrs.pop('command', None)
        self.view = attrs.pop('view', None)
        self.invoked_with = attrs.pop('invoked_with', None)
        self.invoked_subcommand = attrs.pop('invoked_subcommand', None)
        self.subcommand_passed = attrs.pop('subcommand_passed', None)
        self.command_failed = attrs.pop('command_failed', False)

    async def invoke(self, *args, **kwargs):
        try:
            command = args[0]
        except IndexError:
            raise TypeError('Missing command to invoke.') from None

        arguments = []
        if command.cog is not None:
            arguments.append(command.cog)

        arguments.append(self)
        arguments.extend(args[1:])

        ret = await command.callback(*arguments, **kwargs)
        return ret

    async def reinvoke(self, *, call_hooks=False, restart=True):
        cmd = self.command
        view = self.view
        if cmd is None:
            raise ValueError('This context is not valid.')

        index, previous = view.index, view.previous
        invoked_with = self.invoked_with
        invoked_subcommand = self.invoked_subcommand
        subcommand_passed = self.subcommand_passed

        if restart:
            to_call = cmd.root_parent or cmd
            view.index = len(self.prefix)
            view.previous = 0
            view.get_word()
        else:
            to_call = cmd

        try:
            await to_call.reinvoke(self, call_hooks=call_hooks)
        finally:
            self.command = cmd
            view.index = index
            view.previous = previous
            self.invoked_with = invoked_with
            self.invoked_subcommand = invoked_subcommand
            self.subcommand_passed = subcommand_passed

    async def reply(self, text, **kwargs):
        return await self.send(text, reply_to_message_id=self.message.message_id,**kwargs)

    @property
    def cog(self):
        """Returns the cog associated with this context's command. None if it does not exist."""
        if self.command is None:
            return None
        return self.command.cog

    @property
    def valid(self):
        """Checks if the invocation context is valid to be invoked with."""
        return self.prefix is not None and self.command is not None

    @property
    def author(self):
        """Shorthand for :attr:`.Message.from_id`"""
        return self.message.user

    @property
    def from_id(self):
        """Shorthand for :attr:`.Message.from_id`"""
        return self.message.user.id

    @property
    def peer_id(self):
        """Shorthand for :attr:`.Message.peer_id`"""
        return self.message.chat.id

    @property
    def user(self):
        return self.message.user

    @property
    def chat(self):
        return self.message.chat

    @property
    def text(self):
        """Shorthand for :attr:`.Message.text`"""
        return self.message.text

    async def _get_conversation(self):
        return self.message.chat.id

    @property
    def me(self):
        """Returns bot :class:`.Group` or :class:`.User`, depending on whether it is :class:`.Bot` or :class:`.UserBot`"""
        return self.bot.group or self.bot.user
