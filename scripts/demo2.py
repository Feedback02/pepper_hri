import sys
import time
import os
import requests
import random
import threading

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
    #sys.path.insert(0, os.getenv('PEPPER_TOOLS')+'/cmd_server')
except Exception as e:
    print("Please set MODIM_HOME environment variable to MODIM folder.")
    sys.exit(1)

# Add the path to the `pepper` folder
pepper_path = "/home/lattinone/src/Pepper/pepper_tools/cmd_server"
sys.path.insert(0, pepper_path)

# Import `pepper_cmd`
import pepper_cmd

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

def demo():
    global continue_interaction
    import random
    import os
    im.init()

    # Initialize variables for interaction flow
    continue_interaction = True
    bool_old_user = True
    bool_play_tutorial = True

    while continue_interaction:
        pepper_cmd.robot.hello()

        if bool_old_user:
            def animation():
                pepper_cmd.robot.welcomeback()
            
            def tablet():
                global continue_interaction
                user_answer = im.ask('welcome_back', timeout=800)
                if user_answer == 'No':
                    im.execute('goodbye')
                    continue_interaction = False
            
            animation_thread = threading.Thread(target=animation)
            tablet_thread = threading.Thread(target=tablet)
            animation_thread.start()
            tablet_thread.start()
            animation_thread.join()
            tablet_thread.join()

            if not continue_interaction:
                break  # Exit the loop to restart the demo

            user_answer = im.ask('tutorial_remember', timeout=800)
            if user_answer == 'Yes':
                bool_play_tutorial = False

        if bool_play_tutorial:
            user_answer = im.ask('tutorial_intro')

        while bool_play_tutorial:
            user_answer = im.ask('tutorial_show_1')
            user_answer = im.ask('tutorial_show_2')
            user_answer = im.ask('tutorial_select')
            user_answer = im.ask('tutorial_time')
            user_answer = im.ask('tutorial_points')
            user_answer = im.ask('tutorial_is_clear', timeout=800)
            if user_answer == 'Yes':
                bool_play_tutorial = False

        # Quiz interaction loop
        points = 0
        alphabet = [l for l in 'ABCDEFGJKLMNOPQRSTUVWXYZ']
        letter = random.choice(alphabet)

        correct_answer = False
        user_answer = im.ask(letter)  # Display the quiz and wait for the user's answer

        while True:
            if user_answer == letter:
                # Correct answer
                im.execute('correct')
                correct_answer = True
                letter = random.choice(alphabet)
                user_answer = im.ask(letter)
            elif user_answer in alphabet:
                # Wrong answer
                im.execute('wrong')
                user_answer = im.ask(letter)
            else:
                # No valid input received
                im.executeModality('TEXT_default', 'I did not understand. Please try again.')
                im.executeModality('TTS', 'I did not understand. Please try again.')

            if user_answer == 'timeout':
                im.execute('goodbye')
                continue_interaction = False
                break

        if not continue_interaction:
            break  # Exit the loop to restart the demo

    im.init()  # Reset the interface


if __name__ == "__main__":
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    try:
        # Loop to restart the demo after it ends
        while True:
            mws.run_interaction(demo)
    except KeyboardInterrupt:
        print("\nExiting MODIM interaction. Goodbye!")
        sys.exit(0)
    # Loop to restart the demo after it ends
    #while True:
    #    mws.run_interaction(demo)

#il problema con questa che se premo ctrl+c non si stoppa,
#premo due volte e va comunque avanti, ho provato a fare ctlr+c
#su modim e non esce da la. per il resto fa