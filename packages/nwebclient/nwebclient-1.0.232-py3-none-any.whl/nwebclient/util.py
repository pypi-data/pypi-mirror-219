
import os
import os.path
import sys
import importlib
import json
import socket
from contextlib import closing

class Args:
    """
      Arg-Parser der eine Überprüfung der Argument vornimmt. 
      Wenn man beim aufruf noch nicht weiß welche Argument abgefragt werden sollen
    """
    argv = []
    cfg=None
    def __init__(self, argv = None):
        if argv is None:
            self.argv = sys.argv
        else:    
            self.argv = argv
    def help_requested(self):
        return self.hasFlag('help') or self.hasShortFlag('h') or '?' in self.argv
    def hasFlag(self, name):
        return '--'+name in self.argv
    def hasShortFlag(self, name):
        return '-'+name in self.argv
    def getValue(self, name, default=None):
        for i in range(len(self.argv)-1):
            if self.argv[i]=='--'+name:
                return self.argv[i+1]
        return default
    def val(self, name, default=None):
        if self.hasFlag(name):
            return self.getValue(name, default)
        else:
            return self.env(name, default)
    def getValues(self, name):
        res = []
        for i in range(len(self.argv)-1):
            if self.argv[i]=='--'+name:
                res.append(self.argv[i+1])
        return res
    def __read_cfg(self):
        if os.path.isfile('nweb.json'):
            with open('nweb.json') as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {}
    def env(self, name, default=None):
        self.__read_cfg();
        if name in self.cfg:
            return self.cfg[name]
        return os.getenv(name, default)
    def __getitem__(self, name):
        if self.hasFlag(name):
            return self.getValue(name)
        else:
            return self.env(name)
    def __get__(self, i):
        return self.argv[i]
    
def load_class(spec, create=False):
    """ spec = 'module:ClassName' """
    try:
        a = spec.split(':')
        m = importlib.import_module(a[0])
        c = getattr(m, a[1])
        if create:
            return c()
        else:
            return c
    except ModuleNotFoundError as e:
        print("[nwebclient.util.load_class] ModuleNotFoundError Spec: " + str(spec), file=sys.stderr)
        print("[nwebclient.util.load_class] PWD: " + str(os.getcwd()), file=sys.stderr)
        raise e

def exists_module(module_name):
    """
      itertools = importlib.import_module('itertools')
      import pkg_resources
      pkg_resources.get_distribution('requests').version
    """
    import importlib.util
    module_spec = importlib.util.find_spec(module_name)
    found = module_spec is not None
    return found

def download(url, filename, ssl_verify=True):
    import requests
    r = requests.get(url, stream=True, verify=ssl_verify) 
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]