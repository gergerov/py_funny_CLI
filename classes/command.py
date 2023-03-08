import click, typing as t
from funnyCLI.classes.application import Application
from funnyCLI.classes.parser_ import CmdSequence, CmdOpt, CmdName
from funnyCLI.classes.voice_manager import VoiceManager


class CommandMeta(object):
    """
        is_raise = True 
    бросать ли исключение в приложение из контроллера команд
        
        cmd = {
            'name': 'команда', 
            'description': 'описание',
            'opt': {
                'keyword': 'тип',
                'position': 0,
                'keyword_short': 'т'
                }
            }
    словарь-определение команды
        
        func = None
    можно передать функцию, которая будет выполняться
    в базовом методе execute, либо переопределить этот метод
        
        app: Application
    приложение - базовое или унаследованное приложение
    для управление которым служит команда
        
        voice: VoiceManager
    менеджер озвучки cmd, доступен в команде как self.voice 
    """
    is_raise = True
    cmd = { 'name': 'команда', 'description': 'описание'} 
    func = None
    
    def __init__(self, app: Application, voice: VoiceManager) -> None:
        self.app: Application = app
        self.voice: VoiceManager = voice
        
        cmd_name = CmdName(self.cmd['name'], self.cmd.get('description', '<без описания>'))
        opts = []
        if 'opt' in self.cmd.keys():
            for opt in self.cmd['opt']:
                cmd_opt = CmdOpt(**opt) 
                opts.append(cmd_opt)
        opts.append(cmd_name)
        self.cmd_sequence: CmdSequence = CmdSequence(opts)

    def help(self):
        return self.cmd_sequence.help()

    def its_me(self, cmd_text: str) -> bool:
        """Для определения команды при переборе"""
        if ' ' in cmd_text:
            return cmd_text.split(' ')[0].lower() == self.cmd['name'].lower()
        return cmd_text.lower() == self.cmd['name'].lower()

    def parse_cmd(self, cmd_text) -> dict:
        """Не хранить в себе параметры разобранные параметры cmd!!!"""
        return self.cmd_sequence.parse(cmd_text)

    def accept(self, *args, **kwargs) -> bool:
        """Что делает перед выполнением команды (например вывод сообщения)"""
        return True

    def execute(self, *args, **kwargs):
        """То, что будет выполнять, задано в func или переопределяем"""
        self.func(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Что делает при ошибке, например вывод сообщения"""
        click.echo(
            click.style(
                text=str(kwargs['exception']),
                fg='red',
                bold=True 
            )
        )

    def success(self, *args, **kwargs):
        """Что делает при успешном execute"""
        pass

    def cannot(self, *args, **kwargs):
        """Если не можем выполнить команду"""
        pass

    def print(self, 
        message: t.Optional[t.Any] = None,
        file: t.Optional[t.IO[t.AnyStr]] = None,
        nl: bool = True,
        err: bool = False,
        color: t.Optional[bool] = None,
        fg = None,
        bg = None,
        bold = None
    ):
        message = '>> ' + message
        click.echo(
            click.style(message, fg=fg, bg=bg, bold=bold)
            , file=file, nl=nl,err=err,color=color
        )


class UnknownCommand(CommandMeta):
    text = 'Неизвестная команда'
    def execute(self, *args, **kwargs):
        self.voice.threaded_cannot()
        self.print(self.text)


class GreetCommand(CommandMeta):
    text = 'Жду приказаний'
    def execute(self, *args, **kwargs):
        self.voice.threaded_greet()
        self.print(self.text)


class HelpCommand(CommandMeta):
    cmd = {
        'name': 'помощь',
        'description': 'вывод доступных команд'
    }

    def __init__(self, app: Application, voice: VoiceManager, helptxt: str = '') -> None:
        super().__init__(app, voice)
        self.helptxt = helptxt
    
    def execute(self, *args, **kwargs):
        self.print(self.helptxt, fg='green')
