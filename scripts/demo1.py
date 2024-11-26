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
        pass #print(f"Error fetching emotion data: {e}")
    return None


def interaction():
    import random 
    im.init()
    #im.robot.dance()
    #im.execute('song1')
    # user_answer = im.ask('welcome', timeout=200)  # wait for butto
    bool_old_user = True
    bool_play_tutorial = True


    if bool_old_user:
        user_answer = im.ask('tutorial_remember',timeout=800)  # wait for buttonuser_answer = im.ask('welcome', timeout=800)  # wait for button
        if user_answer == 'Yes':
            bool_play_tutorial = False

    if bool_play_tutorial:
        user_answer = im.ask('tutorial_intro') 

    while(bool_play_tutorial):
         
        user_answer = im.ask('tutorial_show_1')
        user_answer = im.ask('tutorial_show_2')  
        user_answer = im.ask('tutorial_select')  
        user_answer = im.ask('tutorial_time')
        user_answer = im.ask('tutoria_points')  # wait for button
        user_answer = im.ask('tutorial_is_clear',timeout=800)  # wait for buttonuser_answer = im.ask('welcome', timeout=800)  # wait for button
        if user_answer == 'Yes':
            bool_play_tutorial = False
    
    points = 0
    alphabet = [l for l in 'ABCDEFGJKLMNOPQRSTUVWXYZ']

    
    letter = random.choice(alphabet)

    # Display the quiz and wait for the user's answer
    correct_answer = False
    user_answer = im.ask(letter)  # Displays the quiz action and waits for user input
    
    
    while(True):
        if user_answer == letter:
            # Correct answer
            im.execute('correct')
            correct_answer = True
            letter = random.choice(alphabet)
            user_answer = im.ask(letter)  # Displays the quiz action and waits for user input
        elif user_answer in alphabet:
            # Wrong answer
            im.execute('wrong')
            # Re-display the quiz question
            user_answer = im.ask(letter)
        else:
            # No valid input received
            im.executeModality('TEXT_default', 'I did not understand. Please try again.')
            im.executeModality('TTS', 'I did not understand. Please try again.')
        
    # After correct answer, execute goodbye action
        if (user_answer=='timeout'):
            im.execute('goodbye')    
    	
    im.init()  # Reset the interface


    
if __name__ == "__main__":
    mws = ModimWSClient()
    
    # Local execution
    mws.setDemoPathAuto(__file__)
    # Remote execution (uncomment and set the correct path if needed)
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    mws.run_interaction(interaction)

