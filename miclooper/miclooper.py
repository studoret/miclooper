#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
miclooper - Micro looper state machine

This python script uses command-line sound recorder for ALSA soundcard driver (arecord) and mplayer to play records.

############
Copyright 2016 Stephane Tudoret

This file is part of miclooper, a python micro looper application.

miclooper is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

miclooper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with miclooper.  If not, see http://www.gnu.org/licenses/.

"""
from utils import statemachine
from utils import task

class Recorder(task.Task):
    """
    Recorder task.
    It uses command-line sound recorder for ALSA soundcard driver (arecord)

    :Args:

        file_name : string
            Name of the output record file

        device : string
            Used to select audio device for example "hw:1,0"
            You can use "arecord -l" to list devices

    """
    def __init__(self, file_name, device, debug=False):
        super(Recorder, self).__init__([
            '/usr/bin/arecord',
            '-f', 'S16_LE',
            '-r', '48000',
            '-c', '2',
            '-D', device,
            file_name], debug)

class Player(task.Task):
    """
    Task to play record in loop.
    It uses command-line mplayer instead of aplayer.
    Instead, aplayer does not support loop directly.

    :Args:

        file_name : string
            Name of the record file

    """
    def __init__(self, file_name, debug=False):
        super(Player, self).__init__(['/usr/bin/mplayer', '-loop', '0', file_name], debug)

class MicLooper(statemachine.StateMachine):
    """
    MicLooper state machine.

    :Args:

        file_name : string
            Name of the record file

        tag : string
            Used to prefix state printing

        device : string
            Used to select audio device for example "hw:1,0"
            You can use "arecord -l" to list devices

        debug : boolean
            If true then show stderr of arecord and mplayer
            else hide stderr

    :Example:
 
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

    """
    def __init__(self, file_name, tag, device, debug=False):
        self._tag = tag
        self._event_start = statemachine.Event("Start")
        self._event_key = statemachine.Event("KeyPressed")
        self._event_quit = statemachine.Event("QuitRequest")
        self._recorder = Recorder(file_name, device, debug)
        self._player = Player(file_name, debug)
        self._state_ready_to_rec = statemachine.State("readyToRecord")
        self._state_rec = statemachine.State("recording")
        self._state_play = statemachine.State("playing")
        self._state_ready_to_play = statemachine.State("readyToPlay")
        self._state_quit = statemachine.State("quitting")

        self._state_ready_to_rec.add_rule(statemachine.Rule(
            self._event_start,
            None,
            self.notif,
            self._state_ready_to_rec))
        
        self._state_ready_to_rec.add_rule(statemachine.Rule(
            self._event_key,
            self.__start_record,
            self.notif,
            self._state_rec))

        self._state_ready_to_rec.add_rule(statemachine.Rule(
            self._event_quit,
            self.__quit,
            self.notif,
            self._state_quit))

        self._state_rec.add_rule(statemachine.Rule(
            self._event_key,
            self.__stop_record,
            self.notif,
            self._state_ready_to_play))

        self._state_rec.add_rule(statemachine.Rule(
            self._event_quit,
            self.__quit,
            self.notif,
            self._state_quit))

        self._state_ready_to_play.add_rule(statemachine.Rule(
            self._event_key,
            self.__play,
            self.notif,
            self._state_play))

        self._state_ready_to_play.add_rule(statemachine.Rule(
            self._event_quit,
            self.__quit,
            self.notif,
            self._state_quit))

        self._state_play.add_rule(statemachine.Rule(
            self._event_key,
            self.__stop,
            self.notif,
            self._state_ready_to_play))

        self._state_play.add_rule(statemachine.Rule(
            self._event_quit,
            self.__quit,
            self.notif,
            self._state_quit))

        super(MicLooper, self).__init__(self._state_ready_to_rec)
        self.on_event(self._event_start)

    def __start_record(self):
        self._recorder.start()

    def __stop_record(self):
        self._recorder.stop()

    def __play(self):
        self._player.start()

    def __stop(self):
        self._player.stop()

    def __quit(self):
        self._recorder.stop()
        self._player.stop()

    def notif(self, state_str):
        """
        Notif a state change.
        By default print the new state.
        This method is public to allow a child class to override it.

        :Args:
            state_str : string
                Name of the new state
        """
        print self._tag + " " + state_str
        
    def on_event_key_pressed(self):
        """ event key pressed callback
        """
        self.on_event(self._event_key)

    def on_event_quit_request(self):
        """ event quit request callback
        """
        self.on_event(self._event_quit)
