import setting
import myapp
import quickfix
import logging
import default_cfg

logging.basicConfig(filename=default_cfg.logfile,level=default_cfg.level)

cfg = quickfix.SessionSettings(setting.MY_CFG)
store = quickfix.FileStoreFactory(cfg)
log = quickfix.FileLogFactory(cfg)
msg = quickfix.DefaultMessageFactory()
url = "tcp://localhost:61616"
app = myapp.MyApp(url)

iniator = quickfix.SocketInitiator(app,store,cfg,log,msg)
#iniator = quickfix.SocketAcceptor(app,store,cfg,log,msg)
#iniator = quickfix.Initiator()
iniator.start()


def webapp(background=False):
    """ """
    # webapp
    from rocket import Rocket
    from webapp import app as webapp

    webapp.app.config['session'] = cfg

    # set up wsgi server 
    server = Rocket(('127.0.0.1', default_cfg.port), 'wsgi', {"wsgi_app":webapp.app})
    server.start(background=background)

# import autoreload
# autoreload.main(webapp)

webapp()
# #
from code import InteractiveConsole
a = InteractiveConsole(locals())
a.interact("->")

iniator.stop()
server.stop()

from java.lang import System
System.exit(0)