#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
milo - Micro looper application

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

import argparse
import os
import sys
import tty
import termios
import time

from miclooper import MicLooper

def get_char():
    """ Wait key pressed and returns its code """
    fdesc = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fdesc)
    ch = 0
    try:
        tty.setraw(fdesc)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fdesc, termios.TCSADRAIN, old_settings)
    return ch

def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Micro looper application")
    parser.add_argument('-p', '--path', help='Root record directory path', default="records")
    parser.add_argument('-k', '--keys', help='Keyboard characters', default="123")
    parser.add_argument('-D', '--device', help='Select PCM by name', default="hw:0,0")
    parser.add_argument('-v', '--verbose', help='Display stderr of arecord and aplay', action='store_true', default=False)
    args = parser.parse_args()
    return args

def main():
    """main function
    """
    args = parse_cmd_line()

    rec_dir = args.path + os.sep + "rec_" + time.strftime("%Y%m%d-%H%M%S")
    
    print "records directory = %s" % rec_dir

    os.makedirs(rec_dir)

    micloopers = {}
    
    for key in args.keys:
        rec_file = rec_dir + os.sep +  "rec_" + key + ".raw"
        micloopers[key]=MicLooper(rec_file, "LOOP_" + key, args.device, args.verbose)

    running = True

    while running:
        ch = get_char()
        if micloopers.has_key(ch):
            micloopers[ch].on_event_key_pressed()
        else:
            print "Goodbye"
            for key in args.keys:
                micloopers[key].on_event_quit_request()
            running = False

if __name__ == "__main__" and __package__ is None:
    main()
