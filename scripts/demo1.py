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



def demo(stop_event):
    import random
    import os
    import json


    def get_latest_emotion():
        import requests
        try:
            response = requests.get('http://127.0.0.1:5000/get_emotion')
            if response.status_code == 200:
                data = response.json()
                print(data)
                print(data.get('emotion'))
                return data.get('emotion')
        except Exception as e:
            print("Error fetching emotion data:" + str(e))
        return None

    while True:
        im.init()
   
        shared_dict = {"restart_interaction":"Yes"}
        shared_dict = {"is_clear":"No"}
        shared_dict = {"playagain":"No"}
        shared_dict = {"select_level":"Easy"}
        shared_dict = {"remember":"No"}
        #restart_answer = 'Yes' #if this is No, restart the interaction

        pepper_cmd.robot.hello()

        bool_old_user = False
        bool_play_tutorial = True
        #restart_program = False


        if bool_old_user:
            #se utente in memoria(riconoscimento facciale), "welcome back, do you want to learn more?" 
            def animation():
                pepper_cmd.robot.welcomeback()
            def tablet(shared_dict):
                shared_dict["restart_interaction"] = str(im.ask('welcome_back',timeout=800))

            animation_thread = threading.Thread(target=animation)
            tablet_thread = threading.Thread(target=tablet, args=(shared_dict,))
            animation_thread.start()
            tablet_thread.start()
            animation_thread.join()
            tablet_thread.join()

            if shared_dict["restart_interaction"] == 'No':
                continue
        
            #emotions = ['neutral', 'happy', 'sad',  'angry', 'fearful', 'disgusted', 'surprised']
            user_emotion = str(get_latest_emotion())

            #chiede "do you remember how to play?" DA CONTROLLAREEEEEEEEEEEEEEEEEEE
            def animation():
                pepper_cmd.robot.think() #forse cambiare?
            def tablet(shared_dict):
                shared_dict["remember"] = str(im.ask('tutorial_remember',timeout=800))

            animation_thread = threading.Thread(target=animation)
            tablet_thread = threading.Thread(target=tablet, args=(shared_dict,))
            animation_thread.start()
            tablet_thread.start()
            animation_thread.join()
            tablet_thread.join()

            if shared_dict["remember"] == 'Yes':
                bool_play_tutorial = False

        if bool_play_tutorial and not bool_old_user:

            pepper_cmd.robot.comehere()
            time.sleep(1)

            def animation():
                pepper_cmd.robot.introduceMarco()
                time.sleep(1)
            def tablet():
                im.execute('show_marco')
            
            animation_thread = threading.Thread(target=animation)
            tablet_thread = threading.Thread(target=tablet)
            animation_thread.start()
            tablet_thread.start()
            animation_thread.join()
            tablet_thread.join()
            
            pepper_cmd.robot.intro()

            def animation():
                pepper_cmd.robot.very_short_explain()
            def say_tablet():
                user_answer = im.ask('tutorial_intro')

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()
            

        while(bool_play_tutorial):

            import threading
        
            def animation():
                pepper_cmd.robot.explain_1()
            def say_tablet():
                user_answer = im.ask('tutorial_show_1')

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()

            #animazione corta
            def animation():
                pepper_cmd.robot.explain_short()
            def say_tablet():
                user_answer = im.ask('tutorial_show_2') 

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()

            def animation():
                pepper_cmd.robot.explain_2()
            def say_tablet():
                user_answer = im.ask('tutorial_select')

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()
            

            #animazione lunga
            def animation():
                pepper_cmd.robot.explain_1()
            def say_tablet():
                user_answer = im.ask('tutorial_time')

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()
            
            
            #animazione lunga
            def animation():
                pepper_cmd.robot.explain_2()
            def say_tablet():
                user_answer = im.ask('tutorial_points')  # wait for button

            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet)
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()
  

            #animazione domanda
            def animation():
                pepper_cmd.robot.question()
            def say_tablet(shared_dict):
                shared_dict["is_clear"] = str(im.ask('tutorial_is_clear',timeout=800)) # wait for buttonuser_answer = im.ask('welcome', timeout=800)  # wait for button 
        
            animation_thread = threading.Thread(target=animation)
            say_tablet_thread = threading.Thread(target=say_tablet, args=(shared_dict,))
            animation_thread.start()
            say_tablet_thread.start()
            animation_thread.join()
            say_tablet_thread.join()

            if shared_dict["is_clear"] == 'Yes':
                bool_play_tutorial = False


        #seleziona livello
        def animation():
            pepper_cmd.robot.very_short_explain_2()
        def say_tablet(shared_dict):
            shared_dict["select_level"] = str(im.ask('level',timeout=800)) # wait for buttonuser_answer = im.ask('welcome', timeout=800)  # wait for button 
    
        animation_thread = threading.Thread(target=animation)
        say_tablet_thread = threading.Thread(target=say_tablet, args=(shared_dict,))
        animation_thread.start()
        say_tablet_thread.start()
        animation_thread.join()
        say_tablet_thread.join()

        # inizializzazione variabili per gioco
        #full_alphabet = [l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] #alfabeto
        points = 0  #punti
        if shared_dict["select_level"] == "Easy":
            time_countdown = 30 
            max_rounds = 5
        elif shared_dict["select_level"] == "Medium":
            time_countdown = 20 
            max_rounds = 10
        else:
            time_countdown = 10 
            max_rounds = 20    
        
        alphabet = [l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'] #alfabeto

        
        n_repetition_letter = dict(zip(alphabet, [0.0]*26))
        n_correct_letter = dict(zip(alphabet, [0.0]*26))
        letter_correctness_perc = dict(zip(alphabet, [1.0]*26)) # vale 0 se sempre corretto, 1 se sempre sbagliato e/o mai chiesto
        shown = [] #lettere gia' mostrate

        # lettera a caso 
        letter = random.choice(alphabet)

        #mostro la lettera se non l'ha mai vista
        if letter not in shown:
            im.execute(letter+'_show')
            shown.append(letter)

        #qua non ho fatto animazione, potrebbe essere un problema thread + append (usare shared dict? ma non vale la pena)

        # Display the quiz and wait for the user's answer
        correct_answer = False
        #user_answer = im.ask(letter, timeout=100)  # Displays the quiz action and waits for user input
        n_tentativi = 0

        first_try = True 

        rounds = 0
        while(rounds < max_rounds):
            
            user_answer = im.ask(letter, timeout = 100*time_countdown)  #tempo varia con difficolta' #QUA CHIEDE LA LETTERA MA VALE LA PENA DI METTERE ANIMAZIONE??
            print(n_repetition_letter[letter])
            n_repetition_letter[letter] +=1.0
            
            if user_answer == letter:
                # Correct answer
                
                def animation():
                #animation_strong = pepper_cmd.robot.strong()
                #animation_highfive = pepper_cmd.robot.highfive()

                    correct_animation = random.choice([pepper_cmd.robot.strong, pepper_cmd.robot.highfive])
                    correct_animation()

                def say_tablet():
                    im.execute('correct')

                animation_thread = threading.Thread(target=animation)
                say_tablet_thread = threading.Thread(target=say_tablet)
                animation_thread.start()
                say_tablet_thread.start()
                animation_thread.join()
                say_tablet_thread.join()

                #Se corretto aggiorno n_correct_letter e letter_correctness_perc
                n_correct_letter[letter] +=1.0
                letter_correctness_perc[letter] = 1- n_correct_letter[letter]/n_repetition_letter[letter]
                correct_answer = True

                rounds += 1
                if first_try:
                    points += 1 #incremento punteggio se indovinata al primo tentativo
                    im.executeModality('TEXT_story', 'Wow! '+ str(points)+ (' points!' if points >1 else ' point!'))
                    im.executeModality('TTS', 'Wow! '+ str(points)+ (' points!' if points >1 else ' point!'))
                    if time_countdown > 1:
                        time_countdown -= 1

                #mostro nuovo quiz
                p = random.random() # variabile aleatoria
                #con probabilita 0.5, viene chiesta lettera piu difficile, altrimenti lettera random
                if p < 0.5:
                    letter = max(letter_correctness_perc, key=letter_correctness_perc.get)
                else:
                    letter = random.choice(alphabet)
                if letter not in shown:
                    im.execute(letter+'_show')
                    shown.append(letter)
                #user_answer = im.ask(letter, timeout=100)  # Displays the quiz action and waits for user input
                n_tentativi = 0
                first_try = True

            elif user_answer in alphabet:
                # Wrong answer
                def animation():
                    pepper_cmd.robot.wrong()

                def say_tablet():
                    im.execute('wrong')

                animation_thread = threading.Thread(target=animation)
                say_tablet_thread = threading.Thread(target=say_tablet)
                animation_thread.start()
                say_tablet_thread.start()
                animation_thread.join()
                say_tablet_thread.join()

                
                first_try = False
                n_tentativi +=1

                #Check if angry
                user_emotion = str(get_latest_emotion())
                if user_emotion =='angry':
                    
                    def animation():
                        pepper_cmd.robot.emotion_angry()
                    def say_tablet():
                        action = random.choice(['angry1', 'angry2', 'angry3', 'angry4'])
                        im.execute(action)

                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()

                #Check if sad
                elif user_emotion =='sad':

                    def animation():
                        pepper_cmd.robot.emotion_sad()
                    def say_tablet():
                        action = random.choice(['sad1', 'sad2', 'sad3', 'sad4'])
                        im.execute(action)

                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()


                #altrimenti frase di incoraggiamento generica
                else:

                    def animation():
                        pepper_cmd.robot.generic_encouraging()
                    def say_tablet():
                        action = random.choice(['wrong_reaction1', 'wrong_reaction2', 'wrong_reaction3', 'wrong_reaction4'])
                        im.execute(action)

                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()


                # con probabilita' prob chiedo se vuole fare pausa
                prob = 0.3
                if random.random() < prob:
                    
                    def animation():
                        pepper_cmd.robot.explain_short()
                    def say_tablet():
                        im.ask('pause')

                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()

                # dopo 3 tentativi errati mostro di nuovo la lettera
                if n_tentativi%3 ==0:
                    
                    def animation():
                        pepper_cmd.robot.very_short_explain()
                    def say_tablet():
                        im.execute('review')

                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()
                    
                    im.execute(letter+'_show')
                    time_countdown += 1       
            else:
                # No valid input received
                
                #QUESTO QUANDO ACCADE? AL TIMEOUT? ###########################################
                #DA TESTARE
                def animation():
                    pepper_cmd.robot.think()
                def say_tablet():
                    im.executeModality('TEXT_story', 'I did not understand. Please try again.')
                    im.executeModality('TTS', 'I did not understand. Please try again.')

                animation_thread = threading.Thread(target=animation)
                say_tablet_thread = threading.Thread(target=say_tablet)
                animation_thread.start()
                say_tablet_thread.start()
                animation_thread.join()
                say_tablet_thread.join()

                


            #user_answer = im.ask(letter)   
            
            ########## ma funziona questo timeout????######
            if (user_answer=='timeout'):
                
                def animation():
                    pepper_cmd.robot.goodbye()
                def say_tablet():
                    im.execute('goodbye')
                
                animation_thread = threading.Thread(target=animation)
                say_tablet_thread = threading.Thread(target=say_tablet)
                animation_thread.start()
                say_tablet_thread.start()
                animation_thread.join()
                say_tablet_thread.join()

                break

            if rounds == max_rounds:
                if points > max_rounds/2:

                    im.execute('victory')
                    im.executeModality('TEXT_story', 'Wow! You scored '+str(points)+' out of '+str(max_rounds)+' points!')
                    im.executeModality('TTS', 'Wow! You scored '+str(points)+' out of '+str(max_rounds)+' points!')
                    
                    pepper_cmd.robot.headbang()
                    
                    

                else:
        
                    im.execute('lost')
                    im.executeModality('TEXT_story',  'You scored '+str(points)+' out of '+str(max_rounds)+' points. Better luck next time!')
                    im.executeModality('TTS', 'You scored '+str(points)+' out of '+str(max_rounds)+' points. Better luck next time!')

                    pepper_cmd.robot.lostgame()

                #animazione domanda
                def animation():
                    pepper_cmd.robot.question()
                def say_tablet(shared_dict):
                    shared_dict["playagain"] = str(im.ask('play_again',timeout=800)) # wait for buttonuser_answer = im.ask('welcome', timeout=800)  # wait for button 
            
                animation_thread = threading.Thread(target=animation)
                say_tablet_thread = threading.Thread(target=say_tablet, args=(shared_dict,))
                animation_thread.start()
                say_tablet_thread.start()
                animation_thread.join()
                say_tablet_thread.join()

                if shared_dict["playagain"] == 'Yes':
                    rounds = 0
                    n_tentativi = 0
                    points= 0 
                    first_try = True 
                else:
                    def animation():
                        pepper_cmd.robot.goodbye()
                    def say_tablet():
                        im.execute('goodbye')
                    
                    animation_thread = threading.Thread(target=animation)
                    say_tablet_thread = threading.Thread(target=say_tablet)
                    animation_thread.start()
                    say_tablet_thread.start()
                    animation_thread.join()
                    say_tablet_thread.join()
            
        im.init()  # Reset the interface


if __name__ == "__main__":
    mws = ModimWSClient()
    try:
        import qi
        from getzone import EngagementZoneMonitor

        session = qi.Session()
        session.connect("tcp://" + os.getenv('PEPPER_IP', '127.0.0.1') + ":" + str(9559))

        # Initialize the EngagementZoneMonitor
        zone_monitor = EngagementZoneMonitor(session)
        zone_monitor.start_monitoring()
    except Exception as e:
        print("Cannot start qi session or EngagementZoneMonitor")
        sys.exit(1)

    # Wait until someone is detected in Zone 1
    print("Waiting for someone to enter Zone 1...")
    try:
        while True:
            current_zones = zone_monitor.get_current_zones()
            if current_zones[0] > 0:
                print("Person detected in Zone 1.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        zone_monitor.stop_monitoring()
        sys.exit(0)

    # Clean up
    zone_monitor.stop_monitoring()
    print("Finished")

    # Local execution
    mws.setDemoPathAuto(__file__)
    # Remote execution (uncomment and set the correct path if needed)
    # mws.setDemoPath('<ABSOLUTE_DEMO_PATH_ON_REMOTE_SERVER>')

    # Create a stop event
    stop_event = threading.Event()

    # Create and run the demo interaction in a separate daemon thread
    interaction_thread = threading.Thread(target=mws.run_interaction, args=(demo,
    ))
    interaction_thread.setDaemon(True)
    interaction_thread.start()

    try:
        while interaction_thread.is_alive():
            interaction_thread.join(timeout=1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Stopping program.")
        stop_event.set()
        # Since the thread is daemon, the program will exit even if it doesn't terminate immediately
        print("Program terminated.")