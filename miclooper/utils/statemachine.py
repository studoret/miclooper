#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
statemachine

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

class Event(object):
    """
    Use to define events used to select a rule

    :Args:

        name : string
            Event name

    """
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name

class State(object):
    """
    Use to define states of the state machine

    :Args:

        name : string
            State name

    """
    def __init__(self, name):
        self._name = name
        self._rules = {}

    def __str__(self):
        return self._name

    def add_rule(self, rule):
        """
        Add a transition rule

        :Args:

            rule: Rule
                Transitional rule

        """
        self._rules[str(rule)]=rule

    def on_event(self, event):
        """
        Trigger a transition

        :Args:

            event : Event
                Event used to select the transitional rule

        """
        return self._rules[str(event)].apply()

class Rule(object):
    """
    Use to define rules that trigger a transition bewtween two states

    :Args:

        event : Event
            Event that trigger the rule
        action : function
            Action executed when the rule is triggered
        trace : function
            Print function that take in parameter a State name
        next_state : State
            State after transition

    """
    def __init__(self, event, action, trace, next_state):
        self._event = event
        self._action = action
        self._trace = trace
        self._next_state = next_state

    def __str__(self):
        return str(self._event)

    def apply(self):
        """
        Execute the action of the rule.

        :Return:

            The target state of the transition.

        """
        if self._action != None:
            self._action()

        if self._trace != None:
            self._trace(str(self._next_state))

        return self._next_state

class StateMachine(object):
    """
    Define a state machine

    :Args:
        initial_state : State
            State at starting of the state machine

    """
    def __init__(self, initial_state):
        self._state = initial_state

    def on_event(self, event):
        """
        Execute a transition state

        :Args:
            event : Event
                Event of the transition
        """
        self._state = self._state.on_event(event)
