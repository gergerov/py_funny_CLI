from funnyCLI.classes.command import CommandMeta, UnknownCommand, GreetCommand, HelpCommand
from funnyCLI.classes.application import Application
from funnyCLI.classes.parser_ import ExceptionArgumentQuantity
from funnyCLI.classes.voice_manager import VoiceManager

import typing, click, os, time


class CommandControllerMeta(object):
    audiopath = fr'{os.getcwd()}\audio'
    # TODO аргументы из инпута в методы команды +
    # TODO проверка на одноименные команды
    
    def __init__(
        self, app: Application, 
        command_classes: typing.List[CommandMeta] = [],
        unknown_class: UnknownCommand = UnknownCommand,
        greet_class: GreetCommand = GreetCommand,
        help_class: HelpCommand = HelpCommand
    ) -> None:
        self.voice: VoiceManager = VoiceManager(self.audiopath)
        self.app = app
        self.objs: typing.List[CommandMeta] = []
        self.unknown: UnknownCommand = unknown_class(app, self.voice)
        self.greet: GreetCommand = greet_class(app, self.voice)
        
        for c in command_classes:
            obj: CommandMeta = c(app, self.voice)
            self.objs.append(obj)

        self.help: HelpCommand = help_class(app, self.voice)

    def run(self):
        if self.app.background:  self.voice.threaded_background()
        self.help.helptxt = self._help()
        self.help.execute()
        self.greet.execute()
        while True:
            time.sleep(0.10) # симпатично и voice не упадет
            cmd_text = input(os.getcwd() + ' << ')
            self._search(cmd_text)
            click.echo(f'{"-"*100}')
        
    def _search(self, cmd_text):
        find = False
        if self.help.its_me(cmd_text):
            self.help.execute()
            return
        for o in self.objs:
            find = o.its_me(cmd_text)
            if find:
                try:
                    kwargs = o.parse_cmd(cmd_text)
                except (ValueError, ExceptionArgumentQuantity) as e:
                    self.voice.threaded_error()
                    o.print(o.cmd_sequence.help(), fg='red', bold=True)
                    o.print(str(e), fg='red', bold=True)
                    return -1
                self._run_command(o, kwargs['opt'])
                return
        if not find: self.unknown.execute()

    def _run_command(self, cmd: CommandMeta, kwargs: dict):
        try:
            if cmd.accept(**kwargs):
                cmd.execute(**kwargs)
                cmd.success(**kwargs)
            else:
                cmd.cannot(**kwargs)
        except Exception as e:
            kwargs['exception'] = e
            cmd.error(**kwargs)
            if cmd.is_raise:
                raise e

    def _help(self) -> str:
        helptxt = ''
        for item in self.objs:
            helptxt += item.help()
        helptxt += self.help.help()

        return helptxt