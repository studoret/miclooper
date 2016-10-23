# *Micro looper* package

These python scripts use command-line sound recorder for ALSA soundcard driver (arecord) and mplayer to play records.
The package provides a MicLooper class that allows to record a track and play it in loop.
It provides also the milo.py application that allows to create multi track and loops.

<br/>

Requirements
===================================================

    python -m pip install setuptools

Setup
===================================================

Go to the miclooper parent directory.

    sudo python setup.py install


Uninstall
===================================================

Go to the miclooper parent directory.

    sudo python setup.py install --record files.txt
    sudo bash -c 'cat files.txt | xargs rm ; rm files.txt'


Modules
===================================================

- ***miclooper.py***

MicLooper state machine.



        ┌─────────────┐   key    ┌─────────┐   key    ┌───────────┐   key    ┌───────┐
        │readyToRecord│--event-->│recording│--event-->│readyToPlay│--event-->│playing│
        └─────────────┘          └─────────┘          └───────────┘          └───────┘
                                                           ^-------key event-----┘


        >>> from miclooper.miclooper import MicLooper
        >>> mic_looper = MicLooper("test.raw", "looper_1", "hw:0,0")
        looper_1 readyToRecord
        >>> # start record
        >>> mic_looper.on_event_key_pressed()
        looper_1 recording
        >>> # stop record
        >>> mic_looper.on_event_key_pressed()
        looper_1 readyToPlay
        >>> # play record in loop from start
        >>> mic_looper.on_event_key_pressed()
        looper_1 playing
        >>> # stop playing
        >>> mic_looper.on_event_key_pressed()
        looper_1 readyToPlay
        >>> # play record in loop from start
        >>> mic_looper.on_event_key_pressed()
        looper_1 playing
        >>> # quit
        >>> mic_looper.on_event_quit_request()
        looper_1 quitting

- ***milo.py***

Sample application using miclooper.py with ncurses interface.
For example: the follwowing command will use 4 instances of MicLooper state machines with '1' is the command key for the 1st one, '2' for the 2nd and so on.
The records will be stored in ./Records/rec_time/rec_1.raw, ./Records/rec_time/rec_2.raw ...

    ./milo.py -p "Records" -D "hw:0,0" -k "1234"

For my foot pedal board made with 4 wall switches linked to a usb keyboard controller, where switches are respectively binded to the 'p','o','a' and 'i' keys :

    ./milo.py -p "Records" -D "hw:0,0" -k "poai"

- ***utils/statemachine.py***

Parent class of the MicLooper.

- ***utils/task.py***

Used to launch arecord and mplayer.
