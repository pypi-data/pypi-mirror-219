import time
import os
import os.path
import sys
import threading 
import requests
import json
import base64
import random

from nwebclient import base as b
from nwebclient import NWebClient
from nwebclient import util

class Process(b.Base):
    name = 'process'
    cpu = None
    def __init__(self, name='Process'):
        self.name = name
    def tick(self):
        pass
    def configure(self, arg):
        pass
    def cmd(self, args):
        return False
    def __str__(self):
        return "Process({0}, {1})".format(self.name, self.__class__.__name__)
    def __repr__(self):
        return "Process({0}, {1})".format(self.name, self.__class__.__name__)


class CmdEcho(Process):
    """
       nwebclient.ticker.CmdEcho
    """
    def __init__(self):
        super().__init__('CmdEcho')
    def cmd(self, args):
        print("CMD: " + ' '.join(map(lambda x: str(x), args)))
        return False
    

class CmdOps(Process):
    """
       nwebclient.ticker.CmdOps
    """
    def __init__(self):
        super().__init__('CmdOps')
    def queue_job(self, job_name):
        print("[CmdOps] queue_job")
        self.cpu.jobs.append(util.Args().env('named_jobs')[job_name])
        return True
    def cmd(self, args):
        if len(args)>=1:
            op = args[0]
            if op == 'add':
                load_from_arg(self.cpu, args[1])
                return True
            if op == 'queue_job':
                return self.queue_job(args[1])
        return False


class Ticker(Process):
    last = 0
    interval = 10
    fn = None
    ticks = 0
    def __init__(self, name = 'ticker', interval = 15, fn = None, wait=True):
        super().__init__(name) 
        self.interval = interval
        self.fn = fn
        if wait:
            self.last = int(time.time())
    def tick(self):
        t = int(time.time())
        dur = t - self.last;
        if dur > self.interval:
            self.last = t
            self.ticks = self.ticks + 1
            self.execute()
    def cmd(self, args):
        if len(args)>=2 and args[0]==self.name and args[1]=='set_interval':
            self.interval = int(args[2])
            return True
        return super().cmd(args)
    def execute(self):
        if not self.fn is None:
            self.fn()
    def __str__(self):
        return super().__str__() + " interval="+str(self.interval)
            
class PiepTicker(Ticker):
    msg = 'piep'
    def __init__(self, interval = 60):
        super().__init__(name='piep', interval=interval) 
    def execute(self):
        print(self.msg)
        

class InfoTicker(Ticker):
    msg = 'piep'
    def __init__(self, interval = 180):
        super().__init__(name='info_ticker', interval=interval) 
    def execute(self):
        print("Job-Count:     " + str(len(self.cpu.jobs)))
        print("Process-Count: " + str(len(self.cpu.processes)))
        #print("Child-Count:   " + str(len(self.cpu.__childs)))


class FileExtObserver(Ticker):
    def __init__(self, name = 'ext_observer', ext='.sdjob', interval = 15):
        super().__init__(name=name, interval=interval) 
        self.ext = ext
    def processFile(self, filename):
        pass
    def execute(self):
        filelist = [ f for f in os.listdir('.') if f.endswith(self.ext) ]
        for f in filelist:
            print(self.name + ": Found file: "+ f)
            self.processFile(f)
            
            
class JobFileLoader(Ticker):
    def __init__(self, name = 'job_observer', ext='.job.json', interval = 65):
        super().__init__(name=name, ext=ext, interval=interval) 
    def processFile(self, filename):
        data = util.load_json_file(filename)
        self.cpu.jobs.append(data)


class UrlDownloader(Ticker):
    """
      Laedt periodisch eine URL in eine Datei
    """
    def __init__(self, name = 'UrlDownloader', interval = 3600, url='https://bsnx.net/4.0/', filename='data.txt', fail_on_exists = True):
        super().__init__(name, interval) 
        self.url = url
        self.filename = filename
        self.fail_on_exists = fail_on_exists
    def execute(self):
        res = requests.get(self.url)
        if not (os.path.isfile(self.filename) and self.fail_on_exists):
            with open(self.filename, 'w') as f:
                f.write(self.filename)


