################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys
import ctypes # for mouse control


class LeapListener(Leap.Listener):    
    z_offset = 240      # distance of the leap from the monitor in mm (240)
    y_offset = 500      # top border of the monitor from the leap's top in mm (320)
    x_offset = 330      # left  border of the monitor to the leap's center in mm (260)
    
    mm2pixel = 1200/320
    
    direction_scaling = 1

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
        
        if numHands >= 1:
            # Get the first hand
            hand = hands[0]
            
            # Check if the hand has any fingers
            fingers = hand.fingers()
            numFingers = len(fingers)
            if numFingers >= 1:
                #ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
                
                ray = fingers[0].tip()
                
                x = self.direction_scaling*ray.direction.x*((-self.z_offset) - ray.position.z)/ray.direction.z + ray.position.x
                y = self.direction_scaling*ray.direction.y*((-self.z_offset) - ray.position.z)/ray.direction.z + ray.position.y
                
                # count in the offsets
                x = x - self.x_offset
                y = self.y_offset - y
                
                # scale to pixels instead of mm's
                x = x*self.mm2pixel
                y = y*self.mm2pixel
                
                # I'm on the left monitor...
                x = x + 1920
                
                ctypes.windll.user32.SetCursorPos(int(x + 0.5), int(y + 0.5))
            else:
                #ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
                pass

def main():
    # Create a sample listener and assign it to a controller to receive events
    listener = LeapListener()
    controller = Leap.Controller(listener)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    
    sys.stdin.readline()

    # The controller must be disposed of before the listener
    controller = None


if __name__ == "__main__":
    main()
