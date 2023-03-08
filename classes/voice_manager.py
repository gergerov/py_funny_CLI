from pprint import pprint as print
import os, threading as th, audioplayer as ap, random as rd, typing as tp, time


class VoiceManager(object):
    def __init__(self, audiopath: str, pause: float = 0.05) -> None:
        self.pause = pause
        self.cwd = audiopath
        
        self.folder_background = r'background' # фон
        self.folder_greet = r'greet' # приветствие
        self.folder_accept = r'accept' # прошли проверку
        self.folder_cannot = r'cannot' # не прошли проверку
        self.folder_execute = r'execute' # выполнение
        self.folder_success = r'success' # успешное выполнение
        self.folder_error = r'error' # ошибка / exception
    
        self.errors = set()
        self.accepts = set()
        self.backgrounds = set()
        self.executes = set()
        self.greets = set()
        self.successes = set()
        self.cannots = set()

        self.volume_background = 100
        self.volume_error = 100
        self.volume_accept = 100
        self.volume_execute = 100
        self.volume_greet = 100
        self.volume_success = 100
        self.volume_cannot = 100

        self.cur_background_player: ap.AudioPlayer = None
        self.cur_error_player: ap.AudioPlayer = None
        self.cur_accept_player: ap.AudioPlayer = None
        self.cur_execute_player: ap.AudioPlayer = None
        self.cur_greet_player: ap.AudioPlayer = None
        self.cur_success_player: ap.AudioPlayer = None
        self.cur_cannot_player: ap.AudioPlayer = None

        self._read_dir()     

    def _read_dir(self):
        error_path = os.path.join(self.cwd, self.folder_error)
        accept_path = os.path.join(self.cwd, self.folder_accept)
        background_path = os.path.join(self.cwd, self.folder_background)
        execute_path = os.path.join(self.cwd, self.folder_execute)
        greet_path = os.path.join(self.cwd, self.folder_greet)
        success_path = os.path.join(self.cwd, self.folder_success)
        cannot_path = os.path.join(self.cwd, self.folder_cannot)
        
        for path in os.listdir(error_path):
            self.errors.add(os.path.join(error_path, path))
        for path in os.listdir(accept_path):
            self.accepts.add(os.path.join(accept_path, path))
        for path in os.listdir(background_path):
            self.backgrounds.add(os.path.join(background_path, path))
        for path in os.listdir(execute_path):
            self.executes.add(os.path.join(execute_path, path))
        for path in os.listdir(greet_path):
            self.greets.add(os.path.join(greet_path, path))
        for path in os.listdir(success_path):
            self.successes.add(os.path.join(success_path, path))
        for path in os.listdir(cannot_path):
            self.cannots.add(os.path.join(cannot_path, path))

        self.errors = list(self.errors)
        self.accepts = list(self.accepts)
        self.backgrounds = list(self.backgrounds)
        self.executes = list(self.executes)
        self.greets = list(self.greets)
        self.successes = list(self.successes)
        self.cannots = list(self.cannots)

    def _random(self, group: list):
        return group[rd.randint(0, len(group)-1)]

    def _play(self, fp, loop: bool = False):
        audio = ap.AudioPlayer(fp)
        audio.play(loop = loop, block=True)

    def _threaded(self, method):
        t = th.Thread(target=method)
        t.daemon = True
        t.start()

    def accept(self):
        self._play(self._random(self.accepts))

    def error(self):
        self._play(self._random(self.errors))

    def background(self):
        self._play(self._random(self.backgrounds))

    def backgroundloop(self):
        self._play(self._random(self.backgrounds))

    def execute(self):
        self._play(self._random(self.executes))

    def greet(self):
        self._play(self._random(self.greets))

    def success(self):
        self._play(self._random(self.successes))

    def cannot(self):
        self._play(self._random(self.cannots))

    def threaded_cannot(self):
        time.sleep(self.pause)
        self._threaded(self.cannot)

    def threaded_accept(self):
        time.sleep(self.pause)
        self._threaded(self.accept)

    def threaded_success(self):
        time.sleep(self.pause)
        self._threaded(self.success)

    def threaded_greet(self):
        time.sleep(self.pause)
        self._threaded(self.greet)

    def threaded_execute(self):
        time.sleep(self.pause)
        fp: str = self._random(self.executes)
        self.cur_execute_player = ap.AudioPlayer(fp)
        self.cur_execute_player.play()
        # self._threaded(self.execute)
    
    def set_volume_background(self, volume):
        self.volume_background = volume
        self.cur_background_player.volume = self.volume_background

    def threaded_background(self, volume: int = 30):
        time.sleep(self.pause)
        fp: str = self._random(self.backgrounds)
        self.cur_background_player = ap.AudioPlayer(fp)
        self.cur_background_player.volume = self.volume_background
        self.cur_background_player.play()
        return fp.split('\\')[-1]
    
    def threaded_background_close(self):
        self.cur_background_player.close()

    def threaded_backgroundloop(self):
        time.sleep(self.pause)
        self._threaded(self.backgroundloop)
    
    def threaded_error(self):
        time.sleep(self.pause)
        self._threaded(self.error)
