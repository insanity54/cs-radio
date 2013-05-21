#!/usr/bin/python3

# AUTHOR
# Hi, my name is Chris Grimmett and I'm a geek.
# I love to work on creative projects.
# Hire me!
# www.grimtech.net

# DESCRIPTION
# Plays sounds on your speakerz


# INCLUDES
import os.path
import signal
import sys
import threading
import pygame.mixer
import pygame.time
import pygame.event

def main():

    # CONFIG
    sound_dir = 'sounds'
    start_sounds = ['com_go.wav', 'moveout.wav', 'locknload.wav']  # list of sounds to randomly be selected for game start sound
    tx_delay = 350  # a small delay to wait after keying the radio, before sending audio

    # INIT
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    time = pygame.time
    pygame.mixer.init()

    # FUNCTIONS
    def signal_handler(signal, frame):
        "promptly quits the program if Ctrl+C is received"
        print ('SIGINT received, exiting.')
        # release any PTT keys incase we were transmitting
        # @todo release both PTT keys
        sys.exit(0)

    def file_path(sound_name):
        "accepts soundfile by name only, and returns full path"
        path = os.path.join(main_dir,
                            sound_dir,
                            sound_name)
        return path

    def start_game(start_sounds):
        "picks a random start sound and transmits it on all channels"
        from random import choice
        transmit_all(choice(start_sounds))



    #
    # EXPERIMENTAL
    #

    def next_sound(queue):
        "returns the sound_name of the next sound in queue"
        if queue:
            # if queue has sounds in it, return first in queue
            return queue.pop(0)

    def play_sound(team, queue):
        C_CHANNEL = 0
        T_CHANNEL = 1


        if queue:
            # if there is a sound in the queue
            # play first sound in queue
            sound = pygame.mixer.Sound(file_path(next_sound(queue)))


            if team == 'c':
                channel = pygame.mixer.Channel(C_CHANNEL)
                #channel = sound.play()  # @todo problem, this overrides the above line
                channel.play(sound)
                channel.set_endevent(END_CSOUND_EVENT)
                channel.set_volume(1, 0)

            elif team == 't':
                channel = pygame.mixer.Channel(T_CHANNEL)
                channel.play(sound)
                channel.set_endevent(END_TSOUND_EVENT)
                channel.set_volume(0, 1)

            return channel

    def key_state(team, state):
        "keys or unkeys the radio PTT button for the specified team"
        # @todo use this method(?)
        
        def key(team):
            "keys the specified radio"

            if (team == 'c'):
                # @todo key the c radio ptt                
                print(" key c")
                

            elif (team == 't'):
                # @todo key the t radio ptt
                print(" key t")

            else:
                print("E-ROR:  team letter not in range")

        def rkey(team):
            "releases the ptt key for the specified radio"

            if (team == 'c'):
                # @todo release the c radio ptt
                print(" key c")

            elif (team == 't'):
                # @todo release the c radio ptt
                print(" key t")

            else:
                print("ERROr: team letter not in rainj")

        states = { 0 : rkey(team),
                   1 : key(team),
                 }

        if state in states:
            states[state]

        else:
            print("EERROR: supplied poop sca doop was not in the loop." % (state))


    pygame.init()

    END_CSOUND_EVENT = pygame.USEREVENT + 0
    END_TSOUND_EVENT = pygame.USEREVENT + 1
    PTT_C_EVENT = pygame.USEREVENT + 2
    PTT_T_EVENT = pygame.USEREVENT + 3


    signal.signal(signal.SIGINT, signal_handler) # call this if SIGINT (Ctrl+C)
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    ptt_c_timer = pygame.time.set_timer(PTT_C_EVENT, 0)  # create de-activated timer events
    ptt_t_timer = pygame.time.set_timer(PTT_T_EVENT, 0)

    # Create a queue list
    #c_queue = ['letsgo.wav', 'rescued.wav']
    #t_queue = ['locknload.wav', 'escaped.wav']

    # key the radios
    

    # play the first two sounds    
    #c_channel = play_sound('c', c_queue)
    #t_channel = play_sound('t', t_queue)

    
    # Event loop
    running = 1
    while (running == 1):
        # if sound has been queued
            # while sound is still playing
                # play sound
            # un-key
            # play next sound


        # Watch for events
        events = pygame.event.get()
        if events:
            for event in events:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    print('q key pressed')
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    if c_channel and t_channel:
                        print("c sound playing is: %s" % c_channel.get_sound())
                        print("t sound playing is: %s" % t_channel.get_sound().stop())



                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    # key c is pressed
                    # @todo this is what is triggered on c channel by significant input from xbee
     
                    print('c')          # debug message


                    # if a sound is playing
                    #     queue the sound
                    # 
                    # else if a sound is not playing
                    #     key the radio
                    #     wait time set by tx_delay
                    #     queue the sound
                    #     play the queue
                    #     unkey the radio when sound is done playing

                    if c_channel:
                        if c_channel.get_busy():
                            # if a sound is playing
                            print(' c is busy, sound queued')
                            c_queue.append('blow.wav')                                  # queue the sound -- @todo this sound will be determined by command received from xbee

                        else:
                            # if a sound is not already playing, key up the radio and start delay timer
                            print(' c KEY')                                             # @todo key the radio
                            ptt_c_timer = pygame.time.set_timer(PTT_C_EVENT, tx_delay)  # create timer event with pre-determined ptt timer (set in config)
                        

                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    print('t')

                    if t_channel:

                        if t_channel.get_busy():
                            # if a sound is playing
                            print(' t is busy, sound queued')
                            t_queue.append('blow.wav')                                  # queue the sound -- @todo this sound will be determined by command received from xbee

                        else:
                            # if a sound is not already playing, key up the radio and start delay timer
                            print(' t KEY')                                             # @todo key the radio
                            ptt_t_timer = pygame.time.set_timer(PTT_T_EVENT, tx_delay)  # create timer event with pre-determined ptt timer (set in config)

                        
                elif (event.type == END_CSOUND_EVENT): # and event.code == 0:
                    # when c sound is done playing

                    # if there is a sound in queue
                    #     play the queued sound
                    #
                    # else there is not another sound in queue
                    #     unkey the radio

                    if c_queue:
                        # if there is a sound in queue
                        #print('there is a sound in c queue')
                        print(' c send sound')
