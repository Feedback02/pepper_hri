import sys
import time
import os
import requests

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

# Import MODIM client
import ws_client
from ws_client import *

def get_latest_emotion():
    try:
        response = requests.get('http://127.0.0.1:5000/get_emotion')
        if response.status_code == 200:
            data = response.json()
            return data.get('emotion')
    except Exception as e:
        print(f"Error fetching emotion data: {e}")
    return None


def interaction():
    im.init()
    #im.robot.dance()
    im.execute('song1')
    user_answer = im.ask('welcome', timeout=800)  # wait for button

    
    #im.ask('tutorial')
    
    # Display the quiz and wait for the user's answer
    #im.ask('quiz')  # Displays the quiz action and waits for user input

    correct_answer = False
    user_answer = im.ask('quiz') # Wait for up to 20 seconds
    print("User answered:", user_answer)
    
    
    while(correct_answer == False):
        if user_answer == 'A':
            # Correct answer
            im.execute('correct')
            correct_answer = True
        elif user_answer in ['B', 'D']:
            # Wrong answer
            im.execute('wrong')
            # Re-display the quiz question
            user_answer = im.ask('quiz')
        else:
            # No valid input received
            im.executeModality('TEXT_default', 'I did not understand. Please try again.')
            im.executeModality('TTS', 'I did not understand. Please try again.')
    
    # After correct answer, execute goodbye action
    if (a!='timeout'):
    	im.execute('goodbye')
    	
    im.init()  # Reset the interface


    
if __name__ == "__main__":
    mws = ModimWSClient()
    
    # Local execution
    mws.setDemoPathAuto(__file__)
    # Remote execution (uncomment and set the correct path if needed)
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(interaction)

