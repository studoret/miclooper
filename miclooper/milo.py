#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
milo - Micro looper application

This python script uses command-line sound recorder for ALSA soundcard
driver (arecord) and mplayer to play records.

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
import time

import curses

from miclooper import MicLooper

class CustomMicLooper(MicLooper):
    """
    MicLooper with ncurses interface
    """
    COLOR_READY_TO_RECORD = 1
    COLOR_RECORDING = 2
    COLOR_READY_TO_PLAY = 3
    COLOR_PLAYING = 4
    COLOR_BORDER = 5

    def __init__(self, stdscr, pos_x, pos_y, *args, **kwargs):
        self._stdscr = stdscr
        self._pos_x = pos_x
        self._pos_y = pos_y
        super(CustomMicLooper, self).__init__(*args, **kwargs)

    def __print_button(self, pos_y, pos_x, color):
        self._stdscr.move(pos_y, pos_x)
        self._stdscr.addch(curses.ACS_ULCORNER, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_HLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_HLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_URCORNER, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.move(pos_y + 1, pos_x)
        self._stdscr.addch(curses.ACS_VLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_CKBOARD, curses.color_pair(color))
        self._stdscr.addch(curses.ACS_CKBOARD, curses.color_pair(color))
        self._stdscr.addch(curses.ACS_VLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.move(pos_y + 2, pos_x)
        self._stdscr.addch(curses.ACS_LLCORNER, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_HLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_HLINE, curses.color_pair(CustomMicLooper.COLOR_BORDER))
        self._stdscr.addch(curses.ACS_LRCORNER, curses.color_pair(CustomMicLooper.COLOR_BORDER))

    def notif(self, state_str):
        if state_str == "readyToRecord":
            self.__print_button(self._pos_y, self._pos_x, CustomMicLooper.COLOR_READY_TO_RECORD)
        if state_str == "recording":
            self.__print_button(self._pos_y, self._pos_x, CustomMicLooper.COLOR_RECORDING)
        if state_str == "readyToPlay":
            self.__print_button(self._pos_y, self._pos_x, CustomMicLooper.COLOR_READY_TO_PLAY)
        if state_str == "playing":
            self.__print_button(self._pos_y, self._pos_x, CustomMicLooper.COLOR_PLAYING)

def parse_cmd_line():
    """
    Parse command line
    """
    parser = argparse.ArgumentParser(description="Micro looper application")
    parser.add_argument('-p', '--path', help='Root record directory path', default="records")
    parser.add_argument('-k', '--keys', help='Keyboard characters', default="123")
    parser.add_argument('-D', '--device', help='Select PCM by name', default="hw:0,0")
    parser.add_argument('-v', '--verbose', help='Display stderr of arecord and aplay',
                        action='store_true', default=False)
    args = parser.parse_args()
    return args

def main(stdscr):
    """main function
    """
    args = parse_cmd_line()

    rec_dir = args.path + os.sep + "rec_" + time.strftime("%Y%m%d-%H%M%S")

    # Hide cursor
    curses.curs_set(0)

    # Config colors
    curses.start_color()
    curses.init_pair(CustomMicLooper.COLOR_RECORDING, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(CustomMicLooper.COLOR_PLAYING, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(CustomMicLooper.COLOR_READY_TO_RECORD, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(CustomMicLooper.COLOR_READY_TO_PLAY, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(CustomMicLooper.COLOR_BORDER, curses.COLOR_CYAN, curses.COLOR_BLACK)

    stdscr.addstr(0, 0, "records directory = %s" % rec_dir,
                  curses.color_pair(CustomMicLooper.COLOR_BORDER))

    os.makedirs(rec_dir)

    micloopers = {}
    pos_x = 0
    for key in args.keys:
        rec_file = rec_dir + os.sep +  "rec_" + key + ".raw"
        tag = "LOOP_" + key
        stdscr.addstr(1, pos_x, " " + tag + " ", curses.A_REVERSE)
        micloopers[key] = CustomMicLooper(stdscr, pos_x, 2,
                                          rec_file, tag, args.device, args.verbose)
        pos_x += len(" " + tag + " ") + 1

    running = True

    while running:
        char = stdscr.getkey()
        if micloopers.has_key(char):
            micloopers[char].on_event_key_pressed()
        else:
            print "Goodbye"
            for key in args.keys:
                micloopers[key].on_event_quit_request()
            running = False

if __name__ == "__main__" and __package__ is None:
    curses.wrapper(main)