#                        c_channel = pygame.mixer.find_channel()
                        c_channel = play_sound('c', c_queue)

                    else:
                        # there is not another sound in queue
                        print(' c UNKEY')                                             # @todo unkey the radio


                elif (event.type == END_TSOUND_EVENT):

                    if t_queue:
                        # if there is a sound in queue
                        #print('there is a sound in t queue')
                        print(' t send sound')
                        t_channel = play_sound('t', t_queue)

                    else:
                        # there is not another sound in queue
                        print(' t UNKEY')                                             # @todo unkey the radio


                elif (event.type == PTT_C_EVENT):
                    # ptt timer has expired
                    
                    # disable the ptt timer so it doesn't trigger again
                    ptt_c_timer = pygame.time.set_timer(PTT_C_EVENT, 0)

                    # start playing
                    print(' c send sound')
                    c_queue.append('rounddraw.wav')

                    c_channel = play_sound('c', c_queue)


                elif (event.type == PTT_T_EVENT):
                    # ptt timer expired, play sound
                    ptt_t_timer = pygame.time.set_timer(PTT_T_EVENT, 0)               # kill timer so it doesn't trigger again                    

                    print(' t send sound')
                    t_queue.append('rounddraw.wav')
                    t_channel = play_sound('t', t_queue)




        clock.tick()
        time.wait(0) # lessens CPU usage




#    transmit(t, 'c4_beep1.wav', async)
    #transmit_all('terwin.wav')




# RUNRAR
if __name__ == '__main__': main()
