################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys, pygame

class SampleListener(Leap.Listener):
    down_sound = None
    up_sound = None
    threshold = -350
    hysteresis = 10
    down = False

    def onInit(self, controller):
        print "Initialized"
        self.down_sound = pygame.mixer.Sound('click_down2.ogg')
        self.up_sound = pygame.mixer.Sound('click_up2.ogg')

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
                #print '%d' % fingers[0].velocity().y
                if self.down == False and fingers[0].velocity().y < self.threshold:
                    self.down_sound.play()
                    print 'click - timestamp: %d' % frame.timestamp()
                    self.down = True
                elif self.down == True and fingers[0].velocity().y > self.hysteresis:
                    self.up_sound.play()
                    print 'click up'
                    self.down = False
        else:
            self.down = False


def main():
    #pygame.mixer.pre_init(44100,-16,2, 128)
    pygame.mixer.init()
    pygame.init()
    
    
    # Create a sample listener and assign it to a controller to receive events
    listener = SampleListener()
    controller = Leap.Controller(listener)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # The controller must be disposed of before the listener
    controller = None


if __name__ == "__main__":
    main()
