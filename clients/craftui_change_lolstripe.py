#!/usr/bin/python

###
# Copyright 2015, Aurel Wildfellner.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import unicodedata
import re
import os

import zmq

import uievents_pb2
import craftuiirc



def setLolStripe(color):
    os.system("mosquitto_pub -h 192.168.7.2 -t led -m x" + color*60 )


def toggleChico(port):
    ports = str(port) 
    ports = re.escape(ports)
    os.system('sispmctl -t ' + ports + " > /dev/null")


class EventSubscriber:

    def __init__(self, address):
        self.addr = address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.connected = False


    def connect(self):
        self.socket.connect(self.addr)
        # IMPORTANT subscribe to all messages
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u"")
        self.connected = True


    def receiveEvent(self):
        if not self.connected:
            return None

        msg = self.socket.recv_string()
        msgstr = unicodedata.normalize('NFKD', msg).encode('ascii','ignore')
        event = uievents_pb2.Event()
        event.ParseFromString(msgstr)
        return event




def main():

    evs = EventSubscriber("tcp://127.0.0.1:9001")
    evs.connect()
    print("Connected: ", evs.connected)

    ircclient = craftuiirc.CraftUIIRC("irc.servus.at", 6667, "#test")
    ircclient.start()
    

    while True:
        event = evs.receiveEvent()

        ### Print Event Info ###
        print "########################"
        print event.id + ":"
        if event.elementtype == event.BUTTON:
            print "  Type: BUTTON" 
        elif event.elementtype == event.SLIDER:
            print "  Type: SLIDER" 
        if event.trigger == event.TRIGGERED:
            print "  Triggered!"
        elif event.trigger == event.UNTRIGGERED:
            print "  Untriggered!"
        elif event.trigger == event.INTRIGGER:
            print "  Intrigger."

        ### Do some switching ###
        if event.id == "button_red" and event.trigger == event.TRIGGERED:
            setLolStripe("R")
        if event.id == "button_green" and event.trigger == event.TRIGGERED:
            setLolStripe("G")
        if event.id == "button_blue" and event.trigger == event.TRIGGERED:
            setLolStripe("B")
        if event.id == "button_black" and event.trigger == event.TRIGGERED:
            ircclient.postLine("Someone says Hi at the window!")
            #toggleChico(2)

    ircclient.stop()





if __name__ == "__main__":
    main()

