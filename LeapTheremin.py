################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys
import pygame.midi


class SampleListener(Leap.Listener):
    midi_out = None
    
    note_playing = False
    
    note = 80
    velocity = 127
    channel = 0

    def onInit(self, controller):
        print "Initialized"
        # initialize the midi device
        pygame.midi.init()
        self.set_midi_device()

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
                if self.note_playing == True:
                    pitch_value = int(-fingers[0].tip().position.z*50) + 8192 # (center/normal = 8192)
                    
                    # if the pitch value exceeds the allowed range of 0 to 16383, hold him at the lowest / highest end.
                    if pitch_value > 16383:
                        pitch_value = 16383
                    elif pitch_value < 0:
                        pitch_value = 0
                    
                    self.midi_out.write_short(0xE0 + self.channel, pitch_value - int(pitch_value / 128) * 128, int(pitch_value / 128))
                else:
                    self.midi_out.note_on(self.note, self.velocity, self.channel)
                    self.note_playing = True
        else:
            if self.note_playing == True:
                self.midi_out.note_off(self.note, 0, self.channel)
                self.note_playing = False

    def set_midi_device(self):
        c = pygame.midi.get_count()
        id_device_from_settings = -1
        #print '%s midi devices found' % c
        for i in range(c):
            print '%s name: %s input: %s output: %s opened: %s' % (pygame.midi.get_device_info(i))
            if pygame.midi.get_device_info(i)[1] == 'Fast Track Pro MIDI Out':
                # if the device exists in the computers list, take that!
                id_device_from_settings = i
        
        print 'Default is %s' % pygame.midi.get_device_info(pygame.midi.get_default_output_id())[1]
        
        if id_device_from_settings <> -1:
            self.midi_device = id_device_from_settings
            print 'MIDI device "%s" found. Connecting.' % pygame.midi.get_device_info(id_device_from_settings)[1]
        else:
            # if it was not in the list, take the default one
            self.midi_device = pygame.midi.get_default_output_id()
            print 'Warning: No MIDI device named "%s" found. Choosing the system default ("%s").' % ('Fast Track Pro MIDI Out', pygame.midi.get_device_info(self.midi_device)[1])
        
        if pygame.midi.get_device_info(self.midi_device)[4] == 1:
            print 'Error: Can''t open the MIDI device - It''s already opened!'
            
        self.midi_out = pygame.midi.Output(self.midi_device)


def main():
    # Create a sample listener and assign it to a controller to receive events
    listener = SampleListener()
    controller = Leap.Controller(listener)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    
    listener.midi_out.note_off(listener.note, 0, listener.channel)

    # The controller must be disposed of before the listener
    controller = None


if __name__ == "__main__":
    main()
