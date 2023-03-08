from core.server import TCPServer
from core.controller.event import ServerEventController
from core.controller.user import UserController
import threading as th


class Application(object):
    name = 'Application'
    dir = 'your_project_folder'
    cmd = 'cmd'
    app = 'app'
    background = True
    pass
