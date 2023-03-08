from string import Template
import os, pathlib, shutil


class CLIProjectTemplate(object):
    
    # имена output файлов
    appfname = r'app.py'
    cmdfname = r'cmd.py'
    inifname = r'__init__.py'

    # исходное и целевое имя папки для voice-а
    audiofolder = r'audio'
    
    # имена шаблонов файлов
    templatefolder = r'template'
    ini_template_filename = r'__init__.tmpl'
    cmd_template_filename = r'cmd.tmpl'
    app_template_filename = r'app.tmpl'
    starter_template_filename = r'starter.tmpl'


    def __init__(self, prjname: str) -> None:
        self.prjname = prjname
        self.curpath = os.getcwd()
        self.prjpath = os.path.join(os.getcwd(), self.prjname)
        self.audiopath = os.path.join(pathlib.Path(__file__).parents[1], self.audiofolder)
        self.templatepath = os.path.join(pathlib.Path(__file__).parents[1], self.templatefolder)

    def build(self):
        self.create_prjdir()
        self.make_files()
        self.copy_audio()

    def make_files(self):
        templatedata = {
            'iniimports': ', '.join(['app', 'cmd']),
            'appdir': f'"{self.prjname}"',
            'project_app_module': self.prjname + '.' + 'app'
        }

        src_ini = os.path.join(self.templatepath, self.ini_template_filename)
        src_cmd = os.path.join(self.templatepath, self.cmd_template_filename)
        src_app = os.path.join(self.templatepath, self.app_template_filename)
        src_starter = os.path.join(self.templatepath, self.starter_template_filename)

        dst_ini = os.path.join(self.prjpath, self.inifname)
        dst_cmd = os.path.join(self.prjpath, self.cmdfname)
        dst_app = os.path.join(self.prjpath, self.appfname)
        dst_starter = os.path.join(self.curpath, rf'{self.prjname}.py')

        with open(src_ini, 'r', encoding='utf-8') as f:
            src = Template(f.read())
            initext = src.substitute(templatedata)
            
        with open(src_cmd, 'r', encoding='utf-8') as f:
            src = Template(f.read())
            cmdtext = src.substitute(templatedata)
            
        with open(src_app, 'r', encoding='utf-8') as f:
            src = Template(f.read())
            apptext = src.substitute(templatedata)
        
        with open(src_starter, 'r', encoding='utf-8') as f:
            src = Template(f.read())
            startertext = src.substitute(templatedata)
        
        self._create_file(dst_ini, initext)
        self._create_file(dst_app, apptext)
        self._create_file(dst_cmd, cmdtext)
        self._create_file(dst_starter, startertext)

    def create_prjdir(self):
        os.makedirs(self.prjname)

    def _create_file(self, path, text):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

    def copy_audio(self):
        for d in os.listdir(self.audiopath):
            os.makedirs(os.path.join(self.curpath, self.audiofolder, d))
            for f in os.listdir(os.path.join(self.audiopath, d)):
                shutil.copy2(os.path.join(self.audiopath, d, f), os.path.join(self.curpath, self.audiofolder, d))                
                
            
"""
prjname = r'cli_test_template'
appname = r'app.py'
cmdname = r'cmd.py'
ininame = r'__init__.py'
prjpath = os.path.join(os.getcwd(), prjname)

apptext = 'This is app.py'
cmdtext = 'This is cmd.py'
prjtext = f'This is {prjname}.py'
initext = f'This is {ininame}.py'

os.makedirs(prjname)

with open(os.path.join(prjpath, appname), 'w') as f:
    f.write(apptext)

with open(os.path.join(prjpath, cmdname), 'w') as f:
    f.write(cmdtext)

with open(os.path.join(prjpath, ininame), 'w') as f:
    f.write(initext)

with open(os.path.join(os.path.join(prjpath, r'../'), rf'{prjname}.py'), 'w') as f:
    f.write(prjtext)
"""