class JobFetcher(Ticker):
    def __init__(self, name = 'UrlDownloader', interval = 120, url = None):
        super().__init__(name, interval) 
        self.url = url 
    def execute(self):
        res = requests.get(self.url)
        job = json.loads(res.text)
        self.cpu.jobs.append(job)


class TypeJobExecutor(Ticker):
    def __init__(self, name = 'jobtype', interval = 61, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.cmd(['jobresult', result, current])
                print(str(result))
                
                
class JobExecutor(Ticker):
    def __init__(self, name = 'jobexec', interval = 63, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            current = self.cpu.jobs.pop(0)
            result = self.executor(current)
            self.cpu.cmd(['jobresult', result, current])
            print(str(result))
                
                
class TypeMapJobExecutor(Ticker):
    def __init__(self, name = 'jobtype', interval = 64, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.jobs.append(result)
                

class NWebJobFetch(Ticker):
    """ 
      NWebFetch(NWebClient(...), 42)  
      
      npy-ticker nwebclient.sd.JobFetch:42
      
      Cfg: job_fetch_group_id
    """
    key = None
    def __init__(self, interval = 61, nwebclient=None, group=None):
        super().__init__("NWebFetch",interval) 
        if nwebclient is None:
            self.debug("Reading from nweb.json")
            nwebclient = NWebClient(None)
        self.nweb = nwebclient
        if group is None:
            group = util.Args().val('job_fetch_group_id')
        self.group = group
    def configure(self, arg):
        #from nwebclient import NWebClient
        #self.nweb = NWebClient()
        #self.group = arg
        pass
    def execute(self):
        self.debug("Fetching Jobs...")
        docs = self.nweb.docs('group_id='+str(self.group))
        for doc in docs:
            self.download(doc)
    def download(self, doc):
        self.log("Start Download")
        content = doc.content()
        self.cpu.jobs.append(json.loads(content))
        self.nweb.deleteDoc(doc.id())
    def log(self, message):
        print("JobFetch: "+str(message))
        

class NWebJobResultUploader(Process):
    def __init__(self, nwebclient=None, group=None):
        super().__init__("NWebFetch") 
        if nwebclient is None:
            self.debug("Reading from nweb.json")
            nwebclient = NWebClient(None)
        self.nweb = nwebclient
        if group is None:
            group = util.Args().val('job_result_group_id')
        self.group = group
    def cmd(self, args):
        if len(args)>=2 and args[0]=='jobresult':
            print("Upload to group: " + str(self.group))
            s = json.dumps(args[1])
            #print("JSON: " + str(s))
            self.nweb.createDoc('job_result', s, self.group, kind='json')
            return True
        return False


class UrlPostShTicker(Ticker):
    """
      Sendet Daten an einen POST-Endpoint
      
      nwebclient.ticker.UrlPostShTicker
      
      Sh URL wie folgt: https://bsnx.net/4.0/w/d/514419/sh/3bab31c346b631a34c4fe7689f551330
    """
    SETTINGS = ['ticker_sh_url']
    uptime_counter = 0
    def __init__(self, name = 'UrlPostShTicker', interval = 3600, url=None):
        super().__init__(name, interval) 
        if url is None:
            url = util.Args().val('ticker_sh_url')
        self.url = url  
    def execute(self):
        self.uptime_counter = self.uptime_counter + self.interval
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        requests.post(self.url, data={'uptime': str(self.uptime_counter)+"s up, "+current_time})
        
        
class PeriodicalCronJob(Ticker):
    """
      Settings: named_jobs
    """
    def __init__(self, name = 'PeriodicalCronJob', interval = 3600, named_job_name=None):
        super().__init__(name, interval)
        self.named_job_name = named_job_name
    def configure(self, arg):
        print("[PeriodicalCronJob] configure with "+ str(arg))
        self.named_job_name = arg
        if self.name == 'PeriodicalCronJob':
            self.name = arg
        if self.interval == 3600:
            self.interval = random.randrange(1800, 3900)
    def execute(self):
        jobs = util.Args().env('named_jobs')
        if self.named_job_name in jobs:
            print("[PeriodicalCronJob] Job "+self.named_job_name+" queued.")
            self.cpu.jobs.append(jobs[self.named_job_name])
        else:
            print("[PeriodicalCronJob] Error: Job "+ self.named_job_name + "not found.")


class WebProcess(Process):
    def __init__(self, port = 9080):
        super().__init__('WebProcess')
        self.port = port
        self.startServer()
    def startServer(self):
        f = lambda: self.startAsync()
        x = threading.Thread(target=f)
        x.start()
    def index(self):
        return "Hallo Welt"
    def prop(self):
        from flask import request
        name = request.args.get('name')
        p = self.cpu[name]
        return str(getattr(p, request.args.get('prop'), ''))
    def createApp(self):
        from flask import Flask
        app = Flask(self.name)
        app.add_url_rule('/', 'index', lambda: self.index())
        app.add_url_rule('/status', 'status', lambda: "ok")
        app.add_url_rule('/processes', 'processes', lambda: str(self.cpu.processes))
        app.add_url_rule('/job-count', 'job_count', lambda: str(len(self.cpu.jobs)))
        app.add_url_rule('/prop', 'prop', lambda: self.prop())
        return app
    def startAsync(self):
        app = self.createApp()
        app.run(port=self.port)


class Cpu(b.Base):
    processes = []
    sleep_time = 1
    jobs = []
    def __init__(self, *args):
        for arg in args:
            self.add(arg)
    def __iter__(self):
        return self.processes.__iter__()
    def add(self, process):
        process.cpu = self
        self.addChild(process)
        self.processes.append(process)
        return self
    def tick(self):
        for p in self.processes:
            try: 
                p.tick()
            except Exception as e:
                print("[CPU] Error in Tick Process "+ p.name + ": " + str(e) )
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)
    def cmd(self, args):
        print("[CPU] Start CMD")
        res = False
        for p in self.processes:
            try:
                res = p.cmd(args) or res
            except Exception as e:
                print("[CPU] Error in CMD Process "+ p.name + ": " + str(e) )
                return False
        return res
    def loop(self):
        while True:
            self.tick()
    def loopAsync(self):
        f = lambda: self.loop()
        x = threading.Thread(target=f)
        x.start()
        return x
    def runTicks(self, count=100) :
        for i in range(count):
             self.tick()
    def __getitem__(self, name):
        for p in self.processes:
            if p.name == name:
                return p
        return None
    def __str__(self):
        s = "Cpu("
        for p in self.processes:
            s = s + ' ' + str(p)
        return s


def load_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)

def load_from_arg(cpu, arg):
    try:
        a = arg.split(':')
        a.append('')
        cls = load_class(a[0])
        c = cls()
        c.configure(''.join(a[1:]))
        cpu.add(c)
    except Exception as e:
        print("[nwebclient.ticker] load_from_arg faild for " +str(arg))

def create_cpu(arg):
    params = arg.getValue('ticker')
    if '1'==params:
        params = arg.env('ticker', [])
    cpu = Cpu()
    for param in params:
        print("[CPU] Loading: " + str(param))   
        load_from_arg(cpu, param)
    return cpu
                
def main():
    print("npy-ticker")
    print("npy-ticker namespace.Proc:cfg ...")
    cpu = Cpu()
    for arg in sys.argv[1:]:
        print("[nwebclient.ticker] Loading: " + str(arg))   
        load_from_arg(cpu, arg)
    print(str(cpu))
    print("[nwebclient.ticker] Looping...")
    cpu.loop()
    
# 
if __name__ == '__main__': # npy-ticker vom python-package bereitgestellt
    main()