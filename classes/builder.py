from funnyCLI.classes.command import CommandMeta, GreetCommand, UnknownCommand, HelpCommand
from funnyCLI.classes.application import Application
from funnyCLI.classes.controller import CommandControllerMeta
import inspect, sys, importlib


class CLIBuilder(object):
    
    def __init__(self, dir: str, app: str = 'app', cmd: str = 'cmd') -> None:
        self.dir = dir
        self.app = app
        self.cmd = cmd
        importlib.import_module(f'{dir}')


    def build(self):
        cmds = self._get_commands()
        appinstance = self._get_app()()
        ccm = CommandControllerMeta(
            app=appinstance, 
            **cmds
        )
        ccm.run()

    def _get_commands(self):
        cmd = []
        unknown = None
        greet = None
        help = None
        clss = inspect.getmembers(sys.modules[f'{self.dir}.{self.cmd}'], inspect.isclass)
        for cls in clss:
            if issubclass(cls[1], CommandMeta) and not (cls[1] == CommandMeta):
                if issubclass(cls[1], UnknownCommand):
                    unknown = cls[1]
                elif issubclass(cls[1], GreetCommand):
                    greet = cls[1]
                elif issubclass(cls[1], HelpCommand):
                    help = cls[1]
                else:
                    cmd.append(cls[1])
        r = {}
        r['command_classes'] = cmd
        if unknown is not None: r['unknown_class'] = unknown
        if greet is not None: r['greet_class'] = greet
        if help is not None: r['help_class'] = help
        return r

    def _get_app(self):
        app = None
        clss = inspect.getmembers(sys.modules[f'{self.dir}.{self.app}'], inspect.isclass)
        for cls in clss:
            if issubclass(cls[1], Application):
                if cls[1] != Application:
                    app = cls[1]
        return app
