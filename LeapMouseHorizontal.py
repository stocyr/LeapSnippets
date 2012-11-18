################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys, winsound
import win32api, win32con
import time


class LeapListener(Leap.Listener):
    button_threshold = -500
    button_hysteresis = -100
    button_down = False
    
    palm_threshold = 200
    palm_down = False
    
    mouse_x = 800
    mouse_y = 500
    
    history = 1
    scale = 20
    accel_factor = 0.00

    def onInit(self, controller):
        print "Initialized"

    def onConnect(self, controller):
        print "Connected"

    def onDisconnect(self, controller):
        print "Disconnected"

    def onFrame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands()
        numHands = len(hands)
        
        frame_old = controller.frame(self.history)
        hands_old = frame_old.hands()

        if numHands >= 1:
            # Get the first hand
            hand = hands[0]
            
            # Check if the hand has any fingers
            ####################################
            # Click functionality
            ####################################
            fingers = hand.fingers()
            numFingers = len(fingers)
            #if numFingers >= 1:
            if 0:
                if self.button_down != True and fingers[0].velocity().y < self.button_threshold:
                    click()
                    print 'click - timestamp: %d' % frame.timestamp()
                    self.button_down = True
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
                elif self.button_down == True and fingers[0].velocity().y > self.button_hysteresis and 0:
                    #print 'click up'
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
                    self.button_down = False
            elif self.button_down == True:
                #print 'click up'
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
                self.button_down = False
            
            # Check if the hand has a palm
            ####################################
            # Mouse movement functionality
            ####################################
            palmRay = hand.palm()
            if palmRay is not None:
                palm = hand.palm().position
                
                #print 'palm velocity: x: %d, y: %d, z: %d' % (hand.velocity().x, hand.velocity().y, hand.velocity().z)
                
                
                if self.palm_down == False and hand.velocity().y < -self.palm_threshold:
                    # if the palm is being dropped:
                    print 'mouse down - timestamp: %d' % frame.timestamp()
                    self.palm_down = True
                
                elif self.palm_down == True and hand.velocity().y > self.palm_threshold:
                    # if the palm is being lifted:
                    print 'mouse up - timestamp: %d' % frame.timestamp()
                    self.palm_down = False
                
                if len(hands_old) >= 1 and hands_old[0].palm() != None: # self.palm_down == True and 
                    # find out the relative movement since the last frame
                    delta_x = hands_old[0].palm().position.x - palm.x
                    delta_y = hands_old[0].palm().position.z - palm.z
                    # position the mouse
                    self.mouse_x = self.mouse_x - delta_x*(self.scale + self.accel_factor*hand.velocity().x*hand.velocity().x) # negative because X-axis is negative as well
                    self.mouse_y = self.mouse_y - delta_y*(self.scale + self.accel_factor*hand.velocity().y*hand.velocity().y) # negative because Z-axis is negative as well
                    
                    #print '%f, %f  |  %d, %d' % (delta_x, delta_y, self.mouse_x, self.mouse_y)
                    
                    win32api.SetCursorPos((int(self.mouse_x + 0.5), int(self.mouse_y + 0.5)))
            else:
                self.palm_down = False

def click():
    winsound.PlaySound('Windows-Start.wav', winsound.SND_FILENAME)


def main():
    # Create a sample listener and assign it to a controller to receive events
    listener = LeapListener()
    controller = Leap.Controller(listener)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    
    sys.stdin.readline()
    # if [ENTER] was pressed, reset Mouse Position to initial state:
    #LeapListener.mouse_x = 800
    #LeapListener.mouse_y = 500
    #win32api.SetCursorPos((LeapListener.mouse_x, LeapListener.mouse_y))

    # The controller must be disposed of before the listener
    controller = None


if __name__ == "__main__":
    main()
