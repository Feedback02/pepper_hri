import sys
import time
import os

import qi

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *


begin()

#pepper_cmd.robot.headPose(0.3,1.0,0.7)
#pepper_cmd.robot.hello()

#pepper_cmd.robot.intro()
#pepper_cmd.robot.showTablet()
#pepper_cmd.robot.say('ciao')

#pepper_cmd.robot.hello()
#pepper_cmd.robot.think()
#pepper_cmd.robot.pepperVictory()
#pepper_cmd.robot.strong()
#pepper_cmd.robot.highfive()
#pepper_cmd.robot.sad()
#pepper_cmd.robot.comehere()
pepper_cmd.robot.sad2()


end()

