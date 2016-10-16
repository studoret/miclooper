#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
task

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

import sys
import os
import subprocess

class Task(object):
    """
    Task.

    :Args:

        command : Array of string
            Command to exectute in background.
            e.g : ['/usr/bin/mplayer', '-loop', '0', 'toto.raw'])

        debug : boolean
            If true then show stderr of the command
            else hide stderr

    """
    def __init__(self, command, debug=False):
        self._command = command
        self._process = None
        self._fdevnull = open(os.devnull, 'w')
        if debug is True:
            self._fstderr = None
        else:
            self._fstderr = subprocess.STDOUT

    def start(self):
        """ Execute the task in background """
        try:
            self._process = subprocess.Popen(
                self._command,
                bufsize=-1,
                stdout=self._fdevnull,
                stderr=self._fstderr
            )
        except OSError as err:
            print 'error: %s' % err
            sys.exit(1)

    def stop(self):
        """ Terminate the task """
        if self._process != None:
            self._process.terminate()
        self._process = None
