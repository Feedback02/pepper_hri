#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use run Method"""

import qi
import argparse
import sys


def main(session):
    """
    This example uses the run method.
    """
    # Get the service ALAnimationPlayer.

    tts_service = session.service("ALTextToSpeech")
    animated_speech_service = session.service("ALAnimatedSpeech")

    # Set language and parameters
    tts_service.setLanguage("English")
    configuration = {"bodyLanguageMode": "contextual"}

    # Have the robot speak with automatic gestures
    animated_speech_service.say("Hello, I am Pepper.", configuration)
    animated_speech_service.say("Hellasd asd asd asd asda sd asda sda d d  ds dsdsd asd as das do, I am Pepper.", configuration)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=44009,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)