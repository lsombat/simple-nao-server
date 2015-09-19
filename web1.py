# -*- encoding: UTF-8 -*- 

import sys
import time
import tornado.ioloop
import tornado.web
import os.path
#import json

from naoqi import ALProxy

class MainHandler(tornado.web.RequestHandler):
    def get(self):
		self.render("index.html", messages=None)
       
class NaoCMD(tornado.web.RequestHandler):
    def post(self):
		naoip=self.get_argument('ip','')
		naoport= self.get_argument('port','')
		ncmd= self.get_argument('cmd','')	
		if(ncmd=='walk'):
			motion = ALProxy("ALMotion", str(naoip), int(naoport))
			tts    = ALProxy("ALTextToSpeech", str(naoip), int(naoport))
			motion.moveInit()
			motion.post.moveTo(0.5, 0, 0)
			tts.say("I'm walking")
			self.write("DONE!")
		if(ncmd=='talk'):
			naoip=self.get_argument('ip','')
			naoport= self.get_argument('port','')	
			talk=self.get_argument('nspeak','')	
			if (talk==''):
				talk="Hello, I am Nao"
			animatedSpeechProxy = ALProxy("ALAnimatedSpeech", str(naoip), int(naoport))
			# set the local configuration
			configuration = {"bodyLanguageMode":"contextual"}
			# say the text with the local configuration
			animatedSpeechProxy.say(str(talk), configuration)	
			self.write("DONE!")	
		if(ncmd=='dance'):
			naoip=self.get_argument('ip','')
			naoport= self.get_argument('port','')	
			behaviorName=str(self.get_argument('ndance',''))	
			managerProxy = ALProxy("ALBehaviorManager", str(naoip), int(naoport))
			getBehaviors(managerProxy)
			launchAndStopBehavior(managerProxy, behaviorName)
			defaultBehaviors(managerProxy, behaviorName)
			self.write("DONE!")

def getBehaviors(managerProxy):
  ''' Know which behaviors are on the robot '''

  names = managerProxy.getInstalledBehaviors()
  print "Behaviors on the robot:"
  print names

  names = managerProxy.getRunningBehaviors()
  print "Running behaviors:"
  print names

def launchAndStopBehavior(managerProxy, behaviorName):
  ''' Launch and stop a behavior, if possible. '''

  # Check that the behavior exists.
  if (managerProxy.isBehaviorInstalled(behaviorName)):

    # Check that it is not already running.
    if (not managerProxy.isBehaviorRunning(behaviorName)):
      # Launch behavior. This is a blocking call, use post if you do not
      # want to wait for the behavior to finish.
      managerProxy.post.runBehavior(behaviorName)
      time.sleep(0.5)
    else:
      print "Behavior is already running."

  else:
    print "Behavior not found."
    return

  names = managerProxy.getRunningBehaviors()
  print "Running behaviors:"
  print names

  # Stop the behavior.
  #if (managerProxy.isBehaviorRunning(behaviorName)):
  #  managerProxy.stopBehavior(behaviorName)
  #  time.sleep(1.0)
  #else:
  #  print "Behavior is already stopped."

  names = managerProxy.getRunningBehaviors()
  print "Running behaviors:"
  print names

def defaultBehaviors(managerProxy, behaviorName):
  ''' Set a behavior as default and remove it from default behavior. '''

  # Get default behaviors.
  names = managerProxy.getDefaultBehaviors()
  print "Default behaviors:"
  print names

  # Add behavior to default.
  managerProxy.addDefaultBehavior(behaviorName)

  names = managerProxy.getDefaultBehaviors()
  print "Default behaviors:"
  print names

  # Remove behavior from default.
  managerProxy.removeDefaultBehavior(behaviorName)

  names = managerProxy.getDefaultBehaviors()
  print "Default behaviors:"
  print names

		


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
			(r"/nao",NaoCMD),
        ]
        settings = dict(
            debug=True,            
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
