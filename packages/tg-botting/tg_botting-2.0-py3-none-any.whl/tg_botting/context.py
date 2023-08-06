from tg_botting.abstract import Messageable


class Context(Messageable):
    r"""Represents the context in which a command is being invoked under.

        This class contains a lot of meta data to help you understand more about
        the invocation context. This class is not created manually and is instead
        passed around to commands as the first parameter.

        This class implements the :class:`~tg_botting.abstract.Messageable` ABC.

        Attributes
        -----------
        message: :class:`.Message`
            The message that triggered the command being executed.
        bot: :class:`.Bot`
            The bot that contains the command being executed.
        args: :class:`list`
            The list of transformed arguments that were passed into the command.
            If this is accessed during the :func:`on_command_error` event
            then this list could be incomplete.
        kwargs: :class:`dict`
            A dictionary of transformed arguments that were passed into the command.
            Similar to :attr:`args`\, if this is accessed in the
            :func:`on_command_error` event then this dict could be incomplete.
        prefix: :class:`str`
            The prefix that was used to invoke the command.
        command
            The command (i.e. :class:`.Command` or its subclasses) that is being
            invoked currently.
        invoked_with: :class:`str`
            The command name that triggered this invocation. Useful for finding out
            which alias called the command.
        invoked_subcommand
            The subcommand (i.e. :class:`.Command` or its subclasses) that was
            invoked. If no valid subcommand was invoked then this is equal to
            ``None``.
        subcommand_passed: Optional[:class:`str`]
            The string that was attempted to call a subcommand. This does not have
            to point to a valid registered subcommand and could just point to a
            nonsense string. If nothing was passed to attempt a call to a
            subcommand then this is set to ``None``.
        command_failed: :class:`bool`
            A boolean that indicates if the command failed to be parsed, checked,
            or invoked.
        """

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
        r"""|coro|

        Calls a command with the arguments given.

        This is useful if you want to just call the callback that a
        :class:`.Command` holds internally.

        .. note::

            This does not handle converters, checks, cooldowns, pre-invoke,
            or after-invoke hooks in any matter. It calls the internal callback
            directly as-if it was a regular function.

            You must take care in passing the proper arguments when
            using this function.

        .. warning::

            The first parameter passed **must** be the command being invoked.

        Parameters
        -----------
        command: :class:`.Command`
            A command or subclass of a command that is going to be called.
        \*args
            The arguments to to use.
        \*\*kwargs
            The keyword arguments to use.
        """
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

    async def reply(self, message=None, *, attachment=None, sticker_id=None, keyboard=None):
        """|coro|
        Shorthand for :meth:`.Message.reply`"""
        return await self.message.reply(message, attachment=attachment, sticker_id=sticker_id, keyboard=keyboard)

    async def get_user(self, fields=None, name_case=None):
        """|coro|
        Returns the author of original message as instance of :class:`.User` class
        """
        user = await self.bot.get_page(self.message.from_id, fields=fields, name_case=name_case)
        return user

    async def get_author(self, *args, **kwargs):
        """|coro|
        Alternative for :meth:`.Context.get_user`"""
        return await self.get_user(*args, **kwargs)

    async def fetch_user(self, *args, **kwargs):
        """|coro|
        Alternative for :meth:`.Context.get_user`"""
        return await self.get_user(*args, **kwargs)

    async def fetch_author(self, *args, **kwargs):
        """|coro|
        Alternative for :meth:`.Context.get_user`"""
        return await self.get_user(*args, **kwargs)

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
        return self.message.user.id

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
    def text(self):
        """Shorthand for :attr:`.Message.text`"""
        return self.message.text

    async def _get_conversation(self):
        return self.message.chat.id

    @property
    def me(self):
        """Returns bot :class:`.Group` or :class:`.User`, depending on whether it is :class:`.Bot` or :class:`.UserBot`"""
        return self.bot.group or self.bot.user
